"""
邮件获取器 — IMAP 拉取未读邮件
"""
import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
import time
from typing import Optional
from dataclasses import dataclass, field

from .config_loader import get_config


@dataclass
class EmailMessage:
    """标准化邮件数据结构"""
    uid: str                          # IMAP UID
    message_id: str                   # Message-ID 头
    from_addr: str                    # 发件人地址
    from_name: str                    # 发件人名称
    to_addr: str                      # 收件人
    subject: str                      # 主题
    body_plain: str                   # 纯文本正文
    body_html: str                    # HTML 正文 (备用)
    date: str                         # ISO 日期
    in_reply_to: str = ""             # 回复引用
    references: str = ""              # 引用链
    attachments: list = field(default_factory=list)  # [(filename, mimetype, size)]
    raw_headers: dict = field(default_factory=dict)
    auto_submitted: bool = False      # 是否为自动回复/退信


class EmailFetcher:
    """IMAP 邮件获取器"""

    def __init__(self, config: dict = None):
        cfg = config or get_config()
        imap_cfg = cfg["imap"]
        self.server = imap_cfg["server"]
        self.port = imap_cfg["port"]
        self.username = imap_cfg["username"]
        self.password = imap_cfg["password"]
        self.mailbox = imap_cfg.get("mailbox", "INBOX")
        self.conn: Optional[imaplib.IMAP4_SSL] = None

    def connect(self):
        """建立 IMAP 连接"""
        self.conn = imaplib.IMAP4_SSL(self.server, self.port)
        self.conn.login(self.username, self.password)
        self.conn.select(self.mailbox)

    def disconnect(self):
        """断开连接"""
        if self.conn:
            try:
                self.conn.close()
                self.conn.logout()
            except Exception:
                pass

    def fetch_unread(self, limit: int = 50) -> list[EmailMessage]:
        """拉取未读邮件"""
        if not self.conn:
            self.connect()

        # 搜索未读邮件
        status, messages = self.conn.search(None, "UNSEEN")
        if status != "OK":
            return []

        uids = messages[0].split()
        if not uids:
            return []

        # 限制数量，从最新开始
        uids = uids[-limit:]

        emails = []
        for uid in uids:
            status, msg_data = self.conn.fetch(uid, "(RFC822)")
            if status != "OK":
                continue

            raw_email = msg_data[0][1]
            parsed = self._parse_email(uid.decode(), raw_email)
            if parsed:
                emails.append(parsed)

        return emails

    def mark_read(self, uid: str):
        """标记邮件为已读"""
        if self.conn:
            self.conn.store(uid, "+FLAGS", "\\Seen")

    def _parse_email(self, uid: str, raw_bytes: bytes) -> Optional[EmailMessage]:
        """解析原始邮件为 EmailMessage"""
        try:
            msg = email.message_from_bytes(raw_bytes)
        except Exception:
            return None

        # 解析头部
        subject = self._decode_header(msg.get("Subject", "(No Subject)"))
        from_header = self._decode_header(msg.get("From", ""))
        from_name, from_addr = self._parse_from(from_header)
        to_addr = self._decode_header(msg.get("To", ""))
        message_id = msg.get("Message-ID", uid)
        in_reply_to = msg.get("In-Reply-To", "")
        references = msg.get("References", "")
        date_str = msg.get("Date", "")
        auto_submitted = msg.get("Auto-Submitted", "") != ""

        try:
            date_iso = parsedate_to_datetime(date_str).isoformat() if date_str else ""
        except Exception:
            date_iso = ""

        # 提取正文
        body_plain = ""
        body_html = ""
        attachments = []

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                disposition = str(part.get("Content-Disposition", ""))

                if "attachment" in disposition:
                    filename = part.get_filename()
                    if filename:
                        attachments.append((
                            self._decode_header(filename),
                            content_type,
                            len(part.get_payload(decode=True) or b"")
                        ))
                elif content_type == "text/plain":
                    payload = part.get_payload(decode=True)
                    if payload:
                        body_plain = self._decode_payload(payload)
                elif content_type == "text/html":
                    payload = part.get_payload(decode=True)
                    if payload:
                        body_html = payload.decode("utf-8", errors="replace")
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                body_plain = self._decode_payload(payload)

        # 收集关键头部
        raw_headers = {
            "from": from_header,
            "to": to_addr,
            "subject": subject,
            "date": date_str,
            "message-id": message_id,
            "content-type": msg.get("Content-Type", ""),
            "auto-submitted": msg.get("Auto-Submitted", ""),
            "precedence": msg.get("Precedence", ""),
            "list-unsubscribe": msg.get("List-Unsubscribe", ""),
        }

        return EmailMessage(
            uid=uid,
            message_id=message_id,
            from_addr=from_addr,
            from_name=from_name,
            to_addr=to_addr,
            subject=subject,
            body_plain=body_plain,
            body_html=body_html,
            date=date_iso,
            in_reply_to=in_reply_to,
            references=references,
            attachments=attachments,
            raw_headers=raw_headers,
            auto_submitted=auto_submitted,
        )

    @staticmethod
    def _decode_header(value: str) -> str:
        """解码 RFC 2047 编码的邮件头"""
        if not value:
            return ""
        parts = decode_header(value)
        result = []
        for part, charset in parts:
            if isinstance(part, bytes):
                try:
                    result.append(part.decode(charset or "utf-8", errors="replace"))
                except Exception:
                    result.append(part.decode("utf-8", errors="replace"))
            else:
                result.append(str(part))
        return "".join(result).strip()

    @staticmethod
    def _parse_from(from_str: str) -> tuple[str, str]:
        """解析 From 头: 'Name <addr>' → (name, addr)"""
        if not from_str:
            return "", ""
        # 匹配 "Name <email>" 格式
        import re
        match = re.match(r'(.*?)\s*<(.+?)>', from_str)
        if match:
            return match.group(1).strip().strip('"'), match.group(2).strip()
        # 纯地址
        if "@" in from_str:
            return "", from_str.strip()
        return from_str.strip(), ""

    @staticmethod
    def _decode_payload(payload: bytes) -> str:
        """解码邮件正文"""
        encodings = ["utf-8", "gbk", "gb2312", "iso-8859-1", "latin-1"]
        for enc in encodings:
            try:
                return payload.decode(enc)
            except (UnicodeDecodeError, LookupError):
                continue
        return payload.decode("utf-8", errors="replace")
