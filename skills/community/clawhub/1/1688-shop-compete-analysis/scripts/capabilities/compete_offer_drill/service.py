#!/usr/bin/env python3
"""竞品（商品级）结构下钻服务

一次调用完成竞品分析的三维下钻（本店商品 vs 1~2 个竞品）：
1. 商品引流搜索词榜（seachofferKey，三方词榜 + 落后词/缺失词）
2. 流量来源对比（ipvUvSourceV2，渠道树上的真实访客数与支付金额双列）
3. 商品级买家结构（competeOffer/shopBuyerAnalysis 七维，支持三方）

商品来源：**竞品侧**必须来自竞品监控池（getCompeteList，下钻 gate 只卡竞品）；
**本店侧**不受监控约束，优先取同款商品清单（sameProductOffer，即“有同款竞品
可比对的自家商品池”）+ 监控池内的本店商品合并去重；未指定商品时自动挑选
交易水平最高的竞品，并优先匹配同叶子类目的本店商品作为对位。
"""

from concurrent.futures import ThreadPoolExecutor

from _compete import (compete_query, val, fix_text, offer_id_of,
                      member_id_of, date_range_for)
from _errors import ParamError, ServiceError

_VALID_DATE_TYPE = ("RECENT_7", "RECENT_30")

# 指数脱敏占位常量：真实值过小时后端返固定 magic，不可参与排序/比率计算
_MAGIC = 0.9527275047730654

# 商品级买家维度（不支持店铺级的 byr/fgl；省份须用页面拼错的 provice）
_BUYER_SCENES = (
    ("provice", "省份"),
    ("city", "城市"),
    ("sex", "性别"),
    ("class_type", "买家身份"),
    ("cgdj", "采购等级"),
    ("scence_uv", "访客场景来源"),
    ("scence_trd", "成交场景来源"),
)
# 场景类维度是「各场景独立占比」，同侧累加可能 >1，禁止当互斥占比归一化
_NON_EXCLUSIVE = ("scence_uv", "scence_trd")


def _clean(x):
    if isinstance(x, (int, float)) and abs(x - _MAGIC) < 1e-6:
        return None
    return x


def _pick(row, *keys):
    """按候选 key 依次取值（兼容汉化 key 与英文 key、{value} 包装）"""
    for k in keys:
        if k in (row or {}):
            v = row[k]
            return v.get("value") if isinstance(v, dict) else v
    return None


def _my_shop():
    info = compete_query("compete/competeShop/getMyShopInfo", {}) or {}
    mid = info.get("会员ID") or info.get("memberId")
    if not mid:
        raise ServiceError("获取本店信息失败，无法确定本店会员ID")
    return mid


def _monitor_offers(cate_id, cate_level, date_type, date_range):
    """竞品监控池：本店商品与已监控竞品同在此清单内"""
    raw = compete_query("compete/competeOffer/getCompeteList", {
        "dateType": date_type, "dateRange": date_range,
        "cateId": cate_id, "cateLevel": cate_level, "device": "ALL",
        "orderBy": "payOrdAmtIndex", "order": "desc",
        "page": 1, "pageSize": 60,
    }) or {}
    return raw.get("data") or []


def _offer_quota(cate_id):
    """竞品监控配额（尽力而为）：实测该接口经网关可能返回与监控池
    矛盾的计数（如 0/100 但池内实有商品），由调用方做一致性校验后再用"""
    try:
        return compete_query("compete/common/getOfferMonitorCntInfo",
                             {"cateId": cate_id}) or {}
    except Exception:
        return {}


def _same_product_offers(cate_id, cate_level, date_type, date_range):
    """同款商品清单：本店在该类目下有可识别同款竞品的自家商品池，
    是本店对位商品的首选来源（不受竞品监控 gate 约束）；接口异常时降级为空"""
    try:
        raw = compete_query("compete/offerDiscern/sameProductOffer/getOfferList", {
            "dateType": date_type, "dateRange": date_range,
            "cateId": cate_id, "cateLevel": cate_level,
            "pageNo": 1, "pageSize": 50,
            "orderBy": "payOrdAmtIndex", "order": "desc",
        }) or {}
        return raw.get("data") or []
    except Exception:
        return []


