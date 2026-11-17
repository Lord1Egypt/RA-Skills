"""EU CTR（欧盟临床试验注册库）直连适配器（B 层优化，2026-09-06）。

背景：WHO ICTRP 里最大的非 CT.gov 注册库是 EUCTR。统一网关对 WHO 只回 ~10 条，
而 EU CTR 官网 www.clinicaltrialsregister.eu 是纯 HTML 站点（2026-09-06 实测
检索页/详情页直连 200、无反爬），可绕开网关限制补全 EU/EEA 注册的试验。

原计划直抓 WHO Trial2.aspx 详情页——实测为纯 ASP.NET postback 壳（无数据无 JS
端点），纯 HTTP 不可行，故改走 EU CTR 主库直连（ISRCTN 亦为 JS 壳，一并放弃）。

流程：
  1) GET /ctr-search/search?query=<词> 收集 /ctr-search/trial/<EudraCT>/<CC> 链接
  2) 逐个抓国家版详情（优先 ES/FR/DE/PL…，GB 已停更跳过；内容校验含 "EudraCT number"）
  3) 按 label 解析最小字段集，输出与 normalize.py WHO 路径兼容的记录结构

礼貌抓取：1.5s 间隔 + 按 EudraCT 本地缓存。
"""
import argparse
import html as html_mod
import json
import os
import re
import sys
import time

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE = "https://www.clinicaltrialsregister.eu"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"}

COUNTRY_FALLBACK = ["ES", "FR", "DE", "PL", "IT", "NL", "BE", "PT", "SE", "DK", "HU", "CZ", "AT", "SI", "BG", "HR", "EE", "GR", "FI", "NO"]

# 详情页 label → 输出键（兼容 normalize.py WHO 路径候选键）
LABELS = [
    ("EudraCT number", "EudraCT number"),
    ("Full title of the trial", "公共标题"),
    ("Title of the trial for lay people", "试验通俗题目"),
    ("Name of Sponsor", "主要申办方"),
    ("Trial status", "试验状态"),
    ("Date on which this record was first entered in the EudraCT database", "注册日期"),
    ("Medical condition(s) under investigation", "适应症"),
    ("Study type", "Study type"),
    ("Phase", "试验分期"),
    ("Name of the ethics committee", "伦理委员会"),
]


def _session() -> "requests.Session":
    s = requests.Session()
    s.headers.update(UA)
    s.verify = False
    return s


def _plain(html: str) -> str:
    t = re.sub(r"<(script|style)[\s\S]*?</\1>", "", html, flags=re.I)
    t = re.sub(r"<[^>]+>", "|", t)
    t = html_mod.unescape(t)
    return re.sub(r"(\s*\|\s*)+", " | ", t)


def _search_links(s: "requests.Session", query: str, page: int = 1) -> list:
    url = f"{BASE}/ctr-search/search?query={requests.utils.quote(query)}"
    if page > 1:
        url += f"&page={page}"
    r = s.get(url, timeout=40)
    r.raise_for_status()
    links = re.findall(r'href="(/ctr-search/trial/(\d{4}-\d{6}-\d{2})/([A-Z]{2}))"', r.text)
    # 去重：同一 EudraCT 取第一个国家链接
    seen, out = set(), []
    for path, euct, cc in links:
        if cc == "GB":  # GB 已停更，内容多为空
            continue
        if euct in seen:
            continue
        seen.add(euct)
        out.append({"eudract": euct, "path": path, "cc": cc})
    return out


def _detail(s: "requests.Session", path: str) -> dict:
    """抓一个详情；若首选国家为空壳，按 COUNTRY_FALLBACK 换国家重试。"""
    m = re.match(r"/ctr-search/trial/(\d{4}-\d{6}-\d{2})/([A-Z]{2})", path)
    euct, cc = m.group(1), m.group(2)
    tried = [cc] + [c for c in COUNTRY_FALLBACK if c != cc]
    last_err = ""
    for c in tried[:6]:
        r = s.get(f"{BASE}/ctr-search/trial/{euct}/{c}", timeout=40)
        if r.status_code != 200:
            last_err = f"HTTP {r.status_code}"
            continue
        plain = _plain(r.text)
        if "EudraCT number" not in plain:
            last_err = "empty shell"
            continue
        return {"plain": plain, "cc": c}
    raise RuntimeError(f"no usable country page ({last_err})")


