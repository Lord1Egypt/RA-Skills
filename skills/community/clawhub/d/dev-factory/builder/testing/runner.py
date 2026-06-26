"""TestRunner - 통합 테스트 실행 및 리포팅

Phase 1: Basic test execution
Phase 2: Coverage validation with pytest-cov
"""

import logging
import os
import subprocess
import json
import re
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger('builder-agent.testing')


class TestCoverageResult:
    """테스트 커버리지 결과"""

    def __init__(self, success: bool, coverage_percent: float,
                 under_covered_files: List[str] = None,
                 total_lines: int = 0, covered_lines: int = 0):
        self.success = success
        self.coverage_percent = coverage_percent
        self.under_covered_files = under_covered_files or []
        self.total_lines = total_lines
        self.covered_lines = covered_lines

    @property
    def meets_threshold(self) -> bool:
        """80% 임계값 충족 여부"""
        return self.coverage_percent >= 80.0

    def to_dict(self) -> Dict:
        return {
            'success': self.success,
            'coverage_percent': round(self.coverage_percent, 2),
            'under_covered_files': self.under_covered_files,
            'total_lines': self.total_lines,
            'covered_lines': self.covered_lines,
            'meets_threshold': self.meets_threshold
        }


class TestRunner:
    """프로젝트 테스트 실행 및 결과 분석"""

    # 커버리지 임계값
    COVERAGE_THRESHOLD = 80.0  # 80%

    def __init__(self, timeout: int = 30, use_coverage: bool = True):
        """초기화

        Args:
            timeout: 테스트 타임아웃 (초)
            use_coverage: 커버리지 측정 사용 여부
        """
        self.timeout = timeout
        self.use_coverage = use_coverage
        self._check_pytest_cov()

    def run(self, project_path: Path) -> Dict:
        """프로젝트 테스트 실행"""
        if not project_path.exists():
            return {
                'success': False,
                'output': f'Project path not found: {project_path}',
                'tests_run': 0,
                'failures': 0,
                'errors': 0
            }

        logger.info("Running tests in %s", project_path)

        try:
            result = subprocess.run(
                ['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
                cwd=str(project_path),
                capture_output=True,
                text=True,
                timeout=self.timeout,
                env={**os.environ, 'PYTHONPATH': 'src'}
            )

            output = result.stdout + result.stderr
            parsed = self._parse_unittest_output(output)

            return {
                'success': result.returncode == 0,
                'output': output,
                'returncode': result.returncode,
                **parsed
            }

        except subprocess.TimeoutExpired:
            logger.warning("Test timeout in %s", project_path)
            return {
                'success': False,
                'output': 'Test timeout',
                'tests_run': 0,
                'failures': 0,
                'errors': 0
            }
        except Exception as e:
            logger.warning("Test error: %s", e)
            return {
                'success': False,
                'output': str(e),
                'tests_run': 0,
                'failures': 0,
                'errors': 0
            }

    def run_specific(self, project_path: Path, test_file: str) -> Dict:
        """특정 테스트 파일만 실행"""
        try:
            result = subprocess.run(
                ['python3', '-m', 'unittest', test_file, '-v'],
                cwd=str(project_path),
                capture_output=True,
                text=True,
                timeout=self.timeout,
                env={**os.environ, 'PYTHONPATH': 'src'}
            )

            output = result.stdout + result.stderr
            parsed = self._parse_unittest_output(output)

            return {
                'success': result.returncode == 0,
                'output': output,
                **parsed
            }

        except Exception as e:
            return {
                'success': False,
                'output': str(e),
                'tests_run': 0,
                'failures': 0,
                'errors': 0
            }

    def _parse_unittest_output(self, output: str) -> Dict:
        """unittest 출력 파싱"""
        tests_run = 0
        failures = 0
        errors = 0

        # "Ran X tests in Ys" 패턴
        import re
        match = re.search(r'Ran (\d+) tests?', output)
        if match:
            tests_run = int(match.group(1))

        # "FAILED (failures=X, errors=Y)" 패턴
        match = re.search(r'FAILED \(failures=(\d+), errors=(\d+)\)', output)
        if match:
            failures = int(match.group(1))
            errors = int(match.group(2))

        # "OK" 또는 "FAILED" 확인
        success = 'OK' in output.split('\n')[-1] if output else False

        return {
            'tests_run': tests_run,
            'failures': failures,
            'errors': errors,
            'parsed_success': success
        }

    def save_report(self, result: Dict, report_path: Path):
        """테스트 결과 리포트 저장"""
        report_path.parent.mkdir(parents=True, exist_ok=True)

        report = {
            'timestamp': datetime.now().isoformat(),
            'success': result['success'],
            'tests_run': result['tests_run'],
            'failures': result['failures'],
            'errors': result['errors'],
            'output': result['output'][-1000:] if len(result['output']) > 1000 else result['output']
        }

        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        logger.info("Test report saved to %s", report_path)

    # ──────────────────────────────────────────────
    # Coverage Testing
    # ──────────────────────────────────────────────

    def run_with_coverage(self, project_path: Path, min_coverage: float = None) -> TestCoverageResult:
        """커버리지 측정과 함께 테스트 실행

        Args:
            project_path: 프로젝트 경로
            min_coverage: 최소 커버리지 요구사항 (기본: 80%)

        Returns:
            TestCoverageResult 객체
        """
        if min_coverage is None:
            min_coverage = self.COVERAGE_THRESHOLD

        if not self.use_coverage or not self._has_pytest_cov():
            logger.info("pytest-cov not available, running basic tests")
            # 기본 테스트 실행
            basic_result = self.run(project_path)
            return TestCoverageResult(
                success=basic_result['success'],
                coverage_percent=0.0,
                under_covered_files=[],
                total_lines=0,
                covered_lines=0
            )

        logger.info("Running tests with coverage in %s (min: %.1f%%)",
                   project_path, min_coverage)

        try:
            # pytest-cov로 커버리지 측정
            result = subprocess.run(
                ['python3', '-m', 'pytest',
                 '--cov=.',
                 '--cov-report=json',
                 '--cov-report=term-missing',
                 '-v'],
                cwd=str(project_path),
                capture_output=True,
                text=True,
                timeout=self.timeout + 30,  # 커버리지 측정 추가 시간
                env={**os.environ, 'PYTHONPATH': 'src'}
            )

            output = result.stdout + result.stderr

            # 커버리지 JSON 파일 읽기
            coverage_file = project_path / 'coverage.json'
            if coverage_file.exists():
                with open(coverage_file, 'r') as f:
                    coverage_data = json.load(f)

                coverage_result = self._parse_coverage_data(
                    coverage_data,
                    min_coverage
                )

                # 테스트 성공 여부 확인
                if result.returncode != 0:
                    logger.warning("Tests failed with coverage: %.2f%%",
                                 coverage_result.coverage_percent)
                    coverage_result.success = False

                # 커버리지 미달 시 실패
                if not coverage_result.meets_threshold:
                    logger.warning("Coverage below threshold: %.2f%% < %.1f%%",
                                 coverage_result.coverage_percent, min_coverage)
                    coverage_result.success = False

                logger.info("Coverage: %.2f%% (%d/%d lines), %d files below threshold",
                           coverage_result.coverage_percent,
                           coverage_result.covered_lines,
                           coverage_result.total_lines,
                           len(coverage_result.under_covered_files))

                # 커버리지 리포트 저장
                self._save_coverage_report(coverage_result, output, project_path)

                return coverage_result
            else:
                logger.warning("coverage.json not found, falling back to basic parsing")
                return self._parse_coverage_from_output(output, min_coverage)

        except subprocess.TimeoutExpired:
            logger.warning("Test with coverage timeout in %s", project_path)
            return TestCoverageResult(
                success=False,
                coverage_percent=0.0,
                under_covered_files=[],
                total_lines=0,
                covered_lines=0
            )
        except FileNotFoundError:
            logger.warning("pytest not found, running unittest instead")
            # pytest가 없으면 unittest로 폴백
            basic_result = self.run(project_path)
            return TestCoverageResult(
                success=basic_result['success'],
                coverage_percent=0.0,
                under_covered_files=[],
                total_lines=0,
                covered_lines=0
            )
        except Exception as e:
            logger.warning("Coverage test error: %s", e)
            return TestCoverageResult(
                success=False,
                coverage_percent=0.0,
                under_covered_files=[],
                total_lines=0,
                covered_lines=0
            )

    def _parse_coverage_data(self, coverage_data: Dict, min_coverage: float) -> TestCoverageResult:
        """coverage.json 데이터 파싱"""
        totals = coverage_data.get('totals', {})
        coverage_percent = totals.get('percent_covered', 0.0)
        total_lines = totals.get('num_statements', 0)
        covered_lines = totals.get('covered_lines', 0)

        # 80% 미만 커버리지 파일 식별
        under_covered = []
        files = coverage_data.get('files', {})

        for filename, file_data in files.items():
            summary = file_data.get('summary', {})
            file_coverage = summary.get('percent_covered', 0.0)

            if file_coverage < min_coverage:
                under_covered.append({
                    'file': filename,
                    'coverage': round(file_coverage, 2),
                    'missing': summary.get('missing_lines', 0)
                })

        return TestCoverageResult(
            success=True,
            coverage_percent=coverage_percent,
            under_covered_files=[f['file'] for f in under_covered],
            total_lines=total_lines,
            covered_lines=covered_lines
        )

    def _parse_coverage_from_output(self, output: str, min_coverage: float) -> TestCoverageResult:
        """테스트 출력에서 커버리지 정보 파싱 (폴백)"""
        # pytest-cov 출력에서 커버리지 퍼센트 추출
        match = re.search(r'TOTAL\s+(\d+)\s+\d+\s+(\d+)', output)
        if match:
            total_lines = int(match.group(1))
            # 두 번째 숫자는 커버리지되지 않은 라인
            uncovered_lines = int(match.group(2))
            covered_lines = total_lines - uncovered_lines
            coverage_percent = (covered_lines / total_lines * 100) if total_lines > 0 else 0.0

            return TestCoverageResult(
                success=coverage_percent >= min_coverage,
                coverage_percent=coverage_percent,
                under_covered_files=[],
                total_lines=total_lines,
                covered_lines=covered_lines
            )

        # 파싱 실패 시 기본값 반환
        return TestCoverageResult(
            success=False,
            coverage_percent=0.0,
            under_covered_files=[],
            total_lines=0,
            covered_lines=0
        )

    def _save_coverage_report(self, result: TestCoverageResult, output: str, project_path: Path):
        """커버리지 리포트 저장"""
        report_path = project_path / 'coverage_report.json'

        report = {
            'timestamp': datetime.now().isoformat(),
            'coverage_percent': result.coverage_percent,
            'meets_threshold': result.meets_threshold,
            'total_lines': result.total_lines,
            'covered_lines': result.covered_lines,
            'under_covered_files': result.under_covered_files,
            'test_output': output[-2000:] if len(output) > 2000 else output
        }

        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        logger.info("Coverage report saved to %s", report_path)

    def _check_pytest_cov(self) -> bool:
        """pytest-cov 설치 여부 확인"""
        try:
            result = subprocess.run(
                ['python3', '-c', 'import pytest_cov'],
                capture_output=True,
                timeout=5
            )
            self.pytest_cov_available = result.returncode == 0
            return self.pytest_cov_available
        except Exception:
            self.pytest_cov_available = False
            return False

    def _has_pytest_cov(self) -> bool:
        """pytest-cov 사용 가능 여부"""
        return getattr(self, 'pytest_cov_available', False)
