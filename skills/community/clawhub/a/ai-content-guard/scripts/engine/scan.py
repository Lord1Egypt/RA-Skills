"""PITAX 扫描路由层 v2 — skill 产品路由（与上游管线刻意分叉，见 vendor/SYNC.md）。

v1 复刻上游 codeark/tools/pitax_scan.py@168f660 的互斥路由；2026-10-25 严格测试
（P0-2）证明互斥路由漏检：.md/.txt 不跑隐形字符/编码检测、config 不跑隐形/编码。
v2 改为**全量基础检测 + 按路径追加**，代价是 demo 锚从 12 变宽（skill 产品以覆盖
优先，管线精度口径仍以上游为准）。

路由（v2）：
  全部文件：invisible / trojan / encoded（引擎）+ 中文与劫持覆盖层（zh_rules）
  追加：AI 配置路径 → T-46；文档路径 → N-06；代码文件 → 注释注入 T-51

本文件不属于 vendor 五文件锚；上游双语重构落地后，zh_rules 覆盖层合并回上游。
"""
from __future__ import annotations

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
from .zh_rules import scan_encoded_zh, scan_zh

__all__ = ["scan_file", "scan_repo"]


def _emojiish(ch: str) -> bool:
    o = ord(ch)
    return (0x1F000 <= o <= 0x1FAFF or 0x2600 <= o <= 0x27BF or 0x2190 <= o <= 0x21FF
            or 0x2B00 <= o <= 0x2BFF or ch == "️")


def _emoji_zwj_guard(findings: list[dict], content: str) -> list[dict]:
    """emoji 家族序列误报降级（P1-8）：E-23 命中行的全部 ZWJ 若都位于 emoji
    字符之间（家庭/职业组合 emoji），降为 low。evidence 是记法化文本，
    邻域判断必须回到原始行。"""
    lines = content.splitlines()
    for f in findings:
        if f.get("type") != "PIT-E-23":
            continue
        ln = f.get("line")
        line = lines[ln - 1] if isinstance(ln, int) and 0 < ln <= len(lines) else ""
        zwjis = [i for i, c in enumerate(line) if c == "\u200d"]
        if zwjis and all(0 < i < len(line) - 1
                         and _emojiish(line[i - 1]) and _emojiish(line[i + 1])
                         for i in zwjis):
            f["severity"] = "low"
            f["description"] = (str(f.get("description", "")) +
                                "（ZWJ 位于 emoji 家族序列内部，已降级 low）").strip()
    return findings


def scan_file(path: str, content: str, _n: int = 0) -> list[dict]:
    """单文件扫描：全量基础检测 + 按路径追加 + 中文/劫持覆盖层。永不抛异常。

    全阶段容错（ClawHub 扫描 C 项 #35）：报告转换/emoji 后处理/覆盖层不因
    单阶段异常中断整个扫描——各阶段独立 try，失败阶段置空并继续。
    """
    raw: list = []
    try:
        raw += detect_invisible_text(content, path)
        raw += detect_trojan_source(content, path)
        raw += detect_encoded_payloads(content, path)
        if is_ai_config_path(path):
            raw += detect_ai_config_injection(content, path)
        elif is_doc_path(path):
            raw += detect_doc_injection(content, path)
        else:
            raw += detect_comment_injection(content, path)
    except Exception:
        raw = []
    try:
        findings = [f.to_report_dict(f"pitax-{_n}-{i}") for i, f in enumerate(raw, start=1)]
    except Exception:
        findings = []
    try:
        findings = _emoji_zwj_guard(findings, content)
    except Exception:
        pass
    try:
        findings += scan_zh(content, path, _n=_n)
    except Exception:
        pass
    try:
        findings += scan_encoded_zh(content, path, _n=_n)
    except Exception:
        pass
    return findings


def scan_repo(files: dict[str, str]) -> list[dict]:
    """对 {路径: 内容} 全量扫描。空列表 = 无命中或全部失败。"""
    all_findings: list[dict] = []
    for _n, (path, content) in enumerate(files.items(), start=1):
        all_findings.extend(scan_file(path, content, _n=_n))
    return all_findings