def _fmt_offer(row):
    item = row.get("item") or {}
    shop = row.get("shop") or {}
    return {
        "offerId": str(offer_id_of(row) or ""),
        # 汉化会误伤标题正文（UV400→访客数400），已还原
        "title": fix_text(item.get("商品名称") or item.get("offerTitle")),
        "minPrice": item.get("minPrice"),
        "maxPrice": item.get("maxPrice"),
        "leafCateId": item.get("类目ID") or item.get("categoryID"),
        "shopName": shop.get("shopName"),
        # 同款商品清单无 shop 子对象，memberId 在行级（member_id_of 兼容两种）
        "memberId": member_id_of(row),
        "uvIndex": _clean(val(row, "流量指数")),
        "tradeIndex": _clean(val(row, "交易指数")),
        "buyerIndex": _clean(val(row, "买家指数")),
        "cartIndex": _clean(val(row, "加购指数")),
        "favIndex": _clean(val(row, "收藏指数")),
    }


def _sort_key(o):
    return -(o.get("tradeIndex") or 0), -(o.get("uvIndex") or 0)


def _bigrams(title):
    """中文标题切 2-gram，用于粗略衡量两个商品是否同品类"""
    s = "".join(ch for ch in (title or "") if '\u4e00' <= ch <= '\u9fff')
    return {s[i:i + 2] for i in range(len(s) - 1)}


def _price_mid(o):
    lo, hi = o.get("minPrice"), o.get("maxPrice")
    vals = [x for x in (lo, hi) if isinstance(x, (int, float))]
    return sum(vals) / len(vals) if vals else None


def _match_my_offer(mine, rival):
    """为竞品挑选可比性最好的本店对位商品，返回 (商品, 匹配依据, 标题词重合数)。

    叶子类目是唯一可靠的品类信号，只有同叶子类目才算真正可比；
    池内无同类目商品时，降级用标题词重合 / 价位接近做近似对位，
    但不得宣称同品类（如镜架 vs 镜片的标题也会共现“高度数/近视”等词）。
    """
    same_cate = [o for o in mine
                 if o["leafCateId"] and o["leafCateId"] == rival["leafCateId"]]
    if same_cate:
        return same_cate[0], "sameLeafCate", None

    rival_grams = _bigrams(rival["title"])
    scored = [(len(_bigrams(o["title"]) & rival_grams), o) for o in mine]
    best_overlap = max((n for n, _o in scored), default=0)
    if best_overlap > 0:
        # 词重合最高者优先，同分时按交易水平（mine 已按交易降序）
        return (next(o for n, o in scored if n == best_overlap),
                "titleOverlap", best_overlap)

    rival_mid = _price_mid(rival)
    priced = [o for o in mine if _price_mid(o) is not None]
    if rival_mid is not None and priced:
        return (min(priced, key=lambda o: abs(_price_mid(o) - rival_mid)),
                "priceProximity", 0)

    return mine[0], "tradeIndex", 0


