#!/usr/bin/env python3
"""买家流失商品分析服务（dataSource=ITEM，/item/customerLoss）

把「裸调全景 + 发散多品佐证」的多次调用逻辑沉淀为一条命令：
1. 默认裸调（不传 item_id）：拿流失商品总数 + 50 条 ID 列表 + 随机一品的完整对比
2. 从「流失商品ID列表」发散性取样 N 个品（默认 5），并发带 item_id 再查
3. 多品结果交叉汇总：价格对比（±30% 可比性标记，不可比品不计入便宜占比）、
   竞对更便宜占比、回头率对比；items 按流失严重度排序（流失规模主键、流失宽度次键）
4. 双侧「商品的属性」原样透出，供 Agent 做「同类归口」筛选（先归口再比价）

结论解读仍由 Agent 基于返回的 items/summary 完成；本服务只做
真实调用与事实汇总，不做主观归因。
"""

import json
from concurrent.futures import ThreadPoolExecutor

from _http import call_tool
from _const import TOOL_QUERY_SHOP_DATA
from _errors import ParamError, ServiceError

_API_PATH = "/item/customerLoss"
_IMG_PREFIX = "https://cbu01.alicdn.com/"

# 价差超过该比例不属同层竞品，不可直接对标
_PRICE_GAP_LIMIT = 0.30


def _call(item_id=None):
    """调一次 /item/customerLoss，返回 (最内层中文dict或None, errorMsg或None)"""
    params = {}
    if item_id is not None:
        params["item_id"] = str(item_id)
    raw = call_tool(TOOL_QUERY_SHOP_DATA, {"dataSource": "ITEM", "apiPath": _API_PATH,
                                           "params": params})
    # call_tool 已剥信封并返回最内层中文 dict（无 data 包装）；字符串则二次解析
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except (ValueError, TypeError):
            raw = None
    inner = raw if isinstance(raw, dict) else None
    # 静默返空：inner 为 None（无流失数据）；errorMsg 若存在则透传
    err = (inner or {}).get("errorMsg") or (inner or {}).get("msgInfo")
    return inner, err


def _to_int(x, default=0):
    """浏览买家数/浏览次数是字符串型数字"""
    try:
        return int(x)
    except (TypeError, ValueError):
        return default


def _to_price(x):
    """价格是字符串（如 \"60.00\"），解析为 float；失败返 None"""
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _img(path):
    return (_IMG_PREFIX + path) if isinstance(path, str) and path else None


def _parse_detail(data, source):
    """把一次调用的中文 key 返回解析为结构化记录（缺失字段一律 get）"""
    loss = data.get("买家流失情况") or {}
    mine = data.get("我的商品") or {}
    rival = data.get("竞对商品") or {}
    myshop = data.get("我的店铺") or {}
    rivalshop = data.get("竞对店铺") or {}

    my_price = _to_price(mine.get("商品最低价"))
    rival_price = _to_price(rival.get("商品最低价"))
    gap = None
    comparable = None
    if my_price and rival_price:
        gap = round((rival_price - my_price) / my_price, 4)
        comparable = abs(gap) <= _PRICE_GAP_LIMIT

    return {
        "itemId": str(loss.get("商品ID") or mine.get("商品ID") or ""),
        "source": source,
        "selectMode": loss.get("选取方式"),
        "hasRival": bool(rival),
        "lossDetail": {
            "browsedBuyerCount": _to_int(loss.get("浏览过该商品的买家数")),
            "browseCount": _to_int(loss.get("该商品被浏览次数")),
            "rivalOfferCount": loss.get("买家转而下单的竞对商品数"),
            "rivalOfferIds": loss.get("买家转而下单的竞对商品ID列表") or [],
            "comparedRivalId": loss.get("本次对比的竞对商品ID"),
        },
        "myItem": {
            "title": mine.get("商品标题"),
            "attributes": mine.get("商品的属性") or [],  # 「键:值」数组，供同类归口筛选
            "minPrice": my_price,
            "maxPrice": _to_price(mine.get("商品最高价")),
            "img": _img(mine.get("商品主图")),
        },
        "rivalItem": {
            "itemId": str(rival.get("商品ID") or loss.get("本次对比的竞对商品ID") or ""),
            "title": rival.get("商品标题"),
            "attributes": rival.get("商品的属性") or [],
            "minPrice": rival_price,
            "maxPrice": _to_price(rival.get("商品最高价")),
            "img": _img(rival.get("商品主图")),
        } if rival else None,
        "myShop": {
            "repeatRate": myshop.get("店铺老客回头率"),
            "wangwangRate": myshop.get("店铺旺旺响应率"),
            "companyArea": myshop.get("企业面积"),
            "brandCount": myshop.get("企业拥有品牌数量"),
            "foundDate": myshop.get("企业成立日期"),
        },
        "rivalShop": {
            "repeatRate": rivalshop.get("店铺老客回头率"),
            "wangwangRate": rivalshop.get("店铺旺旺响应率"),
            "companyArea": rivalshop.get("企业面积"),
            "brandCount": rivalshop.get("企业拥有品牌数量"),
            "foundDate": rivalshop.get("企业成立日期"),
        } if rivalshop else None,
        "priceGap": {"mine": my_price, "rival": rival_price,
                     "gapPct": gap, "comparable": comparable}
                    if rival else None,
    }


