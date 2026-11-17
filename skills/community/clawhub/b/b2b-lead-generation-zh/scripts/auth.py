#!/usr/bin/env python3
"""
跨境魔方认证管理
提供 API 密钥申请、充值、账户信息、接口定价查询等功能。

本聚合技能(auth.py / common.py / version_check.py 全技能唯一一份)覆盖以下原始技能,
定价查询已解耦:不再硬依赖目录名 basename(SKILL_BASE_DIR)。
"""
import argparse
import json
import os
import sys

from common import print_json_output, make_request, API_KEY_ENV, UPKUAJING_ENV_FILE, UPKUAJING_DIR, SKILL_BASE_DIR


# 本聚合技能覆盖的原始技能名(用于 price_info 兜底:当平台未注册聚合名时,
# 遍历这些原始技能名查询 /agent/api/list 并合并定价,保证定价始终可查)。
ORIGINAL_SKILL_NAMES = [
    # customs-analysis (6)
    "customs-analysis-area", "customs-analysis-hscode-detail", "customs-analysis-hscode-search",
    "customs-analysis-overview", "customs-analysis-trade-percent", "customs-analysis-trends",
    # customs-company (9)
    "customs-company-area-list", "customs-company-area-stats", "customs-company-hscode-list",
    "customs-company-hscode-stats", "customs-company-partner-stats", "customs-company-port-list",
    "customs-company-product-list", "customs-company-stats", "customs-company-trends",
    # customs-overview (6)
    "customs-overview-date", "customs-overview-summary", "customs-overview-top-n",
    "customs-overview-trade-list", "customs-overview-trend", "customs-overview-us-import",
    # global-company depth (9)
    "global-company-search", "global-company-employee", "global-company-shareholder",
    "global-company-person-search", "global-company-person-colleague", "global-company-person-alumni",
    "global-company-person-experience", "global-company-person-education", "global-company-person-school-detail",
    # linkedin (8)
    "linkedin-company-search", "linkedin-company-employee", "linkedin-person-search",
    "linkedin-person-colleague", "linkedin-person-alumni", "linkedin-person-experience",
    "linkedin-person-education", "linkedin-person-school-detail",
]


def new_key() -> dict:
    """
    申请新的 API 密钥。
    """
    # 检查是否已存在 .env 文件和 API key
    env_file = UPKUAJING_ENV_FILE

    if env_file.exists():
        # 读取现有的 .env 文件
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # 检查是否已有 API key
                for line in content.splitlines():
                    line = line.strip()
                    if line.startswith(f'{API_KEY_ENV}='):
                        existing_key = line.split('=', 1)[1].strip()
                        if existing_key:
                            return {
                                "success": False,
                                "message": f"错误：{env_file} 中已存在API密钥（{existing_key[:10]}...）。\n如需重新申请，请先删除文件中的 {API_KEY_ENV} 后再运行此命令。",
                                "envFilePath": str(env_file)
                            }
        except IOError:
            pass  # 如果读取失败，继续执行

    # 不需要认证申请新密钥
    response = make_request('/agent/auth/create', {}, require_auth=False)

    # 检查是否申请成功
    if response.get('code') != 0:
        error_msg = response.get('msg', '未知错误')
        return {
            "success": False,
            "message": f"API密钥申请失败：{error_msg}。请稍后重试或联系技术支持。"
        }

    # 提取 apiKey
    data = response.get('data', {})
    api_key = data.get('apiKey')

    if not api_key:
        return {
            "success": False,
            "message": "API密钥申请失败：服务器响应格式异常，未返回apiKey。"
        }

    # 确保 ~/.upkuajing 目录存在
    try:
        UPKUAJING_DIR.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        return {
            "success": False,
            "message": f"API密钥申请成功，但创建目录失败：{str(e)}。\n请手动创建目录 {UPKUAJING_DIR} 并设置环境变量 {API_KEY_ENV}。",
            "envFilePath": str(env_file)
        }

    # 保存到 .env 文件
    try:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(f"{API_KEY_ENV}={api_key}\n")
    except IOError as e:
        return {
            "success": False,
            "message": f"API密钥申请成功，但保存到 .env 文件失败：{str(e)}。\n请手动设置环境变量 {API_KEY_ENV}。",
            "envFilePath": str(env_file)
        }

    # 返回成功结果
    return {
        "success": True,
        "message": f"API密钥申请成功！密钥已保存到：{env_file}\n请妥善保管密钥，请勿泄露给他人。",
        "envFilePath": str(env_file)
    }


