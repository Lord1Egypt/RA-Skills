#!/usr/bin/env python
"""商品评分与圈选服务

内部获取商品明细并完成评分，只输出 Top-N 精简结果。
五大评分维度：销售贡献度(30%) + 流量效率(25%) + 成长潜力(20%) + 营销ROI(15%) + 商品健康度(10%)
"""

from typing import Dict, List, Any

from _http import api_post
from _errors import ServiceError


def fetch_item_detail(strategy: str, limit: int) -> dict:
    """调用远程接口获取商品明细数据。"""
    return api_post(
        "/api/skill_1688_item_select_get_item_detail/1.0.0",
        {"strategy": strategy, "limit": limit},
    )


# ---------------------------------------------------------------------------
# 五维评分
# ---------------------------------------------------------------------------

def _calculate_sales_score(item: Dict, shop_total: Dict) -> float:
    """销售贡献度得分（满分100）"""
    score = 0.0

    if isinstance(shop_total, list):
        shop_total = shop_total[0]

    item_amt = item.get('pay_ord_amt_1d', 0) or 0
    shop_amt = shop_total.get('pay_ord_amt_1d_001', 1) or 1
    amt_ratio = item_amt / shop_amt if shop_amt > 0 else 0

    if amt_ratio >= 0.10:
        amt_score = 100
    elif amt_ratio >= 0.05:
        amt_score = 80
    elif amt_ratio >= 0.02:
        amt_score = 60
    else:
        amt_score = min(amt_ratio * 3000, 60)
    score += amt_score * 0.6

    item_buyer = item.get('pay_ord_byr_cnt_1d', 0) or 0
    shop_buyer = shop_total.get('pay_ord_byr_cnt_1d_001', 1) or 1
    buyer_ratio = item_buyer / shop_buyer if shop_buyer > 0 else 0

    if buyer_ratio >= 0.10:
        buyer_score = 100
    elif buyer_ratio >= 0.05:
        buyer_score = 80
    elif buyer_ratio >= 0.02:
        buyer_score = 60
    else:
        buyer_score = min(buyer_ratio * 3000, 60)
    score += buyer_score * 0.3

    new_buyer_amt = item.get('pay_ord_amt_1d_931', 0) or 0
    new_ratio = new_buyer_amt / item_amt if item_amt > 0 else 0
    new_score = min(new_ratio * 200, 100)
    score += new_score * 0.1

    return round(score, 2)


def _calculate_traffic_score(item: Dict) -> float:
    """流量效率得分（满分100）"""
    score = 0.0

    buyer_cnt = item.get('pay_ord_byr_cnt_1d', 0) or 0
    uv = item.get('ipv_uv_1d', 1) or 1
    cvr = buyer_cnt / uv if uv > 0 else 0

    if cvr >= 0.05:
        cvr_score = 100
    elif cvr >= 0.03:
        cvr_score = 80
    elif cvr >= 0.01:
        cvr_score = 60
    else:
        cvr_score = min(cvr * 2000, 60)
    score += cvr_score * 0.6

    ipv = item.get('ipv_1d', 0) or 0
    imps = item.get('imps_cnt_1d', 1) or 1
    imp_cvr = ipv / imps if imps > 0 else 0
    imp_score = min(imp_cvr * 200, 100)
    score += imp_score * 0.2

    cart_uv = item.get('cart_uv_1d', 0) or 0
    cart_rate = cart_uv / uv if uv > 0 else 0
    cart_score = min(cart_rate * 500, 100)
    score += cart_score * 0.2

    return round(score, 2)


def _calculate_potential_score(item: Dict) -> float:
    """成长潜力得分（满分100）"""
    score = 0.0

    if item.get('is_hqp') == 1:
        score += 30
    if item.get('is_pwp') == 1:
        score += 20
    if item.get('is_sjp') == 1:
        score += 15
    if item.get('is_zdzb') == 1:
        score += 10

    growth_level = item.get('gyp_growth_level', '')
    if '高' in str(growth_level) or 'high' in str(growth_level).lower():
        score += 20
    elif '中' in str(growth_level) or 'medium' in str(growth_level).lower():
        score += 10

    if item.get('is_yx') == 1:
        score += 5

    return min(round(score, 2), 100)


def _calculate_roi_score(item: Dict) -> float:
    """营销ROI得分（满分100）"""
    ad_cost = item.get('ad_cost_1d', 0) or 0
    pay_amt = item.get('pay_ord_amt_1d', 0) or 0

    if ad_cost == 0:
        return 100 if pay_amt > 0 else 50

    roi = pay_amt / ad_cost if ad_cost > 0 else 0

    if roi >= 5:
        return 100
    elif roi >= 3:
        return 80
    elif roi >= 1:
        return 60
    else:
        return 30


def _calculate_health_score(item: Dict) -> float:
    """商品健康度得分（满分100）"""
    score = 0.0

    if item.get('is_no_reason_to_return_7d') == 1:
        score += 10
    if item.get('is_48hour_send') == 1:
        score += 10
    if item.get('is_15day_free_refund') == 1:
        score += 5

    stock = item.get('itm_stock', 0) or 0
    if stock > 100:
        score += 10
    elif stock >= 50:
        score += 5

    refund_amt = item.get('suc_rfd_amt_1d', 0) or 0
    pay_amt = item.get('pay_ord_amt_1d', 1) or 1
    refund_rate = refund_amt / pay_amt if pay_amt > 0 else 0

    if refund_rate < 0.05:
        score += 10
    elif refund_rate < 0.10:
        score += 5

    return min(round(score, 2), 100)


