"""
Email Client - IMAP/SMTP 邮件客户端
支持 Gmail, QQ, Outlook 等主流邮件服务
凭证从技能目录下的 .env 文件读取
"""

import os
import base64
import re
import sys
import email
from html import unescape
from email.header import Header, decode_header
from email.utils import formataddr, getaddresses
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from datetime import datetime
from typing import Optional, List, Dict, Any


class EmailClient:
    """邮件客户端封装"""

    def __init__(self, skill_dir: str = None):
        """
        初始化邮件客户端

        Args:
            skill_dir: 技能目录路径，用于读取 .env 文件
        """
        # 确定技能目录
        if skill_dir is None:
            current_file = os.path.abspath(__file__)
            skill_dir = os.path.dirname(os.path.dirname(current_file))

        # 读取 .env 文件
        self._load_env(skill_dir)

        self.address = os.getenv("EMAIL_ADDRESS")
        self.imap_password = os.getenv("EMAIL_IMAP_PASSWORD")
        self.smtp_password = os.getenv("EMAIL_SMTP_PASSWORD")
        self.imap_host = os.getenv("EMAIL_IMAP_HOST", self._get_default_imap_host())
        self.imap_port = int(os.getenv("EMAIL_IMAP_PORT", "993"))
        self.smtp_host = os.getenv("EMAIL_SMTP_HOST", self._get_default_smtp_host())
        self.smtp_port = int(os.getenv("EMAIL_SMTP_PORT", "587"))
        self.smtp_ssl = os.getenv("EMAIL_SMTP_SSL", "").lower() in {"1", "true", "yes", "on"}
        self._imap_id_sent = False

        if not self.address or not self.imap_password:
            raise ValueError(
                f"请在 {skill_dir}/.env 中配置 EMAIL_ADDRESS 和 EMAIL_IMAP_PASSWORD"
            )

        self._imap_conn = None
        self._smtp_conn = None

    def _load_env(self, skill_dir: str):
        """从技能目录加载 .env 文件"""
        env_path = os.path.join(skill_dir, ".env")
        if not os.path.exists(env_path):
            return

        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    os.environ[key] = value

    def _get_default_imap_host(self) -> str:
        """根据邮箱域名推断默认 IMAP 主机"""
        if not self.address:
            return ""
        domain = self.address.split("@")[-1].lower()
        hosts = {
            "gmail.com": "imap.gmail.com",
            "qq.com": "imap.qq.com",
            "foxmail.com": "imap.qq.com",
            "outlook.com": "outlook.office365.com",
            "hotmail.com": "outlook.office365.com",
        }
        return hosts.get(domain, f"imap.{domain}")

    def _get_default_smtp_host(self) -> str:
        """根据邮箱域名推断默认 SMTP 主机"""
        if not self.address:
            return ""
        domain = self.address.split("@")[-1].lower()
        hosts = {
            "gmail.com": "smtp.gmail.com",
            "qq.com": "smtp.qq.com",
            "foxmail.com": "smtp.qq.com",
            "outlook.com": "smtp.office365.com",
            "hotmail.com": "smtp.office365.com",
        }
        return hosts.get(domain, f"smtp.{domain}")

    def _connect_imap(self):
        """建立 IMAP 连接"""
        import imaplib

        if self._imap_conn is None:
            self._imap_conn = imaplib.IMAP4_SSL(
                host=self.imap_host, port=self.imap_port
            )
            self._imap_conn.login(self.address, self.imap_password)
            self._send_imap_id()
        return self._imap_conn

    def _send_imap_id(self):
        """在支持 ID 扩展的服务器上发送客户端标识。"""
        if self._imap_id_sent or self._imap_conn is None:
            return

        capabilities = getattr(self._imap_conn, "capabilities", ())
        normalized = {
            c.decode("ascii", errors="ignore") if isinstance(c, bytes) else str(c)
            for c in capabilities
        }
        if "ID" not in normalized:
            return

        try:
            # 163/188 邮箱要求先发送 IMAP ID，否则后续 SELECT/EXAMINE 会被拒绝。
            self._imap_conn.xatom(
                "ID",
                '("name" "OpenCode" "version" "1.0" "vendor" "OpenAI")',
            )
        except Exception:
            return

        self._imap_id_sent = True

    def _select_folder(self, folder: str, readonly: bool = False):
        """选择邮箱文件夹，并在失败时抛出明确错误。"""
        conn = self._connect_imap()
        status, data = conn.select(folder, readonly=readonly)
        if status == "OK":
            return conn

        details = ""
        if data:
            details = "; ".join(
                item.decode("utf-8", errors="replace") if isinstance(item, bytes) else str(item)
                for item in data
            )
        raise RuntimeError(f"无法选择邮箱文件夹 {folder}: {details or status}")

    def _connect_smtp(self):
        """建立 SMTP 连接"""
        import smtplib

        if self._smtp_conn is None:
            use_ssl = self.smtp_ssl or self.smtp_port == 465
            if use_ssl:
                self._smtp_conn = smtplib.SMTP_SSL(host=self.smtp_host, port=self.smtp_port)
            else:
                self._smtp_conn = smtplib.SMTP(host=self.smtp_host, port=self.smtp_port)
                self._smtp_conn.starttls()
            self._smtp_conn.login(self.address, self.smtp_password)
        return self._smtp_conn

    def _decode_str(self, s: str) -> str:
        """解码 email 字符串"""
        if not s:
            return ""
        parts = decode_header(s)
        result = []
        for part, charset in parts:
            if isinstance(part, bytes):
                charset = charset or "utf-8"
                try:
                    result.append(part.decode(charset, errors="replace"))
                except Exception:
                    result.append(part.decode("utf-8", errors="replace"))
            else:
                result.append(part)
        return "".join(result)

    def _parse_email_address(self, addr: str) -> Dict[str, str]:
        """解析邮件地址"""
        if not addr:
            return {"name": "", "email": ""}
        if "<" in addr:
            parts = addr.split("<")
            name = parts[0].strip().strip('"')
            email = parts[1].strip().rstrip(">")
            return {"name": self._decode_str(name), "email": email}
        return {"name": "", "email": addr}

    def _format_header_address(self, email_addr: str, display_name: str = "") -> str:
        """格式化带编码的邮件地址头。"""
        if display_name:
            return formataddr((str(Header(display_name, "utf-8")), email_addr))
        return email_addr

    def _format_recipient_header(self, value: str) -> str:
        """格式化收件人头，兼容中文显示名。"""
        formatted = []
        for name, email_addr in getaddresses([value or ""]):
            if not email_addr:
                continue
            formatted.append(self._format_header_address(email_addr, self._decode_str(name)))
        return ", ".join(formatted)

    def _parse_recipient_emails(self, *values: Optional[str]) -> List[str]:
        """提取 SMTP 投递使用的纯邮箱地址列表。"""
        recipients = []
        for value in values:
            for _, email_addr in getaddresses([value or ""]):
                if email_addr:
                    recipients.append(email_addr)
        return recipients

    def _encode_header(self, value: str) -> str:
        """按 UTF-8 编码邮件头，避免中文主题乱码。"""
        return str(Header(value or "", "utf-8"))

    def _parse_flags(self, flags: List[str]) -> List[str]:
        """解析邮件标志"""
        flag_map = {
            "\\Seen": "已读",
            "\\Flagged": "星标",
            "\\Deleted": "已删除",
            "\\Draft": "草稿",
            "\\Answered": "已回复",
        }
        return [flag_map.get(f, f) for f in flags]

    def _parse_fetch_metadata(self, response_line: bytes) -> Dict[str, Any]:
        """从 FETCH 响应行中提取 UID、FLAGS 和 RFC822.SIZE。"""
        text = response_line.decode("utf-8", errors="replace")

        uid_match = re.search(r"UID\s+(\d+)", text)
        size_match = re.search(r"RFC822\.SIZE\s+(\d+)", text)
        flags_match = re.search(r"FLAGS\s+\((.*?)\)", text)

        flags = flags_match.group(1).split() if flags_match and flags_match.group(1) else []
        return {
            "uid": int(uid_match.group(1)) if uid_match else None,
            "size": int(size_match.group(1)) if size_match else 0,
            "flags": flags,
        }

    def _html_to_text(self, html: str) -> str:
        """把 HTML 正文压缩成可读纯文本。"""
        if not html:
            return ""

        text = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", html)
        text = re.sub(r"(?i)<br\s*/?>", "\n", text)
        text = re.sub(r"(?i)</p\s*>", "\n", text)
        text = re.sub(r"<[^>]+>", " ", text)
        text = unescape(text)
        text = text.replace("\r", "")
        text = re.sub(r"\n\s*\n+", "\n\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        return text.strip()

    def _is_ascii(self, value: str) -> bool:
        """判断搜索条件是否可直接走 IMAP ASCII 搜索。"""
        try:
            value.encode("ascii")
        except UnicodeEncodeError:
            return False
        return True

    def _decode_imap_folder_name(self, folder: str) -> str:
        """解码 IMAP modified UTF-7 文件夹名。"""
        if "&" not in folder:
            return folder

        def replace(match):
            value = match.group(1)
            if value == "-":
                return "&"
            data = value[:-1].replace(",", "/")
            padding = "=" * (-len(data) % 4)
            try:
                return base64.b64decode(data + padding).decode("utf-16-be")
            except Exception:
                return "&" + value

        return re.sub(r"&([A-Za-z0-9+,]+-|-)", replace, folder)

    def _read_text_file(self, file_path: str) -> str:
        """按 UTF-8 优先读取文本文件。"""
        for encoding in ("utf-8", "utf-8-sig", "gb18030"):
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    # ==================== 读取操作 ====================

    def get_inbox(
        self, count: int = 10, offset: int = 0, folder: str = "INBOX"
    ) -> List[Dict[str, Any]]:
        """
        获取收件箱邮件列表

        Args:
            count: 邮件数量
            offset: 起始偏移
            folder: 文件夹名称

        Returns:
            邮件摘要列表
        """
        conn = self._select_folder(folder)

        status, messages = conn.search(None, "ALL")
        if status != "OK":
            return []

        mail_ids = messages[0].split()
        total = len(mail_ids)

        start = max(0, total - offset - count)
        end = max(0, total - offset)
        selected_ids = mail_ids[start:end]

        results = []
        for mail_id in reversed(selected_ids):
            status, msg_data = conn.fetch(
                mail_id,
                "(UID FLAGS RFC822.SIZE BODY.PEEK[HEADER.FIELDS (SUBJECT FROM TO DATE)])",
            )
            if status != "OK":
                continue

            try:
                if not msg_data or not isinstance(msg_data[0], tuple):
                    continue

                metadata = self._parse_fetch_metadata(msg_data[0][0])
                msg = email.message_from_bytes(msg_data[0][1])

                subject = self._decode_str(msg.get("Subject", ""))
                from_addr = self._parse_email_address(self._decode_str(msg.get("From", "")))
                to_addr = self._parse_email_address(self._decode_str(msg.get("To", "")))
                date_str = msg.get("Date", "")
                size = metadata["size"]
                flags = metadata["flags"]

                try:
                    date = datetime.strptime(date_str, "%d %b %Y %H:%M:%S %z").strftime("%Y-%m-%d %H:%M:%S")
                except Exception:
                    date = date_str

                results.append({
                    "uid": metadata["uid"] or int(mail_id),
                    "subject": subject,
                    "from": from_addr.get("email", ""),
                    "from_name": from_addr.get("name", ""),
                    "to": to_addr.get("email", ""),
                    "date": date,
                    "size": size,
                    "flags": self._parse_flags(flags),
                    "is_read": "\\Seen" in flags,
                })
            except Exception as e:
                print(f"解析邮件失败: {e}")
                continue

        return results

    def get_email(self, uid: int, folder: str = "INBOX") -> Optional[Dict[str, Any]]:
        """
        获取单封邮件详情

        Args:
            uid: 邮件 UID
            folder: 文件夹名称

        Returns:
            邮件详情字典
        """
        conn = self._select_folder(folder, readonly=True)

        status, messages = conn.uid("SEARCH", None, f"UID {uid}")
        if status != "OK" or not messages[0]:
            return None

        mail_id = messages[0].split()[0]
        status, msg_data = conn.uid("FETCH", mail_id, "(RFC822)")
        if status != "OK":
            return None

        raw_msg = msg_data[0][1]
        msg = email.message_from_bytes(raw_msg)

        headers = dict(msg.items())

        body = {"plain": "", "html": ""}
        attachments = []

        if msg.is_multipart():
            for i, part in enumerate(msg.walk()):
                content_type = part.get_content_type()
                content_disposition = part.get_content_disposition()

                if content_disposition == "attachment":
                    filename = part.get_filename()
                    if filename:
                        filename = self._decode_str(filename)
                    attachments.append({
                        "index": i,
                        "name": filename or f"attachment_{i}",
                        "size": len(part.get_payload(decode=True) or b""),
                        "type": content_type,
                    })
                elif content_type.startswith("multipart/"):
                    continue
                else:
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or "utf-8"
                        try:
                            text = payload.decode(charset, errors="replace")
                        except Exception:
                            text = payload.decode("utf-8", errors="replace")

                        if content_type == "text/plain":
                            body["plain"] = text
                        elif content_type == "text/html":
                            body["html"] = text
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                charset = msg.get_content_charset() or "utf-8"
                try:
                    body["plain"] = payload.decode(charset, errors="replace")
                except Exception:
                    body["plain"] = payload.decode("utf-8", errors="replace")

        if not body["plain"] and body["html"]:
            body["plain"] = self._html_to_text(body["html"])

        to_addrs = []
        to_header = msg.get("To", "")
        for addr in to_header.split(","):
            addr = addr.strip()
            if addr:
                to_addrs.append(self._parse_email_address(addr))

        return {
            "uid": uid,
            "subject": self._decode_str(msg.get("Subject", "")),
            "from": self._parse_email_address(self._decode_str(msg.get("From", ""))),
            "to": to_addrs,
            "date": msg.get("Date", ""),
            "body": body,
            "attachments": attachments,
            "headers": headers,
        }

    def search_emails(
        self,
        keyword: str = None,
        from_addr: str = None,
        to_addr: str = None,
        date_from: str = None,
        date_to: str = None,
        folder: str = "INBOX",
    ) -> List[Dict[str, Any]]:
        """
        搜索邮件

        Args:
            keyword: 关键词（搜索主题和发件人）
            from_addr: 发件人地址
            to_addr: 收件人地址
            date_from: 开始日期 (YYYY-MM-DD)
            date_to: 结束日期 (YYYY-MM-DD)
            folder: 文件夹名称

        Returns:
            匹配的邮件列表
        """
        conn = self._select_folder(folder)

        criteria = []

        use_local_keyword_filter = False

        if keyword:
            if self._is_ascii(keyword):
                criteria.append(f'OR SUBJECT "{keyword}" FROM "{keyword}"')
            else:
                use_local_keyword_filter = True

        if from_addr:
            criteria.append(f'FROM "{from_addr}"')

        if to_addr:
            criteria.append(f'TO "{to_addr}"')

        if date_from:
            date_from_fmt = datetime.strptime(date_from, "%Y-%m-%d").strftime("%d-%b-%Y")
            criteria.append(f'SINCE {date_from_fmt}')

        if date_to:
            date_to_fmt = datetime.strptime(date_to, "%Y-%m-%d").strftime("%d-%b-%Y")
            criteria.append(f'BEFORE {date_to_fmt}')

        if not criteria:
            criteria.append("ALL")

        search_criteria = " ".join(criteria)
        status, messages = conn.search(None, search_criteria)

        if status != "OK":
            return []

        mail_ids = messages[0].split()
        results = []

        for mail_id in mail_ids[:100]:
            status, msg_data = conn.fetch(
                mail_id,
                "(UID BODY.PEEK[HEADER.FIELDS (SUBJECT FROM DATE)])",
            )
            if status != "OK":
                continue

            try:
                if not msg_data or not isinstance(msg_data[0], tuple):
                    continue

                metadata = self._parse_fetch_metadata(msg_data[0][0])
                msg = email.message_from_bytes(msg_data[0][1])

                results.append({
                    "uid": metadata["uid"] or int(mail_id),
                    "subject": self._decode_str(msg.get("Subject", "")),
                    "from": self._decode_str(msg.get("From", "")),
                    "date": msg.get("Date", ""),
                })
            except Exception:
                continue

        if use_local_keyword_filter:
            keyword_lower = keyword.lower()
            results = [
                item for item in results
                if keyword_lower in item["subject"].lower() or keyword_lower in item["from"].lower()
            ]

        return results

    def save_attachment(
        self, email_uid: int, attachment_index: int, save_path: str = "./downloads"
    ) -> Optional[str]:
        """
        保存邮件附件到本地

        Args:
            email_uid: 邮件 UID
            attachment_index: 附件索引
            save_path: 保存目录

        Returns:
            保存的文件路径
        """
        os.makedirs(save_path, exist_ok=True)

        email_data = self.get_email(email_uid)
        if not email_data:
            raise ValueError(f"邮件 UID {email_uid} 不存在")

        attachments = email_data.get("attachments", [])
        att = next((a for a in attachments if a["index"] == attachment_index), None)

        if not att:
            raise ValueError(f"附件索引 {attachment_index} 不存在")

        conn = self._connect_imap()
        status, messages = conn.uid("SEARCH", None, f"UID {email_uid}")
        if status != "OK":
            raise ValueError("无法获取邮件")

        mail_id = messages[0].split()[0]

        status, msg_data = conn.uid("FETCH", mail_id, "(RFC822)")
        if status != "OK":
            raise ValueError("无法获取邮件内容")

        raw_msg = msg_data[0][1]
        msg = email.message_from_bytes(raw_msg)

        filename = att["name"]
        filepath = os.path.join(save_path, filename)

        if os.path.exists(filepath):
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(filepath):
                filepath = os.path.join(save_path, f"{base}_{counter}{ext}")
                counter += 1

        if msg.is_multipart():
            for i, part in enumerate(msg.walk()):
                if i == attachment_index:
                    payload = part.get_payload(decode=True)
                    if payload:
                        with open(filepath, "wb") as f:
                            f.write(payload)
                        return filepath
        return None

    def get_folders(self) -> List[str]:
        """
        获取邮箱文件夹列表

        Returns:
            文件夹名称列表
        """
        conn = self._connect_imap()
        status, folders = conn.list()
        if status != "OK":
            return []

        result = []
        for folder in folders:
            if isinstance(folder, bytes):
                folder = folder.decode()
            parts = folder.split('"')
            if len(parts) >= 2:
                result.append(self._decode_imap_folder_name(parts[-2]))
            elif len(parts) == 1:
                result.append(self._decode_imap_folder_name(parts[0].strip()))
        return result

    # ==================== 发送操作 ====================

    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        cc: str = None,
        bcc: str = None,
    ) -> bool:
        """
        发送文本邮件

        Args:
            to: 收件人地址（多个用逗号分隔）
            subject: 邮件主题
            body: 邮件正文
            cc: 抄送地址（可选）
            bcc: 密送地址（可选）

        Returns:
            发送是否成功
        """
        msg = MIMEText(body, "plain", "utf-8")
        msg["From"] = self._format_header_address(self.address)
        msg["To"] = self._format_recipient_header(to)
        msg["Subject"] = self._encode_header(subject)

        if cc:
            msg["Cc"] = self._format_recipient_header(cc)
        if bcc:
            msg["Bcc"] = self._format_recipient_header(bcc)

        return self._send_msg(msg, to, cc, bcc)

    def send_html_email(
        self,
        to: str,
        subject: str,
        html_body: str,
        cc: str = None,
        bcc: str = None,
    ) -> bool:
        """
        发送 HTML 格式邮件

        Args:
            to: 收件人地址
            subject: 邮件主题
            html_body: HTML 格式的邮件正文
            cc: 抄送地址（可选）
            bcc: 密送地址（可选）

        Returns:
            发送是否成功
        """
        msg = MIMEText(html_body, "html", "utf-8")
        msg["From"] = self._format_header_address(self.address)
        msg["To"] = self._format_recipient_header(to)
        msg["Subject"] = self._encode_header(subject)

        if cc:
            msg["Cc"] = self._format_recipient_header(cc)
        if bcc:
            msg["Bcc"] = self._format_recipient_header(bcc)

        return self._send_msg(msg, to, cc, bcc)

    def send_email_with_attachments(
        self,
        to: str,
        subject: str,
        body: str,
        attachments: List[str],
        cc: str = None,
        bcc: str = None,
    ) -> bool:
        """
        发送带附件的邮件

        Args:
            to: 收件人地址
            subject: 邮件主题
            body: 邮件正文
            attachments: 附件文件路径列表
            cc: 抄送地址（可选）
            bcc: 密送地址（可选）

        Returns:
            发送是否成功
        """
        msg = MIMEMultipart()
        msg["From"] = self._format_header_address(self.address)
        msg["To"] = self._format_recipient_header(to)
        msg["Subject"] = self._encode_header(subject)

        if cc:
            msg["Cc"] = self._format_recipient_header(cc)
        if bcc:
            msg["Bcc"] = self._format_recipient_header(bcc)

        # 添加正文
        msg.attach(MIMEText(body, "plain", "utf-8"))

        # 添加附件
        for filepath in attachments:
            if not os.path.exists(filepath):
                print(f"警告: 附件文件不存在: {filepath}")
                continue

            filename = os.path.basename(filepath)
            ext = os.path.splitext(filename)[1].lower()

            with open(filepath, "rb") as f:
                content = f.read()

            if ext == ".pdf":
                att = MIMEApplication(content, _subtype="pdf")
            elif ext in (".png", ".jpg", ".jpeg", ".gif", ".bmp"):
                att = MIMEImage(content, _subtype=ext[1:])
            elif ext in (".doc", ".docx"):
                att = MIMEApplication(content, _subtype="msword")
            elif ext in (".xls", ".xlsx"):
                att = MIMEApplication(content, _subtype="vnd.ms-excel")
            elif ext in (".zip", ".rar", ".7z"):
                att = MIMEApplication(content, _subtype=ext[1:])
            else:
                att = MIMEApplication(content, _subtype="octet-stream")

            att.add_header("Content-Disposition", "attachment", filename=filename)
            msg.attach(att)

        return self._send_msg(msg, to, cc, bcc)

    def _send_msg(self, msg, to: str, cc: str = None, bcc: str = None) -> bool:
        """
        内部方法：发送邮件消息

        Args:
            msg: 邮件消息对象
            to: 收件人
            cc: 抄送
            bcc: 密送

        Returns:
            发送是否成功
        """
        conn = self._connect_smtp()

        recipients = self._parse_recipient_emails(to, cc, bcc)

        try:
            conn.sendmail(self.address, recipients, msg.as_string())
            print(f"邮件已发送至: {to}")
            return True
        except Exception as e:
            print(f"发送失败: {e}")
            return False

    def close(self):
        """关闭所有连接"""
        if self._imap_conn:
            try:
                self._imap_conn.close()
                self._imap_conn.logout()
            except Exception:
                pass
            self._imap_conn = None

        if self._smtp_conn:
            try:
                self._smtp_conn.quit()
            except Exception:
                pass
            self._smtp_conn = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def main():
    """命令行入口"""
    import argparse

    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Email Client")
    parser.add_argument("--action", choices=["list", "show", "search", "folders", "send"], default="list", help="操作类型")
    parser.add_argument("--count", type=int, default=10, help="邮件数量")
    parser.add_argument("--uid", type=int, help="邮件 UID")
    parser.add_argument("--keyword", type=str, help="搜索关键词")
    parser.add_argument("--from-addr", type=str, help="发件人")
    parser.add_argument("--folder", type=str, default="INBOX", help="文件夹")
    parser.add_argument("--to", type=str, help="收件人 (send 操作)")
    parser.add_argument("--subject", type=str, help="邮件主题 (send 操作)")
    parser.add_argument("--body", type=str, help="邮件正文 (send 操作)")
    parser.add_argument("--body-file", type=str, help="从文件读取纯文本正文 (UTF-8/GB18030)")
    parser.add_argument("--html-body-file", type=str, help="从文件读取 HTML 正文 (UTF-8/GB18030)")
    parser.add_argument("--cc", type=str, help="抄送")
    parser.add_argument("--attachments", type=str, help="附件路径（逗号分隔）")

    args = parser.parse_args()

    try:
        client = EmailClient()

        if args.action == "list":
            emails = client.get_inbox(count=args.count, folder=args.folder)
            print("\n" + "=" * 50)
            print(f"{args.folder} - 最新邮件")
            print("=" * 50 + "\n")

            for i, email in enumerate(emails, 1):
                status = "已读" if email["is_read"] else "未读"
                print(f"[{i}] 主题: {email['subject']}")
                print(f"    发件人: {email['from']}")
                print(f"    时间: {email['date']}")
                print(f"    状态: {status}")
                print()

            print(f"共 {len(emails)} 封邮件")
            print("=" * 50)

        elif args.action == "show":
            if not args.uid:
                print("错误: 请指定 --uid")
                return
            email = client.get_email(args.uid)
            if email:
                print("\n" + "=" * 50)
                print(f"邮件详情 (UID: {email['uid']})")
                print("=" * 50)
                print(f"主题: {email['subject']}")
                print(f"发件人: {email['from']['name']} <{email['from']['email']}>")
                print(f"时间: {email['date']}")
                print("-" * 50)
                print("正文 (纯文本):")
                print(email["body"]["plain"][:500] if email["body"]["plain"] else "(无纯文本内容)")
                if email["attachments"]:
                    print("-" * 50)
                    print("附件:")
                    for att in email["attachments"]:
                        print(f"  - {att['name']} ({att['size']} bytes)")
                print("=" * 50)
            else:
                print(f"邮件 UID {args.uid} 不存在")

        elif args.action == "search":
            results = client.search_emails(
                keyword=args.keyword,
                from_addr=args.from_addr,
                folder=args.folder
            )
            print(f"\n找到 {len(results)} 封匹配的邮件:\n")
            for email in results:
                print(f"UID {email['uid']}: {email['subject']}")
                print(f"    发件人: {email['from']} | 时间: {email['date']}")
                print()

        elif args.action == "folders":
            folders = client.get_folders()
            print("\n邮件文件夹:")
            for folder in folders:
                print(f"  - {folder}")

        elif args.action == "send":
            if not args.to or not args.subject:
                print("错误: 发送邮件需要 --to, --subject")
                return

            body = args.body
            html_body = None
            if args.body_file:
                body = client._read_text_file(args.body_file)
            if args.html_body_file:
                html_body = client._read_text_file(args.html_body_file)

            if not body and not html_body:
                print("错误: 请通过 --body、--body-file 或 --html-body-file 提供正文")
                return

            attachments = None
            if args.attachments:
                attachments = [a.strip() for a in args.attachments.split(",")]

            if attachments:
                client.send_email_with_attachments(
                    to=args.to,
                    subject=args.subject,
                    body=body or client._html_to_text(html_body),
                    attachments=attachments,
                    cc=args.cc
                )
            elif html_body:
                client.send_html_email(
                    to=args.to,
                    subject=args.subject,
                    html_body=html_body,
                    cc=args.cc
                )
            else:
                client.send_email(
                    to=args.to,
                    subject=args.subject,
                    body=body,
                    cc=args.cc
                )

        client.close()

    except ValueError as e:
        print(f"错误: {e}")
    except Exception as e:
        print(f"操作失败: {e}")


if __name__ == "__main__":
    main()
