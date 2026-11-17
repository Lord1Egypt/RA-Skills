"""InputSanitizer — Agent 0 核心：对目录内源代码执行 PITAX 预扫描。

检测分发（与官方 taxonomy v1.6.1 编号对齐）：
  所有文件           → PIT-E-23 不可见字符 + PIT-E-54 Trojan Source + 编码类
  AI 指令文件        → PIT-T-46（.cursor/rules、CLAUDE.md、copilot-instructions.md）
  项目文档 (.md 等)  → PIT-N-06 文档投毒
  代码文件           → PIT-T-51 注释指令覆盖
"""
from __future__ import annotations

import logging
from pathlib import Path

from .detectors import (
    detect_ai_config_injection,
    detect_comment_injection,
    detect_doc_injection,
    detect_encoded_payloads,
    detect_invisible_text,
    detect_trojan_source,
    is_ai_config_path,
    is_doc_path,
)
from .rules import ALL_RULES, PITAX_VERSION

logger = logging.getLogger("ai_content_guard.pitax")

SCAN_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rs", ".c", ".h",
    ".cpp", ".hpp", ".cs", ".rb", ".php", ".sh", ".yaml", ".yml", ".json",
    ".md", ".mdc", ".cursorrules", ".txt", ".toml", ".cfg", ".ini",
    ".html", ".vue", ".sql",
}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}
MAX_FILE_BYTES = 2 * 1024 * 1024  # 2MB，防 zip 炸弹式超大文件


class InputSanitizer:
    """对单个文件执行全部 PITAX 确定性检测。"""

    def sanitize(self, code: str, file_path: str, language: str = "text") -> tuple[list[dict], list]:
        raw: list = []
        raw += detect_invisible_text(code, file_path)    # PIT-E-23
        raw += detect_trojan_source(code, file_path)     # PIT-E-54
        if is_ai_config_path(file_path):
            raw += detect_ai_config_injection(code, file_path)  # PIT-T-46
        elif is_doc_path(file_path):
            raw += detect_doc_injection(code, file_path)        # PIT-N-06
        else:
            raw += detect_comment_injection(code, file_path)    # PIT-T-51
        raw += detect_encoded_payloads(code, file_path)          # E-07/14/36/57

        findings, seen = [], set()
        for i, f in enumerate(raw, start=1):
            key = (f.pitax_code, f.file, f.line)
            if key in seen:
                continue
            seen.add(key)
            findings.append(f.to_report_dict(f"PITAX-{i:04d}", language))
        return findings, raw


def scan_directory(work_dir: str) -> tuple[list[dict], dict]:
    """Agent 0 入口：扫描目录，返回 (findings, stats)。永不抛异常。"""
    sanitizer = InputSanitizer()
    all_findings: list[dict] = []
    stats = {
        "files_scanned": 0, "files_skipped": 0,
        "pitax_version": PITAX_VERSION,
        "rules": ALL_RULES,
    }
    root = Path(work_dir)
    if not root.exists():
        return all_findings, {**stats, "error": f"path not found: {work_dir}"}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            stats["files_skipped"] += 1
            continue
        if path.stat().st_size > MAX_FILE_BYTES:
            stats["files_skipped"] += 1
            continue
        rel = str(path.relative_to(root))
        if path.suffix.lower() not in SCAN_EXTENSIONS:
            if not is_ai_config_path(rel):
                stats["files_skipped"] += 1
                continue
        try:
            code = path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            logger.debug(f"PITAX scan skip {rel}: {e}")
            stats["files_skipped"] += 1
            continue
        stats["files_scanned"] += 1
        findings, _ = sanitizer.sanitize(code, rel)
        for i, f in enumerate(findings, start=len(all_findings) + 1):
            f["id"] = f"PITAX-{i:04d}"
        all_findings.extend(findings)
    logger.info(f"PITAX scan: {stats['files_scanned']} files, {len(all_findings)} findings")
    return all_findings, stats
