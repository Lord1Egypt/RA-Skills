#!/usr/bin/env python3
"""
deal-closer IMAP/SMTP 原生邮件模块

通过标准库 imaplib/smtplib 实现邮件收发，支持任意邮件服务商。
无需 OAuth2 配置，直接使用 IMAP/SMTP 协议连接。
基于 imap-smtp-email 理念，提供通用邮件集成能力。
"""

import email
import email.header
import email.mime.multipart
import email.mime.text
import email.utils
import imaplib
import json
import os
import smtplib
import ssl
import sys
from datetime import datetime, timedelta
from email.header import decode_header
from typing import Any, Dict, List, Optional, Tuple

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
)


# ============================================================
# 常量与配置
# ============================================================

EMAIL_CONFIG_FILE = "email_config.json"

# 默认端口
DEFAULT_IMAP_PORT = 993
DEFAULT_SMTP_PORT = 587

# 常见邮件服务商 IMAP/SMTP 配置
PROVIDER_CONFIGS = {
    "qq": {
        "imap_host": "imap.qq.com",
        "imap_port": 993,
        "smtp_host": "smtp.qq.com",
        "smtp_port": 587,
    },
    "163": {
        "imap_host": "imap.163.com",
        "imap_port": 993,
        "smtp_host": "smtp.163.com",
        "smtp_port": 465,
    },
    "gmail": {
        "imap_host": "imap.gmail.com",
        "imap_port": 993,
        "smtp_host": "smtp.gmail.com",
        "smtp_port": 587,
    },
    "outlook": {
        "imap_host": "outlook.office365.com",
        "imap_port": 993,
        "smtp_host": "smtp.office365.com",
        "smtp_port": 587,
    },
    "aliyun": {
        "imap_host": "imap.aliyun.com",
        "imap_port": 993,
        "smtp_host": "smtp.aliyun.com",
        "smtp_port": 465,
    },
}


# ============================================================
# 配置管理
# ============================================================

def _get_email_config() -> Dict[str, Any]:
    """读取邮件配置（不含密码）。"""
    filepath = get_data_file(EMAIL_CONFIG_FILE)
    if not os.path.exists(filepath):
        return {}
    data = read_json_file(filepath)
    if isinstance(data, list):
        return {}
    return data


def _save_email_config(config: Dict[str, Any]) -> None:
    """保存邮件配置（不含密码）。"""
    # 确保不保存密码
    safe_config = dict(config)
    safe_config.pop("password", None)
    safe_config["last_updated"] = now_iso()
    write_json_file(get_data_file(EMAIL_CONFIG_FILE), safe_config)


def _get_credentials() -> Dict[str, str]:
    """从环境变量获取邮件凭据。

    Returns:
        包含连接信息的字典。
    """
    return {
        "imap_host": os.environ.get("DC_IMAP_HOST", ""),
        "imap_port": int(os.environ.get("DC_IMAP_PORT", str(DEFAULT_IMAP_PORT))),
        "smtp_host": os.environ.get("DC_SMTP_HOST", ""),
        "smtp_port": int(os.environ.get("DC_SMTP_PORT", str(DEFAULT_SMTP_PORT))),
        "email_user": os.environ.get("DC_EMAIL_USER", ""),
        "email_password": os.environ.get("DC_EMAIL_PASSWORD", ""),
    }


def _auto_detect_provider(email_addr: str) -> Optional[Dict[str, Any]]:
    """根据邮箱地址自动检测服务商配置。

    Args:
        email_addr: 邮箱地址。

    Returns:
        服务商配置字典，未识别返回 None。
    """
    if not email_addr or "@" not in email_addr:
        return None

    domain = email_addr.split("@")[-1].lower()

    for provider, config in PROVIDER_CONFIGS.items():
        if provider in domain:
            return config

    # 尝试域名匹配
    if "qq.com" in domain:
        return PROVIDER_CONFIGS["qq"]
    elif "163.com" in domain or "126.com" in domain:
        return PROVIDER_CONFIGS["163"]
    elif "gmail.com" in domain:
        return PROVIDER_CONFIGS["gmail"]
    elif "outlook.com" in domain or "hotmail.com" in domain:
        return PROVIDER_CONFIGS["outlook"]
    elif "aliyun.com" in domain:
        return PROVIDER_CONFIGS["aliyun"]

    return None


