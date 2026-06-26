#!/usr/bin/env python3
"""
IMAP客户端 - 邮箱连接封装
支持: QQ邮箱、网易邮箱、企业邮箱、Gmail等
"""

import email
import imaplib
import re
from email.header import decode_header
from datetime import datetime
from typing import Optional, List


class IMAPClient:
    """IMAP邮箱客户端"""

    def __init__(self, config: dict):
        self.config = config
        self.server = config.get('server', '')
        self.port = config.get('port', 993)
        self.username = config.get('username', '')
        self.password = config.get('password', '')
        self.use_ssl = config.get('ssl', True)
        self.connection = None

    def connect(self) -> bool:
        """连接邮箱服务器"""
        try:
            if self.use_ssl:
                self.connection = imaplib.IMAP4_SSL(self.server, self.port)
            else:
                self.connection = imaplib.IMAP4(self.server, self.port)

            self.connection.login(self.username, self.password)
            return True

        except Exception as e:
            print(f"连接失败: {e}")
            return False

    def disconnect(self):
        """断开连接"""
        if self.connection:
            try:
                self.connection.logout()
            except Exception:
                pass
            self.connection = None

    def fetch_unread(self, folder: str = 'INBOX', limit: int = 10) -> List[dict]:
        """
        获取未读邮件

        Args:
            folder: 文件夹名称，默认INBOX
            limit: 最大数量

        Returns:
            邮件列表
        """
        if not self.connection:
            return []

        try:
            # 选择收件箱
            status, _ = self.connection.select(folder)
            if status != 'OK':
                return []

            # 搜索未读邮件 (ALL 会获取所有，但可以后续过滤 UNSEEN)
            status, messages = self.connection.search(None, 'UNSEEN')
            if status != 'OK':
                return []

            message_ids = messages[0].split()
            if not message_ids:
                return []

            # 限制数量
            message_ids = message_ids[-limit:] if len(message_ids) > limit else message_ids

            emails = []
            for msg_id in message_ids:
                email_data = self._fetch_email(msg_id)
                if email_data:
                    emails.append(email_data)

            return emails

        except Exception as e:
            print(f"获取邮件失败: {e}")
            return []

    def fetch_all(self, folder: str = 'INBOX', limit: int = 50,
                  since_date: Optional[str] = None) -> List[dict]:
        """
        获取邮件（可按日期过滤）

        Args:
            folder: 文件夹
            limit: 数量限制
            since_date: 起始日期 (格式: '01-Jan-2024')

        Returns:
            邮件列表
        """
        if not self.connection:
            return []

        try:
            status, _ = self.connection.select(folder)
            if status != 'OK':
                return []

            # 构建搜索条件
            criteria = 'ALL'
            if since_date:
                criteria = f'SINCE {since_date}'

            status, messages = self.connection.search(None, criteria)
            if status != 'OK':
                return []

            message_ids = messages[0].split()
            if not message_ids:
                return []

            message_ids = message_ids[-limit:] if len(message_ids) > limit else message_ids

            emails = []
            for msg_id in message_ids:
                email_data = self._fetch_email(msg_id)
                if email_data:
                    emails.append(email_data)

            return emails

        except Exception as e:
            print(f"获取邮件失败: {e}")
            return []

    def _fetch_email(self, msg_id) -> Optional[dict]:
        """获取单封邮件内容"""
        try:
            status, msg_data = self.connection.fetch(msg_id, '(RFC822)')
            if status != 'OK':
                return None

            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            # 解析主题
            subject = self._decode_header(msg.get('Subject', ''))

            # 解析发件人
            from_ = self._decode_header(msg.get('From', ''))

            # 解析日期
            date_str = msg.get('Date', '')
            date = self._parse_date(date_str)

            # 解析正文
            body = self._get_body(msg)

            # 邮件ID
            message_id = msg.get('Message-ID', str(msg_id))

            return {
                'message_id': message_id,
                'subject': subject,
                'from': from_,
                'date': date,
                'body': body,
                'snippet': body[:200] if body else '',
                'raw': raw_email
            }

        except Exception as e:
            print(f"解析邮件失败 ({msg_id}): {e}")
            return None

    def _decode_header(self, header: str) -> str:
        """解码邮件头"""
        if not header:
            return ''

        decoded_parts = decode_header(header)
        result = []

        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                try:
                    result.append(part.decode(encoding or 'utf-8', errors='replace'))
                except Exception:
                    result.append(part.decode('utf-8', errors='replace'))
            else:
                result.append(part)

        return ''.join(result)

    def _parse_date(self, date_str: str) -> str:
        """解析邮件日期"""
        if not date_str:
            return datetime.now().isoformat()

        try:
            dt = email.utils.parsedate_to_datetime(date_str)
            return dt.isoformat()
        except Exception:
            return datetime.now().isoformat()

    def _get_body(self, msg) -> str:
        """提取邮件正文"""
        body = ''

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition', ''))

                # 优先获取纯文本
                if content_type == 'text/plain' and 'attachment' not in content_disposition:
                    try:
                        charset = part.get_content_charset() or 'utf-8'
                        body = part.get_payload(decode=True).decode(charset, errors='replace')
                        break
                    except Exception:
                        pass

                # 其次获取HTML（转文本）
                elif content_type == 'text/html' and 'attachment' not in content_disposition and not body:
                    try:
                        charset = part.get_content_charset() or 'utf-8'
                        html = part.get_payload(decode=True).decode(charset, errors='replace')
                        body = self._html_to_text(html)
                    except Exception:
                        pass
        else:
            try:
                charset = msg.get_content_charset() or 'utf-8'
                body = msg.get_payload(decode=True).decode(charset, errors='replace')
            except Exception:
                pass

        return body.strip()

    def _html_to_text(self, html: str) -> str:
        """简单HTML转文本"""
        # 移除脚本和样式
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)

        # 移除标签
        html = re.sub(r'<[^>]+>', ' ', html)

        # 清理多余空白
        html = re.sub(r'\s+', ' ', html)

        return html.strip()

    def mark_as_read(self, msg_id: bytes) -> bool:
        """标记邮件为已读"""
        if not self.connection:
            return False

        try:
            status, _ = self.connection.store(msg_id, '+FLAGS', '\\Seen')
            return status == 'OK'
        except Exception:
            return False

    def mark_as_unread(self, msg_id: bytes) -> bool:
        """标记邮件为未读"""
        if not self.connection:
            return False

        try:
            status, _ = self.connection.store(msg_id, '-FLAGS', '\\Seen')
            return status == 'OK'
        except Exception:
            return False
