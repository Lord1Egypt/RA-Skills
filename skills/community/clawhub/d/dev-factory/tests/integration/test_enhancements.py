"""Tests for enhanced builder features

- Adaptive scoring system
- Checkpoint and resume
- Test coverage validation
- Spec validation
- Dynamic template management
"""

import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from builder.discovery.scorer import AdaptiveIdeaScorer
from builder.checkpoint import PipelineCheckpoint, ProjectCheckpoint, CheckpointState
from builder.testing.runner import TestRunner, TestCoverageResult
from builder.integration.spec_validator import SpecValidator, ValidationResult
from builder.integration.template_manager import SpecTemplateManager


class TestAdaptiveIdeaScorer:
    """적응형 점수 시스템 테스트"""

    @pytest.fixture
    def scorer(self, tmp_path):
        """테스트용 scorer"""
        feedback_path = tmp_path / "feedback.json"
        return AdaptiveIdeaScorer(feedback_history_path=feedback_path)

    @pytest.fixture
    def sample_cve_idea(self):
        """CVE 아이디어 샘플"""
        return {
            'title': 'CVE-2026-1234 Scanner',
            'description': 'Scanner for CVE-2026-1234',
            'source': 'cve_database',
            'severity': 'HIGH',
            'cvss_score': 8.5,
            'complexity': 'medium',
            'discovered_at': '2026-03-12T10:00:00'
        }

    @pytest.fixture
    def sample_github_idea(self):
        """GitHub 아이디어 샘플"""
        return {
            'title': 'GitHub: example/cool-tool',
            'description': 'A cool tool',
            'source': 'github_trending',
            'complexity': 'medium',
            'url': 'https://github.com/example/cool-tool',
            'github_metrics': {
                'stars': 1500,
                'forks': 200,
                'issues': 15,
                'subscribers': 50
            },
            'discovered_at': '2026-03-12T10:00:00'
        }

    def test_source_specific_weights(self, scorer, sample_cve_idea, sample_github_idea):
        """소스별 가중치 적용 확인"""
        cve_score = scorer.score(sample_cve_idea, [])
        github_score = scorer.score(sample_github_idea, [])

        # CVE는 severity가 중요하므로 HIGH severity로 높은 점수
        assert cve_score > 0.5

        # GitHub는 stars가 중요하므로 많은 stars로 높은 점수
        assert github_score > 0.5

    def test_github_metrics_integration(self, scorer, sample_github_idea):
        """GitHub 메트릭 통합 확인"""
        score = scorer.score(sample_github_idea, [])

        # 높은 stars 수로 인한 높은 수요 점수
        assert score > 0.5

    def test_feedback_recording(self, scorer, sample_cve_idea):
        """피드백 기록 확인"""
        # 성공 기록
        scorer.record_outcome(sample_cve_idea, success=True)

        # 파일에 저장되었는지 확인
        assert scorer.feedback_history_path.exists()

        # 데이터 로드 확인
        data = scorer._load_feedback_history()
        assert 'cve_database' in data
        assert data['cve_database']['success'] == 1

    def test_scoring_insights(self, scorer, sample_cve_idea):
        """점수 시스템 인사이트 확인"""
        scorer.record_outcome(sample_cve_idea, success=True)

        insights = scorer.get_scoring_insights()

        assert 'source_weights' in insights
        assert 'feedback_stats' in insights
        assert 'recommendations' in insights


class TestPipelineCheckpoint:
    """체크포인트 시스템 테스트"""

    @pytest.fixture
    def checkpoint_manager(self, tmp_path):
        """테스트용 체크포인트 관리자"""
        return PipelineCheckpoint(checkpoint_dir=tmp_path / "checkpoints")

    def test_save_and_load_checkpoint(self, checkpoint_manager):
        """체크포인트 저장 및 로드 확인"""
        # 저장
        state_data = {
            'project_title': 'test-project',
            'stage': 'building'
        }
        result = checkpoint_manager.save_state('building', state_data)
        assert result is True

        # 로드
        loaded = checkpoint_manager.load_last_checkpoint()
        assert loaded is not None
        assert loaded.stage == 'building'
        assert loaded.metadata['project_title'] == 'test-project'

    def test_retry_count_increment(self, checkpoint_manager):
        """재시도 횟수 증가 확인"""
        checkpoint_manager.save_state('testing', {'test': 'data'})

        retry_count = checkpoint_manager.increment_retry()
        assert retry_count == 1

        retry_count = checkpoint_manager.increment_retry()
        assert retry_count == 2

    def test_error_recording(self, checkpoint_manager):
        """에러 기록 확인"""
        checkpoint_manager.save_state('building', {})

        checkpoint_manager.add_error("Test error message")

        checkpoint = checkpoint_manager.load_last_checkpoint()
        assert len(checkpoint.errors) == 1
        assert checkpoint.errors[0]['message'] == "Test error message"

    def test_get_checkpoint_by_stage(self, checkpoint_manager):
        """스테이지별 체크포인트 조회 확인"""
        checkpoint_manager._current_checkpoint = CheckpointState(
            stage='testing',
            project_title='test-project'
        )
        checkpoint_manager.save_state('testing', {'data': 'value'})

        checkpoint = checkpoint_manager.get_checkpoint('testing')
        assert checkpoint is not None
        assert checkpoint.stage == 'testing'


