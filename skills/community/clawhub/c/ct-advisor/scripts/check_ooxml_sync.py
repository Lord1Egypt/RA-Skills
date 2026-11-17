#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_ooxml_sync.py — OOXML→MD 转换器「双份副本」漂移检测（stdlib-only）

背景（2026-09-24 审计实测）：
    scripts/office_to_md.py（本地）与 adapters/coze/src/doc/ooxml_md.py（Coze 端）
    是**同一份源码的两个副本**，difflib 序列相似度 0.9169，仅 7 处差异且全是
    Coze 端适配包装（头部注释、`_src()` 路径包装 ×3、CLI 收尾）。

为什么要检测而不是合并：
    本地副本**不能删** —— SKILL.md 规定 OOXML 走本地解码（离线可用、免上传、
    ≤5 MB 不落网络），是刻意设计；Coze 端副本是服务端解码真源。
    两份都必须存在，因此只能靠「漂移检测」保证它们不各自演化。

用法：
    python scripts/check_ooxml_sync.py            # 人类可读报告
    python scripts/check_ooxml_sync.py --quiet    # 仅退出码（CI 用）

退出码：
    0 = 无漂移（相似度 >= 阈值）
    1 = 检出漂移（需人工同步）
    2 = 文件缺失 / 无法读取
"""

from __future__ import annotations

import argparse
import difflib
import os
import re
import sys

# 阈值：低于此值判定为漂移。基线实测 0.9169，留 0.06 余量给注释性改动。
THRESHOLD = 0.86

_HERE = os.path.dirname(os.path.abspath(__file__))
_SKILL = os.path.dirname(_HERE)

LOCAL = os.path.join(_HERE, "office_to_md.py")
COZE = os.path.join(_SKILL, "adapters", "coze", "src", "doc", "ooxml_md.py")

# Coze 端已知适配包装（归一化时还原为本地写法，不计入漂移）
# 说明：只还原「包装」，不删 Coze 端独有函数定义 —— 保持归一化可预测、可复算。
_NORMALIZE = [
    (re.compile(r"zipfile\.ZipFile\(_src\((?:path|p|src)\)\)"), "zipfile.ZipFile(path)"),
    (re.compile(r"[ \t]*#[ \t]*\[coze\][^\n]*"), ""),
]


def _read(p: str):
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            return f.read().replace("\r\n", "\n")
    except OSError:
        return None


def _normalize(text: str, is_coze: bool) -> str:
    """把 Coze 端的已知适配包装还原成本地写法，使两份可公平比对。"""
    if not is_coze:
        return text
    for pat, rep in _NORMALIZE:
        text = pat.sub(rep, text)
    return text


def main() -> int:
    ap = argparse.ArgumentParser(description="OOXML 转换器双份副本漂移检测")
    ap.add_argument("--quiet", action="store_true", help="仅退出码，不打印报告")
    ap.add_argument("--threshold", type=float, default=THRESHOLD)
    args = ap.parse_args()

    a, b = _read(LOCAL), _read(COZE)
    if a is None or b is None:
        if not args.quiet:
            for p in (LOCAL, COZE):
                print("  %s : %s" % ("OK " if _read(p) is not None else "MISSING", p))
            print("\n结论: 文件缺失，无法比对")
        return 2

    la = _normalize(a, False).splitlines()
    lb = _normalize(b, True).splitlines()
    sm = difflib.SequenceMatcher(None, la, lb)
    ratio = sm.ratio()
    drift = ratio < args.threshold

    if not args.quiet:
        print("OOXML→MD 转换器 双份副本漂移检测")
        print("=" * 66)
        print("  本地  %-46s %4d 行" % (os.path.basename(LOCAL), len(la)))
        print("  Coze  %-46s %4d 行" % (os.path.basename(COZE), len(lb)))
        print("  （已归一化 Coze 端已知适配：_src() 包装 / [coze] 标记）")
        print("-" * 66)
        print("  相似度 = %.4f   阈值 = %.2f" % (ratio, args.threshold))
        ops = [o for o in sm.get_opcodes() if o[0] != "equal"]
        print("  差异块 = %d 处" % len(ops))
        for tag, i1, i2, j1, j2 in ops[:10]:
            print("    %-8s L%d-%d -> L%d-%d" % (tag, i1 + 1, i2, j1 + 1, j2))
        if len(ops) > 10:
            print("    ... 另 %d 处" % (len(ops) - 10))
        print("-" * 66)
        if drift:
            print("  结论: ❌ 检出漂移 —— 两份副本已各自演化，需人工同步")
            print("  基线: 2026-09-24 实测 0.9169（差异仅 7 处，均为 Coze 适配）")
        else:
            print("  结论: ✅ 无漂移（在容忍范围内）")
    return 1 if drift else 0


if __name__ == "__main__":
    sys.exit(main())
