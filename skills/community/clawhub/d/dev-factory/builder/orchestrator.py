"""HybridOrchestrator - 복잡도별 개발 엔진 분기"""

import os
import logging
import subprocess
from pathlib import Path
from typing import Dict, Optional

from builder.models import Complexity, BuildResult, ProjectIdea

logger = logging.getLogger('builder-agent.orchestrator')


class HybridOrchestrator:
    """복잡도별로 다른 엔진을 사용하여 비용과 품질 최적화

    - Simple: GLM API (저렴)
    - Medium: Claude Code CLI (균형)
    - Complex: 템플릿 + Claude Code (품질)
    """

    def __init__(self, config=None):
        self.config = config
        self.glm_api_key = os.environ.get('BUILDER_GLM_API_KEY')
        self.claude_timeout = config.orchestration.claude_timeout_seconds if config else 300

    def develop(self, project: ProjectIdea, project_path: Path) -> BuildResult:
        """프로젝트 복잡도에 따른 개발 엔진 선택"""
        complexity = project.complexity if isinstance(project.complexity, str) else project.complexity.value

        logger.info("Developing %s (complexity: %s)", project.title, complexity)

        if complexity == Complexity.SIMPLE.value:
            return self._develop_via_glm(project, project_path)
        elif complexity == Complexity.MEDIUM.value:
            return self._develop_via_claude(project, project_path)
        else:  # COMPLEX
            # 템플릿 먼저 생성 (Sprint 3-5)
            return self._develop_via_claude(project, project_path)

    def fix(self, error: Dict, project_path: Path, complexity: str = "medium") -> bool:
        """에러 수정 시에도 동일 분기 적용"""
        if complexity == Complexity.SIMPLE.value:
            return self._fix_via_glm(error, project_path)
        else:
            return self._fix_via_claude(error, project_path)

    # ──────────────────────────────────────────────
    # GLM API (Simple 전용)
    # ──────────────────────────────────────────────

    def _develop_via_glm(self, project: ProjectIdea, project_path: Path) -> BuildResult:
        """GLM API로 직접 코드 생성 (Simple 프로젝트)"""
        import urllib.request
        import json

        logger.info("Using GLM API for simple project: %s", project.title)

        if not self.glm_api_key:
            logger.warning("GLM API key not configured")
            return BuildResult(
                success=False,
                project_path=str(project_path),
                retry_count=1,
                mode="glm",
                test_output="GLM API key not configured"
            )

        try:
            prompt = self._generate_development_prompt(project)
            data = {
                "model": "glm-4",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
            }

            req = urllib.request.Request(
                "https://open.bigmodel.cn/api/paas/v4/chat/completions",
                data=json.dumps(data).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {self.glm_api_key}",
                    "Content-Type": "application/json",
                },
            )

            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode())
                content = result["choices"][0]["message"]["content"]

            code = self._extract_code_block(content)
            project_path.mkdir(parents=True, exist_ok=True)
            (project_path / "main.py").write_text(code)

            logger.info("GLM API development completed for: %s", project.title)
            return BuildResult(
                success=True,
                project_path=str(project_path),
                retry_count=1,
                mode="glm",
                test_output=content[:200],
            )

        except urllib.error.HTTPError as e:
            logger.warning("GLM API HTTP error: %s", e.code)
            return BuildResult(
                success=False,
                project_path=str(project_path),
                retry_count=1,
                mode="glm",
                test_output=f"HTTP error: {e.code}",
            )
        except Exception as e:
            logger.warning("GLM API error: %s", e)
            return BuildResult(
                success=False,
                project_path=str(project_path),
                retry_count=1,
                mode="glm",
                test_output=str(e),
            )

    def _extract_code_block(self, content: str) -> str:
        """응답에서 코드 블록 추출"""
        if "```" in content:
            parts = content.split("```")
            if len(parts) >= 3:
                code = parts[1]
                if code.startswith("python\n"):
                    code = code[7:]
                elif code.startswith("python"):
                    code = code[6:]
                return code.strip()
        return content.strip()

    def _fix_via_glm(self, error: Dict, project_path: Path) -> bool:
        """GLM API로 에러 수정"""
        logger.info("GLM fix for error: %s", error.get('type'))
        # Sprint 3 구현 예정
        return False

    # ──────────────────────────────────────────────
    # Claude Code CLI (Medium/Complex 전용)
    # ──────────────────────────────────────────────

    def _develop_via_claude(self, project: ProjectIdea, project_path: Path) -> BuildResult:
        """Claude Code CLI로 개발 (토큰 부족 시 GLM-5로 fallback)"""
        logger.info("Using Claude Code CLI for project: %s", project.title)

        prompt = self._generate_development_prompt(project)

        try:
            result = subprocess.run([
                'claude', '-p', prompt,
                '--output-format', 'json',
                '--allowedTools', 'Edit,Write,Bash'
            ], cwd=str(project_path), capture_output=True, text=True,
               timeout=self.claude_timeout, env={**os.environ,
                'CLAUDE_OUTPUT_DIR': str(project_path)})

            if result.returncode == 0:
                logger.info("Claude Code development completed")
                return BuildResult(
                    success=True,
                    project_path=str(project_path),
                    retry_count=1,
                    mode="claude",
                    test_output=result.stdout[-500:] if len(result.stdout) > 500 else result.stdout
                )
            else:
                # Claude Code 실패 - 토큰 부족 또는 기타 에러
                error_msg = result.stderr[-500:] if len(result.stderr) > 500 else result.stderr
                
                # 토큰 관련 에러 확인
                if self._is_token_error(error_msg):
                    logger.warning("Claude Code token exhausted, falling back to GLM-5")
                    return self._fallback_to_glm(project, project_path, "token_exhausted")
                else:
                    logger.warning("Claude Code failed: %s", error_msg[:200])
                    # 기타 에러도 GLM으로 fallback 시도
                    return self._fallback_to_glm(project, project_path, "claude_error")

        except subprocess.TimeoutExpired:
            logger.warning("Claude Code timeout after %ds, falling back to GLM-5", self.claude_timeout)
            return self._fallback_to_glm(project, project_path, "timeout")
            
        except FileNotFoundError:
            logger.warning("Claude Code CLI not found, falling back to GLM-5")
            return self._fallback_to_glm(project, project_path, "cli_not_found")
            
        except Exception as e:
            logger.error("Claude Code unexpected error: %s, falling back to GLM-5", str(e))
            return self._fallback_to_glm(project, project_path, "unexpected_error")

    def _is_token_error(self, error_msg: str) -> bool:
        """토큰 부족 에러인지 확인"""
        token_keywords = [
            'token', 'limit', 'exhausted', 'quota', 'rate limit',
            'insufficient', 'capacity', 'usage limit'
        ]
        error_lower = error_msg.lower()
        return any(keyword in error_lower for keyword in token_keywords)

    def _fallback_to_glm(self, project: ProjectIdea, project_path: Path, reason: str) -> BuildResult:
        """Claude Code 실패 시 GLM-5로 fallback"""
        logger.info("Falling back to GLM-5 (reason: %s)", reason)
        
        result = self._develop_via_glm(project, project_path)
        
        # fallback 정보 추가
        if hasattr(result, 'metadata'):
            result.metadata = result.metadata or {}
            result.metadata['fallback'] = {
                'from': 'claude',
                'to': 'glm',
                'reason': reason
            }
        
        return result

    def _fix_via_claude(self, error: Dict, project_path: Path) -> bool:
        """Claude Code CLI로 에러 수정 (토큰 부족 시 GLM-5로 fallback)"""
        logger.info("Claude Code fix for error: %s", error.get('type'))

        prompt = f"""Fix the following error in this project:

Error Type: {error.get('type')}
Error Details: {error.get('raw_output', '')[:500]}

Analyze the error, identify the root cause, and apply the minimal fix.
Ensure the fix doesn't break other functionality.

After fixing, run tests to verify."""

        try:
            result = subprocess.run([
                'claude', '-p', prompt
            ], cwd=str(project_path), capture_output=True, text=True,
               timeout=120, env={**os.environ,
                'CLAUDE_OUTPUT_DIR': str(project_path)})

            if result.returncode == 0:
                logger.info("Claude Code fix completed")
                return True
            else:
                # Claude Code 실패 - GLM으로 fallback
                error_msg = result.stderr[-300:] if len(result.stderr) > 300 else result.stderr
                
                if self._is_token_error(error_msg):
                    logger.warning("Claude Code token exhausted during fix, falling back to GLM-5")
                else:
                    logger.warning("Claude Code fix failed, falling back to GLM-5: %s", error_msg[:100])
                
                return self._fix_via_glm(error, project_path)

        except subprocess.TimeoutExpired:
            logger.warning("Claude Code fix timeout, falling back to GLM-5")
            return self._fix_via_glm(error, project_path)
            
        except FileNotFoundError:
            logger.warning("Claude Code CLI not found for fix, falling back to GLM-5")
            return self._fix_via_glm(error, project_path)
            
        except Exception as e:
            logger.error("Claude Code fix error: %s, falling back to GLM-5", str(e))
            return self._fix_via_glm(error, project_path)

    # ──────────────────────────────────────────────
    # 프롬프트 생성
    # ──────────────────────────────────────────────

    def _generate_development_prompt(self, project: ProjectIdea) -> str:
        """개발 프롬프트 생성"""
        tech_stack = ', '.join(project.tech_stack) if project.tech_stack else 'Python'

        prompt = f"""Develop the following project:

Title: {project.title}
Description: {project.description}
Complexity: {project.complexity}
Tech Stack: {tech_stack}

Requirements:
1. Create all necessary files in the current directory
2. Include comprehensive error handling
3. Add unit tests in a tests/ directory
4. Ensure code is production-ready and well-documented
5. After creating files, run tests to verify everything works

Project Structure:
- src/ or main source files
- tests/ with unit tests
- README.md with documentation
- requirements.txt or setup.py for dependencies

Please implement this project completely."""

        if project.url:
            prompt += f"\n\nReference: {project.url}"

        if project.cve_id:
            prompt += f"\n\nThis is a security tool for {project.cve_id}"

        return prompt
