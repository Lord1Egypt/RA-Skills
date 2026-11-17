#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
zotero_import.py — Zotero 本地库 **导入** 适配器（升级项 H，2026-11-02）.

与 `scripts/zotero_exporter.py`（单向导出）互补：本模块把用户本机 Zotero 库
当作**检索输入源**读入，补 ct-literature「OA-only 检索」的盲区——用户在机构权限
下已收集的付费文献，同样是合法证据，只是公开 API 检索不到。

接入方式：**Zotero 官方本地 API**（HTTP，非 MCP、非第三方插件）
  Zotero 7 → 设置 → 高级 → 勾选「允许此计算机上的其他应用程序与 Zotero 通信」
  默认端点 http://127.0.0.1:23119/api/users/0
  可用环境变量 ZOTERO_LOCAL_API 覆盖。

纪律：
  - **只读**：本模块只发 GET，不含任何写操作（新增/修改条目一律不做）。
  - **无 key**：本地 API 不需要 API key，凭据零外泄。
  - **精确解析**：集合路径按名称逐级匹配；0 命中 / 同名歧义 → 显式失败并列出候选，
    **绝不"猜一个最像的"**。
  - **附件不重复计数**：子附件（有 parentItem）跟随父条目，不单独计入文献；
    独立附件（无 parentItem）默认不计入，仅在 stats 里如实计数。

参考来源：zotero-research-assistant-skill（本地 JSON CLI 接 Zotero，MCP-free），
见 ct-update/reports/deep_read_wechat8skills_2026-11-02.md。

CLI:
    python adapters/zotero_import.py --health
    python adapters/zotero_import.py --list
    python adapters/zotero_import.py --collection "肿瘤/NSCLC" --out zotero.json
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_BASE = os.environ.get("ZOTERO_LOCAL_API", "http://127.0.0.1:23119/api/users/0")
TIMEOUT = 8
_PAGE = 100

# Zotero itemType → ct-literature 的 study_type / type 词表
_TYPE_MAP = {
    "journalArticle": ("article", None),
    "conferencePaper": ("article", None),
    "preprint": ("preprint", "preprint"),
    "thesis": ("other", None),
    "book": ("other", None),
    "bookSection": ("other", None),
    "report": ("other", None),
    "webpage": ("other", None),
    "dataset": ("other", None),
}


class ZoteroError(RuntimeError):
    """本地 API 不可用 / 集合歧义 / 载荷异常——一律显式抛出，不静默返回空。"""


# 本地回环请求**必须绕过系统代理**：Windows/macOS 上 http_proxy 常把 127.0.0.1
# 也转发出去，导致本地 API 返回 502（2026-11-02 实测踩坑）。这是根因修复，
# 不是把错误消息写得更友好。
_NO_PROXY_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def _get(path, base=None, timeout=TIMEOUT):
    """GET 本地 API，返回 (payload, headers)。100/404 之外的状态一律抛错。"""
    base = base or DEFAULT_BASE
    url = base.rstrip("/") + "/" + path.lstrip("/")
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with _NO_PROXY_OPENER.open(req, timeout=timeout) as r:
            body = r.read().decode("utf-8", "replace")
            try:
                return json.loads(body), dict(r.headers)
            except ValueError:
                raise ZoteroError(
                    "本地 API 返回非 JSON（%s）：端口 23119 可能被其它程序占用。" % url)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, {}
        _hint = ""
        if e.code in (502, 503, 504):
            _hint = ("。端口 23119 很可能是被**系统代理或其它程序**占用，而非 Zotero 本身；"
                     "请确认 Zotero 正在运行，并在代理设置中排除 127.0.0.1/localhost。")
        raise ZoteroError("本地 API HTTP %s：%s%s" % (e.code, url, _hint))
    except urllib.error.URLError as e:
        raise ZoteroError(
            "无法连接 Zotero 本地 API（%s）：%s。请在 Zotero 7 设置→高级 勾选"
            "「允许此计算机上的其他应用程序与 Zotero 通信」并确认 Zotero 正在运行。"
            % (base, getattr(e, "reason", e)))


def health(base=None):
    """健康检查：本地 API 是否可用 + 能否读到集合列表。"""
    try:
        cols, _ = _get("collections?limit=1", base=base)
        return {"ok": True, "base": base or DEFAULT_BASE,
                "collection_sample": len(cols or [])}
    except ZoteroError as e:
        return {"ok": False, "base": base or DEFAULT_BASE, "error": str(e)}