def _resolve_offers(pool, mine_extra, my_member_id, offer_id, offer_id2, my_offer_id):
    """确定对位商品：竞品侧 1~2 个（必须在监控池内）；本店侧 1 个，
    候选 = 同款商品清单 + 监控池内本店商品（去重），不受监控约束"""
    pool_mine = [o for o in pool if o["memberId"] == my_member_id]
    rivals = sorted([o for o in pool if o["memberId"] != my_member_id], key=_sort_key)

    # 本店候选池：同款清单优先（已按交易降序），监控池内本店商品补充去重
    mine, seen = [], set()
    for o in list(mine_extra) + pool_mine:
        if o["offerId"] and o["offerId"] not in seen:
            seen.add(o["offerId"])
            mine.append(o)
    mine.sort(key=_sort_key)
    mine_by_id = {o["offerId"]: o for o in mine}
    rival_by_id = {o["offerId"]: o for o in rivals}

    if not rivals:
        raise ServiceError(
            "竞品监控池内没有竞品商品。请先到生意参谋「竞店竞品配置」竞品 tab "
            "(https://sycm.1688.com/ms/compete/shopOfferSetting?settingType=1) "
            "添加竞品后重试"
        )

    def take_rival(oid, label):
        oid = str(oid)
        if oid in mine_by_id:
            raise ParamError(
                f"{label} {oid} 是本店商品，应作为 --my_offer_id 传入；"
                f"竞品参数请传竞店的商品ID"
            )
        o = rival_by_id.get(oid)
        if o is None:
            raise ParamError(
                f"{label} {oid} 不在竞品监控池内（下钻会返 1001）。"
                f"当前池内竞品 {len(rivals)} 个，可先不传该参数由系统自动选取，"
                f"或到生意参谋竞品配置页添加后重试"
            )
        return o

    if offer_id:
        rival1 = take_rival(offer_id, "指定的竞品商品")
        auto_rival = False
    else:
        rival1 = rivals[0]          # 交易水平最高的已监控竞品
        auto_rival = True

    rival2 = take_rival(offer_id2, "指定的第二个竞品商品") if offer_id2 else None
    if rival2 and rival2["offerId"] == rival1["offerId"]:
        raise ParamError("两个竞品商品ID相同，请传不同的商品")

    if my_offer_id:
        my_offer = mine_by_id.get(str(my_offer_id))
        my_offer_external = False
        if my_offer is None:
            if str(my_offer_id) in rival_by_id:
                raise ParamError(
                    f"指定的本店商品 {my_offer_id} 实为监控池内的竞品，"
                    f"应作为 --offer_id 传入"
                )
            # 候选池有页宽限制，池外本店商品照收；但网关对非本店/不存在的
            # 商品不报错而是静默返空，需在取数后做全空校验（见主流程）
            my_offer = {"offerId": str(my_offer_id), "title": None,
                        "minPrice": None, "maxPrice": None, "leafCateId": None,
                        "shopName": None, "memberId": my_member_id,
                        "uvIndex": None, "tradeIndex": None, "buyerIndex": None,
                        "cartIndex": None, "favIndex": None}
            my_offer_external = True
        auto_mine = False
        match_basis, overlap = "specified", None
    else:
        if not mine:
            raise ServiceError(
                "未能自动取到本店候选商品（同款商品清单为空且监控池内无本店商品）。"
                "请用 --my_offer_id 指定一个本店商品ID作为对位"
            )
        my_offer, match_basis, overlap = _match_my_offer(mine, rival1)
        auto_mine = True
        my_offer_external = False

    same_leaf = bool(my_offer["leafCateId"]
                     and my_offer["leafCateId"] == rival1["leafCateId"])
    return {
        "myOffer": my_offer, "rivals": [r for r in (rival1, rival2) if r],
        "autoPicked": {
            "rival": auto_rival, "myOffer": auto_mine,
            "matchBasis": match_basis,
            "sameLeafCate": same_leaf,
            # 仅同叶子类目才视为真正可比；指定商品但无类目信息时不判定
            "comparable": same_leaf or (match_basis == "specified"
                                        and my_offer["leafCateId"] is None),
            "titleOverlap": overlap,
            "myLeafCateId": my_offer["leafCateId"],
            "rivalLeafCateId": rival1["leafCateId"],
        },
        "myOfferExternal": my_offer_external,
        "poolMine": pool_mine, "mineCandidates": mine, "poolRivals": rivals,
    }


def _offer_keywords(base, offer_id):
    return compete_query("compete/competeOffer/seachofferKey",
                         dict(base, offerId=offer_id, flowSourceType=1)) or []


