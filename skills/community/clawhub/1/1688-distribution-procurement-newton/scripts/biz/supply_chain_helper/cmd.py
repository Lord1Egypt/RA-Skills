#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""供应链助手命令

自动换供功能基于三层流水线架构：
- 场景层：识别换供需求
- 同款筛选层：寻找替代货源
- 货源替换层：调用 link_supply_helper 执行换供

关联货源功能请使用 link_supply_helper
"""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from scripts._sys._output import print_output, print_error
from scripts.biz.supply_chain_helper.service import auto_switch_supply as _auto_switch_supply
from scripts.biz.supply_chain_helper.service import execute_downstream_link as _execute_downstream_link


def auto_switch_supply(
    offer_ids: str = "",
    sku_id: str = "",
    reason: str = "",
    offer_title: str = "",
    current_price: str = "",
    downstream_item_id: str = "",
    downstream_channel: str = "",
    isv_app_key: str = "",
    offer_image_url: str = "",
):
    """自动换供 - 基于三层流水线架构（同款筛选失败时 fallback 到图搜）

    用法：
        python3 scripts/cli.py supply_chain_helper auto_switch_supply --offer_ids=688001234,688005678
        python3 scripts/cli.py supply_chain_helper auto_switch_supply --offer_ids=688001234 --sku_id=xxx --reason=亏损换供
        python3 scripts/cli.py supply_chain_helper auto_switch_supply --offer_ids=688001234 --offer_image_url=https://xxx.jpg
    """
    try:
        if not offer_ids:
            print_output(False, "❌ 缺少必填参数 offer_ids", {})
            return

        offer_id_list = [id.strip() for id in offer_ids.split(",") if id.strip()]

        result = _auto_switch_supply(
            offer_ids=offer_id_list,
            sku_id=sku_id if sku_id else None,
            reason=reason if reason else None,
            offer_title=offer_title if offer_title else None,
            current_price=current_price if current_price else None,
            downstream_item_id=downstream_item_id if downstream_item_id else None,
            downstream_channel=downstream_channel if downstream_channel else None,
            isv_app_key=isv_app_key if isv_app_key else None,
            offer_image_url=offer_image_url if offer_image_url else None,
        )

        if result.get('success'):
            data = result.get('data', {})
            md = f"""## 自动换供完成

**处理商品数**: {data.get('total', 0)}
**替换成功**: {data.get('success', 0)}
**替换失败**: {data.get('failed', 0)}

### 换供详情
"""
            for item in data.get('items', []):
                status = item.get('status', 'UNKNOWN')

                # 判断状态图标
                if status == 'REPLACED':
                    status_icon = "✅"
                    status_text = "替换成功"
                elif status == 'SUCCESS':
                    status_icon = "📝"
                    status_text = "匹配成功但未替换"
                elif status == 'FAILED':
                    status_icon = "❌"
                    status_text = "失败"
                else:
                    status_icon = "⏭️"
                    status_text = status

                md += f"\n{status_icon} **{item.get('offer_id')}** - {status_text}\n"

                if status == 'REPLACED':
                    md += f"   - 下游商品: {item.get('downstream_item_id', '-')}\n"
                    md += f"   - 原商品: ¥{item.get('current_price', '-')} → 新商品: ¥{item.get('recommend_price', '-')}\n"
                    md += f"   - 新商品ID: {item.get('recommend_offer_id', '-')}\n"
                    md += f"   - 推荐理由: {item.get('recommend_reason', '-')}\n"
                elif status == 'SUCCESS':
                    md += f"   - 匹配成功但未执行替换（可能缺少下游商品ID）\n"
                    md += f"   - 推荐商品: {item.get('recommend_offer_id', '-')} (¥{item.get('recommend_price', '-')})\n"
                elif status == 'FAILED':
                    error_msg = item.get('error') or item.get('replace_message', '未知错误')
                    md += f"   - 失败原因: {error_msg}\n"

            print_output(True, md, result)
        else:
            print_output(False, f"换供失败: {result.get('error', '未知错误')}", result)
    except Exception as e:
        print_error(e)


def downstream_link(
    app_key: str = "",
    shop_id: str = "",
    shop_nick: str = "",
    local_item_id: str = "",
    source_offer_url: str = "",
    purchase_account: str = "",
    platform: str = "taobao",
    use_preview: bool = True,
    limit_rows: int = 0,
):
    """
    调用 ISV 技能执行下游关联货源

    用法：
        python3 scripts/cli.py supply_chain_helper downstream_link \
            --app_key=9631867 \
            --shop_id=12345 \
            --shop_nick=我的店铺 \
            --local_item_id=67890 \
            --source_offer_url=https://detail.1688.com/offer/xxxx.html \
            --purchase_account=采购账号1 \
            --platform=taobao
    """
    try:
        if not app_key or not shop_id or not local_item_id or not source_offer_url:
            print_output(False, "❌ 缺少必填参数（app_key, shop_id, local_item_id, source_offer_url）", {})
            return

        result = _execute_downstream_link(
            app_key=app_key,
            shop_id=shop_id,
            shop_nick=shop_nick,
            local_item_id=local_item_id,
            source_offer_url=source_offer_url,
            purchase_account=purchase_account,
            platform=platform,
            use_preview=use_preview in (True, "true", "True", "1"),
            limit_rows=limit_rows if limit_rows > 0 else None,
        )

        if result.get("success"):
            md = f"✅ {result.get('message', '下游关联货源成功')}"
        else:
            md = f"❌ {result.get('message', '下游关联货源失败')}"

        print_output(result.get("success", False), md, result)
    except Exception as e:
        print_error(e)
