#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_i18n_from_ctbase.py -- 发布前从 ct-base 拉取最新共享双语词条快照。

背景：
  ct-advisor 的 scripts/i18n.py 在运行时合并 ct-base 的通用词条
  (auth.* / error.* / generic / exec / ...)。发布态下 ct-advisor 是独立包，
  ~/.workbuddy/skills/ct-base 不一定存在，因此必须把共享词条同步成本包随附的
  scripts/i18n_messages.json 快照，确保发布后也能解析这些 key。

  唯一真源 = ct-base/scripts/i18n_messages.json。本脚本只做「复制快照」，
  不在 ct-advisor 内手维护通用词条（消除双份维护）。

用法：
  python scripts/sync_i18n_from_ctbase.py
"""
import json
import os
import shutil
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.join(
    os.path.expanduser("~"), ".workbuddy", "skills", "ct-base",
    "scripts", "i18n_messages.json",
)
_DST = os.path.join(_HERE, "i18n_messages.json")


def main():
    if not os.path.exists(_SRC):
        print(f"[sync] 源不存在: {_SRC}")
        print("[sync] 请确认 ct-base 技能已安装；若当前即为发布态(无 ct-base)，")
        print("       请手动将共享词条快照放入 ct-advisor/scripts/i18n_messages.json。")
        sys.exit(2)

    with open(_SRC, encoding="utf-8") as f:
        data = json.load(f)

    shutil.copyfile(_SRC, _DST)
    print(f"[sync] 已同步 {len(data)} 条共享词条 -> {_DST}")


if __name__ == "__main__":
    main()
