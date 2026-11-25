#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""官方数据源直查：国标 / 召回 / 3C 入口 / 抽检入口。

避雷技能专用。解决的问题：让结论里的「有/没有负面记录」来自官方数据源的
真实查询结果，而不是模型记忆或网页搜索的二手转述。

三条设计铁律：
  1. 每条结果必带 source（数据源）+ queried_at（查询日期），可直接回查。
  2. 查不到 / 网络失败 / 接口变更 → 明确写 status，绝不返回编造数据。
  3. 没有免密钥官方接口的（3C 证书、工业品抽检）→ 只生成官方检索入口 URL，
     标注 needs_manual_check，不假装查过。

数据源与能力边界（2026-11-24 实测）：
  - 国标：std.samr.gov.cn/gb/search/gbQueryPage 官方 JSON，返回标准号/性质/状态/日期。可用。
  - 召回：Pipeworx 转型代理 SAMR 公开公告（约 1458 条，绝大多数是汽车摩托），
    免密钥，返回 samr.gov.cn 原文链接。可用，但覆盖有限，空结果 ≠ 无召回。
  - 3C：cx.cnca.cn 官方禁止爬虫，第三方 API 收费 → 只给官方查询入口。
  - 抽检：工业品抽检无统一免密钥接口；食品抽检在 spcjsac.gsxt.gov.cn → 只给入口。

用法：
  python3 official_lookup.py gb --keyword "移动电源"
  python3 official_lookup.py recall --query "充电宝" [--limit 20] [--from 2020-01-01]
  python3 official_lookup.py ccc --company "小米" [--cert 证书号]
  python3 official_lookup.py inspection --company "某某" [--food]
  python3 official_lookup.py all --query "充电宝" --format json
  python3 official_lookup.py selftest