# ============================================================
# 邮件解析
# ============================================================

def _decode_header_value(value: str) -> str:
    """解码邮件头字段值，处理中文编码。

    Args:
        value: 原始头字段值。

    Returns:
        解码后的字符串。
    """
    if not value:
        return ""

    try:
        decoded_parts = decode_header(value)
        result = []
        for part, charset in decoded_parts:
            if isinstance(part, bytes):
                # 尝试用指定编码解码
                if charset:
                    try:
                        result.append(part.decode(charset))
                    except (UnicodeDecodeError, LookupError):
                        result.append(part.decode("utf-8", errors="replace"))
                else:
                    result.append(part.decode("utf-8", errors="replace"))
            else:
                result.append(str(part))
        return " ".join(result)
    except Exception:
        return str(value)


def _extract_plain_text(msg: email.message.Message) -> str:
    """从邮件消息中提取纯文本内容。

    处理 multipart 邮件，优先提取 text/plain。

    Args:
        msg: email.message.Message 对象。

    Returns:
        纯文本内容。
    """
    text_parts = []

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition", ""))

            # 跳过附件
            if "attachment" in content_disposition:
                continue

            if content_type == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    try:
                        text_parts.append(payload.decode(charset, errors="replace"))
                    except (UnicodeDecodeError, LookupError):
                        text_parts.append(payload.decode("utf-8", errors="replace"))
    else:
        content_type = msg.get_content_type()
        if content_type == "text/plain":
            payload = msg.get_payload(decode=True)
            if payload:
                charset = msg.get_content_charset() or "utf-8"
                try:
                    text_parts.append(payload.decode(charset, errors="replace"))
                except (UnicodeDecodeError, LookupError):
                    text_parts.append(payload.decode("utf-8", errors="replace"))

    return "\n".join(text_parts)


def _parse_email_message(msg: email.message.Message,
                          msg_id: str = "") -> Dict[str, Any]:
    """解析邮件消息为字典。

    Args:
        msg: email.message.Message 对象。
        msg_id: 邮件 UID。

    Returns:
        解析后的邮件字典。
    """
    subject = _decode_header_value(msg.get("Subject", ""))
    from_addr = _decode_header_value(msg.get("From", ""))
    to_addr = _decode_header_value(msg.get("To", ""))
    date_str = msg.get("Date", "")
    message_id = msg.get("Message-ID", "")

    # 解析日期
    parsed_date = ""
    if date_str:
        try:
            dt = email.utils.parsedate_to_datetime(date_str)
            parsed_date = dt.strftime("%Y-%m-%dT%H:%M:%S")
        except (ValueError, TypeError):
            parsed_date = date_str

    # 提取正文
    body = _extract_plain_text(msg)
    # 限制预览长度
    body_preview = body[:500] if body else ""

    return {
        "uid": msg_id,
        "message_id": message_id,
        "subject": subject,
        "from": from_addr,
        "to": to_addr,
        "date": parsed_date,
        "body_preview": body_preview,
        "body_length": len(body),
    }


# ============================================================
# IMAP 操作
# ============================================================

def _create_imap_connection(creds: Dict[str, Any]) -> Optional[imaplib.IMAP4_SSL]:
    """创建 IMAP SSL 连接。

    Args:
        creds: 连接凭据。

    Returns:
        IMAP4_SSL 连接对象，失败返回 None。
    """
    host = creds.get("imap_host", "")
    port = int(creds.get("imap_port", DEFAULT_IMAP_PORT))
    user = creds.get("email_user", "")
    password = creds.get("email_password", "")

    if not all([host, user, password]):
        return None

    try:
        context = ssl.create_default_context()
        conn = imaplib.IMAP4_SSL(host, port, ssl_context=context)
        conn.login(user, password)
        return conn
    except (imaplib.IMAP4.error, OSError, ssl.SSLError) as e:
        return None


