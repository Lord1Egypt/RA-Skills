"""MemoryBridge - self-improving 스킬 연동"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger('builder-agent.integration.memory')


class MemoryBridge:
    """self-improving 스킬과의 정식 연동

    - 성공 패턴 저장
    - 실패 패턴 로깅
    - 과거 수정 경험 검색
    """

    def __init__(self):
        self.si_dir = Path.home() / "self-improving"
        self.si_dir.mkdir(parents=True, exist_ok=True)

        # 프로젝트별 네임스페이스
        self.projects_dir = self.si_dir / "projects"
        self.projects_dir.mkdir(parents=True, exist_ok=True)

    # ──────────────────────────────────────────────
    # 성공 패턴 저장
    # ──────────────────────────────────────────────

    def log_success(self, project: Dict, build_result: Dict, mode: str = "direct"):
        """성공 패턴을 reflections.md에 저장"""
        reflections_file = self.si_dir / "reflections.md"

        entry = {
            'timestamp': datetime.now().isoformat(),
            'context': f"Builder: {project.get('title', 'Unknown')} ({project.get('complexity', 'unknown')})",
            'reflection': f"성공 (시도 {build_result.get('retry_count', 1)}회, 모드: {mode})",
            'lesson': self._extract_lesson(project, build_result, mode)
        }

        with open(reflections_file, 'a') as f:
            f.write(f"\n### {entry['timestamp']}\n")
            f.write(f"**CONTEXT**: {entry['context']}\n")
            f.write(f"**REFLECTION**: {entry['reflection']}\n")
            f.write(f"**LESSON**: {entry['lesson']}\n")

        # 프로젝트별 파일에도 저장 (네임스페이스 격리)
        self._log_to_project_file(project, entry, 'success')

        logger.info("Success logged to self-improving")

    def _extract_lesson(self, project: Dict, build_result: Dict, mode: str) -> str:
        """성공 요인 추출"""
        retry_count = build_result.get('retry_count', 1)
        complexity = project.get('complexity', 'unknown')

        if retry_count == 1:
            return f"First attempt success via {mode} (complexity: {complexity})"
        else:
            return f"Success after {retry_count - 1} correction(s) via {mode} (complexity: {complexity})"

    # ──────────────────────────────────────────────
    # 실패 패턴 로깅
    # ──────────────────────────────────────────────

    def log_failure(self, project: Dict, error: Dict, attempt: int, max_retries: int, mode: str = "direct"):
        """실패 패턴을 corrections.md에 저장"""
        corrections_file = self.si_dir / "corrections.md"

        with open(corrections_file, 'a') as f:
            f.write(f"\n### {datetime.now().isoformat()}\n")
            f.write(f"**PROJECT**: {project.get('title', 'Unknown')}\n")
            f.write(f"**MODE**: {mode}\n")
            f.write(f"**ATTEMPT**: {attempt}/{max_retries}\n")
            f.write(f"**ERROR**: {error.get('type', 'unknown')}\n")
            f.write(f"**SUGGESTION**: {error.get('fix_suggestion', 'N/A')}\n")
            if error.get('file_path'):
                f.write(f"**FILE**: {error['file_path']}:{error.get('line_number', '?')}\n")

        # 프로젝트별 파일에도 저장
        self._log_to_project_file(project, {
            'timestamp': datetime.now().isoformat(),
            'type': 'failure',
            'error': error
        }, 'failure')

        logger.info("Failure logged to self-improving")

    # ──────────────────────────────────────────────
    # 네임스페이스 격리
    # ──────────────────────────────────────────────

    def _log_to_project_file(self, project: Dict, entry: Dict, entry_type: str):
        """프로젝트별 파일에 로그 저장 (네임스페이스 격리)"""
        source = project.get('source', 'unknown')
        project_file = self.projects_dir / f"builder-{source}.md"

        with open(project_file, 'a') as f:
            f.write(f"\n### {entry['timestamp']}\n")
            f.write(f"**TYPE**: {entry_type.upper()}\n")

            if entry_type == 'success':
                f.write(f"**PROJECT**: {project.get('title')}\n")
                f.write(f"**LESSON**: {entry.get('lesson', '')}\n")
            else:
                error = entry.get('error', {})
                f.write(f"**PROJECT**: {project.get('title')}\n")
                f.write(f"**ERROR**: {error.get('type', 'unknown')}\n")
                f.write(f"**SUGGESTION**: {error.get('fix_suggestion', 'N/A')}\n")

    # ──────────────────────────────────────────────
    # 과거 경험 검색
    # ──────────────────────────────────────────────

    def get_relevant_fixes(self, error_type: str, limit: int = 5) -> List[Dict]:
        """과거 수정 경험에서 관련 컨텍스트 검색"""
        corrections_file = self.si_dir / "corrections.md"

        if not corrections_file.exists():
            return []

        relevant = []
        content = corrections_file.read_text()

        # 각 항목 파싱
        sections = content.split('\n### ')[1:]  # 첫 번째는 비어있음

        for section in sections[:limit * 3]:  # 최근 N개 섹션 확인
            if f"**ERROR**: {error_type}" in section or error_type.lower() in section.lower():
                relevant.append({
                    'section': section,
                    'error_type': error_type
                })

                if len(relevant) >= limit:
                    break

        return relevant

    def get_successful_patterns(self, source: str = None, limit: int = 5) -> List[Dict]:
        """성공 패턴 검색"""
        reflections_file = self.si_dir / "reflections.md"

        if not reflections_file.exists():
            return []

        patterns = []
        content = reflections_file.read_text()

        sections = content.split('\n### ')[1:]

        for section in sections:
            if source and f"source: {source}" not in section.lower():
                continue

            if 'REFLECTION**' in section:
                patterns.append({'section': section})

                if len(patterns) >= limit:
                    break

        return patterns
