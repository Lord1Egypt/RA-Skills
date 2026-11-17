#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DUCC 配置读取脚本。

层级：命名空间(namespace) → 配置文件(config) → 环境/profile(如 dev/common) → 配置项(item: key/value)

子命令：
  namespaces                              列出所有命名空间（可 --search 过滤）
  configs   <ns>                          列出某命名空间下的配置文件
  profiles  <ns> <cfg>                    列出配置文件下的 profile（生产配置/预发配置）
  items     <ns> <cfg> <prof>             列出 profile 下的配置项（key/value），支持分页/搜索
  get       <ns> <cfg> <prof> <key>       读取单个配置项的值

<ns>/<cfg>/<prof> 都可以传 code（如 pop_customs_center / center_config / common）
或直接传数字 ID，脚本自动解析。

环境：--env online(生产,默认) / pre(预发)。预发未开放时读到空或 503。

示例：
  python config.py namespaces --search customs
  python config.py configs pop_customs_center
  python config.py profiles pop_customs_center center_config
  python config.py items pop_customs_center center_config common
  python config.py items pop_customs_center center_config common --search order.trace --size 50
  python config.py get pop_customs_center center_config common ducc.order.trace.merge.read.switch
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
import jme_auth  # noqa: E402
from ducc_client import DuccClient, add_common_args, emit, log  # noqa: E402


def _fail(msg, **extra):
    emit({"ok": False, "error": msg, **extra})
    sys.exit(1)


def cmd_namespaces(c, args):
    _, data = c.get(f"/v1/namespaces/search?page=1&size={args.size}")
    if not c.ok(data):
        _fail("命名空间列表获取失败", raw=data)
    items = data.get("data", [])
    kw = (args.search or "").lower()
    out = []
    for it in items:
        if kw and kw not in (it.get("code", "") + it.get("name", "")).lower():
            continue
        out.append({
            "nsId": it["id"], "code": it.get("code"), "name": it.get("name"),
            "owner": (it.get("owner") or {}).get("code"),
        })
    emit({"ok": True, "total": data.get("pagination", {}).get("totalRecord"),
          "count": len(out), "namespaces": out})


def cmd_configs(c, args):
    ns = c.resolve_ns(args.ns)
    if not ns:
        _fail(f"命名空间未找到：{args.ns}")
    _, data = c.get(
        f"/v1/namespace/{ns['id']}/configs/search?page=1&size={args.size}"
        f"&dataTypes=0,2&filterNoProfile=true")
    if not c.ok(data):
        _fail("配置文件列表获取失败", raw=data)
    out = [{"cId": it["id"], "code": it.get("code"), "name": it.get("name"),
            "dataType": it.get("dataTypeEnum")} for it in data.get("data", [])]
    emit({"ok": True, "namespace": {"nsId": ns["id"], "code": ns.get("code"), "name": ns.get("name")},
          "count": len(out), "configs": out})


def cmd_profiles(c, args):
    ns, cfg, _ = c.resolve_all(args.ns, args.cfg)
    if not ns:
        _fail(f"命名空间未找到：{args.ns}")
    if not cfg:
        _fail(f"配置文件未找到：{args.cfg}")
    _, data = c.get(
        f"/admin/v2/namespace/{ns['id']}/profiles/search?page=1&size={args.size}&configType=0",
        env=args.env)
    if not c.ok(data):
        _fail("profile 列表获取失败", raw=data)
    items = data.get("data", [])
    if not items and c.env == "pre":
        emit({"ok": True, "note": "预发环境未开放或无 profile（data 为空）",
              "env": "pre", "profiles": []})
        return
    out = [{"profileId": it["id"], "code": it.get("code"), "name": it.get("name"),
            "version": (it.get("version") or {}).get("name")} for it in items]
    emit({"ok": True, "env": c.env,
          "namespace": {"nsId": ns["id"], "code": ns.get("code")},
          "config": {"cId": cfg["id"], "code": cfg.get("code")},
          "count": len(out), "profiles": out})


def _resolve_items_ctx(c, args):
    ns, cfg, prof = c.resolve_all(args.ns, args.cfg, args.prof, env=args.env)
    if not ns:
        _fail(f"命名空间未找到：{args.ns}")
    if not cfg:
        _fail(f"配置文件未找到：{args.cfg}")
    if not prof:
        if c.env == "pre":
            _fail(f"profile 未找到：{args.prof}（预发环境可能未开放）", env="pre")
        _fail(f"profile 未找到：{args.prof}")
    return ns, cfg, prof


