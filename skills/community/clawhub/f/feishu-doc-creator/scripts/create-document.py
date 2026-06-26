#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Feishu Document Creator - Command Line Interface
飞书文档创建器 - 命令行工具

Created for OpenClaw @larksuite/openclaw-lark plugin

Can be called directly by agents, automatically reads Feishu configuration
from OpenClaw config file (~/.openclaw/openclaw.json)
"""

import os
import json
import argparse
import requests
import sys
from typing import Dict, Any, Tuple, Optional, List
from datetime import datetime


def load_openclaw_config() -> Dict[str, Any]:
    """从OpenClaw配置文件加载飞书配置

    Returns:
        Dict[str, Any]: 配置字典，包含app_id和app_secret，如果加载失败返回空字典
    """
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    if not os.path.exists(config_path):
        return {}

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception:
        return {}

    # 查找飞书配置
    # 典型结构: channels.feishu.accounts.main.appId/appSecret
    try:
        feishu_config = config.get('channels', {}).get('feishu', {})
        accounts = feishu_config.get('accounts', {})

        # 优先使用 main 账号
        if 'main' in accounts:
            main_config = accounts['main']
            return {
                'app_id': main_config.get('appId') or main_config.get('app_id'),
                'app_secret': main_config.get('appSecret') or main_config.get('app_secret')
            }

        # 如果没有main，使用第一个找到的账号
        if accounts:
            first_account = next(iter(accounts.values()))
            return {
                'app_id': first_account.get('appId') or first_account.get('app_id'),
                'app_secret': first_account.get('appSecret') or first_account.get('app_secret')
            }
    except Exception:
        pass

    return {}


def get_tenant_access_token(app_id: str, app_secret: str) -> Tuple[str, Exception]:
    """获取 tenant_access_token

    Args:
        app_id: 应用ID
        app_secret: 应用密钥

    Returns:
        Tuple[str, Exception]: (access_token, error)
    """
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()

        if result.get("code", 0) != 0:
            return "", Exception(f"failed to get tenant_access_token: {result.get('msg', 'unknown error')}")

        return result["tenant_access_token"], None

    except Exception as e:
        if hasattr(e, 'response') and e.response is not None:
            return "", Exception(f"getting tenant_access_token: {e}, response: {e.response.text}")
        return "", e


def get_user_info(tenant_access_token: str, open_id: str) -> Tuple[Dict[str, Any], Exception]:
    """获取用户信息

    Args:
        tenant_access_token: 租户访问令牌
        open_id: 用户open_id

    Returns:
        Tuple[Dict[str, Any], Exception]: (user_info, error)
    """
    url = f"https://open.feishu.cn/open-apis/contact/v3/users/{open_id}?user_id_type=open_id"
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        result = response.json()

        if result.get("code", 0) != 0:
            return {}, Exception(f"failed to get user info: {result.get('msg', 'unknown error')}")

        if not result.get("data") or not result["data"].get("user"):
            return {}, Exception("未获取到用户信息")

        return result["data"]["user"], None

    except Exception as e:
        return {}, e


def create_bitable(tenant_access_token: str, name: str) -> Tuple[str, Exception]:
    """创建多维表格

    Args:
        tenant_access_token: 租户访问令牌
        name: 多维表格名称

    Returns:
        Tuple[str, Exception]: (app_token, error)
    """
    url = "https://open.feishu.cn/open-apis/bitable/v1/apps"
    payload = {
        "name": name
    }
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()

        if result.get("code", 0) != 0:
            return "", Exception(f"failed to create bitable: {result.get('msg', 'unknown error')}")

        if not result.get("data") or not result["data"].get("app"):
            return "", Exception("未获取到多维表格信息")

        app_token = result["data"]["app"].get("app_token", "")
        if not app_token:
            return "", Exception("未获取到app_token")

        return app_token, None

    except Exception as e:
        return "", e


def create_docx(tenant_access_token: str, title: str) -> Tuple[str, Exception]:
    """创建云文档

    Args:
        tenant_access_token: 租户访问令牌
        title: 文档标题

    Returns:
        Tuple[str, Exception]: (document_id, error)
    """
    url = "https://open.feishu.cn/open-apis/docx/v1/documents"
    payload = {
        "title": title
    }
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()

        if result.get("code", 0) != 0:
            return "", Exception(f"failed to create docx: {result.get('msg', 'unknown error')}")

        if not result.get("data") or not result["data"].get("document"):
            return "", Exception("未获取到文档信息")

        document_id = result["data"]["document"].get("document_id", "")
        if not document_id:
            return "", Exception("未获取到document_id")

        return document_id, None

    except Exception as e:
        return "", e


def create_spreadsheet(tenant_access_token: str, title: str) -> Tuple[str, Exception]:
    """创建电子表格

    Args:
        tenant_access_token: 租户访问令牌
        title: 电子表格标题

    Returns:
        Tuple[str, Exception]: (spreadsheet_token, error)
    """
    url = "https://open.feishu.cn/open-apis/sheets/v3/spreadsheets"
    payload = {
        "title": title
    }
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()

        if result.get("code", 0) != 0:
            return "", Exception(f"failed to create spreadsheet: {result.get('msg', 'unknown error')}")

        if not result.get("data") or not result["data"].get("spreadsheet"):
            return "", Exception("未获取到电子表格信息")

        spreadsheet_token = result["data"]["spreadsheet"].get("spreadsheet_token", "")
        if not spreadsheet_token:
            return "", Exception("未获取到spreadsheet_token")

        return spreadsheet_token, None

    except Exception as e:
        return "", e


def create_slide(tenant_access_token: str, title: str) -> Tuple[str, Exception]:
    """创建幻灯片

    Args:
        tenant_access_token: 租户访问令牌
        title: 幻灯片标题

    Returns:
        Tuple[str, Exception]: (presentation_id, error)
    """
    url = "https://open.feishu.cn/open-apis/slides/v1/presentations"
    payload = {
        "title": title
    }
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()

        if result.get("code", 0) != 0:
            return "", Exception(f"failed to create slide: {result.get('msg', 'unknown error')}")

        if not result.get("data") or not result["data"].get("presentation"):
            return "", Exception("未获取到幻灯片信息")

        presentation_id = result["data"]["presentation"].get("presentation_id", "")
        if not presentation_id:
            return "", Exception("未获取到presentation_id")

        return presentation_id, None

    except Exception as e:
        return "", e



def add_collaborator(tenant_access_token: str, token: str, token_type: str, member_type: str, member_id: str, perm: str) -> Tuple[bool, Exception]:
    """添加协作者

    Args:
        tenant_access_token: 租户访问令牌
        token: 文档token
        token_type: 文档类型
        member_type: 成员类型 (openid/email/userid等)
        member_id: 成员ID
        perm: 权限 (view/edit/full_access)

    Returns:
        Tuple[bool, Exception]: (success, error)
    """
    url = f"https://open.feishu.cn/open-apis/drive/v1/permissions/{token}/members?type={token_type}&need_notification=false"
    payload = {
        "member_type": member_type,
        "member_id": member_id,
        "perm": perm
    }
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()

        if result.get("code", 0) != 0:
            return False, Exception(f"failed to add collaborator: {result.get('msg', 'unknown error')}")

        return True, None

    except Exception as e:
        return False, e


def update_permission_settings(tenant_access_token: str, token: str, token_type: str) -> Tuple[bool, Exception]:
    """更新文档权限设置为企业内成员可见

    Args:
        tenant_access_token: 租户访问令牌
        token: 文档token
        token_type: 文档类型

    Returns:
        Tuple[bool, Exception]: (success, error)
    """
    url = f"https://open.feishu.cn/open-apis/drive/v1/permissions/{token}/settings?type={token_type}"
    payload = {
        "link_share": {
            "enabled": True,
            "share_entity": "tenant",
            "access": "view"
        }
    }
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    try:
        response = requests.put(url, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()

        if result.get("code", 0) != 0:
            return False, Exception(f"failed to update permission settings: {result.get('msg', 'unknown error')}")

        return True, None

    except Exception as e:
        return False, e


def transfer_owner(tenant_access_token: str, token: str, token_type: str, new_owner_id: str) -> Tuple[bool, Exception]:
    """转移文档所有者

    Args:
        tenant_access_token: 租户访问令牌
        token: 文档token (app_token、document_id、spreadsheet_token或presentation_id)
        token_type: 文档类型 (bitable、docx、spreadsheet或slide)
        new_owner_id: 新所有者的open_id或应用ID

    Returns:
        Tuple[bool, Exception]: (success, error)
    """
    type_mapping = {
        "bitable": "bitable",
        "docx": "docx",
        "spreadsheet": "sheet",
        "slide": "slide"
    }

    if token_type not in type_mapping:
        return False, Exception(f"不支持的文档类型: {token_type}")

    url = f"https://open.feishu.cn/open-apis/drive/v1/permissions/{token}/members/transfer_owner?type={type_mapping[token_type]}"

    # 检查是否是应用ID (以cli_开头)
    if new_owner_id.startswith("cli_"):
        payload = {
            "member_type": "app_id",
            "member_id": new_owner_id
        }
    else:
        payload = {
            "member_type": "openid",
            "member_id": new_owner_id
        }
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()

        if result.get("code", 0) != 0:
            return False, Exception(f"failed to transfer owner: {result.get('msg', 'unknown error')}")

        return True, None

    except Exception as e:
        return False, e


def send_interactive_message(tenant_access_token: str, receive_id: str, card_content: Dict[str, Any]) -> Tuple[Dict[str, Any], Exception]:
    """发送卡片消息

    Args:
        tenant_access_token: 租户访问令牌
        receive_id: 接收者ID (open_id)
        card_content: 卡片内容

    Returns:
        Tuple[Dict[str, Any], Exception]: (message_info, error)
    """
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"

    # 使用内嵌卡片格式，不需要template_id
    doc_type = card_content['template_variable'].get('doc_type', '文档')
    content_str = json.dumps({
        "config": {
            "wide_screen_mode": True
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "content": f"已为您创建{doc_type}：**{card_content['template_variable']['name']}**",
                    "tag": "lark_md"
                }
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "content": "📄 打开文档",
                            "tag": "plain_text"
                        },
                        "type": "primary",
                        "url": card_content['template_variable']['link']
                    }
                ]
            }
        ],
        "header": {
            "template": "blue",
            "title": {
                "content": f"{doc_type}创建成功",
                "tag": "plain_text"
            }
        }
    }, ensure_ascii=False)

    payload = {
        "receive_id": receive_id,
        "msg_type": "interactive",
        "content": content_str
    }
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()

        if result.get("code", 0) != 0:
            return {}, Exception(f"failed to send interactive message: {result.get('msg', 'unknown error')}")

        if not result.get("data"):
            return {}, Exception("未获取到消息发送结果")

        return result["data"], None

    except Exception as e:
        return {}, e


def create_docx_with_permissions(
    tenant_access_token: str,
    title: str,
    target_app_open_id: str,
    admin_open_ids: List[str],
    current_user_open_id: str
) -> Tuple[str, Exception]:
    """创建云文档并设置特殊权限（用于wen_admin模式）

    Args:
        tenant_access_token: 租户访问令牌
        title: 文档标题
        target_app_open_id: 目标机器人应用的open_id
        admin_open_ids: 管理者的open_id列表
        current_user_open_id: 当前用户（点击按钮的用户）的open_id

    Returns:
        Tuple[str, Exception]: (document_id, error)
    """
    # 创建云文档
    document_id, err = create_docx(tenant_access_token, title)
    if err:
        return "", err

    # 转移文档所有者给目标应用
    _, err = transfer_owner(tenant_access_token, document_id, "docx", target_app_open_id)
    if err:
        print(f"警告: 转移文档所有者给目标应用失败: {err}", file=sys.stderr)

    # 添加指定的管理者
    for admin_id in admin_open_ids:
        _, err = add_collaborator(tenant_access_token, document_id, "docx", "openid", admin_id, "full_access")
        if err:
            print(f"警告: 添加管理者 {admin_id} 失败: {err}", file=sys.stderr)

    # 添加当前用户为管理者（如果当前用户不在管理者列表中）
    if current_user_open_id not in admin_open_ids:
        _, err = add_collaborator(tenant_access_token, document_id, "docx", "openid", current_user_open_id, "full_access")
        if err:
            print(f"警告: 添加当前用户为管理者失败: {err}", file=sys.stderr)

    # 设置企业内成员可见
    _, err = update_permission_settings(tenant_access_token, document_id, "docx")
    if err:
        print(f"警告: 设置企业内成员可见失败: {err}", file=sys.stderr)

    return document_id, None


def get_document_url(doc_type: str, token: str) -> str:
    """根据文档类型获取文档URL

    Args:
        doc_type: 文档类型
        token: 文档token

    Returns:
        str: 文档URL
    """
    url_mapping = {
        'bitable': f"https://feishu.cn/base/{token}",
        'docx': f"https://feishu.cn/docx/{token}",
        'spreadsheet': f"https://feishu.cn/sheets/{token}",
        'slide': f"https://feishu.cn/slides/{token}"
    }
    return url_mapping.get(doc_type, f"https://feishu.cn/{token}")


def get_document_type_name(doc_type: str) -> str:
    """获取文档类型中文名称

    Args:
        doc_type: 文档类型

    Returns:
        str: 中文名称
    """
    name_mapping = {
        'bitable': "多维表格",
        'docx': "云文档",
        'spreadsheet': "电子表格",
        'slide': "幻灯片"
    }
    return name_mapping.get(doc_type, doc_type)


def create_document(
    app_id: str,
    app_secret: str,
    doc_type: str,
    user_open_id: str,
    mode: str = 'normal',
    target_app_open_id: Optional[str] = None,
    admin_open_ids: Optional[List[str]] = None
) -> Tuple[Dict[str, Any], Optional[Exception]]:
    """创建文档主函数

    Args:
        app_id: 飞书应用ID
        app_secret: 飞书应用密钥
        doc_type: 文档类型
        user_open_id: 用户open_id
        mode: 创建模式 normal/wen_admin
        target_app_open_id: wen_admin模式下目标应用open_id
        admin_open_ids: wen_admin模式下管理员open_id列表

    Returns:
        Tuple[Dict[str, Any], Optional[Exception]]: (结果, 错误)
    """
    admin_open_ids = admin_open_ids or []

    # 获取 tenant_access_token
    tenant_access_token, err = get_tenant_access_token(app_id, app_secret)
    if err:
        return {}, err

    # 获取用户信息
    user_info, err = get_user_info(tenant_access_token, user_open_id)
    if err:
        return {}, err

    user_name = user_info.get("name", "未知用户")

    # 获取当前时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 根据模式和类型创建文档
    if mode == 'wen_admin':
        # wen_admin模式 - 创建周报
        now = datetime.now()
        year = now.year
        week_number = now.isocalendar()[1]
        doc_title = f"{year}-第{week_number}周-周报-{user_name}"

        if not target_app_open_id:
            return {}, Exception("wen_admin模式需要指定 --target-app-open-id")

        document_id, err = create_docx_with_permissions(
            tenant_access_token,
            doc_title,
            target_app_open_id,
            admin_open_ids,
            user_open_id
        )
        if err:
            return {}, err

        doc_url = get_document_url('docx', document_id)
        doc_type_name = "周报"
        doc_name = doc_title
        doc_token = document_id

    else:
        # normal模式 - 根据类型创建
        doc_name = f"{current_time}_{user_name}_{get_document_type_name(doc_type)}"

        if doc_type == 'bitable':
            token, err = create_bitable(tenant_access_token, doc_name)
        elif doc_type == 'docx':
            token, err = create_docx(tenant_access_token, doc_name)
        elif doc_type == 'spreadsheet':
            token, err = create_spreadsheet(tenant_access_token, doc_name)
        elif doc_type == 'slide':
            token, err = create_slide(tenant_access_token, doc_name)
        else:
            return {}, Exception(f"不支持的文档类型: {doc_type}")

        if err:
            return {}, err

        # 转移所有者给用户
        # slide 的 Drive 权限 API 不支持 transfer_owner，降级为添加协作者（full_access）
        if doc_type == 'slide':
            _, err = add_collaborator(tenant_access_token, token, "slide", "openid", user_open_id, "full_access")
            if err:
                print(f"警告: 为幻灯片添加协作者失败: {err}", file=sys.stderr)
        else:
            _, err = transfer_owner(tenant_access_token, token, doc_type, user_open_id)
            if err:
                return {}, err

        doc_url = get_document_url(doc_type, token)
        doc_type_name = get_document_type_name(doc_type)
        doc_token = token

    # 发送交互式卡片消息给用户
    card_content = {
        'template_variable': {
            'link': doc_url,
            'name': doc_name,
            'doc_type': doc_type_name
        }
    }
    message_info, err = send_interactive_message(tenant_access_token, user_open_id, card_content)
    if err:
        print(f"警告: 发送卡片消息失败: {err}", file=sys.stderr)

    # 返回结果
    result = {
        'success': True,
        'document_url': doc_url,
        'document_name': doc_name,
        'document_type': doc_type_name,
        'document_token': doc_token,
        'message': '创建成功'
    }

    return result, None


def main():
    """主函数 - 命令行入口

    优先级：
    1. 命令行参数 --app-id/--app-secret
    2. 环境变量 FEISHU_APP_ID/FEISHU_APP_SECRET
    3. OpenClaw配置文件 ~/.openclaw/openclaw.json 中的飞书配置
    """
    parser = argparse.ArgumentParser(description='Feishu Document Creator - 创建飞书文档\n'
                                                 '自动从OpenClaw配置读取飞书凭证，不需要手动提供')
    parser.add_argument('--app-id', help='飞书应用ID（优先级高于自动读取）')
    parser.add_argument('--app-secret', help='飞书应用密钥（优先级高于自动读取）')
    parser.add_argument('--type', required=True,
                        choices=['bitable', 'docx', 'spreadsheet', 'slide'],
                        help='文档类型：bitable/docx/spreadsheet/slide')
    parser.add_argument('--user-open-id', required=True, help='操作用户的open_id')
    parser.add_argument('--mode', default='normal', choices=['normal', 'wen_admin'],
                        help='创建模式：normal（默认）或 wen_admin（周报管理模式）')
    parser.add_argument('--target-app-open-id', help='wen_admin模式：目标应用open_id')
    parser.add_argument('--admin-open-ids', help='wen_admin模式：管理员open_id列表（逗号分隔）')
    parser.add_argument('--output', default='json', choices=['json', 'text'],
                        help='输出格式：json（默认）或 text')

    args = parser.parse_args()

    # 优先级：命令行参数 > 环境变量 > OpenClaw配置
    app_id = args.app_id
    app_secret = args.app_secret

    if not app_id:
        app_id = os.environ.get('FEISHU_APP_ID')

    if not app_secret:
        app_secret = os.environ.get('FEISHU_APP_SECRET')

    # 如果还没找到，尝试从OpenClaw配置读取
    if not app_id or not app_secret:
        oc_config = load_openclaw_config()
        if not app_id:
            app_id = oc_config.get('app_id')
        if not app_secret:
            app_secret = oc_config.get('app_secret')

    if not app_id:
        error_result = {'success': False, 'error': '--app-id 未提供，环境变量 FEISHU_APP_ID 为空，也未从OpenClaw配置读取到'}
        print(json.dumps(error_result, ensure_ascii=False))
        sys.exit(1)

    if not app_secret:
        error_result = {'success': False, 'error': '--app-secret 未提供，环境变量 FEISHU_APP_SECRET 为空，也未从OpenClaw配置读取到'}
        print(json.dumps(error_result, ensure_ascii=False))
        sys.exit(1)

    # 解析管理员列表
    admin_open_ids = []
    if args.admin_open_ids:
        admin_open_ids = [id.strip() for id in args.admin_open_ids.split(',') if id.strip()]

    # 创建文档
    result, err = create_document(
        app_id=app_id,
        app_secret=app_secret,
        doc_type=args.type,
        user_open_id=args.user_open_id,
        mode=args.mode,
        target_app_open_id=args.target_app_open_id,
        admin_open_ids=admin_open_ids
    )

    if err:
        result = {'success': False, 'error': str(err)}

    # 输出结果
    if args.output == 'json':
        print(json.dumps(result, ensure_ascii=False))
    else:
        if result.get('success'):
            print(f"创建成功!")
            print(f"文档名称: {result.get('document_name')}")
            print(f"文档类型: {result.get('document_type')}")
            print(f"文档链接: {result.get('document_url')}")
            print(f"文档Token: {result.get('document_token')}")
        else:
            print(f"创建失败: {result.get('error')}")
            sys.exit(1)


if __name__ == "__main__":
    main()
