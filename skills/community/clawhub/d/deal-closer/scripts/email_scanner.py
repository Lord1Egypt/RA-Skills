#!/usr/bin/env python3
"""
deal-closer 邮件扫描模块（付费功能）

扫描 Gmail / Outlook 邮箱中的邮件，提取商机信号，关联到商机记录。
支持 OAuth2 认证的 Gmail API 和 Outlook API。
"""

import json
import os
import re
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import URLError

from utils import (
    check_subscription,
    generate_id,
    get_data_file,
    load_input_data,
    mask_email,
    now_iso,
    today_str,
    output_error,
    output_success,
    parse_common_args,
    read_json_file,
    require_paid_feature,
    write_json_file,
    calculate_days_since,
)

# 延迟导入 IMAP 和学习模块（避免循环依赖）
_imap_module = None
_learning_module = None


def _get_imap_module():
    """延迟加载 imap_email 模块。"""
    global _imap_module
    if _imap_module is None:
        try:
            import imap_email as _mod
            _imap_module = _mod
        except ImportError:
            _imap_module = False
    return _imap_module if _imap_module is not False else None


def _get_learning_module():
    """延迟加载 learning_engine 模块。"""
    global _learning_module
    if _learning_module is None:
        try:
            import learning_engine as _mod
            _learning_module = _mod
        except ImportError:
            _learning_module = False
    return _learning_module if _learning_module is not False else None


# ============================================================
# 常量与配置
# ============================================================

EMAILS_FILE = "emails.json"
DEALS_FILE = "deals.json"

# 信号关键词定义
POSITIVE_KEYWORDS = [
    "同意", "可以", "没问题", "感兴趣", "非常好", "合作", "签约",
    "确认", "批准", "通过", "接受", "agree", "interested", "approve",
    "confirmed", "accept", "deal", "go ahead", "proceed", "sign",
    "好的", "行", "成交", "下单", "购买", "采购",
]

NEGATIVE_KEYWORDS = [
    "推迟", "延期", "考虑", "再看看", "暂时不", "预算不够",
    "竞争对手", "其他方案", "不合适", "太贵", "价格高",
    "delay", "postpone", "competitor", "budget", "expensive",
    "not now", "reconsider", "cancel", "暂缓", "放弃", "取消",
]

NEUTRAL_KEYWORDS = [
    "了解", "咨询", "请问", "资料", "方案", "报价",
    "详情", "介绍", "信息", "inquiry", "information",
    "question", "brochure", "proposal", "quote", "什么时候",
]

# 信号类型常量
SIGNAL_POSITIVE = "POSITIVE"
SIGNAL_NEGATIVE = "NEGATIVE"
SIGNAL_NEUTRAL = "NEUTRAL"


# ============================================================
# 数据操作
# ============================================================

def _get_emails() -> List[Dict[str, Any]]:
    """读取所有邮件记录。"""
    return read_json_file(get_data_file(EMAILS_FILE))


def _save_emails(emails: List[Dict[str, Any]]) -> None:
    """保存邮件记录到文件。"""
    write_json_file(get_data_file(EMAILS_FILE), emails)


def _get_deals() -> List[Dict[str, Any]]:
    """读取所有商机数据。"""
    return read_json_file(get_data_file(DEALS_FILE))


# ============================================================
# Gmail API 集成
# ============================================================

