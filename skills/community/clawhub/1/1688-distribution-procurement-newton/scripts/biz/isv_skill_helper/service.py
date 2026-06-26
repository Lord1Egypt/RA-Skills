#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISV Skill 调用服务

负责发现和调用 ISV 技能（如 fx-procurement-9018264、fx-distribute-offer-{appKey} 等）。
从 1688-distribution-distribute-offer 复制并适配。
"""

import json
import os
import subprocess
import sys
from typing import Optional, Dict, List

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from scripts._sys._skill_discovery import (
    find_isv_skill,
    find_skill_by_name,
    find_best_isv_skill,
    discover_builtin_isv_skills,
)
from scripts._sys._errors import ServiceError


def list_builtin_isv_skills() -> List[Dict]:
    """
    列举所有项目内置的 ISV 技能（从 Provider 注册表获取）。

    :return: [{"name": "zhangfei", "display_name": "...", "app_keys": [...], "provider_dir": "..."}, ...]
    """
    try:
        from scripts.isv.base import get_all_providers
        providers = get_all_providers()
        return [
            {
                "name": provider.name,
                "display_name": provider.display_name,
                "app_keys": provider.app_keys,
                "provider_dir": provider.provider_dir,
            }
            for provider in providers.values()
        ]
    except ImportError:
        return discover_builtin_isv_skills()


def discover_isv_skill(app_key: str) -> Dict:
    """
    根据 appKey 查找已安装的 ISV 技能。

    :param app_key: 三方服务商唯一标识
    :return: {"found": True, "skill_name": "...", "skill_path": "..."}
             或 {"found": False}
    """
    return find_isv_skill(app_key)


def discover_skill_by_name(skill_name: str) -> Dict:
    """
    根据技能名称查找已安装的技能。

    :param skill_name: 技能名称（如 "fx-procurement-9018264"）
    :return: {"found": True, "skill_name": "...", "skill_path": "..."}
             或 {"found": False}
    """
    return find_skill_by_name(skill_name)


def discover_best_isv_skill(tool_list: List[Dict]) -> Dict:
    """
    从 toolList 中查找最优的 ISV 铺货技能。

    :param tool_list: shop_and_tool_info 返回的 toolList
    :return: {"found": True, "app_key": "...", "skill_name": "...", ...}
             或 {"found": False}
    """
    return find_best_isv_skill(tool_list)


def _run_isv_cli(skill_path: str, command: str, token: str, extra_args: List[str] = None) -> Dict:
    """
    调用 ISV 技能的 cli.py 命令。

    :param skill_path: ISV 技能目录路径
    :param command: 子命令（如 confirm-link, log, publish 等）
    :param token: ISV Token
    :param extra_args: 额外参数列表
    :return: 解析后的 JSON 响应
    :raises ServiceError: 调用失败时抛出异常
    """
    if not skill_path or not os.path.isdir(skill_path):
        raise ServiceError(f"ISV 技能目录不存在: {skill_path}")

    cmd = [sys.executable, "cli.py", command, "--token", token]
    if extra_args:
        cmd.extend(extra_args)

    try:
        result = subprocess.run(
            cmd,
            cwd=skill_path,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        raise ServiceError("ISV 技能调用超时")
    except Exception as e:
        raise ServiceError(f"ISV 技能调用异常: {e}")

    if result.returncode != 0:
        stderr = result.stderr.strip() if result.stderr else ""
        raise ServiceError(f"ISV 技能执行失败: {stderr}")

    stdout = result.stdout.strip()
    if not stdout:
        return {}

    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        # 返回原始文本
        return {"raw_output": stdout}


def call_isv_link_supply(
    skill_path: str,
    token: str,
    shop_id: str,
    shop_nick: str,
    local_item_id: str,
    source_offer_url: str,
    purchase_account: str,
    platform: str = "taobao",
    limit_rows: Optional[int] = None,
) -> Dict:
    """
    调用 ISV 技能执行关联货源（confirm-link）。

    :param skill_path: ISV 技能目录路径
    :param token: ISV Token
    :param shop_id: 店铺 ID
    :param shop_nick: 店铺名称
    :param local_item_id: 下游商品 ID
    :param source_offer_url: 1688 货源链接
    :param purchase_account: 采购账号
    :param platform: 平台（taobao/douyin）
    :param limit_rows: 仅提交前 N 条 SKU 映射（可选）
    :return: ISV 技能返回结果
    """
    if platform == "taobao":
        extra_args = [
            "--shop-id", shop_id,
            "--shop-nick", shop_nick,
            "--local-item-id", local_item_id,
            "--source-offer-url", source_offer_url,
            "--purchase-account", purchase_account,
        ]
        if limit_rows:
            extra_args.extend(["--limit-rows", str(limit_rows)])
        return _run_isv_cli(skill_path, "confirm-link", token, extra_args)

    elif platform == "douyin":
        # 抖音使用 douyin-confirm-link，无 SKU 预览
        extra_args = [
            "--shop-id", shop_id,
            "--shop-nick", shop_nick,
            "--local-item-id", local_item_id,
            "--source-offer-url", source_offer_url,
        ]
        return _run_isv_cli(skill_path, "douyin-confirm-link", token, extra_args)

    else:
        raise ServiceError(f"不支持的平台: {platform}")


def call_isv_link_preview(
    skill_path: str,
    token: str,
    shop_id: str,
    shop_nick: str,
    local_item_id: str,
    source_offer_url: str,
    purchase_account: str,
) -> Dict:
    """
    调用 ISV 技能执行 SKU 预览匹配（淘宝专用）。

    :param skill_path: ISV 技能目录路径
    :param token: ISV Token
    :param shop_id: 店铺 ID
    :param shop_nick: 店铺名称
    :param local_item_id: 下游商品 ID
    :param source_offer_url: 1688 货源链接
    :param purchase_account: 采购账号
    :return: SKU 匹配预览结果
    """
    extra_args = [
        "--shop-id", shop_id,
        "--shop-nick", shop_nick,
        "--local-item-id", local_item_id,
        "--source-offer-url", source_offer_url,
        "--purchase-account", purchase_account,
    ]
    return _run_isv_cli(skill_path, "link-preview", token, extra_args)


def call_isv_distribute_log(
    skill_path: str,
    token: str,
    product_id: Optional[str] = None,
    shop_code: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: Optional[int] = None,
) -> Dict:
    """
    调用 ISV 技能查询铺货日志。

    :param skill_path: ISV 技能目录路径
    :param token: ISV Token
    :param product_id: 商品 ID（可选）
    :param shop_code: 店铺编码（可选）
    :param start_date: 开始日期（可选）
    :param end_date: 结束日期（可选）
    :param limit: 返回数量限制（可选）
    :return: 铺货日志数据
    """
    extra_args = []
    if product_id:
        extra_args.extend(["--product-id", product_id])
    if shop_code:
        extra_args.extend(["--shop-code", shop_code])
    if start_date:
        extra_args.extend(["--start-date", start_date])
    if end_date:
        extra_args.extend(["--end-date", end_date])
    if limit:
        extra_args.extend(["--limit", str(limit)])

    return _run_isv_cli(skill_path, "log", token, extra_args)


def call_isv_publish(
    skill_path: str,
    token: str,
    shop_code: str,
    item_ids: str,
) -> Dict:
    """
    调用 ISV 技能执行铺货。

    :param skill_path: ISV 技能目录路径
    :param token: ISV Token
    :param shop_code: 店铺编码
    :param item_ids: 商品 ID，逗号分隔
    :return: 铺货结果
    """
    extra_args = [
        "--shop-code", shop_code,
        "--item-ids", item_ids,
    ]
    return _run_isv_cli(skill_path, "publish", token, extra_args)
