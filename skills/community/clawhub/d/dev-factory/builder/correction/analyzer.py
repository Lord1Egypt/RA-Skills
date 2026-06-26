"""에러 분석기 - 에러 타입 감지 및 수정 전략 결정"""

import re
import logging
from typing import Dict, Optional, Tuple

logger = logging.getLogger('builder-agent.correction.analyzer')


class ErrorAnalyzer:
    """에러 출력에서 구조화된 분석 결과를 생성"""

    def analyze(self, test_output: str) -> Dict:
        """테스트 출력에서 에러 타입, 위치, 수정 전략 분석"""
        error_type = self._detect_type(test_output)
        file_path, line_number = self._extract_location(test_output)
        details = self._extract_details(error_type, test_output)

        return {
            'type': error_type,
            'raw_output': test_output[:500],
            'file_path': file_path,
            'line_number': line_number,
            'details': details,
            'fix_suggestion': self._get_suggestion(error_type, details),
        }

    def _detect_type(self, output: str) -> str:
        """에러 타입 감지 (우선순위순)"""
        # import 에러 먼저 (가장 흔하고 수정이 쉬움)
        if 'ModuleNotFoundError' in output or 'ImportError' in output:
            return 'import_error'
        if 'KeyError' in output:
            return 'key_error'
        if 'AttributeError' in output:
            return 'attribute_error'
        if 'TypeError' in output:
            return 'type_error'
        if 'FAIL:' in output or 'AssertionError' in output or 'AssertionError' in output:
            return 'test_failure'
        if 'SyntaxError' in output:
            return 'syntax_error'
        if 'NameError' in output:
            return 'name_error'
        if 'ValueError' in output:
            return 'value_error'
        return 'unknown'

    def _extract_location(self, output: str) -> Tuple[Optional[str], Optional[int]]:
        """에러 위치 추출 (우선순위순 패턴 리스트)"""
        patterns = [
            # 표준 CPython: File "path", line N [, in func]
            r'\s*File "([^"]+)", line (\d+)',
            # 짧은 형식: path:N: message
            r'([\w./\\-]+\.py):(\d+):',
        ]
        for pattern in patterns:
            match = re.search(pattern, output)
            if match:
                return match.group(1), int(match.group(2))
        return None, None

    def _extract_details(self, error_type: str, output: str) -> Dict:
        """에러 타입별 상세 정보 추출"""
        details = {}

        if error_type == 'import_error':
            match = re.search(r"No module named '([\w.]+)'", output)
            if match:
                details['module'] = match.group(1)

        elif error_type == 'key_error':
            match = re.search(r"KeyError: ['\"](\w+)['\"]", output)
            if match:
                details['key'] = match.group(1)

        elif error_type == 'attribute_error':
            match = re.search(r"'(\w+)' object has no attribute '(\w+)'", output)
            if match:
                details['object_type'] = match.group(1)
                details['attribute'] = match.group(2)

        elif error_type == 'name_error':
            match = re.search(r"name '(\w+)' is not defined", output)
            if match:
                details['name'] = match.group(1)

        return details

    def _get_suggestion(self, error_type: str, details: Dict) -> str:
        """에러에 맞는 구체적 수정 제안"""
        if error_type == 'import_error' and 'module' in details:
            module = details['module']
            return f"Add 'import {module}' or fix import path for '{module}'"

        if error_type == 'key_error' and 'key' in details:
            key = details['key']
            return f"Use .get('{key}', default) instead of ['{key}']"

        if error_type == 'attribute_error' and 'attribute' in details:
            attr = details['attribute']
            return f"Add missing method/attribute '{attr}' or check object type"

        suggestions = {
            'import_error': 'Fix import paths or install missing module',
            'key_error': 'Check dictionary keys and use .get() for optional access',
            'attribute_error': 'Add missing attribute or check object initialization',
            'type_error': 'Fix data type mismatches',
            'test_failure': 'Review test assertions and fix implementation',
            'syntax_error': 'Fix Python syntax error',
            'name_error': 'Define the missing variable or fix typo',
            'value_error': 'Check input values and validation',
        }
        return suggestions.get(error_type, 'Manual review required')