def list_collections(base=None):
    """拉全量集合 → [{key, name, parent, path}]（path 为 'A/B/C' 形式）。"""
    out, start = [], 0
    while True:
        page, hdrs = _get("collections?limit=%d&start=%d" % (_PAGE, start), base=base)
        page = page or []
        out.extend(page)
        if len(page) < _PAGE:
            break
        start += _PAGE
    by_key = {}
    for c in out:
        d = c.get("data") or c
        by_key[d.get("key")] = {
            "key": d.get("key"),
            "name": (d.get("name") or "").strip(),
            "parent": (d.get("parentCollection") or False) or None,
            "path": None,
        }
    for k, c in by_key.items():
        parts, cur, guard = [], c, 0
        while cur and guard < 32:
            parts.append(cur["name"])
            cur = by_key.get(cur.get("parent"))
            guard += 1
        c["path"] = "/".join(reversed(parts))
    return sorted(by_key.values(), key=lambda x: x["path"] or "")


def resolve_collection(path, collections=None, base=None):
    """按 'A/B/C' 名称路径精确解析集合 key。

    0 命中 → 抛错并列出最接近的候选；同名多命中 → 抛错并列出 key 让用户指定，
    绝不静默挑一个。
    """
    cols = collections if collections is not None else list_collections(base=base)
    want = "/".join(p.strip() for p in (path or "").split("/") if p.strip())
    if not want:
        raise ZoteroError("集合路径为空")
    exact = [c for c in cols if (c.get("path") or "").lower() == want.lower()]
    if len(exact) == 1:
        return exact[0]
    if len(exact) > 1:
        raise ZoteroError(
            "集合路径「%s」有 %d 个同名命中，请改用唯一路径或指定 key：%s"
            % (want, len(exact), ", ".join(c["key"] for c in exact)))
    # 退一步：允许只给叶子名（唯一时才接受，避免误取）
    leaves = [c for c in cols
              if (c.get("name") or "").lower() == want.split("/")[-1].lower()]
    if len(leaves) == 1:
        return leaves[0]
    if len(leaves) > 1:
        raise ZoteroError(
            "集合「%s」在多个父级下同名，请给出完整路径（如 A/%s）：%s"
            % (want, want, ", ".join("%s(%s)" % (c["path"], c["key"]) for c in leaves)))
    near = [c["path"] for c in cols if want.lower() in (c.get("path") or "").lower()][:10]
    raise ZoteroError(
        "找不到集合「%s」。%s" % (
            want, ("相近路径：" + "; ".join(near)) if near else "本库共 %d 个集合，"
            "用 --list 查看。" % len(cols)))


def _descendant_keys(col_key, collections):
    kids = {col_key}
    changed = True
    while changed:
        changed = False
        for c in collections:
            if c.get("parent") in kids and c["key"] not in kids:
                kids.add(c["key"])
                changed = True
    return kids


def _creators_to_authors(data):
    out = []
    for c in (data.get("creators") or []):
        nm = c.get("name") or ""
        if not nm:
            last = (c.get("lastName") or "").strip()
            first = (c.get("firstName") or "").strip()
            nm = ("%s %s" % (first, last)).strip() if first else last
        if nm:
            out.append(nm)
    return out


def _year_of(data):
    raw = (data.get("date") or "").strip()
    import re as _re
    m = _re.search(r"(1[6-9]\d{2}|20\d{2})", raw)
    return int(m.group(1)) if m else None


def to_work(item):
    """Zotero item → ct-literature work schema（字段名对齐 fetch_* 产出）。"""
    d = item.get("data") or item
    it = d.get("itemType") or "journalArticle"
    typ, study = _TYPE_MAP.get(it, ("other", None))
    doi = (d.get("DOI") or "").strip()
    if doi.lower().startswith("https://doi.org/"):
        doi = doi[len("https://doi.org/"):]
    publication = (d.get("publicationTitle") or d.get("proceedingsTitle")
                   or d.get("bookTitle") or d.get("repository") or "")
    work = {
        "title": (d.get("title") or "").strip(),
        "doi": doi or None,
        "authors": _creators_to_authors(d),
        "year": _year_of(d),
        "publication": publication,
        "abstract_snippet": (d.get("abstractNote") or "").strip()[:1200] or None,
        "url": d.get("url") or None,
        "type": typ,
        "study_type": study,
        "source": "Zotero",
        "zotero_key": d.get("key") or item.get("key"),
        "zotero_item_type": it,
    }
    tags = [t.get("tag") for t in (d.get("tags") or []) if isinstance(t, dict) and t.get("tag")]
    if tags:
        work["keywords"] = tags
    return {k: v for k, v in work.items() if v not in (None, "", [])}