零依赖，仅标准库，Python 3.8+。退出码：成功 0；查询失败也 0（不阻断主流程，
失败信息在 status 字段里如实返回）。
"""

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import date

TIMEOUT = 12
UA = "Mozilla/5.0 (compatible; bilei-skill/1.0; official-lookup)"
TODAY = date.today().isoformat()

GB_API = "https://std.samr.gov.cn/gb/search/gbQueryPage"
GB_DETAIL = "https://std.samr.gov.cn/gb/search/gbDetailed?id={id}"
RECALL_API = "https://gateway.pipeworx.io/v1/tools/china_search_recalls"
CCC_ENTRY = "https://cx.cnca.cn/CertECloud/result/skipResultList"
FOOD_INSPECTION_ENTRY = "https://spcjsac.gsxt.gov.cn/"
SAMR_SEARCH = "https://www.samr.gov.cn/zw/zh/"


def _fetch(url, data=None, headers=None):
    """返回 (text, None) 或 (None, error_str)。"""
    hdr = {"User-Agent": UA}
    if headers:
        hdr.update(headers)
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        hdr["Content-Type"] = "application/json"
    try:
        req = urllib.request.Request(url, data=body, headers=hdr)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.read().decode("utf-8", "replace"), None
    except Exception as exc:
        return None, "%s: %s" % (type(exc).__name__, exc)


def _strip_tags(s):
    return re.sub(r"<[^>]+>", "", s or "")


def _ok(source, **kw):
    out = {"status": "ok", "source": source, "queried_at": TODAY}
    out.update(kw)
    return out


def _fail(source, reason, **kw):
    out = {"status": "error", "source": source, "queried_at": TODAY,
           "error": reason}
    out.update(kw)
    return out


# ---------- 国标 ----------

def query_gb(keyword, page_size=10):
    """查国家标准全文公开系统的标准元数据。不下载全文（GB/T 受版权保护）。"""
    params = urllib.parse.urlencode({
        "searchText": keyword, "pageNumber": 1, "pageSize": page_size,
    })
    text, err = _fetch(GB_API + "?" + params)
    if err:
        return _fail("国家标准全文公开系统 std.samr.gov.cn", err, keyword=keyword)
    try:
        obj = json.loads(text)
    except (ValueError, TypeError):
        return _fail("国家标准全文公开系统 std.samr.gov.cn",
                     "响应不是合法 JSON（接口可能已变更）", keyword=keyword,
                     raw_head=text[:200])
    rows = obj.get("rows") or []
    items = []
    for r in rows:
        code = r.get("C_STD_CODE", "")
        items.append({
            "std_code": code,
            "name": _strip_tags(r.get("C_C_NAME", "")),
            "nature": r.get("STD_NATURE", ""),
            "state": r.get("STATE", ""),
            "effective_date": r.get("ACT_DATE", ""),
            "issue_date": r.get("ISSUE_DATE", ""),
            "url": GB_DETAIL.format(id=r.get("id", "")),
        })
    return _ok("国家标准全文公开系统 std.samr.gov.cn", keyword=keyword,
               total=obj.get("total", len(items)), results=items,
               note="仅元数据；强制性国标(GB)可下载全文，推荐性国标(GB/T)禁止程序化下载，"
                    "全文请到官方预览页在线阅读。")


def fmt_gb(r):
    if r["status"] != "ok":
        return "国标查询失败：%s（%s）" % (r["error"], r["source"])
    lines = ["国标检索「%s」：共 %s 条（%s，%s）" %
             (r["keyword"], r["total"], r["source"], r["queried_at"])]
    for it in r["results"][:8]:
        lines.append("  - %s | %s | %s | %s | 实施 %s | %s" %
                     (it["std_code"], it["nature"], it["state"], it["name"],
                      it["effective_date"] or "未标注", it["url"]))
    if not r["results"]:
        lines.append("  （无匹配标准；关键词可能不是标准命名用语，换词再查）")
    lines.append("  注：" + r["note"])
    return "\n".join(lines)


# ---------- 召回 ----------

def query_recall(query, limit=20, date_from=None, category="all"):
    """查 SAMR 产品召回公告（经 Pipeworx 免密钥网关，返回官方原文链接）。"""
    args = {"query": query, "limit": max(1, min(50, limit)), "category": category}
    if date_from:
        args["from"] = date_from
    text, err = _fetch(RECALL_API, data=args)
    if err:
        return _fail("SAMR 召回公告（Pipeworx 网关）", err, query=query)
    try:
        obj = json.loads(text)
    except (ValueError, TypeError):
        return _fail("SAMR 召回公告（Pipeworx 网关）",
                     "响应不是合法 JSON", query=query, raw_head=text[:200])
    recalls = []
    for x in obj.get("recalls", []):
        recalls.append({
            "title": x.get("title", ""),
            "date": x.get("date", ""),
            "category": x.get("category", ""),
            "url": x.get("url", ""),
        })
    return _ok("SAMR 召回公告（Pipeworx 网关）", query=query,
               upstream_total=obj.get("list_total_upstream"),
               matched=obj.get("matched", len(recalls)),
               data_as_of=obj.get("data_as_of", ""),
               results=recalls,
               scope_note=obj.get("scope_note", ""),
               note="空结果不等于「无召回」——该库绝大多数是汽车摩托，消费品覆盖有限；"
                    "须到 samr.gov.cn 原文页再确认。")


def fmt_recall(r):
    if r["status"] != "ok":
        return "召回查询失败：%s（%s）" % (r["error"], r["source"])
    head = "召回检索「%s」：命中 %s 条（%s，数据截至 %s，查询 %s）" % (
        r["query"], r["matched"], r["source"], r["data_as_of"] or "未标注", r["queried_at"])
    lines = [head]
    for it in r["results"][:15]:
        lines.append("  - %s | %s | %s" % (it["date"], it["title"], it["url"]))
    if not r["results"]:
        lines.append("  （未命中；注意：空结果 ≠ 无召回，见下方覆盖说明）")
    lines.append("  覆盖说明：" + (r["scope_note"] or "未标注"))
    lines.append("  判定注意：" + r["note"])
    return "\n".join(lines)


# ---------- 3C 与抽检：只给官方入口，不伪造查询结果 ----------

def query_ccc(company=None, cert=None):
    params = {}
    if cert:
        params["certNo"] = cert
    if company:
        params["enterpriseName"] = company
    suffix = ("?" + urllib.parse.urlencode(params)) if params else ""
    return {
        "status": "manual_check_required",
        "source": "全国认证认可信息公共服务平台 cx.cnca.cn",
        "queried_at": TODAY,
        "url": CCC_ENTRY + suffix,
        "params": params,
        "note": "官方明示禁止爬虫获取认证数据，第三方 API 收费。本脚本不抓取、不编造证书信息。"
                "请打开上述官方入口人工核对：证书编号、申请人、制造商、有效期、证书状态。"
                "3C 证书缺失即一票否决——必须人工确认，不得凭商家宣传判定「有」。",
    }


def fmt_ccc(r):
    return ("3C 认证：需人工核实（%s，%s）\n  官方查询入口：%s\n  %s" %
            (r["source"], r["queried_at"], r["url"], r["note"]))


def query_inspection(company=None, food=False):
    if food:
        return {
            "status": "manual_check_required",
            "source": "食品安全抽检公布结果查询平台 spcjsac.gsxt.gov.cn",
            "queried_at": TODAY,
            "url": FOOD_INSPECTION_ENTRY,
            "note": "食品抽检结果在官方平台查询；本脚本不抓取。查到不合格通报须附原文链接与日期。",
        }
    q = urllib.parse.quote(company or "")
    return {
        "status": "manual_check_required",
        "source": "国家市场监督管理总局 samr.gov.cn",
        "queried_at": TODAY,
        "url": SAMR_SEARCH,
        "search_hint": "站内搜索关键词：%s + 抽检 / 不合格 / 行政处罚" % (company or "品牌名"),
        "note": "工业品抽检无统一免密钥接口（部分省级平台需实名令牌）。本脚本不声称已查。"
                "请到 SAMR 官网按品牌/企业名搜索抽检通报与行政处罚，逐条记录文号、日期、原文链接。",
    }


def fmt_inspection(r):
    return ("抽检/处罚：需人工核实（%s，%s）\n  官方入口：%s\n  %s\n  %s" %
            (r["source"], r["queried_at"], r["url"],
             r.get("search_hint", ""), r["note"]))


# ---------- 组合与输出 ----------

def run_all(query, limit=20, date_from=None):
    return {
        "generated_at": TODAY,
        "query": query,
        "gb": query_gb(query),
        "recall": query_recall(query, limit=limit, date_from=date_from),
        "ccc": query_ccc(company=query),
        "inspection": query_inspection(company=query),
        "verdict_hint": "国标与召回为实查；3C 与抽检为人工入口。"
                        "任何「无负面记录」的结论，只有在四项都核实后才能写。",
    }


def print_report(res, as_json=False):
    if as_json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return
    print("=" * 60)
    print("避雷 · 官方数据源查询 | 查询词：%s | %s" %
          (res.get("query", "—"), res.get("generated_at", TODAY)))
    print("=" * 60)
    if "gb" in res:
        print(fmt_gb(res["gb"]))
        print()
        print(fmt_recall(res["recall"]))
        print()
        print(fmt_ccc(res["ccc"]))
        print()
        print(fmt_inspection(res["inspection"]))
        print()
        print("判定：" + res["verdict_hint"])
    else:
        print(json.dumps(res, ensure_ascii=False, indent=2))


def selftest():
    """离线自检：只测纯函数与结构，不依赖网络。"""
    checks = []
    r = query_ccc(company="测试企业", cert="ABC123")
    checks.append(("ccc 不抓取且给入口",
                   r["status"] == "manual_check_required" and "cx.cnca.cn" in r["url"]))
    r2 = query_inspection(company="测试企业")
    checks.append(("抽检不伪造结果",
                   r2["status"] == "manual_check_required" and "samr.gov.cn" in r2["url"]))
    r3 = query_inspection(food=True)
    checks.append(("食品抽检给专用入口", "spcjsac.gsxt.gov.cn" in r3["url"]))
    checks.append(("标签清洗", _strip_tags("<sacinfo>移动</sacinfo><sacinfo>电源</sacinfo>") == "移动电源"))
    r4 = _fail("测试源", "模拟失败")
    checks.append(("失败不返回假数据", r4["status"] == "error" and "error" in r4))
    r5 = _ok("测试源", results=[])
    checks.append(("成功结果带来源与日期",
                   r5["status"] == "ok" and r5["source"] == "测试源" and r5["queried_at"] == TODAY))
    fail = 0
    for name, ok in checks:
        print(("PASS  " if ok else "FAIL  ") + name)
        if not ok:
            fail += 1
    print("\n%d/%d 通过" % (len(checks) - fail, len(checks)))
    sys.exit(1 if fail else 0)


def main():
    ap = argparse.ArgumentParser(description="避雷 · 官方数据源直查")
    sub = ap.add_subparsers(dest="cmd")

    p_gb = sub.add_parser("gb", help="查国家标准元数据")
    p_gb.add_argument("--keyword", required=True)
    p_gb.add_argument("--size", type=int, default=10)
    p_gb.add_argument("--format", choices=["text", "json"], default="text")

    p_rc = sub.add_parser("recall", help="查 SAMR 产品召回公告")
    p_rc.add_argument("--query", required=True)
    p_rc.add_argument("--limit", type=int, default=20)
    p_rc.add_argument("--from", dest="date_from", default=None)
    p_rc.add_argument("--format", choices=["text", "json"], default="text")

    p_ccc = sub.add_parser("ccc", help="3C 官方查询入口（需人工核实）")
    p_ccc.add_argument("--company", default=None)
    p_ccc.add_argument("--cert", default=None)
    p_ccc.add_argument("--format", choices=["text", "json"], default="text")

    p_ins = sub.add_parser("inspection", help="抽检/处罚官方入口（需人工核实）")
    p_ins.add_argument("--company", default=None)
    p_ins.add_argument("--food", action="store_true")
    p_ins.add_argument("--format", choices=["text", "json"], default="text")

    p_all = sub.add_parser("all", help="一次查全部（国标+召回实查，3C+抽检给入口）")
    p_all.add_argument("--query", required=True)
    p_all.add_argument("--limit", type=int, default=20)
    p_all.add_argument("--from", dest="date_from", default=None)
    p_all.add_argument("--format", choices=["text", "json"], default="text")

    sub.add_parser("selftest", help="离线自检")

    args = ap.parse_args()
    if not args.cmd:
        ap.print_help()
        sys.exit(1)
    if args.cmd == "selftest":
        selftest()  # 内部会 sys.exit，不返回

    as_json = getattr(args, "format", "text") == "json"
    if args.cmd == "gb":
        res = query_gb(args.keyword, page_size=args.size)
        print(json.dumps(res, ensure_ascii=False, indent=2) if as_json else fmt_gb(res))
    elif args.cmd == "recall":
        res = query_recall(args.query, limit=args.limit, date_from=args.date_from)
        print(json.dumps(res, ensure_ascii=False, indent=2) if as_json else fmt_recall(res))
    elif args.cmd == "ccc":
        res = query_ccc(company=args.company, cert=args.cert)
        print(json.dumps(res, ensure_ascii=False, indent=2) if as_json else fmt_ccc(res))
    elif args.cmd == "inspection":
        res = query_inspection(company=args.company, food=args.food)
        print(json.dumps(res, ensure_ascii=False, indent=2) if as_json else fmt_inspection(res))
    elif args.cmd == "all":
        print_report(run_all(args.query, limit=args.limit, date_from=args.date_from), as_json)


if __name__ == "__main__":
    main()
