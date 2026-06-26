#!/usr/bin/env python3
"""
bingo-email: 统一邮件管理工具
基于 Python IMAPClient + smtplib，支持任意 IMAP/SMTP 邮箱
兼容腾讯企业邮箱、126/163（IMAP ID）、Gmail、Outlook 等
"""

import sys
import os
import json
import argparse
import email
import re as _re
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ============================================================
# 配置文件路径
# ============================================================
CONFIG_DIR = Path.home() / ".config" / "bingo-email"
CONFIG_FILE = CONFIG_DIR / "config.toml"

# 默认配置（当配置文件不存在时使用）
DEFAULT_CONFIG = {
    "account": {
        "email": "",
        "display_name": "",
    },
    "imap": {
        "host": "",
        "port": 993,
        "encryption": "tls",
        "login": "",
        "password": "",
        # 126/163 网易邮箱需要 IMAP ID (RFC 2971)
        "require_imap_id": False,
    },
    "smtp": {
        "host": "",
        "port": 465,
        "encryption": "tls",
        "login": "",
        "password": "",
    },
}

# 时区：东八区
CST = timezone(timedelta(hours=8))

SEEN_FLAG = b"\\Seen"


# ============================================================
# 配置管理
# ============================================================

def ensure_config_dir():
    """确保配置目录存在"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config():
    """
    从 ~/.config/bingo-email/config.toml 加载配置。
    支持以下格式：
    
    [account]
    email = "your@email.com"
    display_name = "Your Name"

    [imap]
    host = "imap.example.com"
    port = 993
    encryption = "tls"          # tls | starttls | none
    login = "your@email.com"
    password = "your_auth_code"
    require_imap_id = false     # true for 126/163 网易邮箱

    [smtp]
    host = "smtp.example.com"
    port = 465
    encryption = "tls"          # tls | starttls | none
    login = "your@email.com"
    password = "your_auth_code"
    """
    if not CONFIG_FILE.exists():
        return None

    config = dict(DEFAULT_CONFIG)
    try:
        # 简单的 TOML 解析（避免额外依赖）
        current_section = None
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                # section header
                if line.startswith("[") and line.endswith("]"):
                    current_section = line[1:-1].strip()
                    if current_section not in config:
                        config[current_section] = {}
                    continue
                # key = value
                if "=" in line and current_section:
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    # 布尔值转换
                    if value.lower() in ("true", "yes"):
                        value = True
                    elif value.lower() in ("false", "no"):
                        value = False
                    else:
                        # 尝试数字
                        try:
                            value = int(value)
                        except ValueError:
                            pass
                    config[current_section][key] = value
        return config
    except Exception as e:
        print(f"警告: 解析配置文件失败 - {e}")
        return None


def save_config(config):
    """保存配置到 TOML 文件"""
    ensure_config_dir()
    lines = ["# bingo-email 配置文件", "# 生成时间: " + datetime.now().strftime("%Y-%m-%d %H:%M"), ""]
    for section, items in config.items():
        lines.append(f"[{section}]")
        for k, v in items.items():
            if isinstance(v, bool):
                lines.append(f"{k} = {str(v).lower()}")
            elif isinstance(v, int):
                lines.append(f"{k} = {v}")
            else:
                # TOML 字符串需要引号
                escaped = str(v).replace('"', '\\"')
                lines.append(f'{k} = "{escaped}"')
        lines.append("")
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    # 安全: 限制配置文件仅本人可读（防止密码泄露）
    os.chmod(CONFIG_FILE, 0o600)


def get_config():
    """获取有效配置，如果不存在则报错提示用户先运行 init"""
    config = load_config()
    if config is None:
        print("错误: 未找到配置文件")
        print(f"请先运行: python3 {__file__.replace('bingo_email.py', '')}scripts/bingo_email.py init")
        print(f"或手动创建配置文件: {CONFIG_FILE}")
        sys.exit(1)
    
    # 校验必要字段
    imap_host = config.get("imap", {}).get("host", "")
    smtp_host = config.get("smtp", {}).get("host", "")
    email_addr = config.get("account", {}).get("email", "")
    
    if not imap_host or not smtp_host or not email_addr:
        print("错误: 配置不完整，请检查以下字段:")
        if not email_addr:
            print("  - account.email（邮箱地址）")
        if not imap_host:
            print("  - imap.host（IMAP 服务器地址）")
        if not smtp_host:
            print("  - smtp.host（SMTP 服务器地址）")
        sys.exit(1)
    
    return config


# ============================================================
# IMAP ID 支持（126/163 网易邮箱）
# ============================================================

def create_imap_client_with_id(host, port, login, password, require_imap_id=False, encryption="tls"):
    """
    创建 IMAP 客户端，支持网易邮箱的 IMAP ID 要求。
    
    背景：126/163 邮箱强制要求 RFC 2971 IMAP ID，
    客户端必须在 SELECT 之前发送 ID 命令，否则报 "Unsafe Login"。
    
    方案：
    - 如果 require_imap_id=True，使用 raw SSL socket 手动实现 ID → LOGIN → SELECT 流程
    - 否则使用标准 imapclient 库
    """
    try:
        from imapclient import IMAPClient
    except ImportError:
        print("错误: 需要安装 imapclient: pip3 install imapclient")
        sys.exit(1)

    if require_imap_id:
        return _create_imap_raw_id(host, port, login, password)

    # 标准连接
    if encryption == "tls":
        m = IMAPClient(host, port=port, ssl=True)
    elif encryption == "starttls":
        m = IMAPClient(host, port=port, ssl=False)
        m.starttls()
    else:
        m = IMAPClient(host, port=port, ssl=False)
    
    m.login(login, password)
    return m


def _create_imap_raw_id(host, port, login, password):
    """
    使用 raw socket 实现 IMAP 连接，支持 126/163 的 ID 要求。
    
    流程：
    1. 建立 TLS 连接
    2. 读取服务器欢迎消息
    3. 发送 CAPABILITY（确认支持 ID）
    4. 发送 ID (RFC 2971)
    5. 发送 LOGIN
    6. 返回一个可用的 IMAPClient 实例
    
    注意：此函数创建连接后返回 IMAPClient 对象用于后续操作。
           由于 imapclient 不直接暴露底层 socket 来发送原始命令，
           我们这里用一个 workaround：先通过 raw socket 完成 ID+LOGIN，
           然后将 socket 交给 imapclient（或直接用 raw 操作）。
           
    实际方案：我们使用 imapclient 但在登录前注入 ID 命令。
    imapclient 底层允许通过 _connect 后直接操作。
    """
    import ssl
    import socket
    
    # 创建 TLS socket
    context = ssl.create_default_context()
    sock = socket.create_connection((host, port))
    sock = context.wrap_socket(sock, server_hostname=host)
    
    # 读取欢迎消息
    _read_line(sock)
    
    def tag_cmd(tag, cmd):
        """发送带标签的 IMAP 命令并读取响应"""
        sock.sendall(f"{tag} {cmd}\r\n".encode())
        return _read_response(sock)
    
    # CAPABILITY
    cap_resp = tag_cmd("A01", "CAPABILITY")
    
    # ID 命令 (RFC 2971)
    id_params = '(("name" "bingo-email") ("version" "1.0"))'
    id_resp = tag_cmd("A02", f"ID {id_params}")
    
    # LOGIN
    # 注意：密码中可能包含特殊字符，但 IMAP LOGIN 用双引号包裹即可
    login_safe = login.replace('"', '\\"')
    pass_safe = password.replace('"', '\\"')
    login_resp = tag_cmd("A03", f'LOGIN "{login_safe}" "{pass_safe}"')
    
    if "A03 OK" not in login_resp[-1] if login_resp else "":
        sock.close()
        raise Exception(f"IMAP 登录失败: {' '.join(login_resp[-3:] if len(login_resp) >= 3 else login_resp)}")
    
    # 现在 socket 已经处于 authenticated 状态
    # 我们无法直接把这个 socket 传给 imapclient（它有自己的连接管理）
    # 所以改用策略：封装这个 raw socket 为一个简易 IMAP 客户端
    return RawIMAPClient(sock, login)


class RawIMAPClient:
    """
    基于 raw socket 的轻量 IMAP 客户端，专用于 126/163 等需要 IMAP ID 的场景。
    提供与 imapclient 兼容的核心接口。
    """
    
    def __init__(self, sock, username):
        self.sock = sock
        self.username = username
        self.tag_counter = 10
        self._current_folder = None
    
    def _next_tag(self):
        self.tag_counter += 1
        return f"B{self.tag_counter:02d}"
    
    def _cmd(self, cmd):
        tag = self._next_tag()
        self.sock.sendall(f"{tag} {cmd}\r\n".encode())
        return _read_response(self.sock)
    
    def select_folder(self, folder):
        resp = self._cmd(f'SELECT "{folder}"')
        self._current_folder = folder
        return resp
    
    def search(self, criteria="ALL"):
        if isinstance(criteria, list):
            criteria_str = " ".join(str(c) for c in criteria)
        else:
            criteria_str = str(criteria)
        resp = self._cmd(f'SEARCH {criteria_str}')
        # 解析 SEARCH 响应中的 UID 列表
        uids = []
        for line in resp:
            if line.startswith("* SEARCH") or line.startswith("* SEARCH\r\n"):
                part = line.replace("* SEARCH", "").strip()
                if part:
                    uids.extend(int(x) for x in part.split() if x.isdigit())
        return uids
    
    def fetch(self, messages, parts):
        """获取邮件数据。parts 可以是字符串或列表。"""
        if isinstance(parts, list):
            parts_str = " ".join(parts)
        else:
            parts_str = str(parts)
        
        if isinstance(messages, list):
            msg_ids = ",".join(str(m) for m in messages)
        else:
            msg_ids = str(messages)
        
        resp = self._cmd(f'FETCH {msg_ids} ({parts_str})')
        
        # 简单解析 FETCH 响应为字典格式
        result = {}
        current_uid = None
        current_data = {}
        fetch_parts_str = parts_str.replace("[", "").replace("]", "")
        fetch_part_list = fetch_parts_str.upper().split()
        
        for line in resp:
            # * UID FETCH ...
            m = _re.match(r'\*\s+(\d+)\s+FETCH', line)
            if m:
                current_uid = int(m.group(1))
                current_data = {}
                continue
            
            if current_uid is not None:
                # 尝试匹配各部分
                for fp in fetch_part_list:
                    prefix = f"{fp} "
                    if prefix in line.lower() or (fp.upper()) + " " in line:
                        # 提取值（简化处理）
                        idx = line.upper().find(fp.upper())
                        if idx >= 0:
                            rest = line[idx + len(fp):].lstrip(": {")
                            # BODY[] 是特殊的大块数据，跨多行
                            if fp.upper() == "BODY[]" or fp.upper().startswith("BODY["):
                                # 收集到下一个 ) 为止
                                current_data[fp.encode()] = rest.encode() if isinstance(rest, str) else rest
                            else:
                                current_data[fp.encode()] = rest
                
                if line.strip() == ")":
                    result[current_uid] = current_data
                    current_uid = None
        
        return result
    
    def get_flags(self, messages):
        resp = self._fetch_flag(messages)
        result = {}
        for mid in (messages if isinstance(messages, list) else [messages]):
            result[mid] = [b"\\Seen"]  # 简化
        return result
    
    def set_flags(self, messages, flags, silent=False):
        flag_str = b" ".join(flags).decode() if isinstance(flags[0], bytes) else " ".join(flags)
        mid = messages if isinstance(messages, int) else messages[0]
        self._cmd(f'STORE {mid} FLAGS ({flag_str})')
        return {mid: flags}
    
    def expunge(self):
        return self._cmd('EXPUNGE')
    
    def append(self, folder, message, flags=None):
        # 简化的 append 实现
        msg_bytes = message.encode() if isinstance(message, str) else message
        length = len(msg_bytes)
        flag_str = f" ({flags.decode() if isinstance(flags, bytes) else flags})" if flags else ""
        self.sock.sendall(f'B99 APPEND "{folder}"{flag_str} {{{length}}}\r\n'.encode())
        resp = _read_line(self.sock)
        if b"+" in resp or b"ready" in resp.lower():
            self.sock.sendall(msg_bytes + b"\r\n")
            resp = _read_response(self.sock)
        return resp
    
    def move(self, messages, folder):
        mid = messages if isinstance(messages, int) else (messages[0] if isinstance(messages, list) else messages)
        self._cmd(f'MOVE {mid} "{folder}"')
    
    def list_folders(self):
        resp = self._cmd('LIST "" "*"')
        folders = []
        for line in resp:
            if 'LIST' in line.upper():
                folders.append(("", "", line.split('"')[-2] if '"' in line else line))
        return folders
    
    def logout(self):
        try:
            self._cmd('LOGOUT')
            self.sock.close()
        except Exception:
            pass


def _read_line(sock):
    """从 socket 读取一行"""
    data = b""
    while True:
        ch = sock.recv(1)
        if ch in (b"\n",):
            break
        if ch == b"":
            break
        data += ch
    return data


def _read_response(sock):
    """读取完整的 IMAP 响应（多行）"""
    lines = []
    while True:
        line = _read_line(sock)
        if isinstance(line, bytes):
            try:
                line = line.decode("utf-8", errors="replace")
            except Exception:
                line = repr(line)
        lines.append(line)
        # 响应结束标记：tag OK / tag NO / tag BAD
        stripped = line.strip()
        if stripped and (stripped.startswith(("B", "A")) and any(stripped.endswith(x) for x in ("OK)", "OK", "NO)", "NO", "BAD)", "BAD"))):
            # 进一步确认是 tag 开头
            parts = stripped.split(None, 1)
            if len(parts) >= 2 and parts[0].startswith(("B", "A")):
                break
        # 也检查不带括号的格式
        if stripped and _re.match(r'^[AB]\d+\s+(OK|NO|BAD)', stripped):
            break
    return lines


def _fetch_flag(messages):
    """内部辅助：获取标志"""
    return []


def get_imap_client(config=None):
    """创建已登录的 IMAP 客户端"""
    if config is None:
        config = get_config()
    
    imap_cfg = config.get("imap", {})
    smtp_cfg = config.get("smtp", {})
    acct_cfg = config.get("account", {})
    
    host = imap_cfg.get("host")
    port = int(imap_cfg.get("port", 993))
    login = imap_cfg.get("login") or acct_cfg.get("email", "")
    password = imap_cfg.get("password") or smtp_cfg.get("password", "")
    require_id = imap_cfg.get("require_imap_id", False)
    encryption = imap_cfg.get("encryption", "tls")
    
    return create_imap_client_with_id(host, port, login, password, require_id, encryption)


def get_smtp_client(config=None):
    """创建 SMTP 客户端上下文管理器"""
    if config is None:
        config = get_config()
    return config


def get_smtp_config(config=None):
    """获取 SMTP 配置参数"""
    if config is None:
        config = get_config()
    smtp_cfg = config.get("smtp", {})
    acct_cfg = config.get("account", {})
    return {
        "host": smtp_cfg.get("host"),
        "port": int(smtp_cfg.get("port", 465)),
        "encryption": smtp_cfg.get("encryption", "tls"),
        "login": smtp_cfg.get("login") or acct_cfg.get("email", ""),
        "password": smtp_cfg.get("password", ""),
    }


def get_email_user(config=None):
    """获取当前邮箱地址"""
    if config is None:
        config = get_config()
    return config.get("account", {}).get("email", "")


# ============================================================
# 工具函数
# ============================================================

def decode_str(s):
    """解码邮件头部的编码字符串"""
    if s is None:
        return ""
    if isinstance(s, bytes):
        try:
            s = s.decode("utf-8")
        except (UnicodeDecodeError, LookupError):
            s = s.decode("latin-1")
    if not isinstance(s, str):
        return str(s)
    parts = decode_header(s)
    result = []
    for data, charset in parts:
        if isinstance(data, bytes):
            charset = charset or "utf-8"
            try:
                result.append(data.decode(charset))
            except (LookupError, UnicodeDecodeError):
                result.append(data.decode("utf-8", errors="replace"))
        else:
            result.append(data)
    return "".join(result).strip()


def format_date(date_str):
    """格式化日期显示"""
    if not date_str:
        return ""
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(date_str)
        if dt.tzinfo:
            dt_local = dt.astimezone(CST)
        else:
            dt_local = dt.replace(tzinfo=CST)
        return dt_local.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return date_str


def extract_body(msg):
    """提取邮件纯文本正文"""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition") or "")
            if content_type == "text/plain" and "attachment" not in content_disposition:
                payload = part.get_payload(decode=True)
                charset = part.get_content_charset() or "utf-8"
                try:
                    return payload.decode(charset)
                except (LookupError, UnicodeDecodeError):
                    return payload.decode("utf-8", errors="replace")
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition") or "")
            if content_type == "text/html" and "attachment" not in content_disposition:
                payload = part.get_payload(decode=True)
                charset = part.get_content_charset() or "utf-8"
                try:
                    html = payload.decode(charset)
                    text = _re.sub(r"<[^>]+>", "", html)
                    text = _re.sub(r"\s+", " ", text).strip()
                    return f"[HTML 邮件]\n{text}"
                except Exception:
                    return "[无法解析的 HTML 内容]"
        return "[空内容]"
    else:
        payload = msg.get_payload(decode=True)
        if payload is None:
            return "[空内容]"
        charset = msg.get_content_charset() or "utf-8"
        try:
            return payload.decode(charset)
        except (LookupError, UnicodeDecodeError):
            return payload.decode("utf-8", errors="replace")


def addr_display(envelope, field):
    """安全地获取地址显示名"""
    addrs = getattr(envelope, field) or []
    if not addrs:
        return ""
    first = addrs[0] if isinstance(addrs, (list, tuple)) else addrs
    if hasattr(first, "name"):
        name = decode_str(getattr(first, "name", None))
        if name:
            return name
        mailbox = getattr(first, "mailbox", None)
        host = getattr(first, "host", None)
        if mailbox:
            return f"{mailbox}@{host}" if host else str(mailbox)
    return str(first)


def addr_list_display(envelope, field):
    """获取地址列表的显示字符串"""
    addrs = getattr(envelope, field) or []
    results = []
    for a in addrs:
        if hasattr(a, "name"):
            name = decode_str(getattr(a, "name", None))
            if name:
                results.append(name)
            else:
                mb = getattr(a, "mailbox", None)
                h = getattr(a, "host", None)
                results.append(f"{mb}@{h}" if mb else str(a))
        else:
            results.append(str(a))
    return ", ".join(results)


def print_table(rows, headers):
    """打印格式化表格"""
    if not rows:
        print("(无结果)")
        return
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    print(header_line)
    print("-" * len(header_line))
    for row in rows:
        line = " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
        print(line)


def get_messages_sorted(m, criteria="ALL", limit=20):
    """搜索邮件并按 UID 降序排列（最新的在前）"""
    messages = m.search(criteria)
    msg_ids = sorted(messages, reverse=True)[:limit]
    if not msg_ids:
        return {}
    fetched = m.fetch(msg_ids, ["ENVELOPE"])
    from collections import OrderedDict
    ordered = OrderedDict()
    for mid in msg_ids:
        ordered[mid] = fetched[mid]
    return ordered


# ============================================================
# 初始化命令
# ============================================================

PRESETS = {
    "tencent": {
        "name": "腾讯企业邮箱",
        "account": {"email": "", "display_name": ""},
        "imap": {
            "host": "imap.exmail.qq.com",
            "port": 993,
            "encryption": "tls",
            "login": "",
            "password": "",
            "require_imap_id": False,
        },
        "smtp": {
            "host": "smtp.exmail.qq.com",
            "port": 465,
            "encryption": "tls",
            "login": "",
            "password": "",
        },
    },
    "qq": {
        "name": "QQ 邮箱",
        "account": {"email": "", "display_name": ""},
        "imap": {
            "host": "imap.qq.com",
            "port": 993,
            "encryption": "tls",
            "login": "",
            "password": "",
            "require_imap_id": False,
        },
        "smtp": {
            "host": "smtp.qq.com",
            "port": 465,
            "encryption": "tls",
            "login": "",
            "password": "",
        },
    },
    "163": {
        "name": "163 网易邮箱",
        "account": {"email": "", "display_name": ""},
        "imap": {
            "host": "imap.163.com",
            "port": 993,
            "encryption": "tls",
            "login": "",
            "password": "",
            "require_imap_id": True,  # 关键！网易需要 IMAP ID
        },
        "smtp": {
            "host": "smtp.163.com",
            "port": 465,
            "encryption": "tls",
            "login": "",
            "password": "",
        },
    },
    "126": {
        "name": "126 网易邮箱",
        "account": {"email": "", "display_name": ""},
        "imap": {
            "host": "imap.126.com",
            "port": 993,
            "encryption": "tls",
            "login": "",
            "password": "",
            "require_imap_id": True,  # 关键！网易需要 IMAP ID
        },
        "smtp": {
            "host": "smtp.126.com",
            "port": 465,
            "encryption": "tls",
            "login": "",
            "password": "",
        },
    },
    "gmail": {
        "name": "Gmail",
        "account": {"email": "", "display_name": ""},
        "imap": {
            "host": "imap.gmail.com",
            "port": 993,
            "encryption": "tls",
            "login": "",
            "password": "",  # 应用专用密码
            "require_imap_id": False,
        },
        "smtp": {
            "host": "smtp.gmail.com",
            "port": 587,
            "encryption": "starttls",
            "login": "",
            "password": "",
        },
    },
    "outlook": {
        "name": "Outlook / Hotmail",
        "account": {"email": "", "display_name": ""},
        "imap": {
            "host": "outlook.office365.com",
            "port": 993,
            "encryption": "tls",
            "login": "",
            "password": "",
            "require_imap_id": False,
        },
        "smtp": {
            "host": "smtp.office365.com",
            "port": 587,
            "encryption": "starttls",
            "login": "",
            "password": "",
        },
    },
}


def cmd_init(args):
    """交互式初始化配置"""
    print("=" * 50)
    print("  bingo-email 初始化向导")
    print("=" * 50)
    print()
    
    # 选择邮箱类型
    print("选择你的邮箱服务商:")
    preset_keys = list(PRESETS.keys())
    for i, key in enumerate(preset_keys):
        info = PRESETS[key]
        print(f"  {i + 1}. {info['name']} ({key})")
    print(f"  {len(preset_keys) + 1}. 自定义/其他")
    print()
    
    choice = input("请输入编号 [1-{}]: ".format(len(preset_keys) + 1)).strip()
    try:
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < len(preset_keys):
            preset_key = preset_keys[choice_idx]
            import copy
            config = copy.deepcopy(PRESETS[preset_key])
            print(f"\n已选择: {PRESETS[preset_key]['name']}")
        elif choice_idx == len(preset_keys):
            config = copy.deepcopy(DEFAULT_CONFIG)
            print("\n已选择: 自定义配置")
        else:
            print("\n无效选择，将使用自定义配置")
            import copy
            config = copy.deepcopy(DEFAULT_CONFIG)
    except (ValueError, IndexError):
        print("\n无效输入，将使用自定义配置")
        import copy
        config = copy.deepcopy(DEFAULT_CONFIG)
    
    print()
    
    # 收集用户信息
    email_addr = input("邮箱地址: ").strip()
    if email_addr:
        config["account"]["email"] = email_addr
        config["imap"]["login"] = email_addr
        config["smtp"]["login"] = email_addr
    
    display_name = input("显示名称（可选）: ").strip()
    if display_name:
        config["account"]["display_name"] = display_name
    
    print()
    print("授权码/密码说明:")
    print("  - 腾讯企业邮箱: 在企业邮箱后台 → 设置 → POP/SMTP 服务中获取")
    print("  - QQ 邮箱: 在设置 → 账户 → POP3/SMTP服务 中开启并获取授权码")
    print("  - 163/126: 在设置 → POP3/SMTP/IMAP 中开启并获取授权码")
    print("  - Gmail: 需要「应用专用密码」（非登录密码）")
    print("  - Outlook: 可使用账户密码或应用专用密码")
    print()
    
    password = getpass.getpass("授权码/密码: ").strip()
    if password:
        config["imap"]["password"] = password
        config["smtp"]["password"] = password
    
    # 自定义模式下的额外信息
    if choice_idx == len(preset_keys) or not email_addr:
        print()
        print("自定义服务器配置（留空使用默认值）:")
        
        imap_host = input("IMAP 服务器地址: ").strip()
        if imap_host:
            config["imap"]["host"] = imap_host
        
        imap_port = input("IMAP 端口 [993]: ").strip()
        if imap_port:
            config["imap"]["port"] = int(imap_port)
        
        smtp_host = input("SMTP 服务器地址: ").strip()
        if smtp_host:
            config["smtp"]["host"] = smtp_host
        
        smtp_port = input("SMTP 端口 [465]: ").strip()
        if smtp_port:
            config["smtp"]["port"] = int(smtp_port)
        
        id_choice = input("是否需要 IMAP ID (RFC 2971)? 适用于 126/163 [y/N]: ").strip().lower()
        config["imap"]["require_imap_id"] = id_choice in ("y", "yes")
    
    # 保存配置
    print()
    print("-" * 50)
    print("配置预览:")
    print(f"  邮箱:   {config['account'].get('email', '(未设置)')}")
    print(f"  IMAP:   {config['imap'].get('host', '?')}:{config['imap'].get('port', '?')} (ID={'是' if config['imap'].get('require_imap_id') else '否'})")
    print(f"  SMTP:   {config['smtp'].get('host', '?')}:{config['smtp'].get('port', '?')}")
    print(f"  文件:   {CONFIG_FILE}")
    print("-" * 50)
    
    confirm = input("确认保存? [Y/n]: ").strip().lower()
    if confirm in ("", "y", "yes"):
        save_config(config)
        print(f"\n✓ 配置已保存到 {CONFIG_FILE}")
        print("  你现在可以使用了！试试: python3 bingo_email.py unread")
    else:
        print("\n已取消")


def cmd_test(args):
    """测试配置是否正确"""
    config = get_config()
    acct = config.get("account", {})
    print(f"正在测试连接...")
    print(f"  邮箱: {acct.get('email', '?')}")
    print(f"  IMAP: {config['imap'].get('host')}:{config['imap'].get('port')}")
    print(f"  SMTP: {config['smtp'].get('host')}:{config['smtp'].get('port')}")
    print()
    
    # 测试 IMAP
    try:
        m = get_imap_client(config)
        m.select_folder("INBOX")
        count = len(m.search("ALL"))
        m.logout()
        print(f"  ✓ IMAP 连接成功 — 收件箱共 {count} 封邮件")
    except Exception as e:
        print(f"  ✗ IMAP 连接失败: {e}")
    
    # 测试 SMTP（只验证能否连接和认证，不发邮件）
    try:
        import smtplib
        sc = get_smtp_config(config)
        if sc["encryption"] == "tls":
            with smtplib.SMTP_SSL(sc["host"], sc["port"]) as s:
                s.login(sc["login"], sc["password"])
        elif sc["encryption"] == "starttls":
            with smtplib.SMTP(sc["host"], sc["port"]) as s:
                s.starttls()
                s.login(sc["login"], sc["password"])
        else:
            with smtplib.SMTP(sc["host"], sc["port"]) as s:
                s.login(sc["login"], sc["password"])
        print(f"  ✓ SMTP 连接成功")
    except Exception as e:
        print(f"  ✗ SMTP 连接失败: {e}")


def cmd_check(args):
    """非交互式环境检查 — 供 AI agent 首次调用时诊断环境"""
    import importlib, json

    issues = []
    ok = []

    # 1. 检查 Python 依赖
    try:
        importlib.import_module("imapclient")
        ok.append("Python依赖: imapclient ✓")
    except ImportError:
        issues.append("Python依赖: 缺少 imapclient → 运行 pip3 install imapclient")

    # 2. 检查配置文件
    config_path = CONFIG_FILE
    if not os.path.exists(config_path):
        issues.append(f"配置文件: 不存在 ({config_path}) → 运行 python3 bingo_email.py init")
    else:
        try:
            # 尝试用 toml 解析（兼容 json）
            try:
                import tomllib
                with open(config_path, "rb") as f:
                    cfg = tomllib.load(f)
            except ImportError:
                try:
                    import toml
                    with open(config_path, "r") as f:
                        cfg = toml.load(f)
                except ImportError:
                    # 都没有 toml 库，用简单文本检测
                    with open(config_path, "r") as f:
                        content = f.read()
                    has_email = "email" in content and "@" in content
                    has_password = "password" in content
                    has_imap = "imap" in content
                    has_smtp = "smtp" in content
                    if has_email and has_password and has_imap and has_smtp:
                        ok.append("配置文件: ✓ (TOML 格式)")
                    else:
                        parts = []
                        if not has_email: parts.append("缺少 email")
                        if not has_password: parts.append("缺少 password")
                        if not has_imap: parts.append("IMAP 配置不完整")
                        if not has_smtp: parts.append("SMTP 配置不完整")
                        issues.append(f"配置文件: 存在但不完整 ({', '.join(parts)}) → 运行 python3 bingo_email.py init 补全")
                    # 跳过后续结构化检查
                    cfg = None

            if cfg:
                acct = cfg.get("account", {})
                email = acct.get("email", "")
                has_pwd = bool(acct.get("password"))
                has_imap = all(k in cfg.get("imap", {}) for k in ("host", "port", "login", "password"))
                has_smtp = all(k in cfg.get("smtp", {}) for k in ("host", "port", "login", "password"))

                if email and has_pwd and has_imap and has_smtp:
                    ok.append(f"配置文件: ✓ (邮箱: {email})")
                else:
                    parts = []
                    if not email: parts.append("缺少 email")
                    if not has_pwd: parts.append("缺少 password")
                    if not has_imap: parts.append("IMAP 配置不完整")
                    if not has_smtp: parts.append("SMTP 配置不完整")
                    issues.append(f"配置文件: 存在但不完整 ({', '.join(parts)}) → 运行 python3 bingo_email.py init 补全")
        except Exception as e:
            issues.append(f"配置文件: 存在但解析失败 ({e}) → 删除后重新运行 python3 bingo_email.py init")

    # 输出结果（AI 可读 + 人可读）
    print("=" * 50)
    print("bingo-email 环境检查")
    print("=" * 50)

    for line in ok:
        print(f"  ✓ {line}")

    if issues:
        print()
        print("  需要处理的问题:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. ✗ {issue}")
        print()
        if len(issues) == 1 and "pip3" in issues[0]:
            print("  快速修复: pip3 install imapclient")
        elif any("init" in iss for iss in issues):
            print("  快速修复: python3 bingo_email.py init")
        print()
        print(f"  状态: 需要操作 ({len(issues)} 项)")
        sys.exit(2)   # exit code 2 = 有问题需要用户处理
    else:
        print()
        print(f"  状态: 一切就绪 ✓")
        sys.exit(0)   # exit code 0 = OK


# ============================================================
# 命令实现
# ============================================================

def cmd_list(args):
    """列出最近 N 封邮件"""
    limit = args.limit or 20
    config = get_config()
    m = get_imap_client(config)
    m.select_folder("INBOX")
    messages = get_messages_sorted(m, "ALL", limit)

    rows = []
    for mid, data in messages.items():
        envelope = data[b"ENVELOPE"]
        flags = set(m.get_flags([mid])[mid])
        flag_mark = "*" if SEEN_FLAG not in flags else " "
        subject = decode_str(envelope.subject) or "(无主题)"
        from_name = addr_display(envelope, "sender")
        date_str = format_date(envelope.date)
        if len(subject) > 40:
            subject = subject[:37] + "..."
        rows.append((mid, flag_mark, subject, from_name, date_str))

    m.logout()
    print_table(rows, headers=["ID", "标记", "主题", "发件人", "日期"])


def cmd_unread(args):
    """列出未读邮件"""
    limit = args.limit or 50
    config = get_config()
    m = get_imap_client(config)
    m.select_folder("INBOX")
    messages = get_messages_sorted(m, ["UNSEEN"], limit)

    if not messages:
        print("(没有未读邮件)")
        m.logout()
        return

    rows = []
    for mid, data in messages.items():
        envelope = data[b"ENVELOPE"]
        subject = decode_str(envelope.subject) or "(无主题)"
        from_name = addr_display(envelope, "sender")
        date_str = format_date(envelope.date)
        if len(subject) > 40:
            subject = subject[:37] + "..."
        rows.append((mid, "*", subject, from_name, date_str))

    m.logout()
    print_table(rows, headers=["ID", "标记", "主题", "发件人", "日期"])


def cmd_read(args):
    """读取指定 ID 的邮件详情"""
    mail_id = args.id
    config = get_config()
    m = get_imap_client(config)
    m.select_folder("INBOX")

    messages = m.search(["UID", str(mail_id)])
    if not messages:
        print(f"错误: 找不到 ID 为 {mail_id} 的邮件")
        m.logout()
        return

    mid = messages[0]
    data = m.fetch([mid], ["ENVELOPE"])[mid]
    envelope = data[b"ENVELOPE"]

    print(f"From: {addr_display(envelope, 'sender')}")
    print(f"To: {addr_list_display(envelope, 'to')}")
    if envelope.cc:
        print(f"Cc: {addr_list_display(envelope, 'cc')}")
    print(f"Subject: {decode_str(envelope.subject)}")
    print(f"Date: {format_date(envelope.date)}")
    if hasattr(envelope, "message_id") and envelope.message_id:
        print(f"Message-ID: {envelope.message_id}")

    print("\n--- 正文 ---\n")
    raw_msg = m.fetch([mid], ["BODY[]"])[mid][b"BODY[]"]
    msg = email.message_from_bytes(raw_msg)
    body = extract_body(msg)
    print(body)

    m.logout()


def cmd_folders(args):
    """列出所有文件夹"""
    config = get_config()
    m = get_imap_client(config)
    folders = m.list_folders()
    m.logout()

    print("文件夹列表:")
    for folder_info in folders:
        name = folder_info[2]
        if isinstance(name, bytes):
            name = name.decode("utf-7").replace("&-", "&")
        flags = folder_info[0] if folder_info[0] else ""
        print(f"  [{flags}] {name}")


def cmd_send(args):
    """发送新邮件"""
    to_addr = args.to
    subject = args.subject
    body = args.body

    if body is None:
        if not sys.stdin.isatty():
            body = sys.stdin.read().strip()
        else:
            print("请输入邮件正文（输入空行结束）:")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            body = "\n".join(lines)

    if not body:
        print("错误: 邮件正文不能为空")
        sys.exit(1)

    config = get_config()
    email_user = get_email_user(config)
    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = email_user
    msg["To"] = to_addr
    msg["Subject"] = subject

    import smtplib
    sc = get_smtp_config(config)
    _send_smtp(msg, email_user, sc)

    print(f"✓ 邮件已发送至 {to_addr}")


def _send_smtp(msg, from_addr, sc):
    """通过 SMTP 发送邮件"""
    import smtplib
    if sc["encryption"] == "tls":
        with smtplib.SMTP_SSL(sc["host"], sc["port"]) as s:
            s.login(sc["login"], sc["password"])
            s.send_message(msg)
    elif sc["encryption"] == "starttls":
        with smtplib.SMTP(sc["host"], sc["port"]) as s:
            s.starttls()
            s.login(sc["login"], sc["password"])
            s.send_message(msg)
    else:
        with smtplib.SMTP(sc["host"], sc["port"]) as s:
            s.login(sc["login"], sc["password"])
            s.send_message(msg)


def _build_reply_message(orig_msg, email_user, body, reply_all=False):
    """
    构建回复邮件消息（MIMEText）。

    包含：
    - 标准的 In-Reply-To / References 头
    - Re: 前缀主题（避免重复）
    - 原始邮件的 inline quote 引用（> 前缀）
    - reply_all=True 时自动 Cc 给原始 To/Cc 中的其他收件人

    Args:
        orig_msg: 原始邮件 (email.message.Message)
        email_user: 当前用户邮箱地址
        body: 用户输入的回复正文
        reply_all: 是否回复所有人

    Returns:
        (msg, to_addr_str) — MIMEText 对象和目标收件人字符串
    """
    # --- 收件人逻辑 ---
    orig_from = decode_str(orig_msg.get("From", ""))
    # 解析原始 From 中的邮箱地址，去掉显示名
    from_addr = _extract_email(orig_from)

    if reply_all:
        # Reply-All: To = 原始发件人, Cc = 原始 To/Cc 中除自己以外的其他人
        to_addr = from_addr
        cc_list = _build_reply_cc_list(orig_msg, email_user)
    else:
        # 普通回复: 只回复发件人
        to_addr = from_addr
        cc_list = []

    # --- 主题 ---
    subject = decode_str(orig_msg.get("Subject", ""))
    if not subject.upper().startswith("RE:"):
        subject = f"Re: {subject}"

    # --- 正文：拼接用户回复 + 原文引用 ---
    original_body = extract_body(orig_msg)
    quoted_original = _quote_original(original_body, orig_from)
    full_body = body + "\n\n" + quoted_original

    # --- 构建消息 ---
    msg = MIMEMultipart()
    msg["From"] = email_user
    msg["To"] = to_addr
    if cc_list:
        msg["Cc"] = ", ".join(cc_list)
    msg["Subject"] = subject

    message_id = orig_msg.get("Message-ID", "")
    if message_id:
        msg["In-Reply-To"] = message_id
        refs = orig_msg.get("References") or ""
        msg["References"] = f"{refs} {message_id}".strip()

    msg.attach(MIMEText(full_body, "plain", "utf-8"))

    return msg


def _extract_email(from_header):
    """从 From 头中提取纯邮箱地址"""
    if not from_header:
        return from_header
    # 尝试从 <addr> 格式提取
    m = _re.search(r'<([^>]+)>', from_header)
    if m:
        return m.group(1)
    # 如果没有 <>，检查是否像纯邮箱
    if "@" in from_header:
        return from_header.strip()
    return from_header


def _build_reply_cc_list(orig_msg, email_user):
    """
    构建 Reply-All 的 Cc 列表。
    规则：
    - 收集原始邮件的 To 和 Cc 中所有地址
    - 排除当前用户自己（不要 Cc 给自己）
    - 排除原始发件人（已经在 To 里了）
    """
    import email.utils
    self_addrs = _normalize_addr_set(email_user)
    from_addr = _normalize_addr_set(decode_str(orig_msg.get("From", "")))

    all_recipients = []
    for header_name in ("To", "Cc"):
        hdr_val = orig_msg.get(header_name, "")
        if hdr_val:
            # email.utils.getaddresses 可以解析 "Name <addr>, Name2 <addr2>" 格式
            pairs = email.utils.getaddresses([hdr_val])
            for _, addr in pairs:
                if addr:
                    all_recipients.append(addr.lower().strip())

    # 去重、排除自己和发件人
    seen = set()
    cc_list = []
    for addr in all_recipients:
        if addr in seen:
            continue
        seen.add(addr)
        if addr in self_addrs or addr in from_addr:
            continue
        cc_list.append(addr)

    return cc_list


def _quote_original(body, from_label):
    """
    将原始邮件正文格式化为标准 inline quote。
    使用 > 前缀，每行都加上引用标记。
    """
    lines = body.split("\n")
    quoted_lines = []
    for line in lines:
        quoted_lines.append(f"> {line}")
    header = f"\n---- {from_label} 写道 ----"
    footer = "\n--------------------------------"
    return header + "\n" + "\n".join(quoted_lines) + footer


def _normalize_addr_set(addr_str):
    """将地址字符串规范化为小写集合"""
    import email.utils
    if not addr_str:
        set()
    pairs = email.utils.getaddresses([addr_str])
    return {a.lower().strip() for _, a in pairs if a}


def cmd_reply(args):
    """回复指定邮件（支持 --all 回复所有人）"""
    mail_id = args.id
    body = args.body
    reply_all = getattr(args, "all", False)

    if body is None:
        if not sys.stdin.isatty():
            body = sys.stdin.read().strip()
        else:
            print("请输入回复正文（输入空行结束）:")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            body = "\n".join(lines)

    if not body:
        print("错误: 回复正文不能为空")
        sys.exit(1)

    config = get_config()
    email_user = get_email_user(config)
    m = get_imap_client(config)
    m.select_folder("INBOX")
    messages = m.search(["UID", str(mail_id)])
    if not messages:
        print(f"错误: 找不到 ID 为 {mail_id} 的邮件")
        m.logout()
        sys.exit(1)

    mid = messages[0]
    raw_msg = m.fetch([mid], ["BODY[]"])[mid][b"BODY[]"]
    orig_msg = email.message_from_bytes(raw_msg)
    m.logout()

    msg = _build_reply_message(orig_msg, email_user, body, reply_all=reply_all)

    sc = get_smtp_config(config)
    _send_smtp(msg, email_user, sc)

    action = "回复已发送（全部）" if reply_all else "回复已发送"
    print(f"✓ {action}")


def cmd_forward(args):
    """转发指定邮件"""
    mail_id = args.id
    to_addr = args.to
    extra_text = args.body or ""

    config = get_config()
    email_user = get_email_user(config)
    m = get_imap_client(config)
    m.select_folder("INBOX")
    messages = m.search(["UID", str(mail_id)])
    if not messages:
        print(f"错误: 找不到 ID 为 {mail_id} 的邮件")
        m.logout()
        sys.exit(1)

    mid = messages[0]
    raw_msg = m.fetch([mid], ["BODY[]"])[mid][b"BODY[]"]
    orig_msg = email.message_from_bytes(raw_msg)
    m.logout()

    subject = decode_str(orig_msg.get("Subject", ""))
    fwd_subject = f"Fwd: {subject}"
    original_body = extract_body(orig_msg)
    body = extra_text + "\n\n---------- 转发的邮件 ----------\n" + original_body

    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = email_user
    msg["To"] = to_addr
    msg["Subject"] = fwd_subject

    sc = get_smtp_config(config)
    _send_smtp(msg, email_user, sc)

    print(f"✓ 已转发至 {to_addr}")


def cmd_draft(args):
    """写新邮件草稿到草稿箱"""
    to_addr = args.to
    subject = args.subject
    body = args.body

    if body is None:
        if not sys.stdin.isatty():
            body = sys.stdin.read().strip()
        else:
            print("请输入邮件正文（输入空行结束）:")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            body = "\n".join(lines)

    config = get_config()
    email_user = get_email_user(config)
    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = email_user
    msg["To"] = to_addr
    msg["Subject"] = subject

    m = get_imap_client(config)
    m.select_folder("Drafts")
    m.append("Drafts", msg.as_string())
    m.logout()
    print("✓ 草稿已保存到草稿箱")


def cmd_draft_reply(args):
    """写回复草稿到草稿箱（支持 --all 回复所有人）"""
    mail_id = args.id
    body = args.body
    reply_all = getattr(args, "all", False)

    if body is None:
        if not sys.stdin.isatty():
            body = sys.stdin.read().strip()
        else:
            print("请输入回复正文（输入空行结束）:")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            body = "\n".join(lines)

    config = get_config()
    email_user = get_email_user(config)
    m = get_imap_client(config)
    m.select_folder("INBOX")
    messages = m.search(["UID", str(mail_id)])
    if not messages:
        print(f"错误: 找不到 ID 为 {mail_id} 的邮件")
        m.logout()
        sys.exit(1)

    mid = messages[0]
    raw_msg = m.fetch([mid], ["BODY[]"])[mid][b"BODY[]"]
    orig_msg = email.message_from_bytes(raw_msg)
    m.logout()

    msg = _build_reply_message(orig_msg, email_user, body, reply_all=reply_all)

    m = get_imap_client(config)
    m.select_folder("Drafts")
    m.append("Drafts", msg.as_string())
    m.logout()

    action = "回复全部草稿" if reply_all else "回复草稿"
    print(f"✓ {action}已保存到草稿箱")


def cmd_delete(args):
    """删除邮件（移至已删除）"""
    mail_id = args.id
    config = get_config()
    m = get_imap_client(config)
    m.select_folder("INBOX")
    messages = m.search(["UID", str(mail_id)])
    if not messages:
        print(f"错误: 找不到 ID 为 {mail_id} 的邮件")
        m.logout()
        sys.exit(1)

    mid = list(messages)[0]
    m.set_flags(mid, [b"\\Deleted"], silent=False)
    m.expunge()
    m.logout()
    print(f"✓ 邮件 {mail_id} 已删除")


def cmd_move(args):
    """移动邮件到其他文件夹"""
    mail_id = args.id
    folder = args.folder
    config = get_config()
    m = get_imap_client(config)
    m.select_folder("INBOX")
    messages = m.search(["UID", str(mail_id)])
    if not messages:
        print(f"错误: 找不到 ID 为 {mail_id} 的邮件")
        m.logout()
        sys.exit(1)

    mid = list(messages)[0]

    try:
        m.move([mid], folder)
        print(f"✓ 邮件 {mail_id} 已移至 {folder}")
    except Exception as e:
        print(f"错误: 移动失败 - {e}")
        print(f"可用的文件夹:")
        folders = m.list_folders()
        for fi in folders:
            name = fi[2]
            if isinstance(name, bytes):
                name = name.decode("utf-7").replace("&-", "&")
            print(f"  {name}")
    finally:
        m.logout()


# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        prog="bingo-email",
        description="统一邮件管理工具 (IMAP + SMTP)",
    )
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # 初始化 & 测试 & 环境检查
    subparsers.add_parser("init", help="首次运行：交互式配置邮箱")
    subparsers.add_parser("test", help="测试当前配置是否能正常连接")
    subparsers.add_parser("check", help="检查环境依赖和配置状态（非交互式，适合自动诊断）")

    p_list = subparsers.add_parser("list", help="列出最近邮件")
    p_list.add_argument("limit", nargs="?", type=int, default=None, help="数量限制")

    p_unread = subparsers.add_parser("unread", help="列出未读邮件")
    p_unread.add_argument("limit", nargs="?", type=int, default=None, help="数量限制")

    p_read = subparsers.add_parser("read", help="读取邮件详情")
    p_read.add_argument("id", type=int, help="邮件ID")

    subparsers.add_parser("folders", help="列出文件夹")

    p_send = subparsers.add_parser("send", help="发送邮件")
    p_send.add_argument("to", help="收件人地址")
    p_send.add_argument("subject", help="邮件主题")
    p_send.add_argument("--body", default=None, help="邮件正文")

    p_reply = subparsers.add_parser("reply", help="回复邮件")
    p_reply.add_argument("id", type=int, help="回复的邮件ID")
    p_reply.add_argument("--body", default=None, help="回复正文")
    p_reply.add_argument("--all", action="store_true", dest="all",
                         help="回复所有人（Reply-All），自动 Cc 给原始邮件 To/Cc 中的其他收件人")

    p_fwd = subparsers.add_parser("forward", help="转发邮件")
    p_fwd.add_argument("id", type=int, help="转发的邮件ID")
    p_fwd.add_argument("to", help="目标地址")
    p_fwd.add_argument("--body", default=None, help="附加说明")

    p_draft = subparsers.add_parser("draft", help="写草稿")
    p_draft.add_argument("--to", required=True, help="收件人地址")
    p_draft.add_argument("--subject", required=True, help="邮件主题")
    p_draft.add_argument("--body", default=None, help="邮件正文")

    p_dr = subparsers.add_parser("draft-reply", help="写回复草稿")
    p_dr.add_argument("id", type=int, help="回复的邮件ID")
    p_dr.add_argument("--body", default=None, help="回复正文")
    p_dr.add_argument("--all", action="store_true", dest="all",
                       help="回复所有人草稿（Reply-All），自动 Cc 给原始邮件 To/Cc 中的其他收件人")

    p_del = subparsers.add_parser("delete", help="删除邮件")
    p_del.add_argument("id", type=int, help="邮件ID")

    p_move = subparsers.add_parser("move", help="移动邮件")
    p_move.add_argument("id", type=int, help="邮件ID")
    p_move.add_argument("folder", help="目标文件夹")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    commands = {
        "init": cmd_init,
        "test": cmd_test,
        "check": cmd_check,
        "list": cmd_list,
        "unread": cmd_unread,
        "read": cmd_read,
        "folders": cmd_folders,
        "send": cmd_send,
        "reply": cmd_reply,
        "forward": cmd_forward,
        "draft": cmd_draft,
        "draft-reply": cmd_draft_reply,
        "delete": cmd_delete,
        "move": cmd_move,
    }

    fn = commands.get(args.command)
    if fn:
        try:
            fn(args)
        except KeyboardInterrupt:
            print("\n操作已取消")
        except Exception as e:
            print(f"错误: {e}")
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
