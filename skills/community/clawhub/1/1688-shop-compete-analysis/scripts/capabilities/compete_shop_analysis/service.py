#!/usr/bin/env python3
"""初步竞店分析服务

一次调用完成竞店分析 Step 0~1 的取数与解析：本店信息、行业店铺排行（标记本店
名次与是否已监控）、客户流失去向 TOP、监控配额，输出可直接用于展示的扁平结构。
"""

from concurrent.futures import ThreadPoolExecutor

from _compete import (compete_query, val, member_id_of, date_range_for,
                      single_day)
from _errors import ParamError, ServiceError

_VALID_DATE_TYPE = ("RECENT_7", "RECENT_30")

# 指数脱敏占位常量：真实值过小时后端不返 0 而是固定 magic，
# 若不归一会被当成真值参与差距/比率计算（实测会算出 +187796% 这种荒谬差距）
_MAGIC = 0.9527275047730654


def _clean_index(x):
    if isinstance(x, (int, float)) and abs(x - _MAGIC) < 1e-6:
        return None
    return x


def _my_shop(cate_id):
    return compete_query("compete/competeShop/getMyShopInfo", {}) or {}


def _shop_list(cate_id, cate_level, date_type, date_range, page_size):
    return compete_query("compete/competeShop/shopList", {
        "dateRange": date_range, "dateType": date_type,
        "cateId": cate_id, "cateLevel": cate_level, "device": "ALL",
        "orderBy": "payOrdAmtIndex", "order": "desc",
        "page": 1, "pageSize": page_size,
    }) or {}


def _monitor_shops(cate_id):
    return compete_query("compete/common/getShopMonitorInfo",
                         {"cateId": cate_id}) or []


def _monitor_quota(cate_id):
    return compete_query("compete/common/getShopMonitorCntInfo",
                         {"cateId": cate_id}) or {}


def _loss_top(cate_id, cate_level, top):
    """客户流失榜：日粒度专属，昨天数据未出时自动用 periodsAgo 回溯前一天"""
    base = {
        "dateType": "RECENT_1", "cateId": cate_id, "cateLevel": cate_level,
        "device": "ALL", "orderBy": "lossIndex", "order": "desc",
        "pageNo": 1, "pageSize": top,
    }
    for days_ago, periods_ago in ((1, None), (2, 1), (3, 2)):
        params = dict(base, dateRange=single_day(days_ago))
        if periods_ago is not None:
            params["periodsAgo"] = periods_ago
        try:
            data = compete_query("compete/shopDiscern/lossShop/getLossTopShopList",
                                 params)
        except Exception:
            continue
        rows = data.get("data") if isinstance(data, dict) else data
        if rows:
            return {"rows": rows, "dateRange": params["dateRange"],
                    "periodsAgo": periods_ago}
    return {"rows": [], "dateRange": None, "periodsAgo": None}


def _fmt_shop_row(row, rank, monitored_ids, my_member_id):
    shop = row.get("shop") or {}
    mid = member_id_of(row)
    is_my = row.get("isMyShop") == "y" or (my_member_id and mid == my_member_id)
    return {
        "rank": rank,
        "shopName": shop.get("shopName"),
        "memberId": mid,
        "isMyShop": bool(is_my),
        "isMonitored": mid in monitored_ids if mid else False,
        "identity": shop.get("IDentity") or shop.get("identity"),
        "tradeMedal": shop.get("交易等级Grade") or shop.get("tradeMedalGrade"),
        "tradeIndex": _clean_index(val(row, "交易指数")),
        "tradeIndexCrc": val(row, "交易指数", "cycleCrc"),
        "uvIndex": _clean_index(val(row, "流量指数")),
        "uvIndexCrc": val(row, "流量指数", "cycleCrc"),
        "searchIndex": _clean_index(val(row, "搜索指数")),
        "buyerIndex": _clean_index(val(row, "买家指数")),
        "cateRank": val(row, "行业排名"),
        "newItemCnt": val(row, "上新商品数"),
        "repeatRate": val(row, "回头率"),
        "uvGrowth": val(row, "流量增长幅度"),
        "tradeGrowth": val(row, "交易增长幅度"),
    }