def cmd_items(c, args):
    ns, cfg, prof = _resolve_items_ctx(c, args)
    all_items = []
    page = 1
    while True:
        _, data = c.get(
            f"/admin/v2/namespace/{ns['id']}/config/{cfg['id']}/profile/{prof['id']}"
            f"/items/search?size={args.size}&page={page}&fromRelease=false"
            f"&orderField=updateTime&desc=desc", env=args.env)
        if not c.ok(data):
            _fail("配置项获取失败", raw=data)
        batch = data.get("data", [])
        all_items.extend(batch)
        pg = data.get("pagination", {})
        if args.all and page < pg.get("pages", 1):
            page += 1
            continue
        break
    kw = (args.search or "").lower()
    out = []
    for it in all_items:
        if kw and kw not in (it.get("key", "") + (it.get("description") or "")).lower():
            continue
        out.append({
            "key": it.get("key"),
            "value": it.get("value"),
            "description": it.get("description"),
            "dataType": it.get("dataType"),
            "isReleased": it.get("isReleased"),
            "updateBy": (it.get("updateBy") or {}).get("code"),
        })
    emit({"ok": True, "env": c.env,
          "namespace": ns.get("code"), "config": cfg.get("code"), "profile": prof.get("code"),
          "totalRecord": data.get("pagination", {}).get("totalRecord"),
          "count": len(out), "items": out})


def cmd_get(c, args):
    ns, cfg, prof = _resolve_items_ctx(c, args)
    # 优先精确搜索，再本地匹配 key
    _, data = c.get(
        f"/admin/v2/namespace/{ns['id']}/config/{cfg['id']}/profile/{prof['id']}"
        f"/items/search?size=1000&page=1&fromRelease=false"
        f"&orderField=updateTime&desc=desc", env=args.env)
    if not c.ok(data):
        _fail("配置项获取失败", raw=data)
    for it in data.get("data", []):
        if it.get("key") == args.key:
            emit({"ok": True, "env": c.env,
                  "namespace": ns.get("code"), "config": cfg.get("code"), "profile": prof.get("code"),
                  "key": it.get("key"), "value": it.get("value"),
                  "description": it.get("description"),
                  "dataType": it.get("dataType"), "isReleased": it.get("isReleased"),
                  "updateBy": (it.get("updateBy") or {}).get("code")})
            return
    _fail(f"配置项 key 未找到：{args.key}")


def main():
    ap = argparse.ArgumentParser(description="DUCC 配置读取")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("namespaces", help="列出所有命名空间")
    p.add_argument("--search", default="", help="按 code/name 过滤")
    p.add_argument("--size", type=int, default=1000)
    add_common_args(p)
    p.set_defaults(func=cmd_namespaces)

    p = sub.add_parser("configs", help="列出命名空间下的配置文件")
    p.add_argument("ns", help="命名空间 code 或 nsId")
    p.add_argument("--size", type=int, default=1000)
    add_common_args(p)
    p.set_defaults(func=cmd_configs)

    p = sub.add_parser("profiles", help="列出配置文件下的 profile（生产配置/预发配置）")
    p.add_argument("ns")
    p.add_argument("cfg", help="配置文件 code 或 cId")
    p.add_argument("--size", type=int, default=100)
    add_common_args(p)
    p.set_defaults(func=cmd_profiles)

    p = sub.add_parser("items", help="列出 profile 下的配置项")
    p.add_argument("ns")
    p.add_argument("cfg")
    p.add_argument("prof", help="profile code(如 dev/common) 或 profileId")
    p.add_argument("--search", default="", help="按 key/描述 过滤")
    p.add_argument("--size", type=int, default=100)
    p.add_argument("--all", action="store_true", help="翻遍所有分页")
    add_common_args(p)
    p.set_defaults(func=cmd_items)

    p = sub.add_parser("get", help="读取单个配置项的值")
    p.add_argument("ns")
    p.add_argument("cfg")
    p.add_argument("prof")
    p.add_argument("key", help="配置项 key")
    add_common_args(p)
    p.set_defaults(func=cmd_get)

    args = ap.parse_args()

    if getattr(args, "clear_cache", False):
        jme_auth.clear_cache()
        print("token 缓存已清除")
        return

    c = DuccClient(env=getattr(args, "env", "online"),
                   force_refresh=getattr(args, "force_refresh", False))
    args.func(c, args)


if __name__ == "__main__":
    main()
