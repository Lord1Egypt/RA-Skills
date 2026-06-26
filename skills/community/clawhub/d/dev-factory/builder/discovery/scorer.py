"""IdeaScorer - 아이디어 품질 점수화

Phase 1: Static 5-dimensional scoring
Phase 2: Adaptive multi-dimensional scoring with source-specific weights
"""

import json
import logging
import math
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger('builder-agent.discovery.scorer')


class IdeaScorer:
    """5차원 아이디어 점수화"""

    # 가중치
    WEIGHTS = {
        'recency': 0.25,
        'severity': 0.20,
        'feasibility': 0.20,
        'novelty': 0.20,
        'demand': 0.15,
    }

    def score(self, idea: Dict, existing_ideas: list = None) -> float:
        """아이디어 종합 점수 계산 (0.0 ~ 1.0)"""
        scores = {
            'recency': self._score_recency(idea),
            'severity': self._score_severity(idea),
            'feasibility': self._score_feasibility(idea),
            'novelty': self._score_novelty(idea, existing_ideas),
            'demand': self._score_demand(idea),
        }

        total = sum(self.WEIGHTS[k] * scores[k] for k in self.WEIGHTS)

        logger.debug("Score %s: %.2f (recency=%.2f, severity=%.2f, feasibility=%.2f, novelty=%.2f, demand=%.2f)",
                    idea['title'][:30], total, scores['recency'], scores['severity'],
                    scores['feasibility'], scores['novelty'], scores['demand'])

        return total

    def _score_recency(self, idea: Dict) -> float:
        """최신성 점수"""
        discovered_at = idea.get('discovered_at', '')
        if not discovered_at:
            return 0.5

        try:
            dt = datetime.fromisoformat(discovered_at)
            age_hours = (datetime.now() - dt).total_seconds() / 3600

            if age_hours < 1:
                return 1.0
            elif age_hours < 24:
                return 0.8
            elif age_hours < 168:  # 7일
                return 0.5
            else:
                return 0.2
        except:
            return 0.5

    def _score_severity(self, idea: Dict) -> float:
        """심각도 점수"""
        severity = idea.get('severity', '').upper()
        cvss_score = idea.get('score', 0)

        # CVE인 경우 CVSS 점수 사용
        if cvss_score:
            return min(cvss_score / 10.0, 1.0)

        # priority 기반
        priority = idea.get('priority', '').lower()
        if priority == 'critical':
            return 1.0
        elif priority == 'high':
            return 0.8
        elif priority == 'medium':
            return 0.5
        else:
            return 0.2

    def _score_feasibility(self, idea: Dict) -> float:
        """구현 가능성 점수"""
        complexity = idea.get('complexity', '').lower()

        if complexity == 'simple':
            return 1.0
        elif complexity == 'medium':
            return 0.7
        elif complexity == 'complex':
            return 0.4
        else:
            return 0.5

    def _score_novelty(self, idea: Dict, existing_ideas: list = None) -> float:
        """새로움 점수 (기존 아이디어와 중복 여부)"""
        if not existing_ideas:
            return 1.0

        title = idea.get('title', '').lower()
        description = idea.get('description', '').lower()

        # 간단한 중복 체크 (Sprint 4에서 semantic dedup으로 개선)
        for existing in existing_ideas:
            existing_title = existing.get('title', '').lower()
            # 제목 유사도 70% 이상이면 중복
            if self._similar(title, existing_title):
                return 0.3

        return 1.0

    def _score_demand(self, idea: Dict) -> float:
        """수요 점수"""
        # GitHub stars가 있으면 사용
        url = idea.get('url', '')
        if 'github.com' in url:
            # 현재는 stars 정보 없음, Sprint 2-3에서 개선
            return 0.5

        # CVE는 높은 수요
        if idea.get('source') == 'cve_database':
            return 0.8

        return 0.5

    def _similar(self, a: str, b: str) -> bool:
        """간단한 유사도 체크"""
        if a == b:
            return True
        if a in b or b in a:
            return True
        return False