def _create_smtp_connection(creds: Dict[str, Any]) -> Optional[smtplib.SMTP]:
    """创建 SMTP 连接。

    Args:
        creds: 连接凭据。

    Returns:
        SMTP 连接对象，失败返回 None。
    """
    host = creds.get("smtp_host", "")
    port = int(creds.get("smtp_port", DEFAULT_SMTP_PORT))
    user = creds.get("email_user", "")
    password = creds.get("email_password", "")

    if not all([host, user, password]):
        return None

    try:
        if port == 465:
            # SSL 直连
            context = ssl.create_default_context()
            conn = smtplib.SMTP_SSL(host, port, context=context)
        else:
            # STARTTLS
            conn = smtplib.SMTP(host, port, timeout=30)
            conn.starttls()

        conn.login(user, password)
        return conn
    except (smtplib.SMTPException, OSError, ssl.SSLError) as e:
        return None


# ============================================================
# 操作函数
# ============================================================

def connect_test(data: Optional[Dict[str, Any]] = None) -> None:
    """测试 IMAP/SMTP 连接。

    可选字段: provider（自动填充服务商配置）

    Args:
        data: 可选参数。
    """
    if not require_paid_feature("email_scan", "IMAP/SMTP 邮件"):
        return

    creds = _get_credentials()
    data = data or {}

    # 如果环境变量未设置，尝试自动检测
    if not creds.get("imap_host") and creds.get("email_user"):
        auto_config = _auto_detect_provider(creds["email_user"])
        if auto_config:
            if not creds.get("imap_host"):
                creds["imap_host"] = auto_config["imap_host"]
                creds["imap_port"] = auto_config["imap_port"]
            if not creds.get("smtp_host"):
                creds["smtp_host"] = auto_config["smtp_host"]
                creds["smtp_port"] = auto_config["smtp_port"]

    # 也可手动指定 provider
    provider = data.get("provider", "")
    if provider and provider in PROVIDER_CONFIGS:
        pc = PROVIDER_CONFIGS[provider]
        if not creds.get("imap_host"):
            creds["imap_host"] = pc["imap_host"]
            creds["imap_port"] = pc["imap_port"]
        if not creds.get("smtp_host"):
            creds["smtp_host"] = pc["smtp_host"]
            creds["smtp_port"] = pc["smtp_port"]

    if not creds.get("email_user") or not creds.get("email_password"):
        output_error(
            "请设置以下环境变量：\n"
            "  DC_EMAIL_USER — 邮箱地址\n"
            "  DC_EMAIL_PASSWORD — 邮箱密码或授权码\n"
            "可选：DC_IMAP_HOST, DC_IMAP_PORT, DC_SMTP_HOST, DC_SMTP_PORT",
            code="NO_CREDENTIALS",
        )
        return

    results = {"imap": False, "smtp": False, "imap_error": "", "smtp_error": ""}

    # 测试 IMAP
    try:
        imap_conn = _create_imap_connection(creds)
        if imap_conn:
            results["imap"] = True
            imap_conn.logout()
        else:
            results["imap_error"] = "连接失败，请检查 IMAP 配置"
    except Exception as e:
        results["imap_error"] = str(e)

    # 测试 SMTP
    try:
        smtp_conn = _create_smtp_connection(creds)
        if smtp_conn:
            results["smtp"] = True
            smtp_conn.quit()
        else:
            results["smtp_error"] = "连接失败，请检查 SMTP 配置"
    except Exception as e:
        results["smtp_error"] = str(e)

    # 保存配置（不含密码）
    config = {
        "imap_host": creds.get("imap_host", ""),
        "imap_port": creds.get("imap_port", DEFAULT_IMAP_PORT),
        "smtp_host": creds.get("smtp_host", ""),
        "smtp_port": creds.get("smtp_port", DEFAULT_SMTP_PORT),
        "email_user": mask_email(creds.get("email_user", "")),
        "imap_connected": results["imap"],
        "smtp_connected": results["smtp"],
    }
    _save_email_config(config)

    if results["imap"] and results["smtp"]:
        output_success({
            "message": "IMAP 和 SMTP 连接测试成功！",
            "imap": {"connected": True, "host": creds.get("imap_host", "")},
            "smtp": {"connected": True, "host": creds.get("smtp_host", "")},
            "user": mask_email(creds.get("email_user", "")),
        })
    elif results["imap"] or results["smtp"]:
        output_success({
            "message": "部分连接成功",
            "imap": {
                "connected": results["imap"],
                "host": creds.get("imap_host", ""),
                "error": results["imap_error"],
            },
            "smtp": {
                "connected": results["smtp"],
                "host": creds.get("smtp_host", ""),
                "error": results["smtp_error"],
            },
            "user": mask_email(creds.get("email_user", "")),
        })
    else:
        output_error(
            f"连接失败。\n"
            f"IMAP: {results['imap_error']}\n"
            f"SMTP: {results['smtp_error']}",
            code="CONNECTION_FAILED",
        )


