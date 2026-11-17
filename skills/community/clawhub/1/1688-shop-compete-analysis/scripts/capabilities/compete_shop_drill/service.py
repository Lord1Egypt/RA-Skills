#!/usr/bin/env python3
"""竞店结构下钻服务

一次调用完成竞店分析 Step 3~4 的核心指标对比与四维结构下钻（本店 vs 单个竞店）：
0. 核心指标双列对比（getCompeteShopCoreIndex，流量/搜索/交易/买家 + 排名/上新）
1. 热销商品 TOP（topItmList，双列）
2. 成交价格带 GMV 占比（tradeAmountRange，双列）
3. 引流搜索词对比（inputShopKey 分别拉本店与竞店词榜后做交/差集与落后词计算）
4. 买家结构六维（shopBuyerAnalysis：byr/sex/city/class_type/cgdj/fgl）

前置约束：目标竞店 memberId 必须已在本店竞店监控清单内（否则网关返 1001），
memberId 应取自 compete_shop_analysis 输出的 industryRank / monitor 清单。
"""

from concurrent.futures import ThreadPoolExecutor

from _compete import (compete_query, val, fix_text, offer_id_of,
                      date_range_for)
from _errors import ParamError, ServiceError

_VALID_DATE_TYPE = ("RECENT_7", "RECENT_30")

# 指数脱敏占位常量：真实值过小时后端返回固定 magic，不可参与排序/比率计算
_MAGIC = 0.9527275047730654

_BUYER_SCENES = (
    ("byr", "新老客"),
    ("sex", "性别"),
    ("city", "城市TOP10"),
    ("class_type", "买家身份"),
    ("cgdj", "采购等级"),
    ("fgl", "回头率"),
)


def _clean_index(x):
    """脱敏 magic 归一为 None，调用方据此展示为「脱敏/–」并跳过计算"""
    if isinstance(x, (int, float)) and abs(x - _MAGIC) < 1e-6:
        return None
    return x


def _common_params(cate_id, cate_level, date_type, date_range):
    return {"dateType": date_type, "dateRange": date_range,
            "cateId": cate_id, "cateLevel": cate_level, "device": "ALL"}


def _my_member_id():
    info = compete_query("compete/competeShop/getMyShopInfo", {}) or {}
    mid = info.get("会员ID") or info.get("memberId")
    if not mid:
        raise ServiceError("获取本店信息失败，无法确定本店会员ID")
    return mid, info


def _core_index(base, member_id):
    return compete_query("compete/competeShop/getCompeteShopCoreIndex",
                         dict(base, memberId1=member_id, memberId2="null")) or {}


def _top_items(base, member_id):
    return compete_query("compete/competeShop/topItmList",
                         dict(base, memberId1=member_id, memberId2="null",
                              tabFlag="payOrdAmtIndex")) or {}


def _price_range(base, member_id):
    return compete_query("compete/competeShop/tradeAmountRange",
                         dict(base, memberId1=member_id, memberId2="null")) or {}


def _shop_keywords(base, member_id):
    return compete_query("compete/competeShop/inputShopKey",
                         dict(base, memberId=member_id, flowSourceType=1)) or []


def _buyer_scene(base, member_id, scence):
    params = {k: v for k, v in base.items() if k != "cateLevel"}
    params.update({"scenceName": scence, "memberId1": member_id,
                   "memberId2": "null"})
    return compete_query("compete/competeShop/shopBuyerAnalysis",
                         params) or {}


def _parse_core_index(raw, my_member_id):
    """核心指标双列：返回为并列数组，用会员ID数组定位本店/竞店索引，不假设顺序"""
    if not isinstance(raw, dict) or not raw.get("会员ID"):
        return None
    ids = raw.get("会员ID") or []
    try:
        my_i = ids.index(my_member_id)
    except ValueError:
        my_i = 0
    cp_i = 1 - my_i if len(ids) > 1 else None

    def at(key, i):
        arr = raw.get(key) or []
        return arr[i] if i is not None and i < len(arr) else None

    metrics = []
    for name, crc_key in (("流量指数", "流量增长幅度"), ("搜索指数", None),
                          ("交易指数", "交易增长幅度"), ("买家指数", None)):
        my_v = _clean_index(at(name, my_i))
        cp_v = _clean_index(at(name, cp_i))
        metrics.append({
            "name": name, "my": my_v, "competitor": cp_v,
            # 本店相对竞店的领先幅度（正=领先）；任一侧脱敏时不计算
            "myLeadRate": (my_v / cp_v - 1) if my_v and cp_v else None,
            "myCrc": at(crc_key, my_i) if crc_key else None,
            "competitorCrc": at(crc_key, cp_i) if crc_key else None,
        })
    return {
        "date": at("时间", my_i),
        "metrics": metrics,
        "cateTradeRank": {"my": at("按交易量排行", my_i),
                          "competitor": at("按交易量排行", cp_i)},
        "newItemCnt": {"my": at("上新商品数", my_i),
                       "competitor": at("上新商品数", cp_i)},
    }


