#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""独立进程探测 WSL home 路径并写入缓存文件。

由 run_all.py 用普通 python 调用，外层可加超时；即使 UNC 访问卡死，
超时杀掉本进程也不影响主流程（缓存为空则跳过 WSL 会话）。

交互模式（WORKLOG_PROMPT=1 且 stdin 是 TTY）下，若自动探测无结果且
用户未通过环境变量指定，会提示输入非常规的用户名 / 发行版。
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import ask, interactive_enabled

CACHE = os.path.join(HERE, "_env_paths_cache.json")

DISTROS = ["Ubuntu", "Ubuntu-22.04", "Ubuntu-24.04", "debian", "Debian",
           "kali-linux", "openSUSE-Leap-15.6", "Arch", "fedora"]
USERS = ["root", "ubuntu", os.path.basename(os.path.expanduser("~"))]
d_extra = os.environ.get("WORKLOG_WSL_DISTRO", "")
u_extra = os.environ.get("WORKLOG_WSL_USER", "")
if d_extra:
    DISTROS.insert(0, d_extra)
if u_extra:
    USERS.insert(0, u_extra)


def probe(distros, users):
    """按候选发行版 × 用户名做 isdir 校验（不做 UNC 根 os.listdir）。"""
    found, seen = [], set()
    for d in dict.fromkeys(distros):
        for u in dict.fromkeys(users):
            suffix = "root" if u == "root" else f"home\\{u}"
            for unc in ("\\\\wsl.localhost", "\\\\wsl$"):
                p = f"{unc}\\{d}\\{suffix}"
                try:
                    ok = os.path.isdir(p)
                except Exception:
                    ok = False
                if ok:
                    k = os.path.normpath(p).lower()
                    if k not in seen:
                        seen.add(k)
                        found.append(p)
                    break  # 同一发行版+用户只保留一种 UNC 前缀
    return found


def is_dir(v):
    return os.path.isdir(v)


def main():
    found = probe(DISTROS, USERS)

    # 交互补充：自动探测为空 + 未显式指定用户名/发行版 + 允许交互
    if not found and interactive_enabled() and not u_extra and not d_extra:
        print("未自动找到 WSL 会话目录。若你用了非常规用户名/发行版，可手动指定。")
        u = ask("WSL 用户名", default="", validator=lambda x: bool(x) and "/" not in x and "\\" not in x)
        d = ask("WSL 发行版名（如 Ubuntu-22.04）", default="", validator=lambda x: bool(x))
        if u or d:
            users2 = ([u] if u else []) + USERS
            distros2 = ([d] if d else []) + DISTROS
            found = probe(distros2, users2)

    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump({"wsl_homes": found}, f, ensure_ascii=False)
    print(f"WSL homes found: {len(found)}")
    for p in found:
        print("  " + p)


if __name__ == "__main__":
    main()
