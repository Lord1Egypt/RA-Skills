"""BaseCorrectionEngine - 자가 수정 공통 로직"""

import os
import re
import subprocess
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger('builder-agent.correction')


class BaseCorrectionEngine:
    """자가 수정 엔진 기본 클래스

    self_correction_engine.py, acp_self_correction.py, hybrid_acp_correction.py의
    공통 메서드를 통합합니다.
    """

    MAX_RETRIES = 3

    def __init__(self, project_path: str, config=None):
        self.project_path = Path(project_path)
        self.retry_count = 0
        self.error_history: List[Dict] = []
        self.config = config

    # ──────────────────────────────────────────────
    # 테스트 실행 (3개 파일에서 동일했던 코드)
    # ──────────────────────────────────────────────

    def run_tests(self, timeout: int = 30) -> Dict:
        """프로젝트 테스트 실행"""
        if not self.project_path.exists():
            return {'success': False, 'output': 'Project path does not exist'}

        try:
            result = subprocess.run(
                ['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=timeout,
                env={**os.environ, 'PYTHONPATH': 'src'}
            )

            return {
                'success': result.returncode == 0,
                'output': result.stdout + result.stderr,
                'returncode': result.returncode
            }

        except subprocess.TimeoutExpired:
            return {'success': False, 'output': 'Test timeout'}
        except Exception as e:
            return {'success': False, 'output': str(e)}

    # ──────────────────────────────────────────────
    # 에러 분석 (3개 파일에서 동일했던 코드)
    # ──────────────────────────────────────────────

    ERROR_PATTERNS = {
        'import_error': ['ModuleNotFoundError', 'ImportError'],
        'missing_method': ['has no attribute'],
        'type_error': ['KeyError', 'TypeError', 'AttributeError'],
        'test_failure': ['FAIL:', 'AssertionError', 'AssertionError'],
    }

    def analyze_error(self, test_result: Dict) -> Dict:
        """테스트 결과에서 에러 분석"""
        output = test_result.get('output', '')

        for error_type, patterns in self.ERROR_PATTERNS.items():
            for pattern in patterns:
                if pattern in output:
                    # 파일 경로와 라인 번호 추출
                    file_path, line_number = self._extract_location(output)

                    return {
                        'type': error_type,
                        'raw_output': output[:500],
                        'fix_suggestion': self._get_fix_suggestion(error_type),
                        'file_path': file_path,
                        'line_number': line_number,
                    }

        return {
            'type': 'unknown',
            'raw_output': output[:500],
            'fix_suggestion': 'Manual review required',
            'file_path': None,
            'line_number': None,
        }

    def _extract_location(self, output: str) -> tuple:
        """에러 출력에서 파일 경로와 라인 번호 추출"""
        match = re.search(r'File "([^"]+)", line (\d+)', output)
        if match:
            return match.group(1), int(match.group(2))
        return None, None

    def _get_fix_suggestion(self, error_type: str) -> str:
        """에러 타입별 수정 제안"""
        suggestions = {
            'type_error': 'Check data structure and use .get() for optional keys',
            'import_error': 'Fix import paths or add module to PYTHONPATH',
            'missing_method': 'Implement the missing method in the class',
            'test_failure': 'Review test assertions and fix implementation',
        }
        return suggestions.get(error_type, 'Review error and fix accordingly')

    # ──────────────────────────────────────────────
    # 메모리/로깅 (3개 파일에서 동일했던 코드)
    # ──────────────────────────────────────────────

    def save_success(self, project_idea: Dict, mode: str = "direct"):
        """성공 패턴을 self-improving에 저장"""
        si_dir = Path.home() / "self-improving"
        si_dir.mkdir(parents=True, exist_ok=True)

        reflections_file = si_dir / "reflections.md"

        with open(reflections_file, 'a') as f:
            f.write(f"\n### {datetime.now().isoformat()}\n")
            f.write(f"**CONTEXT**: {project_idea.get('title', 'Unknown')} "
                    f"({project_idea.get('complexity', 'unknown')})\n")
            f.write(f"**REFLECTION**: Succeeded after {self.retry_count} attempt(s) via {mode}\n")
            f.write(f"**LESSON**: Mode={mode}, Retries={self.retry_count}\n")

        logger.info("Success pattern saved to self-improving")

    def log_failure(self, project_idea: Dict, error: Dict, mode: str = "direct"):
        """실패 패턴을 self-improving에 로깅"""
        si_dir = Path.home() / "self-improving"
        si_dir.mkdir(parents=True, exist_ok=True)

        corrections_file = si_dir / "corrections.md"

        with open(corrections_file, 'a') as f:
            f.write(f"\n### {datetime.now().isoformat()}\n")
            f.write(f"**PROJECT**: {project_idea.get('title', 'Unknown')}\n")
            f.write(f"**MODE**: {mode}\n")
            f.write(f"**ATTEMPT**: {self.retry_count}/{self.MAX_RETRIES}\n")
            f.write(f"**ERROR**: {error.get('type', 'unknown')}\n")
            f.write(f"**SUGGESTION**: {error.get('fix_suggestion', 'N/A')}\n")

        logger.info("Failure logged to self-improving")

    # ──────────────────────────────────────────────
    # 메인 루프 (서브클래스에서 오버라이드)
    # ──────────────────────────────────────────────

    def develop(self, project_idea: Dict) -> Dict:
        """자가 수정 루프를 통한 개발 - 서브클래스에서 구현"""
        raise NotImplementedError