def _summarize(items):
    """多品交叉汇总（只做事实统计，归因留给 Agent）"""
    with_data = [x for x in items if x["hasData"]]
    with_rival = [x for x in with_data if x["hasRival"]]
    gaps = [x["priceGap"] for x in with_rival
            if x.get("priceGap") and x["priceGap"]["gapPct"] is not None]
    # 价差超 ±30% 不属同层竞品，不计入便宜/贵占比（先归口再比价）
    comparable_gaps = [g for g in gaps if g["comparable"] is not False]
    rival_cheaper = [g for g in comparable_gaps if g["gapPct"] < -0.05]
    my_cheaper = [g for g in comparable_gaps if g["gapPct"] > 0.05]
    incomparable = [g for g in gaps if g["comparable"] is False]

    # 双侧回头率/旺旺响应率都有值时做直观对比
    shop_signals = []
    for x in with_rival:
        ms, rs = x.get("myShop") or {}, x.get("rivalShop") or {}
        if ms.get("repeatRate") and rs.get("repeatRate"):
            shop_signals.append({"itemId": x["itemId"],
                                 "myRepeatRate": ms["repeatRate"],
                                 "rivalRepeatRate": rs["repeatRate"]})
    return {
        "probed": len(items),
        "withData": len(with_data),
        "withRival": len(with_rival),
        "noData": [x["itemId"] for x in items if not x["hasData"]],
        "priceCompared": len(comparable_gaps),
        "rivalCheaper": len(rival_cheaper),
        "myCheaper": len(my_cheaper),
        "incomparablePriceGap": len(incomparable),
        "repeatRateCompare": shop_signals,
    }


def analyze_customer_loss(item_ids=None, sample_n=3):
    """裸调全景 + 发散取样佐证 + 交叉汇总。

    Args:
        item_ids:  可选，指定要下钻的流失商品ID列表（本店商品，纯数字）；
                   不传则自动从返回的「流失商品ID列表」取样
        sample_n:  发散取样品数，默认 5（不含裸调随机命中的那一个）
    """
    if sample_n < 0 or sample_n > 20:
        raise ParamError("sample_n 应在 0~20 之间")

    # ① 裸调全景
    overview_data, overview_err = _call()
    if overview_data is None:
        raise ServiceError(
            "裸调无流失数据：" + (overview_err or "该店铺近期没有出现买家流失"))

    total = overview_data.get("流失商品总数")
    id_list = [str(i) for i in (overview_data.get("流失商品ID列表") or [])]
    warnings = []

    items = []
    random_rec = _parse_detail(overview_data, source="random")
    random_rec["hasData"] = True
    items.append(random_rec)

    # ② 确定发散取样品：指定优先，否则从 ID 列表取样（排除已对比的随机品）
    if item_ids:
        samples = [str(i) for i in item_ids]
    else:
        probed = {random_rec["itemId"]}
        samples = [i for i in id_list if i not in probed][:sample_n]

    # ③ 并发逐品下钻
    def probe(iid):
        try:
            data, err = _call(item_id=iid)
        except Exception as e:  # 单品失败不阻断整体
            return {"itemId": iid, "source": "specified" if item_ids else "sampled",
                    "hasData": False, "errorMsg": str(e)}
        if data is None:
            return {"itemId": iid, "source": "specified" if item_ids else "sampled",
                    "hasData": False, "errorMsg": err or "近期没有出现买家流失"}
        rec = _parse_detail(data, source="specified" if item_ids else "sampled")
        rec["hasData"] = True
        rec["itemId"] = rec["itemId"] or iid
        return rec

    if samples:
        with ThreadPoolExecutor(max_workers=min(len(samples), 8)) as pool:
            items.extend(list(pool.map(probe, samples)))

    # 按流失严重度排序：主键「浏览过该商品的买家数」（流失规模），
    # 次键「买家转而下单的竞对商品数」（流失宽度）；无数据品沉底
    def _sev(x):
        d = x.get("lossDetail") or {}
        return (d.get("browsedBuyerCount") or 0,
                _to_int(d.get("rivalOfferCount")))
    items.sort(key=_sev, reverse=True)

    if total and id_list and len(id_list) < total:
        warnings.append(f"流失商品ID列表仅前 {len(id_list)} 条"
                        f"（总数 {total}，按商品ID升序截断）")

    return {
        "overview": {
            "totalLossItems": total,
            "lossItemIdList": id_list,
            "randomPicked": random_rec["itemId"],
        },
        "items": items,
        "summary": _summarize(items),
        "warnings": warnings,
    }
