#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""供应链助手 - 自动换供、同款筛选、搜索货源

基于 1688-distribution-procurement-supplychange 的三层流水线架构：
- 场景层：识别换供需求
- 同款筛选层：寻找替代货源
- 货源替换层：执行换供（调用 link_supply_helper）

关联货源功能已独立到 link_supply_helper，可被本模块调用
"""

import os
import sys
import csv
import json
import time
from typing import Dict, List, Optional
from collections import OrderedDict

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from scripts._sys._http import api_post
from scripts._sys._errors import ServiceError
from scripts.biz.link_supply_helper.service import link_supply, batch_link_supply
from scripts.biz.isv_token.service import fetch_isv_token
from scripts.biz.isv_skill_helper.service import (
    discover_isv_skill,
    discover_skill_by_name,
    call_isv_link_supply,
    call_isv_link_preview,
)
from scripts.biz.image_search_helper.service import image_search_offer


# ==================== 自动换供（三层流水线架构）====================

# CSV 字段定义
SUPPLY_DEMAND_CSV_FIELDS = [
    'offer_id', 'sku_id', 'offer_title', 'current_price', 'reason',
    'downstream_item_id', 'downstream_price', 'downstream_channel', 'isv_app_key'
]

SUPPLY_PLAN_CSV_FIELDS = [
    'offer_id', 'sku_id', 'offer_title', 'current_price', 'reason',
    'recommend_offer_id', 'recommend_title', 'recommend_price', 'recommend_reason',
    'downstream_item_id', 'downstream_channel', 'isv_app_key'
]

# 轮询配置
POLL_INTERVAL = 5
MAX_POLL_SECONDS = 300  # 最多等待 5 分钟


def auto_switch_supply(
    offer_ids: List[str] = None,
    sku_id: str = None,
    reason: str = None,
    offer_title: str = None,
    current_price: str = None,
    downstream_item_id: str = None,
    downstream_channel: str = None,
    isv_app_key: str = None,
    offer_image_url: str = None,
) -> Dict:
    """
    自动换供 - 完整流程

    三层流水线架构：
    1. 场景层：识别换供需求
    2. 同款筛选层：寻找替代货源（同款筛选失败时 fallback 到图搜）
    3. 货源替换层：执行换供

    :param offer_ids: 1688商品ID列表
    :param sku_id: SKU ID
    :param reason: 换供原因
    :param offer_title: 商品标题
    :param current_price: 当前采购价
    :param downstream_item_id: 下游商品ID
    :param downstream_channel: 下游渠道
    :param isv_app_key: ISV AppKey
    :param offer_image_url: 商品主图URL（用于同款筛选失败时的图搜 fallback）
    :return: 换供结果
    """
    if not offer_ids:
        return {"success": False, "error": "请提供 offer_ids"}

    # Step 1: 场景层 - 识别换供需求
    demand_items = _identify_supply_demand(
        offer_ids=offer_ids,
        sku_id=sku_id,
        reason=reason,
        offer_title=offer_title,
        current_price=current_price,
        downstream_item_id=downstream_item_id,
        downstream_channel=downstream_channel,
        isv_app_key=isv_app_key,
        offer_image_url=offer_image_url,
    )

    if not demand_items:
        return {"success": False, "error": "未识别到换供需求"}

    # Step 2: 同款筛选层 - 寻找替代货源
    plan_items = _find_supply_matches(demand_items)

    # Step 2.5: 同款筛选失败时，fallback 到图搜找同款
    plan_items = _fallback_image_search_if_needed(plan_items, demand_items)

    # Step 3: 货源替换层 - 执行换供（调用 link_supply_helper）
    replaced_items = _execute_supply_replace(plan_items)

    success_count = sum(1 for item in replaced_items if item.get('status') == 'REPLACED')

    return {
        "success": True,
        "data": {
            "total": len(replaced_items),
            "success": success_count,
            "failed": len(replaced_items) - success_count,
            "items": replaced_items
        }
    }


def _execute_supply_replace(plan_items: List[Dict]) -> List[Dict]:
    """
    货源替换层：执行换供

    对匹配成功的商品，调用 link_supply_helper 进行货源替换

    :param plan_items: 换供方案列表
    :return: 执行结果列表
    """
    results = []

    for item in plan_items:
        result = dict(item)

        # 只有匹配成功的才执行替换
        if item.get('status') != 'SUCCESS':
            results.append(result)
            continue

        downstream_item_id = item.get('downstream_item_id')
        recommend_offer_id = item.get('recommend_offer_id')

        # 如果没有下游商品ID，无法执行替换
        if not downstream_item_id:
            result['replace_status'] = 'SKIPPED'
            result['replace_message'] = '缺少下游商品ID，无法执行替换'
            results.append(result)
            continue

        # 如果没有推荐商品ID，无法执行替换
        if not recommend_offer_id:
            result['replace_status'] = 'SKIPPED'
            result['replace_message'] = '缺少推荐商品ID，无法执行替换'
            results.append(result)
            continue

        try:
            # 调用 link_supply_helper 执行货源替换
            link_result = link_supply(
                downstream_item_id=downstream_item_id,
                downstream_sku_id=item.get('downstream_sku_id'),
                offer_id=recommend_offer_id,
                sku_id=item.get('recommend_sku_id'),
                isv_app_key=item.get('isv_app_key'),
                platform=item.get('downstream_channel'),
            )

            # 判断替换结果
            if link_result.get('success'):
                result['status'] = 'REPLACED'
                result['replace_status'] = 'SUCCESS'
                result['replace_message'] = '货源替换成功'
                result['replace_detail'] = link_result
            else:
                result['replace_status'] = 'FAILED'
                result['replace_message'] = link_result.get('error', '货源替换失败')
                result['replace_detail'] = link_result

        except Exception as e:
            result['replace_status'] = 'FAILED'
            result['replace_message'] = f'货源替换异常: {str(e)}'

        results.append(result)

    return results


def _identify_supply_demand(
    offer_ids: List[str],
    sku_id: str = None,
    reason: str = None,
    offer_title: str = None,
    current_price: str = None,
    downstream_item_id: str = None,
    downstream_channel: str = None,
    isv_app_key: str = None,
    offer_image_url: str = None,
) -> List[Dict]:
    """场景层：识别换供需求"""
    items = []
    for offer_id in offer_ids:
        # 如果未提供价格，查询商品信息
        price = current_price
        if not price:
            try:
                response = api_post('distribution_offer_info', {'offerId': str(offer_id)})
                data = response.get('data', {})
                if isinstance(data, dict) and 'data' in data:
                    offer_data = data.get('data', {})
                else:
                    offer_data = data

                if offer_data:
                    price_info = offer_data.get('priceInInfo', {})
                    price = _build_price(
                        price_info.get('multiPiecePriceInteger'),
                        price_info.get('multiPiecePriceDecimal')
                    )
            except Exception as e:
                print(f"查询商品价格失败: {e}")

        items.append({
            'offer_id': offer_id,
            'sku_id': sku_id or '',
            'offer_title': offer_title or '',
            'current_price': price or '',
            'reason': reason or '自动换供',
            'downstream_item_id': downstream_item_id or '',
            'downstream_price': '',
            'downstream_channel': downstream_channel or '',
            'isv_app_key': isv_app_key or '',
            'offer_image_url': offer_image_url or '',
        })
    return items


def _build_price(integer_part, decimal_part) -> str:
    """拼接价格字符串"""
    if integer_part is None:
        return ""
    price = str(integer_part)
    if decimal_part:
        price += f".{decimal_part}"
    return price


def _find_supply_matches(demand_items: List[Dict]) -> List[Dict]:
    """同款筛选层：寻找替代货源"""
    if not demand_items:
        return []

    user_id = _get_current_user_id()

    # Step 1: 逐个商品启动异步任务
    batch_id_to_item = OrderedDict()
    for item in demand_items:
        batch_id = _start_single_supply_match(user_id, item)
        if batch_id:
            batch_id_to_item[batch_id] = item

    # Step 2: 轮询获取结果
    finished_results = _poll_all_results(user_id, batch_id_to_item)

    # Step 3: 合并结果
    return _merge_all_results(demand_items, batch_id_to_item, finished_results)


def _get_current_user_id() -> str:
    """获取当前用户 ID

    优先从环境变量获取，否则返回默认值
    """
    import os
    # 尝试从环境变量获取
    user_id = os.environ.get("USER_ID")
    if user_id:
        return user_id
    # TODO: 从 AK 或接口中解析真实用户 ID
    return "2212555791283"


def _start_single_supply_match(user_id: str, item: Dict) -> Optional[str]:
    """为单个商品启动同款筛选任务"""
    try:
        request = {
            'offerId': item.get('offer_id'),
            'skuId': item.get('sku_id', ''),
            'offerTitle': item.get('offer_title', ''),
            'currentPrice': item.get('current_price', ''),
            'reason': item.get('reason', ''),
            'appKey': item.get('isv_app_key', ''),
            'offerImageUrl': '',
            'skuImageUrl': '',
            'skuText': '',
            'cpv': ''
        }

        response = api_post('supply_match_start_supply_match', {
            'userId': user_id,
            'request': request
        })

        if not response.get('success'):
            return None

        return response.get('data')
    except Exception as e:
        print(f"启动同款筛选任务异常: {e}")
        return None


def _poll_all_results(user_id: str, batch_id_to_item: OrderedDict) -> Dict[str, Dict]:
    """轮询所有 batchId 获取结果

    固定间隔轮询，最多等待 MAX_POLL_SECONDS（5分钟）。
    过程中持续输出进度，避免大模型误判为执行卡死。
    """
    pending_batch_ids = set(batch_id_to_item.keys())
    total_tasks = len(pending_batch_ids)
    finished_results = {}
    start_time = time.time()
    attempt = 0

    while pending_batch_ids:
        elapsed = time.time() - start_time
        if elapsed >= MAX_POLL_SECONDS:
            print(f"[同款筛选] 轮询达到最大等待时间 {MAX_POLL_SECONDS}s，剩余 {len(pending_batch_ids)} 个任务未结束")
            break

        attempt += 1
        print(
            f"[同款筛选] 第 {attempt} 轮轮询，已等待 {int(elapsed)}s，"
            f"进行中 {len(pending_batch_ids)}/{total_tasks}"
        )

        for batch_id in list(pending_batch_ids):
            result = _query_single_result(user_id, batch_id)
            if result is None:
                # 查询异常，继续等待下一轮（不单独重试）
                continue

            status = result.get('status')
            if status == 'RUNNING':
                # 仍在运行中，正常等待下一轮
                continue

            # 任务结束（SUCCESS / FAILED / 其他）
            pending_batch_ids.remove(batch_id)
            finished_results[batch_id] = result
            msg = result.get('errorMessage', '') if status == 'FAILED' else ''
            print(f"[同款筛选] 任务完成，状态: {status}{'，' + msg if msg else ''}")

        if pending_batch_ids:
            time.sleep(POLL_INTERVAL)

    # 处理超时任务
    for batch_id in pending_batch_ids:
        finished_results[batch_id] = {
            'status': 'TIMEOUT',
            'errorMessage': '轮询超时'
        }
        print(f"[同款筛选] 任务超时: {batch_id}")

    total_elapsed = int(time.time() - start_time)
    print(f"[同款筛选] 轮询结束，共耗时 {total_elapsed}s，完成 {len(finished_results)} 个任务")
    return finished_results


def _query_single_result(user_id: str, batch_id: str) -> Optional[Dict]:
    """查询单个 batchId 的结果"""
    try:
        response = api_post('supply_match_query_supply_match_result', {
            'userId': user_id,
            'batchId': batch_id
        })

        results = response.get('result', [])
        if not results:
            return None

        return results[0]
    except Exception as e:
        print(f"查询结果异常: {e}")
        return None


def _merge_all_results(
    demand_items: List[Dict],
    batch_id_to_item: OrderedDict,
    finished_results: Dict[str, Dict]
) -> List[Dict]:
    """合并所有结果"""
    batch_id_to_offer_id = {
        batch_id: item.get('offer_id')
        for batch_id, item in batch_id_to_item.items()
    }

    all_results = []

    for item in demand_items:
        result = dict(item)

        match_result = None
        for batch_id, match_data in finished_results.items():
            if batch_id_to_offer_id.get(batch_id) == item.get('offer_id'):
                match_result = match_data
                break

        if match_result is None:
            result['status'] = 'FAILED'
            result['error'] = '未获取到匹配结果'
            all_results.append(result)
            continue

        status = match_result.get('status')
        result['status'] = status if status in ['SUCCESS', 'FAILED', 'TIMEOUT'] else 'FAILED'

        if status == 'SUCCESS':
            recommendations = match_result.get('recommendations', [])
            best = next((r for r in recommendations if r.get('rank') == 1), None)

            if best:
                result['recommend_offer_id'] = best.get('recommendOfferId')
                result['recommend_title'] = best.get('title')
                result['recommend_price'] = best.get('price')
                result['recommend_reason'] = best.get('recommendReason')
            else:
                result['status'] = 'FAILED'
                result['error'] = '未找到推荐商品'
        elif status == 'FAILED':
            result['error'] = match_result.get('errorMessage', '匹配任务失败')
        elif status == 'TIMEOUT':
            result['error'] = '轮询超时'

        all_results.append(result)

    return all_results


# ==================== 图搜 Fallback ====================

def _fallback_image_search_if_needed(
    plan_items: List[Dict],
    demand_items: List[Dict],
) -> List[Dict]:
    """
    同款筛选失败后，尝试图搜 fallback 找替代货源。

    对匹配失败的商品，仅使用传入的商品图片URL进行图搜（不使用关键词搜索，
    因为关键词搜索结果大概率不是同款）。
    从搜索结果中选择价格和服务更优的商品作为推荐。
    """
    for item in plan_items:
        # 只处理匹配失败的
        if item.get('status') == 'SUCCESS' and item.get('recommend_offer_id'):
            continue

        offer_id = item.get('offer_id')
        demand_item = next((d for d in demand_items if d.get('offer_id') == offer_id), {})
        image_url = demand_item.get('offer_image_url', '')
        current_price = item.get('current_price', '')

        try:
            if image_url:
                print(f"[图搜Fallback] 商品 {offer_id} 同款筛选失败，尝试图搜...")
                search_result = image_search_offer(image_url=image_url, page_size=10)
            else:
                item['status'] = 'FAILED'
                item['error'] = item.get('error', '') + '；缺少商品图片URL，无法进行图搜找同款'
                continue

            best = _select_best_from_image_search(search_result, current_price)
            if best:
                item['status'] = 'SUCCESS'
                item['recommend_offer_id'] = best['offer_id']
                item['recommend_title'] = best['title']
                item['recommend_price'] = best['price']
                item['recommend_reason'] = best['reason']
                item['fallback_source'] = 'image_search'
                print(f"[图搜Fallback] 商品 {offer_id} 找到替代货源: {best['offer_id']} (¥{best['price']})")
            else:
                item['status'] = 'FAILED'
                item['error'] = item.get('error', '') + '；图搜未找到合适的替代货源'

        except Exception as e:
            item['status'] = 'FAILED'
            item['error'] = item.get('error', '') + f'；图搜失败: {e}'

    return plan_items


def _select_best_from_image_search(search_result: Dict, current_price: str = None) -> Optional[Dict]:
    """
    从图搜结果中选择最优商品。

    排序逻辑：
    1. 优先选择价格更低的商品
    2. 加分项：实力商家、48h/24h发货、支持密文面单
    """
    items = search_result.get('data', [])
    if not items:
        return None

    # 提取有效商品
    valid_items = []
    for it in items:
        offer_id = it.get('offerId')
        if not offer_id:
            continue
        valid_items.append({
            'offer_id': str(offer_id),
            'title': it.get('title', ''),
            'price': it.get('price'),
            'raw': it,
        })

    if not valid_items:
        return None

    # 解析当前价格
    current_price_val = None
    if current_price:
        try:
            current_price_val = float(current_price)
        except ValueError:
            pass

    def _score(it):
        """分数越低越优（价格为基础，服务指标为加分）"""
        price_val = it['price'] if it['price'] is not None else float('inf')
        score = price_val

        raw = it['raw']
        member_info = raw.get('memberInfo', {}) or {}
        fullfill_info = raw.get('fullfillInfo', {}) or {}
        proxy_advice = raw.get('proxyAdvice', {}) or {}

        # 加分项（降低分数）
        if member_info.get('isPmPlus'):
            score -= 5
        if fullfill_info.get('pickupAssurance48H') or fullfill_info.get('pickupAssurance24H'):
            score -= 3
        if proxy_advice.get('materialPackTag') == 'supported':
            score -= 2

        return score

    valid_items.sort(key=_score)
    best = valid_items[0]

    # 构造推荐理由
    reason_parts = []
    if current_price_val and best['price'] is not None and best['price'] < current_price_val:
        reason_parts.append(f"价格更优(¥{best['price']} < ¥{current_price_val})")

    raw = best['raw']
    member_info = raw.get('memberInfo', {}) or {}
    fullfill_info = raw.get('fullfillInfo', {}) or {}
    if member_info.get('isPmPlus'):
        reason_parts.append("实力商家")
    if fullfill_info.get('pickupAssurance24H'):
        reason_parts.append("24h发货")
    elif fullfill_info.get('pickupAssurance48H'):
        reason_parts.append("48h发货")

    reason = "，".join(reason_parts) if reason_parts else "图搜推荐"

    return {
        'offer_id': best['offer_id'],
        'title': best['title'],
        'price': best['price'],
        'reason': reason,
    }


# ==================== ISV 下游关联货源 ====================

def execute_downstream_link(
    app_key: str,
    shop_id: str,
    shop_nick: str,
    local_item_id: str,
    source_offer_url: str,
    purchase_account: str,
    platform: str = "taobao",
    use_preview: bool = True,
    limit_rows: int = None,
) -> Dict:
    """
    调用 ISV 技能执行下游关联货源。

    完整流程：
    1. 发现 ISV 技能（fx-procurement-9018264 或 fx-distribute-offer-{appKey}）
    2. 获取 ISV Token
    3. 淘宝平台：可选 SKU 预览匹配
    4. 执行关联货源（confirm-link / douyin-confirm-link）

    :param app_key: ISV 的 AppKey
    :param shop_id: 下游店铺 ID
    :param shop_nick: 下游店铺名称
    :param local_item_id: 下游商品 ID
    :param source_offer_url: 1688 货源链接
    :param purchase_account: 采购账号
    :param platform: 平台（taobao/douyin）
    :param use_preview: 淘宝平台是否先执行 SKU 预览匹配
    :param limit_rows: 仅提交前 N 条 SKU 映射
    :return: 关联结果
    """
    result = {
        "success": False,
        "stage": "discovery",
        "message": "",
        "data": {}
    }

    # Step 1: 发现 ISV 技能
    # 先尝试按 appKey 查找 fx-distribute-offer-{appKey}
    isv_result = discover_isv_skill(app_key)

    # 如果没找到，尝试查找 fx-procurement-9018264
    if not isv_result.get("found"):
        isv_result = discover_skill_by_name("fx-procurement-9018264")

    if not isv_result.get("found"):
        result["message"] = f"未找到对应的 ISV 技能（AppKey: {app_key}）"
        return result

    skill_path = isv_result["skill_path"]
    result["data"]["skill_name"] = isv_result.get("skill_name")
    result["data"]["skill_path"] = skill_path

    # Step 2: 获取 ISV Token
    result["stage"] = "token"
    try:
        token = fetch_isv_token(app_key)
        result["data"]["token_fetched"] = True
    except Exception as e:
        result["message"] = f"获取 ISV Token 失败: {e}"
        return result

    # Step 3: 淘宝平台可选 SKU 预览
    if platform == "taobao" and use_preview:
        result["stage"] = "preview"
        try:
            preview_result = call_isv_link_preview(
                skill_path=skill_path,
                token=token,
                shop_id=shop_id,
                shop_nick=shop_nick,
                local_item_id=local_item_id,
                source_offer_url=source_offer_url,
                purchase_account=purchase_account,
            )
            result["data"]["preview"] = preview_result
        except Exception as e:
            result["message"] = f"SKU 预览匹配失败: {e}"
            # 预览失败可以继续执行关联

    # Step 4: 执行关联货源
    result["stage"] = "link"
    try:
        link_result = call_isv_link_supply(
            skill_path=skill_path,
            token=token,
            shop_id=shop_id,
            shop_nick=shop_nick,
            local_item_id=local_item_id,
            source_offer_url=source_offer_url,
            purchase_account=purchase_account,
            platform=platform,
            limit_rows=limit_rows,
        )
        result["success"] = link_result.get("success", False)
        result["data"]["link_result"] = link_result
        if result["success"]:
            result["message"] = "下游关联货源成功"
        else:
            result["message"] = link_result.get("markdown") or link_result.get("error", "关联货源失败")
    except Exception as e:
        result["message"] = f"执行关联货源失败: {e}"

    return result
