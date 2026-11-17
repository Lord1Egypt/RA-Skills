#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ct-advisor — 旧调用兼容壳（v1.3.19 · 2026-10-22）

本技能已收敛为**单一路径**：`scripts/entry.py` 是对外唯一入口，其 stdout 直接是
「明文答案 + <<<CT_ANSWER_END>>> + checksum」，**agent 侧零解码**。

历史包袱说明（已彻底解决）：
  v1.3.9 为免疫中文 Windows（cp936）控制台乱码，把对外出口改成 base64 信封；
  但 agent 必须自己把约 2600 字符的 base64 逐字搬进另一条命令解码，LLM 没有可靠的
  「长随机串搬运」通道（日志里 agent 自认 `5Lzd vs 5L+d` 打错），于是 2026-10-16 加了
  本脚本把解包放进代码。两层协议由此并存，且 base64 的 4× 膨胀正压住通道上限。

  v1.3.19 把 base64 收回到**内部进程间协议**（orchestrate / refine_answer / serve
  之间仍用它保证二进制安全），对外出口一次性解开为明文——两层协议合一。

本文件保留的**唯一目的**是让遗漏的旧调用仍能工作。它零逻辑：
把参数原样转发给 entry.py，继承其 stdout / stderr / 退出码，不做任何捕获、
解码、重编码。新调用请直接用 entry.py。

已废弃参数：`--raw`（出口已是明文）、`--timeout`（entry.py 内部自管超时），
传入会被忽略并在 stderr 提示。
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

_CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)


def _hidden_kwargs() -> dict:
    """抑制子进程控制台弹窗（非 Windows 返回 {}）。"""
    if not sys.platform.startswith("win"):
        return {}
    kw = {"creationflags": _CREATE_NO_WINDOW}
    try:
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = 0  # SW_HIDE
        kw["startupinfo"] = si
    except Exception:  # noqa: BLE001
        pass
    return kw


def _forward_argv(argv: list) -> list:
    """剥离已废弃参数，其余原样转发。"""
    out, i = [], 0
    while i < len(argv):
        a = argv[i]
        if a == "--raw":
            sys.stderr.write("[ask] --raw 已废弃（entry.py 出口已是明文），已忽略\n")
            i += 1
            continue
        if a == "--timeout":
            sys.stderr.write("[ask] --timeout 已废弃（entry.py 内部自管超时），已忽略\n")
            i += 2
            continue
        out.append(a)
        i += 1
    return out


def main() -> int:
    cmd = [sys.executable, str(SCRIPT_DIR / "entry.py")] + _forward_argv(sys.argv[1:])
    sys.stderr.write(
        "[ask] 兼容壳：本技能已收敛为单一路径，请直接调用 scripts/entry.py"
        "（stdout 即明文答案）。\n")
    try:
        # 不捕获输出：子进程直接继承当前 stdout/stderr，零拷贝、零编码转换、
        # 不存在任何缓冲区上限。这是「单一形态」在只有一层时唯一正确的做法。
        #
        # 🔴 必须显式传 stdout/stderr（2026-10-22 实测）：Windows 上
        # CREATE_NO_WINDOW 会让子进程脱离父控制台，**不传 stdout 时子进程的输出会
        # 整体丢失**（rc=0 但 stdout 为空）。显式绑定父进程句柄即可两全——
        # 既不弹窗，又不丢输出。
        try:
            return subprocess.run(
                cmd, stdout=sys.stdout, stderr=sys.stderr, **_hidden_kwargs()
            ).returncode
        except (OSError, ValueError, AttributeError):
            # stdout 无可继承 fd（如被替换为 StringIO / 纯 GUI 宿主）→ 退回继承模式
            return subprocess.run(cmd).returncode
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
