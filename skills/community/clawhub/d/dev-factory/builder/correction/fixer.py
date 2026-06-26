"""CodeFixer - 실제 코드 수정 (규칙 기반 + LLM fallback)"""

import os
import re
import logging
import subprocess
import urllib.request
import json
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger('builder-agent.correction.fixer')


class CodeFixer:
    """에러 분석 결과를 바탕으로 실제 코드 수정"""

    def __init__(self, glm_api_key: Optional[str] = None):
        self.glm_api_key = glm_api_key or os.environ.get('BUILDER_GLM_API_KEY')

    def fix(self, error: Dict, project_path: Path, complexity: str = "medium") -> bool:
        """에러 수정 시도

        Args:
            error: analyze_error() 반환값
            project_path: 프로젝트 경로
            complexity: 'simple', 'medium', 'complex'

        Returns:
            수정 성공 여부
        """
        error_type = error.get('type', 'unknown')
        file_path = error.get('file_path')
        line_number = error.get('line_number')

        if not file_path:
            logger.warning("No file path in error, cannot auto-fix")
            return False

        file_path = Path(file_path)
        if not file_path.exists():
            logger.warning("File %s not found", file_path)
            return False

        # 규칙 기반 수정 시도
        if self._fix_by_rules(error, file_path, line_number):
            return True

        # 규칙 기반 실패 시 LLM fallback
        if complexity == 'simple':
            return self._fix_via_glm(error, file_path, project_path)
        else:
            return self._fix_via_claude(error, file_path, project_path)

    def _fix_by_rules(self, error: Dict, file_path: Path, line_number: Optional[int]) -> bool:
        """규칙 기반 수정"""
        error_type = error.get('type')

        try:
            if error_type == 'key_error':
                return self._fix_key_error(error, file_path, line_number)
            elif error_type == 'import_error':
                return self._fix_import_error(error, file_path)
            elif error_type == 'attribute_error':
                return self._fix_attribute_error(error, file_path)
            elif error_type == 'name_error':
                return self._fix_name_error(error, file_path)
        except Exception as e:
            logger.warning("Rule-based fix failed: %s", e)

        return False

    def _fix_key_error(self, error: Dict, file_path: Path, line_number: Optional[int]) -> bool:
        """KeyError 수정: dict['key'] -> dict.get('key', '')"""
        if not line_number:
            return False

        key = error.get('details', {}).get('key')
        if not key:
            return False

        content = file_path.read_text()
        lines = content.splitlines()

        if line_number > len(lines):
            return False

        line = lines[line_number - 1]

        # dict['key'] 패턴을 dict.get('key', '')로 변경
        new_line = re.sub(
            rf"(\w+)\['{re.escape(key)}'\]",
            rf"\1.get('{key}', '')",
            line
        )

        if new_line != line:
            lines[line_number - 1] = new_line
            file_path.write_text('\n'.join(lines))
            logger.info("Fixed KeyError: changed ['%s'] to .get('%s', '') at line %d",
                       key, key, line_number)
            return True

        return False

    def _fix_import_error(self, error: Dict, file_path: Path) -> bool:
        """ImportError 수정: 누락된 import 추가"""
        module = error.get('details', {}).get('module')
        if not module:
            return False

        content = file_path.read_text()
        lines = content.splitlines()

        # 이미 import 되어 있는지 확인
        for line in lines:
            if f'import {module}' in line or f'from {module}' in line:
                return False

        # import 추가 (shebang이나 docstring 다음에)
        import_line = f'import {module}'
        insert_idx = 0

        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('#!'):
                insert_idx = i + 1
            elif stripped.startswith('"""') or stripped.startswith("'''"):
                # docstring 건너뛰기
                for j in range(i + 1, len(lines)):
                    if '"""' in lines[j] or "'''" in lines[j]:
                        insert_idx = j + 1
                        break
                break
            elif stripped.startswith('import ') or stripped.startswith('from '):
                insert_idx = i + 1

        lines.insert(insert_idx, import_line)
        file_path.write_text('\n'.join(lines))
        logger.info("Added import: %s at line %d", module, insert_idx + 1)
        return True

    def _fix_attribute_error(self, error: Dict, file_path: Path) -> bool:
        """AttributeError 수정: 간단한 경우만 처리"""
        details = error.get('details', {})
        obj_type = details.get('object_type')
        attr = details.get('attribute')

        # None 객체에서 속성 접근 시 guard 추가
        if obj_type == 'NoneType':
            content = file_path.read_text()

            # None.x 패턴을 찾아서 None 체크 추가
            # 이는 복잡하므로 LLM fallback 권장
            return False

        return False

    def _fix_name_error(self, error: Dict, file_path: Path) -> bool:
        """NameError 수정: 오타 교정"""
        name = error.get('details', {}).get('name')
        if not name:
            return False

        content = file_path.read_text()

        # 흔한 오타 목록
        typos = {
            'strng': 'string',
            'lst': 'list',
            'dictn': 'dictionary',
            'intger': 'integer',
        }

        if name in typos:
            fixed = content.replace(f" {name} ", f" {typos[name]} ")
            if fixed != content:
                file_path.write_text(fixed)
                logger.info("Fixed typo: %s -> %s", name, typos[name])
                return True

        return False

    # ──────────────────────────────────────────────
    # LLM Fallback
    # ──────────────────────────────────────────────

    def _fix_via_glm(self, error: Dict, file_path: Path, project_path: Path) -> bool:
        """GLM API로 수정 (Simple 프로젝트용)"""
        if not self.glm_api_key:
            logger.warning("GLM API key not configured")
            return False

        try:
            import urllib.request
            import json

            # GLM API 호출 (ZhipuAI / ChatGLM format)
            # 에러 컨텍스트와 파일 내용 전송
            file_content = file_path.read_text()

            prompt = f"""Fix the following error in this Python code:

Error Type: {error.get('type')}
Error Details: {error.get('raw_output', '')[:500]}
File: {file_path}
Line: {error.get('line_number', '?')}

Code:
```python
{file_content}
```

Return ONLY the fixed Python code, no explanations.
"""

            data = {
                "model": "glm-4",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1
            }

            req = urllib.request.Request(
                "https://open.bigmodel.cn/api/paas/v4/chat/completions",
                data=json.dumps(data).encode('utf-8'),
                headers={
                    'Authorization': f'Bearer {self.glm_api_key}',
                    'Content-Type': 'application/json'
                }
            )

            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode())
                content = result['choices'][0]['message']['content']

                # 코드 블록 추출
                if '```' in content:
                    code_lines = content.split('```')[1].split('\n')
                    if code_lines[0].startswith('python'):
                        code_lines = code_lines[1:]
                    fixed_code = '\n'.join(code_lines).rstrip()
                else:
                    fixed_code = content.strip()

                # 백업 후 수정
                backup_path = file_path.with_suffix('.py.backup')
                backup_path.write_text(file_content)
                file_path.write_text(fixed_code)

                logger.info("GLM fix applied, backup at %s", backup_path)
                return True

        except Exception as e:
            logger.warning("GLM API fix failed: %s", e)
            return False

    def _fix_via_claude(self, error: Dict, file_path: Path, project_path: Path) -> bool:
        """Claude Code CLI로 수정 (Medium/Complex 프로젝트용)"""
        import subprocess

        file_content = file_path.read_text()

        try:
            rel_path = file_path.relative_to(project_path)
        except ValueError:
            rel_path = file_path  # fallback: 절대 경로 사용

        prompt = f"""Fix the following error in this project:

Error Type: {error.get('type')}
Error Details: {error.get('raw_output', '')[:500]}
File: {rel_path}
Line: {error.get('line_number', '?')}

Analyze the error, identify the root cause, and apply the minimal fix.
Ensure the fix doesn't break other functionality.

After fixing, the code should pass all tests.
"""

        try:
            result = subprocess.run([
                'claude', '-p', prompt,
                '--allowedTools', 'Edit,Write,Bash'
            ], cwd=str(project_path), capture_output=True, text=True,
               timeout=120, env={**os.environ,
                'CLAUDE_OUTPUT_DIR': str(project_path)})

            if result.returncode == 0:
                logger.info("Claude Code fix completed")
                return True
            else:
                logger.warning("Claude Code fix failed: %s", result.stderr[-100:])
                return False

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            logger.warning("Claude Code fix error: %s", e)
            return False
