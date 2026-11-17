#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI 插件市场浏览器 —— 列插件、按能力分组、搜接口、看参数。

比 a7w.py 的 apps/schema 多做的事：
  · 按「能力分组」而不是平台的原始分类展示（更好找）
  · 按关键词搜插件或接口
  · 一条命令看某个插件全部接口的必填参数

用法：
  python3 market.py list                 列出全部插件（按能力分组）
  python3 market.py list --raw           按平台原始分类列出
  python3 market.py find 视频超分         搜插件 / 接口
  python3 market.py show nano_banana     看某个插件的接口与必填参数
  python3 market.py groups               只看分组概览
"""
import argparse
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import a7w  # noqa: E402

# 按能力分组（找插件比平台原始分类直观）
GROUPS = [
    ("图片生成", ["nano_banana"]),
    ("视频生成", ["full_video", "happy_horse", "grok_video", "wan", "seedance"]),
    ("数字人与口播", ["image_human", "pic_lipsync", "lipsync"]),
    ("视频剪辑与特效", ["action_transfer", "person_replacement",
                       "dressing_diffusion", "smart_clip", "flashvsr"]),
    ("音频与音乐", ["voice_tts", "music_generation", "music_search",
                   "mmaudio", "seedsvc"]),
    ("文档与检索", ["file_qa"]),
]

EXCLUDE = {"watermark_removal"}   # 平台数据抓取 + 去水印，属红线，不收录


def fetch_apps():
    d = a7w._unwrap(a7w._request("GET", a7w.HOST + "/api/v1/apps", a7w.load_key()))
    lst = d.get("data") if isinstance(d, dict) and "data" in d else d
    if isinstance(lst, dict):
        lst = lst.get("list") or lst.get("apps") or []
    return [a for a in lst if isinstance(a, dict) and a.get("code") not in EXCLUDE]


def fetch_one(app):
    d = a7w._unwrap(a7w._request("GET", a7w.HOST + "/api/v1/apps/" + app, a7w.load_key()))
    return d.get("data") if isinstance(d, dict) and "data" in d else d


def params_of(api):
    ps = api.get("params_schema")
    if isinstance(ps, str):
        try:
            ps = json.loads(ps)
        except ValueError:
            return {}, []
    if not isinstance(ps, dict):
        return {}, []
    if isinstance(ps.get("properties"), dict):
        props = ps["properties"]
        req = ps.get("required") or []
        req = [r for r in req if r in props]
        return props, req
    meta = {"required", "properties", "type", "title", "description", "$schema"}
    props = {k: v for k, v in ps.items() if k not in meta and isinstance(v, dict)}
    req = [k for k, v in props.items()
           if str((v or {}).get("required")) in ("True", "1", "true")]
    return props, req


def cmd_groups():
    print("AI 插件市场 · %d 个能力分组\n" % len(GROUPS))
    for name, codes in GROUPS:
        print("  %-14s %d 个：%s" % (name, len(codes), "、".join(codes)))


def cmd_list(raw=False):
    apps = fetch_apps()
    if raw:
        print("共 %d 个插件（平台原始分类）\n" % len(apps))
        for a in apps:
            print("  %-22s %-24s %2d 接口  %s"
                  % (a.get("code"), a.get("name"), len(a.get("apis") or []),
                     (a.get("description") or "")[:38]))
        return
    by_code = {a.get("code"): a for a in apps}
    total = 0
    for gname, codes in GROUPS:
        have = [c for c in codes if c in by_code]
        if not have:
            continue
        print("=== %s ===" % gname)
        for c in have:
            a = by_code[c]
            n = len(a.get("apis") or [])
            total += n
            print("  %-22s %-22s %2d 接口" % (c, a.get("name"), n))
            if a.get("description"):
                print("      %s" % a["description"][:70])
        print()
    print("合计 %d 个插件 / %d 个接口" % (len(by_code), total))
    missing = [c for _, cs in GROUPS for c in cs if c not in by_code]
    if missing:
        print("（未收录：%s）" % "、".join(missing))


def cmd_find(kw):
    apps = fetch_apps()
    hit = 0
    for a in apps:
        code = a.get("code") or ""
        name = a.get("name") or ""
        desc = a.get("description") or ""
        in_app = kw in code or kw in name or kw in desc
        apis = [x for x in (a.get("apis") or [])
                if kw in (x.get("code") or "") or kw in (x.get("name") or "")]
        if in_app or apis:
            hit += 1
            print("%s（%s）" % (name, code))
            if desc:
                print("   %s" % desc[:80])
            for x in (apis or a.get("apis") or []):
                mark = "→" if x in apis else " "
                print("   %s %-16s %s" % (mark, x.get("code"), x.get("name")))
            print()
    if not hit:
        print("没找到含「%s」的插件或接口" % kw)


def cmd_show(app):
    a = fetch_one(app)
    print("%s（%s）" % (a.get("name") or "", app))
    if a.get("description"):
        print("  %s" % str(a["description"]).strip())
    print()
    for x in (a.get("apis") or []):
        mode = "异步" if x.get("call_type") == 2 else "同步"
        print("  %s · %s  [%s]" % (x.get("code"), x.get("name"), mode))
        print("    POST /api/v1/apps/%s/%s" % (app, x.get("code")))
        if x.get("description"):
            print("    %s" % str(x["description"])[:90])
        props, req = params_of(x)
        if req:
            print("    必填：%s" % "、".join("`%s`" % r for r in req))
        for k, v in props.items():
            if k in req:
                continue
            print("    可选：%-18s %-8s %s"
                  % (k, (v or {}).get("type") or "-",
                     ((v or {}).get("description") or "")[:50]))
        print()


def main():
    ap = argparse.ArgumentParser(prog="market.py",
                                 description="AI 插件市场浏览器 · api.a7w.cn")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("list", help="列出全部插件")
    p.add_argument("--raw", action="store_true", help="用平台原始分类")
    sub.add_parser("groups", help="只看能力分组概览")
    p = sub.add_parser("find", help="搜插件 / 接口")
    p.add_argument("keyword")
    p = sub.add_parser("show", help="看某插件的接口与必填参数")
    p.add_argument("app")
    args = ap.parse_args()

    if args.cmd == "list":
        cmd_list(args.raw)
    elif args.cmd == "groups":
        cmd_groups()
    elif args.cmd == "find":
        cmd_find(args.keyword)
    elif args.cmd == "show":
        cmd_show(args.app)
    return 0


if __name__ == "__main__":
    sys.exit(main())