def fetch_inbox(data: Optional[Dict[str, Any]] = None) -> None:
    """获取收件箱最近邮件。

    可选字段: count（数量，默认 20）、folder（文件夹，默认 INBOX）

    Args:
        data: 可选参数。
    """
    if not require_paid_feature("email_scan", "IMAP邮件获取"):
        return

    data = data or {}
    count = int(data.get("count", 20))
    folder = data.get("folder", "INBOX")

    creds = _get_credentials()
    if not creds.get("imap_host") and creds.get("email_user"):
        auto_config = _auto_detect_provider(creds["email_user"])
        if auto_config:
            creds["imap_host"] = auto_config["imap_host"]
            creds["imap_port"] = auto_config["imap_port"]

    conn = _create_imap_connection(creds)
    if not conn:
        output_error(
            "IMAP 连接失败，请先使用 connect 测试连接配置",
            code="CONNECTION_FAILED",
        )
        return

    try:
        status, _ = conn.select(folder, readonly=True)
        if status != "OK":
            output_error(f"无法打开文件夹: {folder}", code="FOLDER_ERROR")
            conn.logout()
            return

        # 搜索所有邮件
        status, data_list = conn.search(None, "ALL")
        if status != "OK":
            output_error("搜索邮件失败", code="SEARCH_ERROR")
            conn.logout()
            return

        msg_ids = data_list[0].split()
        if not msg_ids:
            output_success({
                "message": "收件箱为空",
                "total": 0,
                "emails": [],
            })
            conn.logout()
            return

        # 取最近 N 封
        recent_ids = msg_ids[-count:]
        recent_ids.reverse()  # 最新的在前

        emails_list = []
        for mid in recent_ids:
            try:
                status, msg_data = conn.fetch(mid, "(RFC822)")
                if status == "OK" and msg_data[0]:
                    raw = msg_data[0][1]
                    if isinstance(raw, bytes):
                        msg = email.message_from_bytes(raw)
                        parsed = _parse_email_message(msg, mid.decode("utf-8"))
                        emails_list.append(parsed)
            except Exception:
                continue

        conn.logout()

        output_success({
            "message": f"获取到 {len(emails_list)} 封邮件",
            "folder": folder,
            "total": len(emails_list),
            "emails": emails_list,
        })

    except Exception as e:
        try:
            conn.logout()
        except Exception:
            pass
        output_error(f"获取邮件失败: {e}", code="FETCH_ERROR")