def _flow_source(base, my_offer_id, rival_offer_id):
    return compete_query("compete/competeOffer/ipvUvSourceV2",
                         dict(base, offerId1=my_offer_id, offerId2=rival_offer_id,
                              flowSourceType=1)) or []


def _buyer_scene(base, scence, my_offer_id, rival_ids):
    params = {k: v for k, v in base.items() if k != "cateLevel"}
    params.update({"scenceName": scence, "offerId1": my_offer_id,
                   "offerId2": rival_ids[0],
                   # 第三方对比不用时传空串（该接口空串合法，"null" 会被当成 ID）
                   "offerId3": rival_ids[1] if len(rival_ids) > 1 else ""})
    return compete_query("compete/competeOffer/shopBuyerAnalysis",
                         params) or {}


def _kw_map(rows):
    m = {}
    for r in rows if isinstance(rows, list) else []:
        w = fix_text(val(r, "关键词"))
        if not w:
            continue
        m[w] = {"rank": r.get("orderNum"),
                "uvIndex": _clean(val(r, "流量指数")),
                "uvIndexCrc": val(r, "流量指数", "cycleCrc"),
                "tradeIndex": _clean(val(r, "交易指数"))}
    return m


def _parse_keywords(my_rows, rival_rows_map, top):
    """三方词榜 + 本店相对每个竞品的落后词 / 缺失词"""
    my_m = _kw_map(my_rows)
    rivals = {oid: _kw_map(rows) for oid, rows in rival_rows_map.items()}

    def to_list(m, others):
        keys = sorted(m, key=lambda k: m[k]["rank"] or 10 ** 9)[:top]
        return [dict(m[k], keyword=k,
                     sharedWith=[o for o, om in others.items() if k in om])
                for k in keys]

    per_rival = {}
    for oid, rm in rivals.items():
        behind, missing = [], []
        for w, d in rm.items():
            mu, cu = (my_m.get(w) or {}).get("uvIndex"), d["uvIndex"]
            if w not in my_m:
                if cu is not None:
                    missing.append({"keyword": w, "rivalUvIndex": cu,
                                    "rivalTradeIndex": d["tradeIndex"]})
            elif mu is not None and cu is not None and cu > mu:
                behind.append({"keyword": w, "myUvIndex": mu, "rivalUvIndex": cu,
                               "gapRate": (cu / mu - 1) if mu else None})
        behind.sort(key=lambda x: x["rivalUvIndex"] - x["myUvIndex"], reverse=True)
        missing.sort(key=lambda x: -x["rivalUvIndex"])
        per_rival[oid] = {
            "total": len(rm),
            "sharedCount": len(set(rm) & set(my_m)),
            "behindCount": len(behind), "missingCount": len(missing),
            "top": to_list(rm, {"my": my_m}),
            "behindWords": behind[:top],    # 候选「买词」：已布局但流量落后
            "missingWords": missing[:top],  # 候选「加标题」：完全未布局
        }
    return {"myTotal": len(my_m), "myTop": to_list(my_m, rivals),
            "byRival": per_rival}


def _parse_flow_source(tree):
    """渠道树拍平为行；本店侧访客/支付无 my 前缀（网关汉化不对称）"""
    rows = []

    def walk(node, parent):
        name = _pick(node, "流量来源名称", "outerName")
        row = {
            "channel": name,
            "level": _pick(node, "来源层级", "outerLevel"),
            "parent": parent,
            "myUv": _clean(_pick(node, "访客数", "myOfferIpvUv")),
            "myPayAmt": _clean(_pick(node, "支付金额", "myOfferPayOrdAmt")),
            "myOrderBuyer": _clean(_pick(node, "my下单买家数", "myPlaceOrderByrCnt")),
            "myInquiry": _clean(_pick(node, "myInquiry指数值", "myInquiryIndex")),
            "rivalUv": _clean(_pick(node, "firstOffer访客数", "firstOfferIpvUv")),
            "rivalPayAmt": _clean(_pick(node, "firstOffer支付金额", "firstOfferPayOrdAmt")),
            "rivalOrderBuyer": _clean(_pick(node, "first下单买家数", "firstPlaceOrderByrCnt")),
            "rivalInquiry": _clean(_pick(node, "firstInquiry指数值", "firstInquiryIndex")),
        }
        if any(isinstance(row[k], (int, float)) and row[k]
               for k in ("myUv", "myPayAmt", "rivalUv", "rivalPayAmt")):
            rows.append(row)
        for ch in node.get("children") or []:
            walk(ch, name)

    for root in tree if isinstance(tree, list) else []:
        walk(root, None)
    return rows


