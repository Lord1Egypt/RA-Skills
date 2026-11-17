# /// script
# requires-python = ">=3.11"
# dependencies = ["aiohttp"]
# ///
# -*- coding: utf-8 -*-
"""买手全网最低价一键查询

流程: 关键词搜索(source=0 全平台) -> 按券后价升序 -> 对最便宜的 top N 调详情接口取购买链接。
输出: 默认 Markdown 表格（商品名称/平台/店铺/标价/券后价/券/月销/购买链接）；--json 输出原始数组。

用法:
    uv run best_price.py "米家空调 新风Pro 1.5匹"
    uv run best_price.py "关键词" --top 5 --json
    uv run best_price.py "关键词" --must-contain 小米官方旗舰店   # 标题过滤杂音
"""
import argparse
import asyncio
import io
import json
import os
import sys

import aiohttp

if sys.stdout.encoding.upper() != "UTF-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

INVITE_CODE = os.getenv("MAISHOU_INVITE_CODE") or "7509789"
OPENID = os.getenv("MAISHOU_OPENID") or "e28b49b39e41f3adbee447348861e9f7"

HEADERS = {
    aiohttp.hdrs.ACCEPT: "application/json",
    aiohttp.hdrs.REFERER: "https://hnbc018.kuaizhan.com/",
    aiohttp.hdrs.USER_AGENT: "MaiShouApp/3.7.7 (iPhone; iOS 26.3; Scale/3.00)",
    "openid": OPENID,
    "version": "3.7.7.2",
}
SOURCE_NAMES = {"1": "淘宝/天猫", "2": "京东", "3": "拼多多", "4": "苏宁",
                "5": "唯品会", "7": "抖音", "8": "快手", "0": "全部"}


async def search(session, keyword, source="0"):
    resp = await session.post(
        "https://appapi.maishou88.com/api/v1/homepage/searchList",
        data={
            "isCoupon": 0, "keyword": str(keyword), "openid": OPENID,
            "order": "desc", "page": 1, "pddListId": "", "sort": "",
            "sourceType": str(source), "user_id": "",
        },
    )
    data = await resp.json(encoding="utf-8-sig") or {}
    return data.get("data") or []


async def detail_link(session, goods_id, source):
    """详情 + 购买短链；失败返回 ("", "")"""
    params = {
        "goodsId": str(goods_id), "sourceType": str(source),
        "inviteCode": INVITE_CODE, "supplierCode": "", "activityId": "",
        "isShare": "1", "token": "",
    }
    try:
        await session.post("https://appapi.maishou88.com/api/v3/goods/detail",
                           json={**params, "keyword": "", "usageScene": 5})
        resp = await session.post(
            "https://msapi.maishou88.com/api/v1/share/getTargetUrl",
            json={**params, "isDirectDetail": 0})
        info = (await resp.json(encoding="utf-8-sig") or {}).get("data") or {}
        return info.get("appUrl") or info.get("schemaUrl") or "", info.get("kl") or ""
    except Exception:
        return "", ""


def to_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


async def run(keyword, source="0", top=3, must_contain="", min_price=0.0, max_price=0.0, as_json=False):
    async with aiohttp.ClientSession(headers=HEADERS) as s:
        rows = await search(s, keyword, source)
        items = []
        for v in rows:
            price = to_float(v.get("actualPrice"))
            if price is None or price <= 0:
                continue
            title = v.get("title") or ""
            if must_contain and must_contain not in title:
                continue
            if price < min_price or (max_price and price > max_price):
                continue
            items.append({
                "商品名称": title,
                "平台": SOURCE_NAMES.get(str(v.get("sourceType")), str(v.get("sourceType"))),
                "店铺": v.get("shopName") or "",
                "标价": to_float(v.get("originalPrice")),
                "券后价": price,
                "优惠券": to_float(v.get("couponPrice")) or 0,
                "月销": str(v.get("monthSales") or ""),
                "_goodsId": v.get("goodsId"),
                "_source": str(v.get("sourceType")),
            })
        items.sort(key=lambda x: x["券后价"])
        picked = items[:max(1, top)]
        for it in picked:  # 串行取链接，避免限流
            link, kl = await detail_link(s, it["_goodsId"], it["_source"])
            it["购买链接"] = link
            it["淘口令"] = kl
            await asyncio.sleep(1)

    for it in picked:
        it.pop("_goodsId", None)
        it.pop("_source", None)

    if as_json:
        print(json.dumps(picked, ensure_ascii=False, indent=2))
        return
    if not picked:
        print("未找到匹配商品，可放宽 --must-contain 或换关键词重试")
        return
    print(f"关键词「{keyword}」全网最低价 Top {len(picked)}（买手券后价口径，含券不含国补）：\n")
    print("| # | 商品名称 | 平台 | 店铺 | 券后价 | 标价 | 券 | 月销 | 购买链接 |")
    print("|---|---|---|---|---|---|---|---|---|")
    for i, it in enumerate(picked, 1):
        name = it["商品名称"][:38] + ("…" if len(it["商品名称"]) > 38 else "")
        link = it["购买链接"] or it["淘口令"] or "（取链失败）"
        print(f"| {i} | {name} | {it['平台']} | {it['店铺']} | ¥{it['券后价']:g} | "
              f"¥{it['标价']:g} | ¥{it['优惠券']:g} | {it['月销']} | {link} |")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("keyword", help="搜索关键词，越具体越准（品牌+型号+规格）")
    ap.add_argument("--source", default="0", help="0全部 1淘宝/天猫 2京东 3拼多多 4苏宁 5唯品会 7抖音 8快手")
    ap.add_argument("--top", type=int, default=3, help="输出最低价前 N 名并取购买链接（默认 3）")
    ap.add_argument("--must-contain", default="", help="标题必须包含的子串，用于过滤配件/杂音")
    ap.add_argument("--min-price", type=float, default=0.0, help="券后价下限，过滤低价配件")
    ap.add_argument("--max-price", type=float, default=0.0, help="券后价上限（0=不限）")
    ap.add_argument("--json", action="store_true", help="输出 JSON 而非表格")
    args = ap.parse_args()
    asyncio.run(run(args.keyword, args.source, args.top, args.must_contain, args.min_price, args.max_price, args.json))


if __name__ == "__main__":
    main()