def _fmt_item_row(row, rank):
    item = row.get("item") or {}
    offer_id = offer_id_of(row)
    return {
        "rank": rank,
        "offerId": offer_id,
        # 汉化会误伤标题正文（UV400→访客数400），还原后仍建议以 offerId/链接为准
        "title": fix_text(item.get("商品名称") or item.get("offerTitle")),
        "minPrice": item.get("minPrice"),
        "maxPrice": item.get("maxPrice"),
        "detailUrl": item.get("detailurl") or item.get("detailUrl")
                     or (f"https://detail.1688.com/offer/{offer_id}.html" if offer_id else None),
        "isAdServing": val(row, "isAdServing"),
        "uvIndex": _clean_index(val(row, "流量指数")),
        "uvIndexCrc": val(row, "流量指数", "cycleCrc"),
        "tradeIndex": _clean_index(val(row, "交易指数")),
        "tradeIndexCrc": val(row, "交易增长幅度") if not isinstance(
            row.get("交易指数"), dict) else val(row, "交易指数", "cycleCrc"),
    }


def _parse_items(raw, top):
    return {
        "myShop": [_fmt_item_row(r, i) for i, r in
                   enumerate((raw.get("myshop") or [])[:top], 1)],
        "competitor": [_fmt_item_row(r, i) for i, r in
                       enumerate((raw.get("firstShop") or [])[:top], 1)],
    }


def _parse_price_range(raw):
    """价格带双列：以双方价格档的并集为行（本店无成交时 my 为空数组，
    若只遍历 my 会把竞店数据全部丢掉）；价格档颜粒度随类目变化，不可写死"""
    my_map, cp_map, order = {}, {}, []
    for side, target in (("my", my_map), ("first", cp_map)):
        for r in raw.get(side) or []:
            seg = val(r, "价格段")
            if seg is None:
                continue
            target[seg] = val(r, "gmvRate")
            if seg not in order:
                order.append(seg)
    return [{"range": seg,
             "myRate": my_map.get(seg) or 0,
             "competitorRate": cp_map.get(seg) or 0} for seg in order]


def _kw_map(rows):
    m = {}
    for r in rows if isinstance(rows, list) else []:
        kw = fix_text(val(r, "关键词"))
        if not kw:
            continue
        m[kw] = {
            "rank": r.get("orderNum"),
            "uvIndex": _clean_index(val(r, "流量指数")),
            "uvIndexCrc": val(r, "流量指数", "cycleCrc"),
            "tradeIndex": _clean_index(val(r, "交易指数")),
        }
    return m


def _parse_keywords(my_rows, cp_rows, top):
    my_m, cp_m = _kw_map(my_rows), _kw_map(cp_rows)
    both = set(my_m) & set(cp_m)

    def top_list(m, mark_set):
        keys = sorted(m, key=lambda k: m[k]["rank"] or 10 ** 9)[:top]
        return [dict(m[k], keyword=k, shared=(k in mark_set)) for k in keys]

    # 双方共有、本店流量指数落后的词（脱敏值不参与），按绝对差距降序
    behind = []
    for k in both:
        mu, cu = my_m[k]["uvIndex"], cp_m[k]["uvIndex"]
        if mu is not None and cu is not None and cu > mu:
            behind.append({"keyword": k, "myUvIndex": mu, "competitorUvIndex": cu,
                           "gapRate": (cu / mu - 1) if mu else None})
    behind.sort(key=lambda x: x["competitorUvIndex"] - x["myUvIndex"], reverse=True)

    # 仅竞店布局、本店缺失的词，按竞店流量指数降序
    missing = sorted(
        [dict(cp_m[k], keyword=k) for k in set(cp_m) - set(my_m)
         if cp_m[k]["uvIndex"] is not None],
        key=lambda x: -x["uvIndex"])

    return {
        "myTotal": len(my_m), "competitorTotal": len(cp_m),
        "bothCount": len(both),
        "myOnlyCount": len(set(my_m) - set(cp_m)),
        "competitorOnlyCount": len(set(cp_m) - set(my_m)),
        "behindCount": len(behind), "missingCount": len(missing),
        "myTop": top_list(my_m, cp_m.keys()),
        "competitorTop": top_list(cp_m, my_m.keys()),
        "behindWords": behind[:top],       # 候选「买词」清单：已布局但流量落后
        "missingWords": missing[:top],     # 候选「加标题」清单：完全未布局
    }