def account_info() -> dict:
    """
    获取账户信息并格式化返回
    """
    response = make_request('/agent/auth/info', {})

    if response.get('code') != 0:
        return response

    # 提取数据
    data = response.get('data', {})

    # 格式化余额信息（单位：分钱）
    org_balance = data.get('orgBalance', 0)
    api_balance = data.get('apiBalance', 0)

    result = {
        '跨境魔方账号': data.get('orgPhone', ''),
        '跨境魔方账号余额': f'{org_balance}分钱(RMB)',
        '跨境魔方开放平台账号': data.get('apiAccount', ''),
        '跨境魔方开放平台账号余额': f'{api_balance}分钱(RMB)'
    }

    return result


def new_rec_order() -> dict:
    """
    创建充值订单，返回支付地址
    """
    response = make_request('/agent/auth/pay/url', {})
    return response


def price_info() -> dict:
    """
    获取开放平台接口定价信息。

    已解耦:不再硬依赖 basename(SKILL_BASE_DIR) 查平台。
    1) 优先不传 name 拉 /agent/api/list 全量(与 SKILL.md "returns complete pricing
       for all interfaces" 描述一致);
    2) 若平台要求 name(全量返回空/错误),则遍历 ORIGINAL_SKILL_NAMES 逐个查询并合并。
    无论平台是否注册聚合名,定价都能查到。
    """
    # 1) 优先:不传 name,拉取全量接口定价
    try:
        response = make_request('/agent/api/list', {})
        data = response.get('data') if isinstance(response, dict) else None
        if response.get('code') == 0 and data:
            return response
    except Exception:
        pass

    # 2) 兜底:平台可能要求 name,遍历原始技能名合并定价
    merged = []
    seen = set()
    for name in ORIGINAL_SKILL_NAMES:
        try:
            r = make_request('/agent/api/list', {"name": name})
            if not isinstance(r, dict) or r.get('code') != 0:
                continue
            d = r.get('data')
            if not d:
                continue
            items = d if isinstance(d, list) else [d]
            for it in items:
                key = json.dumps(it, ensure_ascii=False, sort_keys=True)
                if key not in seen:
                    seen.add(key)
                    merged.append(it)
        except Exception:
            continue

    return {"code": 0, "data": merged, "msg": "merged pricing from original skill names"}


def main():
    parser = argparse.ArgumentParser(
        description='跨境魔方认证管理'
    )
    parser.add_argument(
        '--new_key',
        action='store_true',
        help='申请新的 API 密钥'
    )
    parser.add_argument(
        '--account_info',
        action='store_true',
        help='获取当前账户信息'
    )
    parser.add_argument(
        '--new_rec_order',
        action='store_true',
        help='创建充值订单'
    )
    parser.add_argument(
        '--price_info',
        action='store_true',
        help='获取开放平台接口定价信息'
    )

    args = parser.parse_args()

    # 验证至少指定一个操作
    action_count = sum([
        args.new_key,
        args.account_info,
        args.new_rec_order,
        args.price_info
    ])

    if action_count == 0:
        print("错误：请指定要执行的操作", file=sys.stderr)
        print("可用操作：--new_key, --account_info, --new_rec_order, --price_info", file=sys.stderr)
        sys.exit(1)

    if action_count > 1:
        print("错误：一次只能执行一个操作", file=sys.stderr)
        sys.exit(1)

    # 执行相应的操作
    if args.new_key:
        result = new_key()
        # new_key 返回的是格式化的结果，直接打印
        print(result.get('message', json.dumps(result, ensure_ascii=False, indent=2)))

    elif args.account_info:
        result = account_info()
        print_json_output(result)

    elif args.new_rec_order:
        result = new_rec_order()
        print_json_output(result)

    elif args.price_info:
        result = price_info()
        print_json_output(result)


if __name__ == '__main__':
    main()
