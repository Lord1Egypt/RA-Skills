#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISV Skill 调用命令"""

import json
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from scripts._sys._output import print_output, print_error
from scripts.biz.isv_skill_helper.service import (
    discover_isv_skill,
    discover_skill_by_name,
    discover_best_isv_skill,
    list_builtin_isv_skills,
    call_isv_link_supply,
    call_isv_link_preview,
    call_isv_distribute_log,
    call_isv_publish,
)


def find_skill(app_key: str = "", skill_name: str = ""):
    """
    查找已安装的 ISV 技能

    :param app_key: 按 appKey 查找（如 9631867）
    :param skill_name: 按技能名称查找（如 fx-procurement-9018264）
    """
    try:
        if app_key:
            result = discover_isv_skill(app_key)
        elif skill_name:
            result = discover_skill_by_name(skill_name)
        else:
            print_output(False, "❌ 请提供 app_key 或 skill_name 参数", {})
            return

        if result.get("found"):
            md = f"✅ 找到 ISV 技能：{result['skill_name']}\n路径：{result['skill_path']}"
        else:
            md = "❌ 未找到匹配的 ISV 技能"

        print_output(result.get("found", False), md, result)
    except Exception as e:
        print_error(e)


def list_builtin():
    """列举所有项目内置的 ISV 技能"""
    try:
        skills = list_builtin_isv_skills()
        if skills:
            lines = [f"✅ 共发现 {len(skills)} 个内置 ISV Provider："]
            for idx, skill in enumerate(skills, 1):
                name = skill.get("name", skill.get("skill_name", "unknown"))
                display = skill.get("display_name", "")
                app_keys = skill.get("app_keys", [])
                path = skill.get("provider_dir", skill.get("skill_path", ""))
                label = f"{name}"
                if display:
                    label += f"（{display}）"
                if app_keys:
                    label += f" [appKeys: {', '.join(app_keys)}]"
                lines.append(f"  {idx}. {label}")
                if path:
                    lines.append(f"     路径：{path}")
            md = "\n".join(lines)
        else:
            md = "❌ 未发现内置 ISV 技能"
        print_output(bool(skills), md, {"skills": skills})
    except Exception as e:
        print_error(e)


def link_supply(
    skill_path: str = "",
    token: str = "",
    shop_id: str = "",
    shop_nick: str = "",
    local_item_id: str = "",
    source_offer_url: str = "",
    purchase_account: str = "",
    platform: str = "taobao",
    limit_rows: int = 0,
):
    """
    调用 ISV 技能执行关联货源

    :param skill_path: ISV 技能目录路径
    :param token: ISV Token
    :param shop_id: 店铺 ID
    :param shop_nick: 店铺名称
    :param local_item_id: 下游商品 ID
    :param source_offer_url: 1688 货源链接
    :param purchase_account: 采购账号
    :param platform: 平台（taobao/douyin）
    :param limit_rows: 仅提交前 N 条 SKU 映射（可选）
    """
    try:
        if not skill_path or not token or not shop_id or not local_item_id or not source_offer_url:
            print_output(False, "❌ 缺少必填参数（skill_path, token, shop_id, local_item_id, source_offer_url）", {})
            return

        result = call_isv_link_supply(
            skill_path=skill_path,
            token=token,
            shop_id=shop_id,
            shop_nick=shop_nick,
            local_item_id=local_item_id,
            source_offer_url=source_offer_url,
            purchase_account=purchase_account,
            platform=platform,
            limit_rows=limit_rows if limit_rows > 0 else None,
        )
        print_output(True, "## ISV 关联货源结果", result)
    except Exception as e:
        print_error(e)


def link_preview(
    skill_path: str = "",
    token: str = "",
    shop_id: str = "",
    shop_nick: str = "",
    local_item_id: str = "",
    source_offer_url: str = "",
    purchase_account: str = "",
):
    """
    调用 ISV 技能执行 SKU 预览匹配（淘宝专用）

    :param skill_path: ISV 技能目录路径
    :param token: ISV Token
    :param shop_id: 店铺 ID
    :param shop_nick: 店铺名称
    :param local_item_id: 下游商品 ID
    :param source_offer_url: 1688 货源链接
    :param purchase_account: 采购账号
    """
    try:
        if not skill_path or not token or not shop_id or not local_item_id or not source_offer_url:
            print_output(False, "❌ 缺少必填参数", {})
            return

        result = call_isv_link_preview(
            skill_path=skill_path,
            token=token,
            shop_id=shop_id,
            shop_nick=shop_nick,
            local_item_id=local_item_id,
            source_offer_url=source_offer_url,
            purchase_account=purchase_account,
        )
        print_output(True, "## SKU 匹配预览结果", result)
    except Exception as e:
        print_error(e)


def distribute_log(
    skill_path: str = "",
    token: str = "",
    product_id: str = "",
    shop_code: str = "",
    start_date: str = "",
    end_date: str = "",
    limit: int = 0,
):
    """
    调用 ISV 技能查询铺货日志

    :param skill_path: ISV 技能目录路径
    :param token: ISV Token
    :param product_id: 商品 ID（可选）
    :param shop_code: 店铺编码（可选）
    :param start_date: 开始日期（可选）
    :param end_date: 结束日期（可选）
    :param limit: 返回数量限制（可选）
    """
    try:
        if not skill_path or not token:
            print_output(False, "❌ 缺少必填参数（skill_path, token）", {})
            return

        result = call_isv_distribute_log(
            skill_path=skill_path,
            token=token,
            product_id=product_id or None,
            shop_code=shop_code or None,
            start_date=start_date or None,
            end_date=end_date or None,
            limit=limit if limit > 0 else None,
        )
        print_output(True, "## 铺货日志查询结果", result)
    except Exception as e:
        print_error(e)


def publish(
    skill_path: str = "",
    token: str = "",
    shop_code: str = "",
    item_ids: str = "",
):
    """
    调用 ISV 技能执行铺货

    :param skill_path: ISV 技能目录路径
    :param token: ISV Token
    :param shop_code: 店铺编码
    :param item_ids: 商品 ID，逗号分隔
    """
    try:
        if not skill_path or not token or not shop_code or not item_ids:
            print_output(False, "❌ 缺少必填参数（skill_path, token, shop_code, item_ids）", {})
            return

        result = call_isv_publish(
            skill_path=skill_path,
            token=token,
            shop_code=shop_code,
            item_ids=item_ids,
        )
        print_output(True, "## 铺货结果", result)
    except Exception as e:
        print_error(e)
