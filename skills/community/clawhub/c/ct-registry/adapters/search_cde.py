#!/usr/bin/env python3
"""search_cde.py - China CDE search / 中国 CDE 检索.

CDE has NO official API and uses JS anti-bot. / CDE 无官方 API，含 JS 反爬。
Opt-in fast path: 3rd-party commercial API via --api-key (data goes through 3rd party, ~1-3s).
Default path: Coze workflow via search_ictrp.py (no key needed, ~15-60s).
"""
import argparse
import json
import urllib.parse
import urllib.request

# dxy 商业接口返回的字段名 -> norm_cde() 已知的字段名（字段映射层）
# dxy 接口文档字段：https://api.dxy.cn/open/medical/cde.clinical.trials.basic.info
_DXY_FIELD_MAP = {
    "nctNumber": "登记号",
    "drugName": "药物名称",
    "indication": "适应症",
    "testStatus": "试验状态",
    "popularTitle": "试验通俗题目",
    "professionalTitle": "试验专业题目",
    "appliers": "申请人名称",
    "phase": "试验分期",
    "enrollment": "实际入组总人数",
    "firstPosted": "首次公示信息日期",
    "startDate": "首次公示信息日期",
    "project_id": "project_id",
    "registration_no": "登记号",
    "main_id": "登记号",
    "public_title": "试验通俗题目",
    "who_title": "试验通俗题目",
    "health_condition": "适应症",
    "recruitment_status": "试验状态",
    "sponsor": "申请人名称",
}


def _map_dxy_record(rec):
    """Map a dxy API record's field names to the names norm_cde() expects.

    norm_cde() already handles a tolerant multi-shape mapping (LIST/DETAIL/WHO-style).
    This layer translates dxy-specific keys into that shared vocabulary so the
    downstream normalize step works unchanged for both the Coze-workflow path and
    the dxy direct-API path.
    """
    if not isinstance(rec, dict):
        return rec
    mapped = {}
    for k, v in rec.items():
        if v is None or v == "" or v == "null":
            continue
        target = _DXY_FIELD_MAP.get(k, k)
        # 同目标字段保留首次出现的值（不覆盖）
        if target not in mapped:
            mapped[target] = v
    # 保留原始 raw 字段供溯源
    mapped["_raw_dxy"] = rec
    return mapped


def search_api(api_key, drug=None, indication=None, regno=None, keyword=None, max_n=20):
    # 丁香园商业接口（第三方，需 key）—— opt-in only.
    url = "https://api.dxy.cn/open/medical/cde.clinical.trials.basic.info"
    params = {"pageSize": max_n, "pageNum": 1}
    if drug:
        params["drugName"] = drug
    if indication:
        params["indication"] = indication
    if regno:
        params["nctNumber"] = regno
    if keyword:
        # dxy 接口支持通用关键词搜索（fallback 到 keyword 字段）
        params["keyword"] = keyword
    req = urllib.request.Request(url + "?" + urllib.parse.urlencode(params),
                                 headers={"User-Agent": "ct-registry/0.1", "apikey": api_key})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def search_playwright(drug=None, indication=None, max_n=20):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit("Playwright 未安装：pip install playwright && playwright install chromium")
    results = []
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        pg = b.new_page()
        pg.goto("https://www.chinadrugtrials.org.cn/clinicaltrials.prosearch.dhtml", timeout=30000)
        if drug:
            # 选择器需按站点实际 DOM 适配（TODO: 实测后固化）
            pg.fill('input[placeholder*="药品"]', drug)
        pg.click("text=查询")
        pg.wait_for_timeout(3000)
        rows = pg.query_selector_all(".search-result-item")
        for row in rows[:max_n]:
            results.append({"popularTitle": row.inner_text()})
        b.close()
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--drug")
    ap.add_argument("--indication")
    ap.add_argument("--regno")
    ap.add_argument("--q", help="通用关键词（中英文均可）")
    ap.add_argument("--max", type=int, default=20, help="每页返回条数 (default 20)")
    ap.add_argument("--api-key", help="第三方 CDE API key (opt-in; 数据经第三方，走商业接口 ~1-3s)")
    ap.add_argument("--out", default="cde.json")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args()

    if not args.run:
        print("[cde][PREVIEW] add --run. With --api-key: 商业接口直连 (~1-3s).")
        print("[cde][PREVIEW] Without --api-key: Coze workflow 代理 (~15-60s, 需 token).")
        return

    if args.api_key:
        data = search_api(args.api_key, args.drug, args.indication, args.regno,
                          keyword=args.q, max_n=args.max)
        raw_recs = data.get("result", {}).get("data", []) if isinstance(data, dict) else []
        # 字段映射：dxy 字段名 -> norm_cde() 已知字段名
        recs = [_map_dxy_record(r) for r in raw_recs]
    else:
        recs = search_playwright(args.drug, args.indication)
    out = {"source": "CDE", "records": recs}
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"[cde] {len(recs)} records -> {args.out}")


if __name__ == "__main__":
    main()