def _parse_buyer(results):
    out = {}
    for scence, label in _BUYER_SCENES:
        raw = results.get(scence) or {}
        comp = {r.get("scenceValue"): r.get("scoreRate")
                for r in raw.get("first") or []}
        rows = []
        for r in sorted(raw.get("my") or [], key=lambda x: x.get("行业实时排名")
                        or x.get("rank") or 0):
            sv = r.get("scenceValue")
            rows.append({"name": sv, "myRate": r.get("scoreRate"),
                         "competitorRate": comp.get(sv)})
        # 竞店独有的维度值（如城市 TOP10 双方不重合的部分）补到末尾
        my_names = {r["name"] for r in rows}
        for sv, rate in comp.items():
            if sv not in my_names:
                rows.append({"name": sv, "myRate": None, "competitorRate": rate})
        out[scence] = {"label": label, "rows": rows}
    return out


def drill_compete_shop(member_id: str, cate_id, cate_level: int = 1,
                       date_type: str = "RECENT_7", top: int = 10) -> dict:
    """竞店四维结构下钻：并发拉取商品/价格带/引流词/买家结构并解析为扁平结构。

    Args:
        member_id:  目标竞店会员ID（必须已在本店竞店监控清单内）
        cate_id:    类目ID（必须来自 compete_category）
        cate_level: 类目层级，需与 cate_id 同层级
        date_type:  RECENT_7 / RECENT_30
        top:        商品榜/词榜各取前 N 条，默认 10

    Returns:
        含 params / topItems / priceRange / keywords / buyer 五块的结果字典
    """
    if not member_id:
        raise ParamError("member_id 不能为空，请从 compete_shop_analysis 的"
                         "行业榜/监控清单中选取已监控竞店")
    if not cate_id:
        raise ParamError("cateId 不能为空，请先调用 compete_category 获取合法类目")

    date_type = (date_type or "RECENT_7").upper()
    if date_type not in _VALID_DATE_TYPE:
        raise ParamError(f"date_type 仅支持 {' / '.join(_VALID_DATE_TYPE)}，收到 {date_type}")

    date_range = date_range_for(date_type)
    base = _common_params(cate_id, cate_level, date_type, date_range)

    # 本店 memberId 是本店词榜的必要入参，先取再并发其余 10 个接口
    my_member_id, _ = _my_member_id()

    with ThreadPoolExecutor(max_workers=5) as pool:
        f_core = pool.submit(_core_index, base, member_id)
        f_items = pool.submit(_top_items, base, member_id)
        f_price = pool.submit(_price_range, base, member_id)
        f_my_kw = pool.submit(_shop_keywords, base, my_member_id)
        f_cp_kw = pool.submit(_shop_keywords, base, member_id)
        f_buyer = {s: pool.submit(_buyer_scene, base, member_id, s)
                   for s, _label in _BUYER_SCENES}

        core_raw = f_core.result()
        items_raw = f_items.result()
        price_raw = f_price.result()
        my_kw_raw = f_my_kw.result()
        cp_kw_raw = f_cp_kw.result()
        buyer_raw = {s: f.result() for s, f in f_buyer.items()}

    items = _parse_items(items_raw, top)
    price_range = _parse_price_range(price_raw)
    keywords = _parse_keywords(my_kw_raw, cp_kw_raw, top)
    buyer = _parse_buyer(buyer_raw)
    core_index = _parse_core_index(core_raw, my_member_id)

    # 子接口级容错：单个维度无数据不应拘毁整次下钻（实测存在“同一类目下
    # 部分竞店没有商品榜数据、其余竞店正常”的情况），改为标记缺失维度
    warnings = []
    if not items["competitor"]:
        warnings.append("竞店热销商品无数据（该竞店近期无商品榜，或网关瞬时降级）")
    if not price_range:
        warnings.append("成交价格带无数据")
    if not keywords["competitorTop"]:
        warnings.append("竞店引流词榜无数据")
    if core_index is None:
        warnings.append("核心指标对比无数据")

    # 只有全部维度都空才判为真正失败（参数/监控错或网关整体降级）
    if len(warnings) == 4 and not any(v["rows"] for v in buyer.values()):
        raise ServiceError(
            f"竞店下钻全维度无数据（memberId={member_id}）。"
            "请确认该竞店已在监控清单内（compete_shop_analysis 的 monitor 输出）、"
            "cateId/cateLevel 层级配对正确；若均无问题则可能是网关暂时降级，稍后重试"
        )

    return {
        "params": {"memberId": member_id, "myMemberId": my_member_id,
                   "cateId": cate_id, "cateLevel": cate_level,
                   "dateType": date_type, "dateRange": date_range},
        # 缺失维度清单：Agent 需向用户如实说明哪些对比维度本次拿不到
        "warnings": warnings,
        "coreIndex": core_index,
        "topItems": items,
        "priceRange": price_range,
        "keywords": keywords,
        "buyer": buyer,
    }