class TestProjectCheckpoint:
    """프로젝트별 체크포인트 테스트"""

    @pytest.fixture
    def project_checkpoint(self, tmp_path):
        """테스트용 프로젝트 체크포인트"""
        return ProjectCheckpoint(
            project_title='test-project',
            checkpoint_dir=tmp_path / "checkpoints"
        )

    def test_save_and_load_stage(self, project_checkpoint):
        """스테이지 저장 및 로드 확인"""
        # 저장
        result = project_checkpoint.save_stage('building', {'key': 'value'})
        assert result is True

        # 로드
        loaded = project_checkpoint.load_stage()
        assert loaded is not None
        assert loaded.stage == 'building'

    def test_can_resume(self, project_checkpoint):
        """재개 가능 여부 확인"""
        # 완료되지 않은 상태에서는 재개 가능
        project_checkpoint.save_stage('building', {})
        assert project_checkpoint.can_resume() is True

        # 완료된 상태에서는 재개 불가
        project_checkpoint.save_stage('completed', {})
        assert project_checkpoint.can_resume() is False


class TestCoverageValidation:
    """커버리지 검증 테스트"""

    @pytest.fixture
    def test_runner(self):
        """테스트용 TestRunner"""
        return TestRunner(use_coverage=True)

    def test_coverage_result_creation(self):
        """커버리지 결과 생성 확인"""
        result = TestCoverageResult(
            success=True,
            coverage_percent=85.5,
            under_covered_files=['file1.py'],
            total_lines=1000,
            covered_lines=855
        )

        assert result.success is True
        assert result.coverage_percent == 85.5
        assert result.meets_threshold is True  # 80% 이상

        data = result.to_dict()
        assert data['coverage_percent'] == 85.5
        assert data['meets_threshold'] is True

    @patch('subprocess.run')
    def test_run_with_coverage_success(self, mock_run, test_runner, tmp_path):
        """커버리지 포함 테스트 실행 성공 확인"""
        # Mock 테스트 결과
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "tests passed"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        # Mock coverage.json
        coverage_file = tmp_path / 'coverage.json'
        coverage_data = {
            'totals': {
                'percent_covered': 85.0,
                'num_statements': 1000,
                'covered_lines': 850
            },
            'files': {}
        }
        coverage_file.write_text(json.dumps(coverage_data))

        result = test_runner.run_with_coverage(tmp_path)

        assert result.success is True
        assert result.coverage_percent == 85.0
        assert result.meets_threshold is True

    def test_coverage_threshold_enforcement(self):
        """커버리지 임계값 강제 확인"""
        # 80% 미만 커버리지
        result = TestCoverageResult(
            success=True,
            coverage_percent=75.0,
            under_covered_files=[],
            total_lines=1000,
            covered_lines=750
        )

        assert result.meets_threshold is False


class TestSpecValidator:
    """스펙 검증 테스트"""

    @pytest.fixture
    def validator(self):
        """테스트용 SpecValidator"""
        return SpecValidator()

    @pytest.fixture
    def sample_idea(self):
        """샘플 아이디어"""
        return {
            'title': 'Test Project',
            'description': 'A test project',
            'source': 'cve_database',
            'complexity': 'medium'
        }

    def test_validate_good_spec(self, validator, sample_idea):
        """좋은 스펙 검증 확인"""
        good_spec = """
## 개요
테스트 프로젝트입니다.

## 목표
다음 목표를 달성합니다.

## 주요 기능
1. 기능 1
2. 기능 2

## 기능
핵심 기능 구현

## 기술 스펙
Python을 사용합니다.

## 아키텍처
모듈 구조로 되어 있습니다.

## 파일 구조
```
project/
├── src/
└── tests/
```

## 성공 기준
- [ ] 기능 구현
- [ ] 테스트 작성
- [ ] 배포 완료

## CVE 정보
- CVE ID: CVE-2026-1234
- 심각도: HIGH
- CVSS: 8.5
"""

        report = validator.validate_spec(good_spec, sample_idea)

        # 높은 점수 (0.7 이상)
        assert report.score >= 0.7
        assert report.overall_result in [ValidationResult.PASS, ValidationResult.WARNING]

    def test_validate_poor_spec(self, validator, sample_idea):
        """나쁜 스펙 검증 확인"""
        poor_spec = "간단한 설명"

        report = validator.validate_spec(poor_spec, sample_idea)

        # 낮은 점수 (0.5 미만)
        assert report.score < 0.5
        assert report.overall_result == ValidationResult.FAIL

    def test_required_sections_check(self, validator, sample_idea):
        """필수 섹션 체크 확인"""
        spec_without_sections = "내용만 있고 섹션이 없음"

        report = validator.validate_spec(spec_without_sections, sample_idea)

        # 필수 섹션 누락으로 FAIL
        fail_checks = [c for c in report.checks if c.result == ValidationResult.FAIL]
        assert len(fail_checks) > 0

    def test_validate_notion_spec_quick_check(self, validator, sample_idea):
        """Notion 스펙 빠른 검사 확인"""
        good_spec = """
## 개요
프로젝트 개요

## 목표
프로젝트 목표

## 기능
핵심 기능 설명

## 주요 기능
기능 설명

## 기술 스펙
기술 스택

## 아키텍처
시스템 아키텍처

## 파일 구조
파일 구조

## 성공 기준
- [ ] 조건 1
- [ ] 조건 2
- [ ] 조건 3
- [ ] 조건 4
- [ ] 조건 5
- [ ] 조건 6
- [ ] 조건 7
- [ ] 조건 8

## CVE 정보
- CVE ID: CVE-2026-1234
- 심각도: HIGH
"""

        result = validator.validate_notion_spec(good_spec, sample_idea)
        assert result is True