def search_emails(data: Dict[str, Any]) -> None:
    """搜索邮件。

    可选字段: subject, from_addr, since（YYYY-MM-DD）, before, folder

    Args:
        data: 搜索参数字典。
    """
    if not require_paid_feature("email_scan", "IMAP邮件搜索"):
        return

    subject = data.get("subject", "")
    from_addr = data.get("from_addr", "")
    since = data.get("since", "")
    before = data.get("before", "")
    folder = data.get("folder", "INBOX")
    max_results = int(data.get("max_results", 50))

    creds = _get_credentials()
    if not creds.get("imap_host") and creds.get("email_user"):
        auto_config = _auto_detect_provider(creds["email_user"])
        if auto_config:
            creds["imap_host"] = auto_config["imap_host"]
            creds["imap_port"] = auto_config["imap_port"]

    conn = _create_imap_connection(creds)
    if not conn:
        output_error("IMAP 连接失败", code="CONNECTION_FAILED")
        return

    try:
        conn.select(folder, readonly=True)

        # 构建 IMAP 搜索条件
        criteria = []
        if subject:
            criteria.append(f'SUBJECT "{subject}"')
        if from_addr:
            criteria.append(f'FROM "{from_addr}"')
        if since:
            try:
                dt = datetime.strptime(since, "%Y-%m-%d")
                imap_date = dt.strftime("%d-%b-%Y")
                criteria.append(f"SINCE {imap_date}")
            except ValueError:
                pass
        if before:
            try:
                dt = datetime.strptime(before, "%Y-%m-%d")
                imap_date = dt.strftime("%d-%b-%Y")
                criteria.append(f"BEFORE {imap_date}")
            except ValueError:
                pass

        search_str = " ".join(criteria) if criteria else "ALL"
        status, data_list = conn.search(None, search_str)

        if status != "OK":
            output_error("搜索失败", code="SEARCH_ERROR")
            conn.logout()
            return

        msg_ids = data_list[0].split()
        msg_ids = msg_ids[-max_results:]
        msg_ids.reverse()

        emails_list = []
        for mid in msg_ids:
            try:
                status, msg_data = conn.fetch(mid, "(RFC822)")
                if status == "OK" and msg_data[0]:
                    raw = msg_data[0][1]
                    if isinstance(raw, bytes):
                        msg = email.message_from_bytes(raw)
                        parsed = _parse_email_message(msg, mid.decode("utf-8"))
                        emails_list.append(parsed)
            except Exception:
                continue

        conn.logout()

        output_success({
            "message": f"搜索到 {len(emails_list)} 封邮件",
            "search_criteria": search_str,
            "total": len(emails_list),
            "emails": emails_list,
        })

    except Exception as e:
        try:
            conn.logout()
        except Exception:
            pass
        output_error(f"搜索失败: {e}", code="SEARCH_ERROR")


def send_email(data: Dict[str, Any]) -> None:
    """发送邮件。

    必填字段: to, subject, body
    可选字段: cc, bcc

    Args:
        data: 邮件参数字典。
    """
    if not require_paid_feature("email_scan", "SMTP邮件发送"):
        return

    to_addr = data.get("to", "")
    subject = data.get("subject", "")
    body = data.get("body", "")

    if not to_addr:
        output_error("收件人（to）为必填字段", code="VALIDATION_ERROR")
        return

    if not subject:
        output_error("主题（subject）为必填字段", code="VALIDATION_ERROR")
        return

    if not body:
        output_error("正文（body）为必填字段", code="VALIDATION_ERROR")
        return

    creds = _get_credentials()
    if not creds.get("smtp_host") and creds.get("email_user"):
        auto_config = _auto_detect_provider(creds["email_user"])
        if auto_config:
            creds["smtp_host"] = auto_config["smtp_host"]
            creds["smtp_port"] = auto_config["smtp_port"]

    from_addr = creds.get("email_user", "")
    if not from_addr:
        output_error("未配置发件人邮箱（DC_EMAIL_USER）", code="NO_CREDENTIALS")
        return

    # 构建邮件
    msg = email.mime.multipart.MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg["Date"] = email.utils.formatdate(localtime=True)

    cc = data.get("cc", "")
    if cc:
        msg["Cc"] = cc

    # 添加正文
    msg.attach(email.mime.text.MIMEText(body, "plain", "utf-8"))

    # 收件人列表
    recipients = [to_addr]
    if cc:
        recipients.extend([a.strip() for a in cc.split(",") if a.strip()])
    bcc = data.get("bcc", "")
    if bcc:
        recipients.extend([a.strip() for a in bcc.split(",") if a.strip()])

    # 发送
    conn = _create_smtp_connection(creds)
    if not conn:
        output_error("SMTP 连接失败", code="CONNECTION_FAILED")
        return

    try:
        conn.sendmail(from_addr, recipients, msg.as_string())
        conn.quit()

        output_success({
            "message": f"邮件已发送至 {mask_email(to_addr)}",
            "to": mask_email(to_addr),
            "subject": subject,
            "sent_at": now_iso(),
        })
    except smtplib.SMTPException as e:
        try:
            conn.quit()
        except Exception:
            pass
        output_error(f"发送失败: {e}", code="SEND_ERROR")


