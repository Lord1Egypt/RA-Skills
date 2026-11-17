#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cad_preflight.py — CAD 输入快速失败预检（第 3 步可靠性加固）。

目标：在入口层（读取前 4KB，不做任何解析/渲染）识别明显不是
DWG/DXF/PDF 的输入（<1KB、魔数错误、空文件）并快速失败（要求 <5 秒），
不假装转换成功；把坏图/加密图/不支持版本交给批量层记录原因后跳过。

只做轻量只读检查，不启动解析器、不写文件、不加载 CAD 库。
"""
from __future__ import annotations

import re
from pathlib import Path

TINY_MIN_BYTES = 1024  # <1KB 视为缺输入（快速失败）

# 常见 DWG 版本魔数（AC1009 ~ AC1032）。
# 未列入本集合的 AC#### 直接判不支持，避免让解析器空跑几十秒。
KNOWN_DWG_VERSIONS = {
    "1009", "1012", "1014", "1015", "1018", "1021", "1024", "1027", "1032",
    # 少数老/实验版本，宁可明确列为不支持也不要硬啃
    "1013", "1016", "1019", "1020", "1022", "1023", "1025", "1026", "1028",
    "1029", "1030", "1031",
}
# ezdwg 实际稳定支持的 DWG 版本（其余算“不支持版本”快速失败）
SUPPORTED_DWG_VERSIONS = {
    "1009", "1012", "1014", "1015", "1018", "1021", "1024", "1027",
}
_DWG_VER_RE = re.compile(rb"\AAC(\d{4,5})")


def preflight_file(path) -> dict:
    """对单个文件做快速预检。

    返回：
      {"ok": True, "format": "DWG"|"DXF"|"PDF", "head": bytes, "size": int} 或
      {"ok": False, "kind": str, "reason": str, ...}
    kind ∈ not_found | not_file | not_readable | empty | tiny
           | bad_magic | unsupported_version
    """
    p = Path(path)
    if not p.exists():
        return {"ok": False, "kind": "not_found", "reason": "文件不存在"}
    if not p.is_file():
        return {"ok": False, "kind": "not_file", "reason": "不是普通文件"}
    try:
        size = p.stat().st_size
    except OSError as exc:
        return {"ok": False, "kind": "not_readable", "reason": f"读取文件大小失败：{exc}"}
    if size == 0:
        return {"ok": False, "kind": "empty", "size": size, "reason": "空文件（0 字节）"}
    if size < TINY_MIN_BYTES:
        return {"ok": False, "kind": "tiny", "size": size,
                "reason": f"输入过小（{size} 字节 < 1KB），视为缺输入"}
    try:
        with p.open("rb") as fh:
            head = fh.read(4096)
    except OSError as exc:
        return {"ok": False, "kind": "not_readable", "reason": f"读取文件头失败：{exc}"}
    if not head:
        return {"ok": False, "kind": "empty", "size": size, "reason": "空文件（读取无内容）"}
    if head.startswith(b"%PDF-"):
        return {"ok": True, "format": "PDF", "head": head, "size": size}
    m = _DWG_VER_RE.match(head)
    if m:
        ver = m.group(1).decode("ascii", "replace")
        if ver not in KNOWN_DWG_VERSIONS:
            return {"ok": False, "kind": "unsupported_version", "format": "DWG", "version": ver,
                    "reason": f"DWG 版本 AC{ver} 无法识别（不支持的 DWG 版本）",
                    "head": head, "size": size}
        if ver not in SUPPORTED_DWG_VERSIONS:
            return {"ok": False, "kind": "unsupported_version", "format": "DWG", "version": ver,
                    "reason": f"DWG 版本 AC{ver} 不在本机 ezdwg 支持列表内（不支持的 DWG 版本）",
                    "head": head, "size": size}
        return {"ok": True, "format": "DWG", "version": ver, "head": head, "size": size}
    lhead = head.lstrip()
    suffix = p.suffix.lower()
    # 沿用 cad_scan.detect_format 的 DXF 判定：首行 0 + SECTION，或 .dxf/.dwt 后缀带头部 SECTION
    if lhead.startswith(b"0") and b"SECTION" in head:
        return {"ok": True, "format": "DXF", "head": head, "size": size}
    if suffix in (".dxf", ".dwt") and b"SECTION" in head:
        return {"ok": True, "format": "DXF", "head": head, "size": size}
    return {"ok": False, "kind": "bad_magic", "reason": "魔数/头部不是标准 DWG、DXF 或 PDF（可能是其它文件或已损坏）",
            "head": head, "size": size}


def input_fail_reason(path) -> str:
    r = preflight_file(path)
    return "" if r.get("ok") else r.get("reason", "")