# ---------------------------------------------------------------------------
# 综合评分与分层
# ---------------------------------------------------------------------------

def _calculate_total_score(item: Dict, shop_total: Dict) -> Dict[str, Any]:
    """计算商品综合得分，返回各维度得分和总分。"""
    sales_score = _calculate_sales_score(item, shop_total)
    traffic_score = _calculate_traffic_score(item)
    potential_score = _calculate_potential_score(item)
    roi_score = _calculate_roi_score(item)
    health_score = _calculate_health_score(item)

    total_score = (
        sales_score * 0.30 +
        traffic_score * 0.25 +
        potential_score * 0.20 +
        roi_score * 0.15 +
        health_score * 0.10
    )

    return {
        'sales_score': sales_score,
        'traffic_score': traffic_score,
        'potential_score': potential_score,
        'roi_score': roi_score,
        'health_score': health_score,
        'total_score': round(total_score, 2),
    }


def _classify_product(total_score: float) -> Dict[str, str]:
    """根据总分对商品进行分层。"""
    if total_score >= 80:
        return {'level': 'S级', 'name': '重点推广品',
                'strategy': '加大投入，抢占流量，优化详情页，参与营销活动'}
    elif total_score >= 60:
        return {'level': 'A级', 'name': '潜力培育品',
                'strategy': '针对性优化短板，适度增加预算，测试潜力'}
    elif total_score >= 40:
        return {'level': 'B级', 'name': '维持运营品',
                'strategy': '维持现状，定期检查，作为辅助商品'}
    else:
        return {'level': 'C级', 'name': '优化调整品',
                'strategy': '停止广告，诊断问题，考虑优化或下架'}


def _compact_product(product: Dict, rank: int) -> Dict:
    """将评分结果精简为 LLM 需要的最小字段集。"""
    return {
        "rank": rank,
        "item_id": product.get("item_id"),
        "title": product.get("title"),
        "scores": product.get("scores"),
        "classification": product.get("classification"),
        "key_metrics": {
            "pay_ord_amt_1d": product.get("raw_data", {}).get("pay_ord_amt_1d", 0),
            "pay_ord_byr_cnt_1d": product.get("raw_data", {}).get("pay_ord_byr_cnt_1d", 0),
            "ipv_uv_1d": product.get("raw_data", {}).get("ipv_uv_1d", 0),
            "ad_cost_1d": product.get("raw_data", {}).get("ad_cost_1d", 0),
        },
    }


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------

def score_and_select(shop_total: dict, strategy: str = "comprehensive",
                     limit: int = 100, top_n: int = 10) -> dict:
    """商品评分与圈选。

    Args:
        shop_total: 店铺维度数据（作为评分基准）
        strategy:   查询策略 comprehensive / sales / all
        limit:      获取商品数量上限
        top_n:      输出排名前N的商品

    Returns:
        包含 total_scored / returned_count / products / summary 的字典
    """
    # 1. 获取商品明细
    item_data = fetch_item_detail(strategy, limit)

    # 兼容不同返回格式
    if isinstance(item_data, list):
        items = item_data
    elif isinstance(item_data, dict):
        items = item_data.get("products") or item_data.get("items") or item_data.get("data", [])
    else:
        items = []

    if not items:
        raise ServiceError("未获取到商品数据")

    # 2. 评分
    scored = []
    for item in items:
        scores = _calculate_total_score(item, shop_total)
        classification = _classify_product(scores['total_score'])
        scored.append({
            'item_id': item.get('item_id'),
            'title': item.get('title', '未知商品'),
            'scores': scores,
            'classification': classification,
            'raw_data': {
                'pay_ord_amt_1d': item.get('pay_ord_amt_1d', 0),
                'pay_ord_byr_cnt_1d': item.get('pay_ord_byr_cnt_1d', 0),
                'ipv_uv_1d': item.get('ipv_uv_1d', 0),
                'imps_cnt_1d': item.get('imps_cnt_1d', 0),
                'ad_cost_1d': item.get('ad_cost_1d', 0),
                'itm_stock': item.get('itm_stock', 0),
            },
        })
    scored.sort(key=lambda x: x['scores']['total_score'], reverse=True)

    # 3. 取 Top-N 精简输出
    actual_top_n = min(top_n, len(scored))
    top_products = [_compact_product(p, i + 1) for i, p in enumerate(scored[:actual_top_n])]

    return {
        "total_scored": len(scored),
        "returned_count": actual_top_n,
        "products": top_products,
        "summary": {
            "S级": len([r for r in scored if r["classification"]["level"] == "S级"]),
            "A级": len([r for r in scored if r["classification"]["level"] == "A级"]),
            "B级": len([r for r in scored if r["classification"]["level"] == "B级"]),
            "C级": len([r for r in scored if r["classification"]["level"] == "C级"]),
        },
    }
