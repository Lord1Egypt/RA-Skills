"""BuilderPipeline - 전체 파이프라인 오케스트레이션

Phase 1: Basic pipeline orchestration
Phase 2: Checkpoint and resume functionality
Phase 3: Async support for Symphony orchestration
"""

import asyncio
import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Dict, Optional

from builder.models import ProjectIdea, BuildResult, PipelineStage, DiscoverySource, PipelineState
from builder.discovery.github_trending import GitHubTrendingSource
from builder.discovery.cve_database import CVEDatabaseSource
from builder.discovery.security_news import SecurityNewsSource
from builder.discovery.cache import DiscoveryCache
from builder.discovery.scorer import IdeaScorer, AdaptiveIdeaScorer
from builder.discovery.dedup import SemanticDeduplicator
from builder.orchestrator import HybridOrchestrator
from builder.correction.base import BaseCorrectionEngine
from builder.correction.analyzer import ErrorAnalyzer
from builder.correction.fixer import CodeFixer
from builder.checkpoint import PipelineCheckpoint, ProjectCheckpoint

logger = logging.getLogger('builder-agent.pipeline')


class BuilderPipeline:
    """Builder Agent 통합 파이프라인

    Discovery -> Dedup -> Score -> Queue -> Build -> Test -> Fix -> Publish
    """

    def __init__(self, config=None, use_adaptive_scoring: bool = True):
        """초기화

        Args:
            config: 설정 객체
            use_adaptive_scoring: 적응형 점수 시스템 사용 여부
        """
        self.config = config

        # State (먼저 설정)
        self.state = PipelineState()
        self.output_dir = Path(config.discovery.output_dir) if config else Path("/tmp/builder-discovery")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Discovery
        cache_dir = self.output_dir / "cache"
        self.cache = DiscoveryCache(cache_dir, ttl_seconds=config.discovery.cache_ttl_seconds if config else 3600)

        self.sources = [
            GitHubTrendingSource(config.discovery.github if config else None),
            CVEDatabaseSource(config.discovery.cve if config else None),
            SecurityNewsSource(config.discovery.security_news if config else None),
        ]

        # 점수 시스템 선택 (이제 output_dir이 설정됨)
        if use_adaptive_scoring:
            feedback_path = self.output_dir / "feedback_history.json"
            self.scorer = AdaptiveIdeaScorer(feedback_history_path=feedback_path)
        else:
            self.scorer = IdeaScorer()

        self.deduplicator = SemanticDeduplicator(similarity_threshold=0.7)

        # Build
        self.orchestrator = HybridOrchestrator(config)
        self.analyzer = ErrorAnalyzer()
        self.fixer = CodeFixer()

        # Checkpoint
        checkpoint_dir = self.output_dir / "checkpoints"
        self.checkpoint_manager = PipelineCheckpoint(checkpoint_dir)
        self.use_checkpoints = True

        # Periodic cleanup
        self._cleanup_old_checkpoints()

    # ──────────────────────────────────────────────
    # Discovery Pipeline
    # ──────────────────────────────────────────────

    def run_discovery_pipeline(self, resume: bool = False) -> Dict:
        """Discovery -> Dedup -> Score -> Queue

        Args:
            resume: 실패한 파이프라인 재개 여부

        Returns:
            파이프라인 실행 결과
        """
        # 재개 모드 체크
        if resume and self.use_checkpoints:
            last_checkpoint = self.checkpoint_manager.load_last_checkpoint()
            if last_checkpoint:
                logger.info("Resuming from checkpoint: %s", last_checkpoint.stage)
                # 재개 로직은 각 스테이지에서 처리

        self.state.set_stage(PipelineStage.DISCOVERING.value)

        # 체크포인트 저장
        if self.use_checkpoints:
            self.checkpoint_manager.save_state('discovering', {'started': True})

        start_time = time.time()

        logger.info("Starting discovery pipeline...")

        try:
            # 1. 병렬 Discovery
            ideas = self._discover_all()
            logger.info("Discovered %d raw ideas", len(ideas))

            if self.use_checkpoints:
                self.checkpoint_manager.save_state('discovering', {
                    'started': True,
                    'ideas_found': len(ideas)
                })

            # 2. 중복 제거
            unique_ideas = self._deduplicate(ideas)
            logger.info("After dedup: %d ideas", len(unique_ideas))

            if self.use_checkpoints:
                self.checkpoint_manager.save_state('deduplicating', {
                    'unique_ideas': len(unique_ideas)
                })

            # 3. 점수화
            scored_ideas = self._score_and_rank(unique_ideas)
            logger.info("Scored ideas: top=%.2f, bottom=%.2f",
                       scored_ideas[0]['score'] if scored_ideas else 0,
                       scored_ideas[-1]['score'] if scored_ideas else 0)

            if self.use_checkpoints:
                self.checkpoint_manager.save_state('scoring', {
                    'scored_ideas': len(scored_ideas)
                })

            # 4. 저장
            self._save_discovered(scored_ideas)

            # 완료 체크포인트
            if self.use_checkpoints:
                self.checkpoint_manager.save_state('completed', {
                    'total_ideas': len(scored_ideas)
                })

            elapsed = time.time() - start_time
            logger.info("Discovery pipeline completed in %.1fs", elapsed)

            return {
                'success': True,
                'ideas': scored_ideas,
                'count': len(scored_ideas),
                'elapsed_seconds': round(elapsed, 1)
            }

        except Exception as e:
            logger.error("Discovery pipeline failed: %s", e)

            if self.use_checkpoints:
                self.checkpoint_manager.add_error(str(e))

            return {
                'success': False,
                'error': str(e),
                'can_resume': True
            }

    def _discover_all(self) -> List[Dict]:
        """병렬 Discovery"""
        all_ideas = []

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(source.discover): source.__class__.__name__
                for source in self.sources if source.enabled
            }

            for future in as_completed(futures, timeout=60):
                source_name = futures[future]
                try:
                    ideas = future.result(timeout=30)
                    all_ideas.extend(ideas)
                    logger.info("%s: %d ideas", source_name, len(ideas))
                except Exception as e:
                    logger.warning("%s failed: %s", source_name, e)

        return all_ideas

    def _deduplicate(self, ideas: List[Dict]) -> List[Dict]:
        """의미론적 중복 제거 (Sprint 4: difflib fuzzy matching)"""
        return self.deduplicator.deduplicate(ideas)

    def _score_and_rank(self, ideas: List[Dict]) -> List[Dict]:
        """점수화 및 정렬"""
        for idea in ideas:
            idea['score'] = self.scorer.score(idea, ideas)

        return sorted(ideas, key=lambda x: x['score'], reverse=True)

    def _save_discovered(self, ideas: List[Dict]):
        """발굴 결과 저장"""
        output_file = self.output_dir / "discovered_ideas.json"
        with open(output_file, 'w') as f:
            json.dump(ideas, f, indent=2, ensure_ascii=False)
        logger.info("Saved %d ideas to %s", len(ideas), output_file)

    # ──────────────────────────────────────────────
    # Build Pipeline
    # ──────────────────────────────────────────────

    def run_build_pipeline(self, idea: Dict, project_path: Path, resume: bool = False) -> Dict:
        """Build -> Test -> Fix with checkpoint support

        Args:
            idea: 프로젝트 아이디어
            project_path: 프로젝트 경로
            resume: 실패한 빌드 재개 여부

        Returns:
            빌드 결과
        """
        # 프로젝트별 체크포인트 관리자 생성
        project_checkpoint = ProjectCheckpoint(
            project_title=idea.get('title', 'unknown'),
            checkpoint_dir=self.output_dir / "checkpoints"
        )

        # 재개 모드 체크
        if resume and project_checkpoint.can_resume():
            last_state = project_checkpoint.load_stage()
            logger.info("Resuming build from stage: %s", last_state.stage)
            # 재개 로직은 각 스테이지에서 처리

        self.state.set_stage(PipelineStage.BUILDING.value)
        self.state.current_project = idea['title']

        # ProjectIdea로 변환
        project = ProjectIdea.from_dict(idea)

        try:
            # 빌딩 스테이지
            project_checkpoint.save_stage('building', {
                'project_path': str(project_path),
                'complexity': project.complexity
            })

            # 개발
            build_result = self.orchestrator.develop(project, project_path)

            if not build_result.success:
                # 빌드 실패
                retry_count = project_checkpoint.checkpoint.increment_retry()
                logger.warning("Build failed, retry count: %d", retry_count)

                if retry_count < 3:
                    return {
                        'success': False,
                        'can_resume': True,
                        'retry_count': retry_count,
                        'error': build_result.test_output
                    }
                else:
                    return {
                        'success': False,
                        'can_resume': False,
                        'retry_count': retry_count,
                        'error': 'Max retries exceeded'
                    }

            # 테스팅 스테이지
            project_checkpoint.save_stage('testing', {
                'build_success': True
            })

            self.state.set_stage(PipelineStage.TESTING.value)
            test_result = self._run_tests(project_path)

            if test_result['success']:
                self.state.set_stage(PipelineStage.COMPLETED.value)
                project_checkpoint.save_stage('completed', {
                    'success': True
                })

                # 성공 결과 기록 (적응형 학습)
                if isinstance(self.scorer, AdaptiveIdeaScorer):
                    self.scorer.record_outcome(idea, success=True)

                logger.info("Build completed: %s", project.title)
                return build_result.to_dict()

            # 수정 스테이지
            project_checkpoint.save_stage('fixing', {
                'test_output': test_result['output'][:500]
            })

            self.state.set_stage(PipelineStage.FIXING.value)
            error = self.analyzer.analyze(test_result['output'])
            fixed = self.fixer.fix(error, project_path, project.complexity)

            if fixed:
                # 재테스트
                test_result = self._run_tests(project_path)
                build_result.success = test_result['success']

                if build_result.success:
                    project_checkpoint.save_stage('completed', {
                        'success': True,
                        'fixed': True
                    })

                    # 성공 결과 기록
                    if isinstance(self.scorer, AdaptiveIdeaScorer):
                        self.scorer.record_outcome(idea, success=True)
                else:
                    # 실패 결과 기록
                    if isinstance(self.scorer, AdaptiveIdeaScorer):
                        self.scorer.record_outcome(idea, success=False)

            self.state.current_project = None
            return build_result.to_dict()

        except Exception as e:
            logger.error("Build pipeline error: %s", e)

            # 실패 결과 기록
            if isinstance(self.scorer, AdaptiveIdeaScorer):
                self.scorer.record_outcome(idea, success=False)

            return {
                'success': False,
                'error': str(e),
                'can_resume': True
            }

    def _run_tests(self, project_path: Path) -> Dict:
        """테스트 실행"""
        import subprocess
        import os

        try:
            result = subprocess.run(
                ['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
                cwd=str(project_path),
                capture_output=True,
                text=True,
                timeout=30,
                env={**os.environ, 'PYTHONPATH': 'src'}
            )

            return {
                'success': result.returncode == 0,
                'output': result.stdout + result.stderr
            }

        except subprocess.TimeoutExpired:
            return {'success': False, 'output': 'Test timeout'}
        except Exception as e:
            return {'success': False, 'output': str(e)}

    # ──────────────────────────────────────────────
    # Helper Methods
    # ──────────────────────────────────────────────

    def _cleanup_old_checkpoints(self):
        """오래된 체크포인트 정리 (24시간 이상)"""
        if self.use_checkpoints:
            self.checkpoint_manager.clear_checkpoints(older_than_hours=24)

    def get_checkpoint_status(self) -> Dict:
        """체크포인트 상태 조회"""
        if not self.use_checkpoints:
            return {'checkpoints_enabled': False}

        return {
            'checkpoints_enabled': True,
            'checkpoints': self.checkpoint_manager.get_all_checkpoints()
        }

    def clear_all_checkpoints(self):
        """모든 체크포인트 삭제"""
        if self.use_checkpoints:
            import shutil
            if self.checkpoint_manager.checkpoint_dir.exists():
                shutil.rmtree(self.checkpoint_manager.checkpoint_dir)
                self.checkpoint_manager.checkpoint_dir.mkdir(parents=True, exist_ok=True)
                logger.info("All checkpoints cleared")

    def get_scoring_insights(self) -> Dict:
        """점수 시스템 인사이트 반환 (적응형 점수 시스템일 때만)"""
        if isinstance(self.scorer, AdaptiveIdeaScorer):
            return self.scorer.get_scoring_insights()
        return {'adaptive_scoring': False}

    # ──────────────────────────────────────────────
    # Async Pipeline Methods (for Symphony)
    # ──────────────────────────────────────────────

    async def run_build_pipeline_async(self, idea: Dict, project_path: Path,
                                       resume: bool = False) -> Dict:
        """Async version of run_build_pipeline for Symphony orchestration

        This method provides the same functionality as run_build_pipeline but
        can be used in async contexts for parallel task execution.

        Args:
            idea: 프로젝트 아이디어
            project_path: 프로젝트 경로
            resume: 실패한 빌드 재개 여부

        Returns:
            빌드 결과
        """
        # Run the synchronous pipeline in a thread pool
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: self.run_build_pipeline(idea, project_path, resume)
        )
        return result

    async def run_discovery_pipeline_async(self, resume: bool = False) -> Dict:
        """Async version of run_discovery_pipeline for Symphony orchestration

        This method provides the same functionality as run_discovery_pipeline but
        can be used in async contexts for parallel task execution.

        Args:
            resume: 실패한 파이프라인 재개 여부

        Returns:
            파이프라인 실행 결과
        """
        # Run the synchronous pipeline in a thread pool
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: self.run_discovery_pipeline(resume)
        )
        return result