def reply_email(data: Dict[str, Any]) -> None:
    """回复邮件。

    必填字段: original_message_id（或 to, subject）, body
    可选字段: to（覆盖原始发件人）

    Args:
        data: 回复参数字典。
    """
    if not require_paid_feature("email_scan", "SMTP邮件回复"):
        return

    body = data.get("body", "")
    to_addr = data.get("to", "")
    subject = data.get("subject", "")
    original_id = data.get("original_message_id", "")

    if not body:
        output_error("回复正文（body）为必填字段", code="VALIDATION_ERROR")
        return

    if not to_addr:
        output_error("收件人（to）为必填字段", code="VALIDATION_ERROR")
        return

    # 自动添加 Re: 前缀
    if subject and not subject.startswith("Re:"):
        subject = f"Re: {subject}"
    elif not subject:
        subject = "Re: (无主题)"

    # 构建回复邮件
    creds = _get_credentials()
    if not creds.get("smtp_host") and creds.get("email_user"):
        auto_config = _auto_detect_provider(creds["email_user"])
        if auto_config:
            creds["smtp_host"] = auto_config["smtp_host"]
            creds["smtp_port"] = auto_config["smtp_port"]

    from_addr = creds.get("email_user", "")
    if not from_addr:
        output_error("未配置发件人邮箱", code="NO_CREDENTIALS")
        return

    msg = email.mime.multipart.MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg["Date"] = email.utils.formatdate(localtime=True)

    if original_id:
        msg["In-Reply-To"] = original_id
        msg["References"] = original_id

    msg.attach(email.mime.text.MIMEText(body, "plain", "utf-8"))

    conn = _create_smtp_connection(creds)
    if not conn:
        output_error("SMTP 连接失败", code="CONNECTION_FAILED")
        return

    try:
        conn.sendmail(from_addr, [to_addr], msg.as_string())
        conn.quit()

        output_success({
            "message": f"回复已发送至 {mask_email(to_addr)}",
            "to": mask_email(to_addr),
            "subject": subject,
            "sent_at": now_iso(),
        })
    except smtplib.SMTPException as e:
        try:
            conn.quit()
        except Exception:
            pass
        output_error(f"回复发送失败: {e}", code="SEND_ERROR")


def list_folders(data: Optional[Dict[str, Any]] = None) -> None:
    """列出邮箱文件夹。

    Args:
        data: 可选参数。
    """
    if not require_paid_feature("email_scan", "IMAP文件夹列表"):
        return

    creds = _get_credentials()
    if not creds.get("imap_host") and creds.get("email_user"):
        auto_config = _auto_detect_provider(creds["email_user"])
        if auto_config:
            creds["imap_host"] = auto_config["imap_host"]
            creds["imap_port"] = auto_config["imap_port"]

    conn = _create_imap_connection(creds)
    if not conn:
        output_error("IMAP 连接失败", code="CONNECTION_FAILED")
        return

    try:
        status, folder_list = conn.list()
        if status != "OK":
            output_error("获取文件夹列表失败", code="FOLDER_ERROR")
            conn.logout()
            return

        folders = []
        for item in folder_list:
            if isinstance(item, bytes):
                decoded = item.decode("utf-8", errors="replace")
                # 解析 IMAP LIST 响应格式
                # 格式: (\\flags) "delimiter" "name"
                parts = decoded.split('"')
                if len(parts) >= 3:
                    folder_name = parts[-2] if parts[-1].strip() == "" else parts[-1].strip()
                    if not folder_name:
                        folder_name = parts[-2]
                    folders.append(folder_name)
                else:
                    folders.append(decoded)

        conn.logout()

        output_success({
            "message": f"共 {len(folders)} 个文件夹",
            "folders": folders,
        })

    except Exception as e:
        try:
            conn.logout()
        except Exception:
            pass
        output_error(f"获取文件夹失败: {e}", code="FOLDER_ERROR")


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("deal-closer IMAP/SMTP 原生邮件")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "connect": lambda: connect_test(data),
        "fetch-inbox": lambda: fetch_inbox(data),
        "search": lambda: search_emails(data or {}),
        "send": lambda: send_email(data or {}),
        "reply": lambda: reply_email(data or {}),
        "list-folders": lambda: list_folders(data),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