def fetch(collection_path=None, recursive=True, limit=2000, base=None,
          include_standalone_attachments=False):
    """读指定集合（或整个库）的文献 → ct-literature source payload。

    Returns {source: "Zotero", query, count, works, stats, ...}
    """
    cols = list_collections(base=base)
    col = resolve_collection(collection_path, collections=cols, base=base) \
        if collection_path else None
    params = ["limit=%d" % _PAGE, "itemType=-attachment||note"]
    if col:
        scope = _descendant_keys(col["key"], cols) if recursive else {col["key"]}
        q = "items?" + "&".join(params)
        # 集合过滤在本地 API 上通过 collection 端点实现；跨多集合时逐个拉取后合并
        raw_items = []
        for ck in sorted(scope):
            start = 0
            while True:
                page, _ = _get("collections/%s/items?limit=%d&start=%d"
                               % (urllib.parse.quote(ck), _PAGE, start), base=base)
                page = page or []
                raw_items.extend(page)
                if len(page) < _PAGE:
                    break
                start += _PAGE
    else:
        raw_items = []
        start = 0
        while True:
            page, _ = _get("items?limit=%d&start=%d&itemType=-attachment||note"
                           % (_PAGE, start), base=base)
            page = page or []
            raw_items.extend(page)
            if len(page) < _PAGE:
                break
            start += _PAGE

    stats = {"raw": len(raw_items), "attachments_skipped": 0,
             "standalone_attachments": 0, "notes_skipped": 0,
             "no_title_skipped": 0, "dup_same_doi": 0}
    works, seen = [], {}
    for it in raw_items:
        d = it.get("data") or it
        it_t = d.get("itemType")
        if it_t == "attachment":
            if d.get("parentItem"):
                stats["attachments_skipped"] += 1
                continue
            stats["standalone_attachments"] += 1
            if not include_standalone_attachments:
                continue
        if it_t == "note":
            stats["notes_skipped"] += 1
            continue
        w = to_work(it)
        if not w.get("title"):
            stats["no_title_skipped"] += 1
            continue
        key = ("doi:" + w["doi"].lower()) if w.get("doi") else ("t:" + w["title"].lower())
        if key in seen:
            stats["dup_same_doi"] += 1
            continue
        seen[key] = True
        works.append(w)

    works = works[:limit]
    return {
        "source": "Zotero",
        "query": collection_path or "(whole library)",
        "count": len(works),
        "works": works,
        "collection": (col["path"] if col else None),
        "recursive": bool(recursive and col),
        "stats": stats,
    }


def main():
    ap = argparse.ArgumentParser(
        description="Import a local Zotero collection as a literature source payload "
                    "(read-only, local API, no API key).")
    ap.add_argument("--health", action="store_true", help="check local API availability")
    ap.add_argument("--list", action="store_true", dest="list_cols", help="list collections")
    ap.add_argument("--collection", default=None, help="collection path, e.g. 'A/B'")
    ap.add_argument("--no-recursive", action="store_true", help="only this collection")
    ap.add_argument("--limit", type=int, default=2000)
    ap.add_argument("--base", default=None, help="override local API base URL")
    ap.add_argument("--out", default=None, help="write payload JSON here")
    args = ap.parse_args()

    try:
        if args.health:
            h = health(base=args.base)
            print(json.dumps(h, ensure_ascii=False, indent=2))
            return 0 if h["ok"] else 3
        if args.list_cols:
            for c in list_collections(base=args.base):
                print("%-50s %s" % (c["path"], c["key"]))
            return 0
        if not args.collection:
            ap.error("需要 --health / --list / --collection 之一")
        payload = fetch(args.collection, recursive=not args.no_recursive,
                        limit=args.limit, base=args.base)
    except ZoteroError as e:
        print("[ERROR] %s" % e, file=sys.stderr)
        return 3

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print("[OK] Zotero import: %d works -> %s (collection=%s)" % (
            payload["count"], args.out, payload.get("collection")))
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    print("[stats] %s" % json.dumps(payload.get("stats", {}), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