class TestSpecTemplateManager:
    """스펙 템플릿 관리자 테스트"""

    @pytest.fixture
    def template_manager(self, tmp_path):
        """테스트용 템플릿 관리자"""
        return SpecTemplateManager(success_patterns_path=tmp_path / "patterns.json")

    def test_generate_simple_spec(self, template_manager):
        """간단한 스펙 생성 확인"""
        idea = {
            'title': 'Simple Tool',
            'description': 'A simple tool',
            'source': 'manual',
            'complexity': 'simple',
            'tech_stack': ['Python']
        }

        spec = template_manager.generate_dynamic_spec(idea)

        # 필수 섹션 포함 확인
        assert '## 📋 프로젝트 개요' in spec
        assert '## 🎯 개발 목표' in spec
        assert '## 💻 기술 스펙' in spec
        assert '## 📁 파일 구조' in spec
        assert '## ✅ 성공 기준' in spec

    def test_generate_cve_spec(self, template_manager):
        """CVE 스펙 생성 확인"""
        idea = {
            'title': 'CVE Scanner',
            'description': 'CVE vulnerability scanner',
            'source': 'cve_database',
            'complexity': 'medium',
            'cve_id': 'CVE-2026-1234',
            'severity': 'HIGH',
            'cvss_score': 8.5,
            'tech_stack': ['Python']
        }

        spec = template_manager.generate_dynamic_spec(idea)

        # CVE 관련 섹션 포함
        assert 'CVE-2026-1234' in spec
        assert 'HIGH' in spec
        assert '## 🔍 CVE 정보' in spec

    def test_generate_github_spec(self, template_manager):
        """GitHub 스펙 생성 확인"""
        idea = {
            'title': 'GitHub: example/tool',
            'description': 'A tool from GitHub',
            'source': 'github_trending',
            'complexity': 'medium',
            'url': 'https://github.com/example/tool',
            'github_metrics': {
                'stars': 1000,
                'forks': 100
            },
            'tech_stack': ['Python']
        }

        spec = template_manager.generate_dynamic_spec(idea)

        # GitHub 관련 섹션 포함
        assert '1,000 ⭐' in spec
        assert '## 🔍 GitHub 정보' in spec

    def test_complexity_adaptation(self, template_manager):
        """복잡도별 적응 확인"""
        simple_idea = {
            'title': 'Simple',
            'description': 'Simple project',
            'source': 'manual',
            'complexity': 'simple',
            'tech_stack': ['Python']
        }

        complex_idea = {
            'title': 'Complex',
            'description': 'Complex project',
            'source': 'manual',
            'complexity': 'complex',
            'tech_stack': ['Python']
        }

        simple_spec = template_manager.generate_dynamic_spec(simple_idea)
        complex_spec = template_manager.generate_dynamic_spec(complex_idea)

        # 복잡한 프로젝트가 더 많은 섹션과 내용을 가짐
        assert len(complex_spec) > len(simple_spec)

        # 복잡한 프로젝트는 아키텍처 섹션 포함
        assert '## 🏗️ 아키텍처' in complex_spec

    def test_success_pattern_recording(self, template_manager, tmp_path):
        """성공 패턴 기록 확인"""
        idea = {
            'title': 'Test',
            'description': 'Test project',
            'source': 'cve_database',
            'complexity': 'medium'
        }

        # 성공 패턴 기록
        template_manager.record_success_pattern(idea, success=True, pattern="custom_pattern")

        # 파일 생성 확인
        assert template_manager.success_patterns_path.exists()

        # 데이터 확인
        import json
        with open(template_manager.success_patterns_path) as f:
            data = json.load(f)

        assert 'patterns' in data
        assert len(data['patterns']) == 1
        assert data['patterns'][0]['pattern'] == 'custom_pattern'
        assert data['patterns'][0]['success_rate'] == 1.0