def analyze_compete_shop(cate_id, cate_level: int = 1, date_type: str = "RECENT_7",
                         top: int = 10) -> dict:
    """初步竞店分析：并发拉取 5 个接口并解析为扁平结构。

    Args:
        cate_id:    类目ID（必须来自 compete_category，传错会导致全部无数据）
        cate_level: 类目层级，需与 cate_id 同层级
        date_type:  RECENT_7 / RECENT_30
        top:        行业榜与流失榜各取前 N 条

    Returns:
        含 myShop / industryRank / lossTop / monitor 四块的结果字典
    """
    if not cate_id:
        raise ParamError("cateId 不能为空，请先调用 compete_category 获取合法类目")

    date_type = (date_type or "RECENT_7").upper()
    if date_type not in _VALID_DATE_TYPE:
        raise ParamError(f"date_type 仅支持 {' / '.join(_VALID_DATE_TYPE)}，收到 {date_type}")

    date_range = date_range_for(date_type)
    page_size = max(top, 50)  # 该接口存在约 50 行内置上限，一次取全便于定位本店名次

    with ThreadPoolExecutor(max_workers=5) as pool:
        f_my = pool.submit(_my_shop, cate_id)
        f_rank = pool.submit(_shop_list, cate_id, cate_level, date_type,
                             date_range, page_size)
        f_mon = pool.submit(_monitor_shops, cate_id)
        f_quota = pool.submit(_monitor_quota, cate_id)
        f_loss = pool.submit(_loss_top, cate_id, cate_level, top)

        my_raw = f_my.result()
        rank_raw = f_rank.result()
        mon_raw = f_mon.result()
        quota_raw = f_quota.result()
        loss_raw = f_loss.result()

    my_member_id = my_raw.get("会员ID") or my_raw.get("memberId")
    my_shop = {
        "shopName": my_raw.get("shopName"),
        "memberId": my_member_id,
        "identity": my_raw.get("IDentity") or my_raw.get("identity"),
        "tradeMedal": my_raw.get("交易等级Grade") or my_raw.get("tradeMedalGrade"),
        "shopUrl": my_raw.get("shopurl") or my_raw.get("shopUrl"),
    }

    monitored = [{"memberId": member_id_of(s), "shopName": s.get("shopName"),
                  "isDelete": s.get("isDelete")}
                 for s in (mon_raw if isinstance(mon_raw, list) else [])]
    monitored_ids = {m["memberId"] for m in monitored
                     if m["memberId"] and m["isDelete"] != "y"}

    rank_rows = rank_raw.get("data") or []
    if not rank_rows:
        raise ServiceError(
            f"行业店铺排行无数据（cateId={cate_id}, cateLevel={cate_level}）。"
            "请先用 compete_category 确认类目合法且层级配对"
        )

    all_rows = [_fmt_shop_row(r, i, monitored_ids, my_member_id)
                for i, r in enumerate(rank_rows, 1)]
    my_row = next((r for r in all_rows if r["isMyShop"]), None)
    # 重点竞店：榜单里排名最高且已监控的非本店店铺（可直接下钻，不会触发 1001）
    focus = next((r for r in all_rows if not r["isMyShop"] and r["isMonitored"]), None)

    loss_top = [{
        "rank": r.get("orderNum"),
        "shopName": (r.get("shop") or {}).get("shopName"),
        "memberId": member_id_of(r),
        "lossIndex": _clean_index(val(r, "流失指数") or val(r, "lossIndex")),
        "isMonitored": bool(r.get("isMonitor")),
    } for r in loss_raw["rows"]]

    return {
        "params": {"cateId": cate_id, "cateLevel": cate_level,
                   "dateType": date_type, "dateRange": date_range},
        "myShop": my_shop,
        "industryRank": {
            "totalCount": rank_raw.get("recordCount"),
            "myRank": my_row["rank"] if my_row else None,
            "myShopRow": my_row,
            "top": all_rows[:top],
            "focusCompetitor": focus,
        },
        "lossTop": {
            "dateRange": loss_raw["dateRange"],
            "periodsAgo": loss_raw["periodsAgo"],
            "rows": loss_top,
        },
        "monitor": {
            "shopCount": quota_raw.get("alreadyMonitorCnt"),
            "shopRemain": quota_raw.get("remainMonitorCnt"),
            # 配额接口的 alreadyMonitorCnt 包含已删除项，此处另给有效监控数
            "shopCountValid": len(monitored_ids),
            "monitoredShops": monitored,
        },
    }