def _load_gmail_credentials() -> Optional[Dict[str, Any]]:
    """加载 Gmail OAuth2 凭据文件。

    从 DC_GMAIL_CREDENTIALS 环境变量指定的路径读取凭据。

    Returns:
        凭据字典，若文件不存在或无效则返回 None。
    """
    cred_path = os.environ.get("DC_GMAIL_CREDENTIALS", "")
    if not cred_path or not os.path.exists(cred_path):
        return None
    try:
        with open(cred_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def _fetch_gmail_messages(credentials: Dict[str, Any], query: str = "", max_results: int = 50) -> List[Dict[str, Any]]:
    """通过 Gmail API 获取邮件列表。

    Args:
        credentials: OAuth2 凭据字典，需包含 access_token。
        query: Gmail 搜索查询字符串。
        max_results: 最大返回数量。

    Returns:
        邮件消息列表。
    """
    access_token = credentials.get("access_token", "")
    if not access_token:
        return []

    params = {"maxResults": max_results}
    if query:
        params["q"] = query

    url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages?{urlencode(params)}"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("messages", [])
    except (URLError, json.JSONDecodeError, Exception):
        return []


def _get_gmail_message_detail(credentials: Dict[str, Any], message_id: str) -> Optional[Dict[str, Any]]:
    """获取 Gmail 邮件详情。

    Args:
        credentials: OAuth2 凭据字典。
        message_id: 邮件 ID。

    Returns:
        邮件详情字典，失败返回 None。
    """
    access_token = credentials.get("access_token", "")
    if not access_token:
        return None

    url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{message_id}?format=metadata"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (URLError, json.JSONDecodeError, Exception):
        return None


# ============================================================
# Outlook API 集成
# ============================================================

def _get_outlook_credentials() -> Optional[Dict[str, str]]:
    """获取 Outlook API 凭据。

    从环境变量读取 DC_OUTLOOK_CLIENT_ID 和 DC_OUTLOOK_SECRET。

    Returns:
        凭据字典，若缺少必要环境变量则返回 None。
    """
    client_id = os.environ.get("DC_OUTLOOK_CLIENT_ID", "")
    secret = os.environ.get("DC_OUTLOOK_SECRET", "")
    if not client_id or not secret:
        return None
    return {"client_id": client_id, "client_secret": secret}


def _fetch_outlook_messages(credentials: Dict[str, str], query: str = "", max_results: int = 50) -> List[Dict[str, Any]]:
    """通过 Outlook API 获取邮件列表。

    Args:
        credentials: 包含 client_id 和 client_secret 的凭据字典。
        query: 搜索查询字符串。
        max_results: 最大返回数量。

    Returns:
        邮件消息列表。
    """
    # 注意：实际集成需完成 OAuth2 flow 获取 access_token
    # 此处为 API 调用框架，需要用户完成 OAuth 授权后获取 token
    access_token = os.environ.get("DC_OUTLOOK_ACCESS_TOKEN", "")
    if not access_token:
        return []

    params = {"$top": max_results}
    if query:
        params["$search"] = f'"{query}"'

    url = f"https://graph.microsoft.com/v1.0/me/messages?{urlencode(params)}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("value", [])
    except (URLError, json.JSONDecodeError, Exception):
        return []


# ============================================================
# IMAP 扫描
# ============================================================

def _scan_imap(config: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """通过 IMAP 协议扫描邮件。

    使用 imap_email 模块获取收件箱最近邮件。

    Args:
        config: 可选配置，支持 count（数量）、folder（文件夹）。

    Returns:
        扫描到的邮件列表。
    """
    imap_mod = _get_imap_module()
    if imap_mod is None:
        return []

    config = config or {}
    creds = imap_mod._get_credentials()

    # 检查凭据是否可用
    if not creds.get("email_user") or not creds.get("email_password"):
        return []

    # 自动检测服务商配置
    if not creds.get("imap_host") and creds.get("email_user"):
        auto_config = imap_mod._auto_detect_provider(creds["email_user"])
        if auto_config:
            creds["imap_host"] = auto_config["imap_host"]
            creds["imap_port"] = auto_config["imap_port"]

    if not creds.get("imap_host"):
        return []

    conn = imap_mod._create_imap_connection(creds)
    if not conn:
        return []

    scanned = []
    try:
        import email as email_stdlib
        folder = config.get("folder", "INBOX")
        count = int(config.get("count", 50))

        status, _ = conn.select(folder, readonly=True)
        if status != "OK":
            conn.logout()
            return []

        status, data_list = conn.search(None, "ALL")
        if status != "OK":
            conn.logout()
            return []

        msg_ids = data_list[0].split()
        recent_ids = msg_ids[-count:]
        recent_ids.reverse()

        for mid in recent_ids:
            try:
                status, msg_data = conn.fetch(mid, "(RFC822)")
                if status == "OK" and msg_data[0]:
                    raw = msg_data[0][1]
                    if isinstance(raw, bytes):
                        msg = email_stdlib.message_from_bytes(raw)
                        parsed = imap_mod._parse_email_message(
                            msg, mid.decode("utf-8")
                        )
                        scanned.append({
                            "provider": "imap",
                            "message_id": parsed.get("message_id", mid.decode("utf-8")),
                            "subject": parsed.get("subject", ""),
                            "from": parsed.get("from", ""),
                            "date": parsed.get("date", ""),
                            "snippet": parsed.get("body_preview", "")[:200],
                        })
            except Exception:
                continue

        conn.logout()
    except Exception:
        try:
            conn.logout()
        except Exception:
            pass

    return scanned


def _record_scan_patterns(scanned: List[Dict[str, Any]]) -> None:
    """将扫描结果中的模式记录到学习引擎。

    Args:
        scanned: 扫描到的邮件列表。
    """
    learning_mod = _get_learning_module()
    if learning_mod is None or not scanned:
        return

    try:
        # 统计信号来源和类型
        provider_counts: Dict[str, int] = {}
        for item in scanned:
            provider = item.get("provider", "unknown")
            provider_counts[provider] = provider_counts.get(provider, 0) + 1

        # 记录扫描模式到学习数据
        learning_data = learning_mod._get_learning_data()
        patterns = learning_data.get("patterns", [])

        # 检查是否已有今日的扫描记录
        today = today_str()
        existing_today = [
            p for p in patterns
            if p.get("category") == "email_scan"
            and p.get("recorded_at", "").startswith(today)
        ]

        if not existing_today:
            from utils import generate_id as _gen_id
            pattern = {
                "id": _gen_id("LP"),
                "category": "email_scan",
                "description": (
                    f"邮件扫描：共 {len(scanned)} 封，"
                    f"来源分布 {json.dumps(provider_counts, ensure_ascii=False)}"
                ),
                "success_rate": 0.5,
                "applicable_stages": [],
                "notes": f"自动记录于 {today}",
                "recorded_at": now_iso(),
            }
            patterns.append(pattern)
            learning_data["patterns"] = patterns
            learning_mod._save_learning_data(learning_data)
    except Exception:
        # 学习记录失败不影响主流程
        pass


# ============================================================
# 信号分析
# ============================================================

def _analyze_signal(text: str) -> Tuple[str, float, List[str]]:
    """分析文本中的商机信号。

    扫描文本内容，根据关键词匹配判断信号类型。

    Args:
        text: 待分析的文本内容。

    Returns:
        (信号类型, 置信度, 匹配的关键词列表) 元组。
    """
    text_lower = text.lower()
    matched_positive = []
    matched_negative = []
    matched_neutral = []

    for kw in POSITIVE_KEYWORDS:
        if kw.lower() in text_lower:
            matched_positive.append(kw)

    for kw in NEGATIVE_KEYWORDS:
        if kw.lower() in text_lower:
            matched_negative.append(kw)

    for kw in NEUTRAL_KEYWORDS:
        if kw.lower() in text_lower:
            matched_neutral.append(kw)

    pos_count = len(matched_positive)
    neg_count = len(matched_negative)
    neu_count = len(matched_neutral)
    total = pos_count + neg_count + neu_count

    if total == 0:
        return SIGNAL_NEUTRAL, 0.0, []

    # 根据匹配数量和比例判断信号类型
    if pos_count > neg_count and pos_count >= neu_count:
        confidence = min(pos_count / max(total, 1), 1.0)
        return SIGNAL_POSITIVE, round(confidence, 2), matched_positive
    elif neg_count > pos_count and neg_count >= neu_count:
        confidence = min(neg_count / max(total, 1), 1.0)
        return SIGNAL_NEGATIVE, round(confidence, 2), matched_negative
    else:
        confidence = min(neu_count / max(total, 1), 1.0)
        return SIGNAL_NEUTRAL, round(confidence, 2), matched_neutral


def _extract_email_addresses(text: str) -> List[str]:
    """从文本中提取邮箱地址。

    Args:
        text: 待搜索的文本。

    Returns:
        匹配到的邮箱地址列表。
    """
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return re.findall(pattern, text)


def _match_deal_by_contact(email_addr: str, deals: List[Dict]) -> Optional[Dict]:
    """根据邮箱地址匹配对应的商机。

    Args:
        email_addr: 邮箱地址。
        deals: 商机列表。

    Returns:
        匹配到的商机字典，未匹配返回 None。
    """
    email_lower = email_addr.lower().strip()
    for deal in deals:
        deal_email = deal.get("contact_email", "").lower().strip()
        if deal_email and deal_email == email_lower:
            return deal
    return None


# ============================================================
# 操作函数
# ============================================================

def scan_emails(data: Optional[Dict[str, Any]] = None) -> None:
    """扫描邮箱中的邮件并存储。

    支持 Gmail 和 Outlook 两种邮箱类型。
    根据环境变量自动选择可用的邮箱源。

    Args:
        data: 可选参数，支持 provider（gmail/outlook）、query、max_results。
    """
    if not require_paid_feature("email_scan", "邮件扫描"):
        return

    data = data or {}
    provider = data.get("provider", "").lower()
    query = data.get("query", "")
    max_results = data.get("max_results", 50)

    scanned = []

    # 尝试 Gmail
    if provider in ("", "gmail"):
        gmail_creds = _load_gmail_credentials()
        if gmail_creds:
            messages = _fetch_gmail_messages(gmail_creds, query=query, max_results=max_results)
            for msg in messages:
                msg_id = msg.get("id", "")
                detail = _get_gmail_message_detail(gmail_creds, msg_id)
                if detail:
                    headers = detail.get("payload", {}).get("headers", [])
                    subject = ""
                    from_addr = ""
                    date_str = ""
                    for h in headers:
                        h_name = h.get("name", "").lower()
                        if h_name == "subject":
                            subject = h.get("value", "")
                        elif h_name == "from":
                            from_addr = h.get("value", "")
                        elif h_name == "date":
                            date_str = h.get("value", "")

                    scanned.append({
                        "provider": "gmail",
                        "message_id": msg_id,
                        "subject": subject,
                        "from": from_addr,
                        "date": date_str,
                        "snippet": detail.get("snippet", ""),
                    })

    # 尝试 Outlook
    if provider in ("", "outlook"):
        outlook_creds = _get_outlook_credentials()
        if outlook_creds:
            messages = _fetch_outlook_messages(outlook_creds, query=query, max_results=max_results)
            for msg in messages:
                scanned.append({
                    "provider": "outlook",
                    "message_id": msg.get("id", ""),
                    "subject": msg.get("subject", ""),
                    "from": msg.get("from", {}).get("emailAddress", {}).get("address", ""),
                    "date": msg.get("receivedDateTime", ""),
                    "snippet": msg.get("bodyPreview", ""),
                })

    # 尝试 IMAP（任意邮箱服务商）
    if provider in ("", "imap"):
        imap_results = _scan_imap({"count": max_results})
        scanned.extend(imap_results)

    if not scanned:
        # 无法连接任何邮箱，提示配置
        output_error(
            "未能连接到任何邮箱。请确认以下环境变量已正确配置：\n"
            "  Gmail: DC_GMAIL_CREDENTIALS（OAuth2 凭据文件路径）\n"
            "  Outlook: DC_OUTLOOK_CLIENT_ID + DC_OUTLOOK_SECRET\n"
            "  IMAP: DC_EMAIL_USER + DC_EMAIL_PASSWORD（+ 可选 DC_IMAP_HOST）\n"
            "详见 references/email-setup-guide.md",
            code="NO_EMAIL_SOURCE",
        )
        return

    # 存储扫描结果
    existing_emails = _get_emails()
    existing_ids = {e.get("message_id") for e in existing_emails}
    new_count = 0

    for item in scanned:
        if item["message_id"] not in existing_ids:
            email_record = {
                "id": generate_id("E"),
                "provider": item["provider"],
                "message_id": item["message_id"],
                "subject": item["subject"],
                "from_address": item["from"],
                "date": item["date"],
                "snippet": item["snippet"],
                "signal": None,
                "signal_confidence": 0.0,
                "matched_keywords": [],
                "linked_deal_id": None,
                "scanned_at": now_iso(),
            }
            existing_emails.append(email_record)
            new_count += 1

    _save_emails(existing_emails)

    # 记录扫描模式到学习引擎
    _record_scan_patterns(scanned)

    output_success({
        "message": f"扫描完成：发现 {len(scanned)} 封邮件，新增 {new_count} 封",
        "total_scanned": len(scanned),
        "new_emails": new_count,
        "total_stored": len(existing_emails),
    })


def extract_signals(data: Optional[Dict[str, Any]] = None) -> None:
    """分析已存储邮件的商机信号。

    对所有未分析的邮件执行信号提取，或对指定邮件重新分析。

    Args:
        data: 可选参数，支持 email_id（指定邮件）、force（强制重新分析）。
    """
    if not require_paid_feature("email_scan", "邮件信号提取"):
        return

    data = data or {}
    email_id = data.get("email_id")
    force = data.get("force", False)

    emails = _get_emails()
    if not emails:
        output_error("暂无邮件记录，请先执行邮件扫描", code="NO_DATA")
        return

    analyzed_count = 0
    results = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}

    for email in emails:
        # 按 ID 过滤
        if email_id and email.get("id") != email_id:
            continue

        # 跳过已分析的（除非强制）
        if email.get("signal") and not force:
            continue

        # 组合文本用于分析
        text = f"{email.get('subject', '')} {email.get('snippet', '')}"
        signal, confidence, keywords = _analyze_signal(text)

        email["signal"] = signal
        email["signal_confidence"] = confidence
        email["matched_keywords"] = keywords
        analyzed_count += 1
        results[signal] = results.get(signal, 0) + 1

    _save_emails(emails)

    output_success({
        "message": f"信号分析完成：已分析 {analyzed_count} 封邮件",
        "analyzed": analyzed_count,
        "signal_summary": results,
    })


def link_deal(data: Dict[str, Any]) -> None:
    """将邮件关联到商机。

    支持手动指定关联或自动按联系人邮箱匹配。

    Args:
        data: 参数字典，支持 email_id + deal_id（手动）或 auto=True（自动匹配）。
    """
    if not require_paid_feature("email_scan", "邮件-商机关联"):
        return

    auto = data.get("auto", False)
    emails = _get_emails()
    deals = _get_deals()

    if not emails:
        output_error("暂无邮件记录", code="NO_DATA")
        return

    if auto:
        # 自动匹配模式
        linked_count = 0
        for email in emails:
            if email.get("linked_deal_id"):
                continue
            from_addr = email.get("from_address", "")
            email_addrs = _extract_email_addresses(from_addr)
            for addr in email_addrs:
                matched_deal = _match_deal_by_contact(addr, deals)
                if matched_deal:
                    email["linked_deal_id"] = matched_deal["id"]
                    linked_count += 1
                    break

        _save_emails(emails)
        output_success({
            "message": f"自动关联完成：成功关联 {linked_count} 封邮件",
            "linked": linked_count,
        })
    else:
        # 手动关联模式
        email_id = data.get("email_id")
        deal_id = data.get("deal_id")

        if not email_id or not deal_id:
            output_error("手动关联需提供 email_id 和 deal_id", code="VALIDATION_ERROR")
            return

        target_email = None
        for e in emails:
            if e.get("id") == email_id:
                target_email = e
                break

        if not target_email:
            output_error(f"未找到ID为 {email_id} 的邮件", code="NOT_FOUND")
            return

        target_deal = None
        for d in deals:
            if d.get("id") == deal_id:
                target_deal = d
                break

        if not target_deal:
            output_error(f"未找到ID为 {deal_id} 的商机", code="NOT_FOUND")
            return

        target_email["linked_deal_id"] = deal_id
        _save_emails(emails)

        output_success({
            "message": f"邮件已关联到商机「{target_deal.get('name', '')}」",
            "email_id": email_id,
            "deal_id": deal_id,
            "deal_name": target_deal.get("name", ""),
        })


def list_emails(data: Optional[Dict[str, Any]] = None) -> None:
    """列出已存储的邮件记录。

    可选过滤: deal_id, signal, provider

    Args:
        data: 可选的过滤条件字典。
    """
    if not require_paid_feature("email_scan", "邮件列表"):
        return

    emails = _get_emails()

    if data:
        # 按商机过滤
        deal_id = data.get("deal_id")
        if deal_id:
            emails = [e for e in emails if e.get("linked_deal_id") == deal_id]

        # 按信号类型过滤
        signal_filter = data.get("signal")
        if signal_filter:
            emails = [e for e in emails if e.get("signal") == signal_filter.upper()]

        # 按来源过滤
        provider_filter = data.get("provider")
        if provider_filter:
            emails = [e for e in emails if e.get("provider") == provider_filter.lower()]

    # 按日期倒序
    emails.sort(key=lambda e: e.get("date", ""), reverse=True)

    # 脱敏处理
    display_list = []
    for e in emails:
        display = dict(e)
        if display.get("from_address"):
            display["from_address"] = mask_email(display["from_address"])
        display_list.append(display)

    # 信号统计
    signal_stats = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0, "未分析": 0}
    for e in emails:
        sig = e.get("signal")
        if sig in signal_stats:
            signal_stats[sig] += 1
        else:
            signal_stats["未分析"] += 1

    output_success({
        "total": len(display_list),
        "signal_stats": signal_stats,
        "emails": display_list,
    })


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("deal-closer 邮件扫描器")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "scan": lambda: scan_emails(data),
        "extract-signals": lambda: extract_signals(data),
        "link-deal": lambda: link_deal(data or {}),
        "list-emails": lambda: list_emails(data),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