class AdaptiveIdeaScorer:
    """적응형 다차원 점수 시스템

    소스별 가중치 동적 조정, 실제 시장 수요 반영, 피드백 루프 통한 최적화
    """

    # 소스별 가중치 (동적 조정 가능)
    SOURCE_WEIGHTS = {
        'cve_database': {
            'severity': 0.30,  # CVE는 심각도가 가장 중요
            'recency': 0.25,
            'demand': 0.20,
            'feasibility': 0.15,
            'novelty': 0.10
        },
        'github_trending': {
            'demand': 0.35,    # GitHub는 실제 수요(stars)가 중요
            'novelty': 0.25,
            'feasibility': 0.20,
            'recency': 0.15,
            'severity': 0.05
        },
        'security_news': {
            'recency': 0.35,   # 뉴스는 최신성이 핵심
            'severity': 0.25,
            'novelty': 0.20,
            'demand': 0.15,
            'feasibility': 0.05
        }
    }

    def __init__(self, feedback_history_path: Optional[Path] = None):
        """초기화

        Args:
            feedback_history_path: 프로젝트 성공/실패 이력 경로
        """
        self.feedback_history_path = feedback_history_path
        self.feedback_data = self._load_feedback_history()
        self.github_metrics_cache = {}

    def score(self, idea: Dict, existing_ideas: List[Dict] = None) -> float:
        """소스별 적응형 점수 계산

        Args:
            idea: 평가할 아이디어
            existing_ideas: 중복 체크를 위한 기존 아이디어 리스트

        Returns:
            0.0 ~ 1.0 사이의 점수
        """
        source = idea.get('source', 'manual')

        # 소스별 가중치 선택
        if source in self.SOURCE_WEIGHTS:
            weights = self.SOURCE_WEIGHTS[source].copy()
            # 피드백 기반 가중치 보정
            weights = self._apply_feedback_correction(source, weights)
        else:
            # 기본 가중치 (기존과 동일)
            weights = {
                'recency': 0.25,
                'severity': 0.20,
                'feasibility': 0.20,
                'novelty': 0.20,
                'demand': 0.15,
            }

        # 개별 점수 계산
        scores = {
            'recency': self._score_recency(idea),
            'severity': self._score_severity(idea),
            'feasibility': self._score_feasibility(idea),
            'novelty': self._score_novelty(idea, existing_ideas),
            'demand': self._score_demand_with_metrics(idea),
        }

        # 가중평균 계산
        total = sum(weights.get(k, 0) * scores[k] for k in weights)

        # 성공 패턴 기반 보정
        total = self._apply_success_pattern_correction(total, idea, source)

        logger.debug(
            "Adaptive Score %s: %.2f (source=%s, recency=%.2f, severity=%.2f, "
            "feasibility=%.2f, novelty=%.2f, demand=%.2f)",
            idea['title'][:30], total, source, scores['recency'], scores['severity'],
            scores['feasibility'], scores['novelty'], scores['demand']
        )

        return min(total, 1.0)  # 최대 1.0 제한

    def _score_demand_with_metrics(self, idea: Dict) -> float:
        """실제 시장 수요 데이터 기반 수요 점수 계산"""
        url = idea.get('url', '')
        source = idea.get('source', '')

        # GitHub인 경우 실제 메트릭 수집
        if 'github.com' in url:
            metrics = self._fetch_github_metrics(url)
            if metrics:
                return self._calculate_demand_index(metrics)

        # CVE는 높은 기본 수요
        if source == 'cve_database':
            severity = idea.get('severity', '').upper()
            if severity == 'CRITICAL':
                return 0.95
            elif severity == 'HIGH':
                return 0.85
            else:
                return 0.70

        # Security News
        if source == 'security_news':
            return 0.75

        return 0.50  # 기본값

    def _fetch_github_metrics(self, url: str) -> Optional[Dict]:
        """GitHub API로 실제 stars, forks, issues 수집"""
        # URL에서 owner/repo 추출
        try:
            if 'github.com' not in url:
                return None

            parts = url.rstrip('/').split('/')
            if len(parts) < 2:
                return None

            repo_index = parts.index('github.com') + 1
            if repo_index >= len(parts):
                return None

            owner_repo = f"{parts[repo_index]}/{parts[repo_index + 1]}"
        except (ValueError, IndexError):
            return None

        # 캐시 확인
        if owner_repo in self.github_metrics_cache:
            return self.github_metrics_cache[owner_repo]

        try:
            # gh CLI로 GitHub API 호출
            result = subprocess.run([
                'gh', 'api', f'repos/{owner_repo}',
                '-q', '{stargazers_count, forks_count, open_issues_count, subscribers_count}'
            ], capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                metrics = json.loads(result.stdout)
                self.github_metrics_cache[owner_repo] = metrics
                logger.debug("GitHub metrics for %s: stars=%d, forks=%d",
                           owner_repo, metrics.get('stargazers_count', 0),
                           metrics.get('forks_count', 0))
                return metrics
        except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError) as e:
            logger.debug("Failed to fetch GitHub metrics: %s", e)

        return None

    def _calculate_demand_index(self, metrics: Dict) -> float:
        """수요 지수 계산 (로그 정규화 적용)"""
        stars = metrics.get('stargazers_count', 0)
        forks = metrics.get('forks_count', 0)
        issues = metrics.get('open_issues_count', 0)
        subscribers = metrics.get('subscribers_count', 0)

        # 로그 정규화 (스타 수의 과도한 영향 방지)
        def log_normalize(x: int) -> float:
            if x <= 0:
                return 0.0
            return math.log10(x + 1) / math.log10(100000 + 1)  # 100K stars를 최대로

        # 가중평균 (stars 60%, forks 20%, issues 10%, subscribers 10%)
        demand_index = (
            log_normalize(stars) * 0.60 +
            log_normalize(forks) * 0.20 +
            log_normalize(issues) * 0.10 +
            log_normalize(subscribers) * 0.10
        )

        return min(demand_index, 1.0)

    def _score_recency(self, idea: Dict) -> float:
        """최신성 점수"""
        discovered_at = idea.get('discovered_at', '')
        if not discovered_at:
            return 0.5

        try:
            dt = datetime.fromisoformat(discovered_at)
            age_hours = (datetime.now() - dt).total_seconds() / 3600

            if age_hours < 1:
                return 1.0
            elif age_hours < 24:
                return 0.8
            elif age_hours < 168:  # 7일
                return 0.5
            else:
                return 0.2
        except:
            return 0.5

    def _score_severity(self, idea: Dict) -> float:
        """심각도 점수"""
        severity = idea.get('severity', '').upper()
        cvss_score = idea.get('cvss_score', 0)

        # CVE인 경우 CVSS 점수 사용
        if cvss_score:
            return min(cvss_score / 10.0, 1.0)

        # priority 기반
        priority = idea.get('priority', '').lower()
        if priority == 'critical':
            return 1.0
        elif priority == 'high':
            return 0.8
        elif priority == 'medium':
            return 0.5
        else:
            return 0.2

    def _score_feasibility(self, idea: Dict) -> float:
        """구현 가능성 점수"""
        complexity = idea.get('complexity', '').lower()

        if complexity == 'simple':
            return 1.0
        elif complexity == 'medium':
            return 0.7
        elif complexity == 'complex':
            return 0.4
        else:
            return 0.5

    def _score_novelty(self, idea: Dict, existing_ideas: List[Dict] = None) -> float:
        """새로움 점수 (의미론적 중복 감지)"""
        if not existing_ideas:
            return 1.0

        title = idea.get('title', '').lower()
        description = idea.get('description', '').lower()

        # 의미론적 중복 체크
        for existing in existing_ideas:
            existing_title = existing.get('title', '').lower()
            existing_desc = existing.get('description', '').lower()

            # 제목 유사도 체크
            if self._calculate_similarity(title, existing_title) > 0.7:
                return 0.3

            # 설명 유사도 체크
            if self._calculate_similarity(description, existing_desc) > 0.75:
                return 0.4

        return 1.0

    def _calculate_similarity(self, a: str, b: str) -> float:
        """두 문자열 간의 유사도 계산 (difflib SequenceMatcher)"""
        from difflib import SequenceMatcher
        if not a or not b:
            return 0.0
        return SequenceMatcher(None, a, b).ratio()

    def _apply_feedback_correction(self, source: str, weights: Dict) -> Dict:
        """피드백 루프 기반 가중치 보정"""
        if not self.feedback_data or source not in self.feedback_data:
            return weights

        source_feedback = self.feedback_data[source]

        # 성공률이 낮은 차원의 가중치 감소
        for dimension in weights:
            success_rate = source_feedback.get(f'{dimension}_success_rate', 0.5)
            if success_rate < 0.4:  # 성공률 40% 미만
                weights[dimension] *= 0.8  # 20% 감축
            elif success_rate > 0.7:  # 성공률 70% 이상
                weights[dimension] *= 1.1  # 10% 증가

        # 정규화 (합이 1이 되도록)
        total = sum(weights.values())
        if total > 0:
            weights = {k: v / total for k, v in weights.items()}

        return weights

    def _apply_success_pattern_correction(self, base_score: float, idea: Dict, source: str) -> float:
        """성공 패턴 기반 점수 보정"""
        if not self.feedback_data or 'success_patterns' not in self.feedback_data:
            return base_score

        patterns = self.feedback_data['success_patterns']

        # 기술 스택 패턴 매칭
        tech_stack = idea.get('tech_stack', [])
        for tech in tech_stack:
            if tech in patterns.get('high_success_techs', {}):
                multiplier = patterns['high_success_techs'][tech]
                base_score *= multiplier

        # 복잡도 패턴 매칭
        complexity = idea.get('complexity', 'medium')
        if complexity in patterns.get('high_success_complexity', []):
            base_score *= 1.05  # 5% 증가

        return min(base_score, 1.0)

    def _load_feedback_history(self) -> Dict:
        """피드백 이력 로드"""
        if not self.feedback_history_path or not self.feedback_history_path.exists():
            return {}

        try:
            with open(self.feedback_history_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning("Failed to load feedback history: %s", e)
            return {}

    def record_outcome(self, idea: Dict, success: bool, metadata: Dict = None):
        """프로젝트 결과 기록 (지속적 학습)"""
        if not self.feedback_history_path:
            return

        # 초기화
        if not self.feedback_history_path.exists():
            self.feedback_history_path.parent.mkdir(parents=True, exist_ok=True)
            self.feedback_data = {}

        # 소스별 통계 업데이트
        source = idea.get('source', 'manual')
        if source not in self.feedback_data:
            self.feedback_data[source] = {
                'total': 0,
                'success': 0,
                'failures': 0
            }

        self.feedback_data[source]['total'] += 1
        if success:
            self.feedback_data[source]['success'] += 1
        else:
            self.feedback_data[source]['failures'] += 1

        # 성공 패턴 업데이트
        if success:
            if 'success_patterns' not in self.feedback_data:
                self.feedback_data['success_patterns'] = {
                    'high_success_techs': {},
                    'high_success_complexity': []
                }

            # 기술 스택 성공률 추적
            for tech in idea.get('tech_stack', []):
                if tech not in self.feedback_data['success_patterns']['high_success_techs']:
                    self.feedback_data['success_patterns']['high_success_techs'][tech] = {'count': 0, 'success': 0}

                stats = self.feedback_data['success_patterns']['high_success_techs'][tech]
                stats['count'] += 1
                stats['success'] += 1

        # 저장
        try:
            with open(self.feedback_history_path, 'w') as f:
                json.dump(self.feedback_data, f, indent=2)
        except Exception as e:
            logger.warning("Failed to save feedback history: %s", e)

    def get_scoring_insights(self) -> Dict:
        """점수 시스템 인사이트 반환"""
        insights = {
            'source_weights': self.SOURCE_WEIGHTS.copy(),
            'feedback_stats': {},
            'recommendations': []
        }

        if self.feedback_data:
            for source, data in self.feedback_data.items():
                if source == 'success_patterns':
                    continue

                total = data.get('total', 0)
                success = data.get('success', 0)
                success_rate = success / total if total > 0 else 0

                insights['feedback_stats'][source] = {
                    'total_projects': total,
                    'success_rate': round(success_rate, 2)
                }

                if success_rate < 0.5:
                    insights['recommendations'].append(
                        f"{source}: 성공률 낮음 ({success_rate:.0%}), 가중치 재조정 권장"
                    )

        return insights
