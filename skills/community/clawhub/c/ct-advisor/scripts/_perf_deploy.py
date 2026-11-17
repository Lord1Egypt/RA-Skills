#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ct-advisor 部署辅助（2026-09-26）

背景：技能目录位于网络共享，ACL 为 creator-owner——可新建文件，但覆盖预装既有文件
会被 PermissionError 拒绝，删除被 trash 钩子拦截。因此任何对 scripts/*.py / SKILL.md
的改动，统一先生成同目录 `.new` 副本，再由用户本机 `move /Y` 覆盖。

用法：
  # 部署已知 4 个文件（从指定本地目录复制到共享并生成 .new）
  python _perf_deploy.py --all <本地目录>

  # 部署指定本地文件（自动映射到共享目录对应位置并加 .new 后缀）
  python _perf_deploy.py /path/to/local/orchestrate.py /path/to/local/entry.py
"""
from __future__ import annotations
import os
import sys
import shutil

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 文件名 -> 共享目录下的相对位置（"" 表示根目录，其余为子目录），不含 .new
_TARGETS = {
    "orchestrate.py": "scripts",
    "entry.py": "scripts",
    "serve.py": "scripts",
    "clarify_loop.py": "scripts",
    "SKILL.md": "",
    "config.json": "",
}


def _deploy_one(local_path: str) -> str | None:
    name = os.path.basename(local_path)
    if name not in _TARGETS:
        print(f"  [跳过] 未登记的文件: {name}")
        return None
    sub = _TARGETS[name]
    dst_dir = SKILL_ROOT if sub == "" else os.path.join(SKILL_ROOT, sub)
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, name + ".new")
    try:
        shutil.copyfile(local_path, dst)
        print(f"  [OK] {name} -> {dst} ({os.path.getsize(dst)} bytes)")
        return dst
    except Exception as e:
        print(f"  [失败] {name}: {type(e).__name__}: {e}")
        return None


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    if args[0] == "--all":
        src = args[1] if len(args) > 1 else os.path.dirname(os.path.abspath(__file__))
        print(f"源目录: {src}")
        for n in ("orchestrate.py", "entry.py", "serve.py", "SKILL.md"):
            lp = os.path.join(src, n)
            if os.path.exists(lp):
                _deploy_one(lp)
            else:
                print(f"  [缺失] 本地未找到 {n}")
    else:
        for lp in args:
            if not os.path.exists(lp):
                print(f"  [缺失] {lp}")
                continue
            _deploy_one(lp)
    print("\n=== 一键覆盖命令（请在本机 CMD 执行）===")
    print(f'cd /d {os.path.join(SKILL_ROOT, "scripts")}')
    print(r'move /Y orchestrate.py.new orchestrate.py')
    print(r'move /Y entry.py.new entry.py')
    print(r'move /Y serve.py.new serve.py')
    print(r'cd ..')
    print(r'move /Y SKILL.md.new SKILL.md')


if __name__ == "__main__":
    main()