def _parse_detail(plain: str, euct: str) -> dict:
    rec: dict = {"Main ID": f"EUCTR{euct}", "登记号": f"EUCTR{euct}",
                 "来源": "EU CTR", "国家": "European Union (EU/EEA)"}
    for label, out_key in LABELS:
        # label 后的值段：到下一个 " | D./A./B. 章节号" 或下一个已知 label 为止
        pat = re.escape(label) + r" \| (.+?)(?=\s*\|\s*[A-E]\.\d|\s*\|\s*(?:EudraCT number|Full title|Title of the trial|Name of Sponsor|Trial status|Date on which|Medical condition|Study type|Phase|Name of the ethics)|$)"
        m = re.search(pat, plain)
        if not m:
            continue
        val = re.sub(r"\s*\|\s*", " ", m.group(1)).strip()
        val = re.sub(r"\s+", " ", val)
        # 多语言并列时取第一段（句间分隔常为多个空格/语言重复）
        val = val.split("  ")[0].strip(" |") or val
        if val and out_key not in rec:
            rec[out_key] = val[:500]
    if not rec.get("EudraCT number"):
        rec["EudraCT number"] = euct
    return rec


def main() -> None:
    ap = argparse.ArgumentParser(description="EU CTR direct search + detail fetcher")
    ap.add_argument("--query", required=True, help="检索词（如 osimertinib 或 osimertinib lung）")
    ap.add_argument("--pages", type=int, default=1, help="检索结果页数（每页 ~20 条）")
    ap.add_argument("--max-trials", type=int, default=0, help="最多抓详情条数（0=不限）")
    ap.add_argument("--cache-dir", default="", help="详情缓存目录（按 EudraCT 幂等）")
    ap.add_argument("--delay", type=float, default=1.5, help="请求间隔秒")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    s = _session()
    cache = args.cache_dir or os.path.join(os.path.dirname(os.path.abspath(args.out)), "_euctr_cache")
    os.makedirs(cache, exist_ok=True)

    trials, seen = [], set()
    for pg in range(1, args.pages + 1):
        links = _search_links(s, args.query, pg)
        print(f"[euctr-direct] search page {pg}: {len(links)} trials")
        for t in links:
            if t["eudract"] not in seen:
                seen.add(t["eudract"])
                trials.append(t)
        if not links:
            break
        time.sleep(args.delay)
    if args.max_trials:
        trials = trials[: args.max_trials]
    print(f"[euctr-direct] {len(trials)} unique trials to fetch")

    records, fails = [], []
    for i, t in enumerate(trials, 1):
        cf = os.path.join(cache, f"{t['eudract']}.json")
        try:
            if os.path.exists(cf):
                with open(cf, encoding="utf-8") as f:
                    rec = json.load(f)
                rec["_cached"] = True
            else:
                d = _detail(s, t["path"])
                rec = _parse_detail(d["plain"], t["eudract"])
                rec["_cc_used"] = d["cc"]
                rec["_detail_url"] = f"{BASE}/ctr-search/trial/{t['eudract']}/{d['cc']}"
                with open(cf, "w", encoding="utf-8") as f:
                    json.dump(rec, f, ensure_ascii=False, indent=1)
            records.append(rec)
            print(f"[euctr-direct] {i}/{len(trials)} {t['eudract']}: {(rec.get('公共标题') or '')[:60]}")
        except Exception as e:
            fails.append({"eudract": t["eudract"], "error": str(e)[:150]})
            print(f"[euctr-direct] {i}/{len(trials)} {t['eudract']}: FAIL {str(e)[:80]}")
        time.sleep(args.delay)

    out = {"source": "EU CTR", "mode": "direct", "query": args.query,
           "records": records, "total": len(records), "failed": fails,
           "is_partial": len(records) < len(trials)}
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"[euctr-direct] done: {len(records)} ok, {len(fails)} failed -> {args.out}")


if __name__ == "__main__":
    main()