def _side_rows(raw, key):
    """my/first/second 可能是类数组对象（keys "0","1"…），统一成列表"""
    side = (raw or {}).get(key)
    if isinstance(side, dict):
        return list(side.values())
    return side or []


def _parse_buyer(results, rival_ids):
    out = {}
    for scence, label in _BUYER_SCENES:
        raw = results.get(scence) or {}
        sides = {"my": {r.get("scenceValue"): r.get("scoreRate")
                        for r in _side_rows(raw, "my")}}
        for idx, key in enumerate(("first", "second")):
            if idx < len(rival_ids):
                sides[rival_ids[idx]] = {r.get("scenceValue"): r.get("scoreRate")
                                         for r in _side_rows(raw, key)}
        names = []
        for m in sides.values():
            for n in m:
                if n not in names:
                    names.append(n)
        names.sort(key=lambda n: -(sides["my"].get(n) or 0))
        rows = [{"name": n, "myRate": sides["my"].get(n),
                 "rivalRates": {oid: sides[oid].get(n)
                                for oid in sides if oid != "my"}}
                for n in names]
        out[scence] = {"label": label, "exclusive": scence not in _NON_EXCLUSIVE,
                       "rows": rows}
    return out


def drill_compete_offer(cate_id, offer_id=None, offer_id2=None, my_offer_id=None,
                        cate_level: int = 1, date_type: str = "RECENT_7",
                        top: int = 10) -> dict:
    """竞品三维结构下钻（引流词 / 流量来源 / 买家结构）。

    Args:
        cate_id:      类目ID（必须来自 compete_category）
        offer_id:     竞品商品ID；不传则自动取监控池内交易水平最高的竞品
        offer_id2:    第二个竞品商品ID（可选，用于三方买家结构对比）
        my_offer_id:  本店对位商品ID；不传则自动匹配同叶子类目的本店商品
        cate_level:   类目层级，需与 cate_id 同层级
        date_type:    RECENT_7 / RECENT_30
        top:          词榜取前 N 条

    Returns:
        含 params / pool / offers / keywords / flowSource / buyer 的结果字典
    """
    if not cate_id:
        raise ParamError("cateId 不能为空，请先调用 compete_category 获取合法类目")

    date_type = (date_type or "RECENT_7").upper()
    if date_type not in _VALID_DATE_TYPE:
        raise ParamError(f"date_type 仅支持 {' / '.join(_VALID_DATE_TYPE)}，收到 {date_type}")

    date_range = date_range_for(date_type)
    base = {"dateType": date_type, "dateRange": date_range, "cateId": cate_id,
            "cateLevel": cate_level, "device": "ALL"}

    with ThreadPoolExecutor(max_workers=4) as pool_ex:
        f_mid = pool_ex.submit(_my_shop)
        f_pool = pool_ex.submit(_monitor_offers, cate_id, cate_level, date_type,
                                date_range)
        f_quota = pool_ex.submit(_offer_quota, cate_id)
        f_same = pool_ex.submit(_same_product_offers, cate_id, cate_level,
                                date_type, date_range)
        my_member_id = f_mid.result()
        pool_raw = f_pool.result()
        quota_raw = f_quota.result()
        same_raw = f_same.result()

    if not pool_raw:
        raise ServiceError(
            f"竞品监控池为空（cateId={cate_id}）。请先到生意参谋「竞店竞品配置」"
            "竞品 tab (https://sycm.1688.com/ms/compete/shopOfferSetting?settingType=1) "
            "添加竞品，或确认 cateId/cateLevel 层级配对正确"
        )

    pool = [_fmt_offer(r) for r in pool_raw]
    # 本店侧候选：同款商品清单（行级 memberId 均为本店，防御性过滤一道）
    mine_extra = [o for o in (_fmt_offer(r) for r in same_raw)
                  if o["memberId"] == my_member_id or o["memberId"] is None]
    sel = _resolve_offers(pool, mine_extra, my_member_id,
                          offer_id, offer_id2, my_offer_id)
    my_offer = sel["myOffer"]
    rivals = sel["rivals"]
    rival_ids = [r["offerId"] for r in rivals]

    # 配额一致性校验：实测该接口可能报 0 已监控但池内实有商品，矛盾时计数不可信
    already = quota_raw.get("alreadyMonitorCnt")
    quota = None
    if isinstance(already, int) and already >= len(pool):
        quota = {"monitorCount": already,
                 "remain": quota_raw.get("remainMonitorCnt")}

    with ThreadPoolExecutor(max_workers=5) as ex:
        f_my_kw = ex.submit(_offer_keywords, base, my_offer["offerId"])
        f_rk = {oid: ex.submit(_offer_keywords, base, oid)
                for oid in rival_ids}
        f_src = {oid: ex.submit(_flow_source, base, my_offer["offerId"], oid)
                 for oid in rival_ids}
        f_buyer = {s: ex.submit(_buyer_scene, base, s, my_offer["offerId"],
                                rival_ids)
                   for s, _label in _BUYER_SCENES}

        my_kw = f_my_kw.result()
        rival_kw = {oid: f.result() for oid, f in f_rk.items()}
        flow = {oid: _parse_flow_source(f.result()) for oid, f in f_src.items()}
        buyer_raw = {s: f.result() for s, f in f_buyer.items()}

    # 池外指定的本店商品：网关对非本店/不存在的商品不报错而是静默返空，
    # 若本店侧词榜与全渠道访客/支付均无数据，判为商品ID无效，拒绝输出
    # “本店全 0”的误导性对比
    if sel["myOfferExternal"]:
        my_kw_empty = not (isinstance(my_kw, list) and my_kw)
        my_flow_empty = all(
            not row["myUv"] and not row["myPayAmt"]
            for rows in flow.values() for row in rows
        )
        if my_kw_empty and my_flow_empty:
            raise ParamError(
                f"指定的本店商品 {my_offer['offerId']} 查无任何数据"
                "（引流词与全渠道访客/支付均为空），大概率不是本店在售商品或ID有误。"
                "请核对商品ID，或不传该参数由系统自动匹配"
            )

    return {
        "params": {"cateId": cate_id, "cateLevel": cate_level,
                   "dateType": date_type, "dateRange": date_range,
                   "myMemberId": my_member_id},
        "pool": {
            "total": len(pool),
            "myOfferCount": len(sel["poolMine"]),
            "rivalOfferCount": len(sel["poolRivals"]),
            # 本店对位候选总数（同款商品清单 + 监控池内本店商品去重）
            "myCandidateCount": len(sel["mineCandidates"]),
            # 监控配额；接口计数与监控池矛盾时为 null（不可信，不外显）
            "quota": quota,
            # 供 Agent 提示用户可换哪些竞品继续下钻
            "topRivals": [{k: o[k] for k in ("offerId", "title", "shopName",
                                             "minPrice", "maxPrice", "tradeIndex")}
                          for o in sel["poolRivals"][:10]],
        },
        "offers": {"myOffer": my_offer, "rivals": rivals,
                   "autoPicked": sel["autoPicked"]},
        "keywords": _parse_keywords(my_kw, rival_kw, top),
        "flowSource": flow,
        "buyer": _parse_buyer(buyer_raw, rival_ids),
    }
