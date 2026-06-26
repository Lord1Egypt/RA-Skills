"""
Email Manager - OpenClaw Skill
支持 POP3 协议查询邮件和 SMTP 协议发送邮件
"""

import poplib
import smtplib
import yaml
import os
from email.parser import Parser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
from email.utils import parseaddr
from typing import Optional, List, Dict


class EmailManager:
    """邮件管理器 - 支持 POP3 收件和 SMTP 发件"""

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化邮件管理器

        Args:
            config_path: 配置文件路径，默认为技能目录下的 config.yaml
        """
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'config.yaml'
            )

        self.config = self._load_config(config_path)
        self.pop3_conn = None

    def _load_config(self, config_path: str) -> dict:
        """加载配置文件"""
        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f'配置文件不存在：{config_path}\n'
                f'请复制 config.example.yaml 为 config.yaml 并填写邮箱信息'
            )

        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        if 'email' not in config:
            raise ValueError('配置文件中缺少 [email] 配置项')

        return config['email']

    def _decode_mime_words(self, text: str) -> str:
        """解码 MIME 编码的邮件头"""
        if not text:
            return ''

        decoded_parts = decode_header(text)
        result = []

        for content, encoding in decoded_parts:
            if isinstance(content, bytes):
                result.append(content.decode(encoding or 'utf-8', errors='replace'))
            else:
                result.append(content)

        return ''.join(result)

    def _get_email_content(self, msg) -> Dict[str, str]:
        """
        提取邮件内容

        Args:
            msg: email.message.Message 对象

        Returns:
            包含邮件各部分的字典
        """
        email_data = {
            'subject': '',
            'from': '',
            'to': '',
            'date': '',
            'body_text': '',
            'body_html': ''
        }

        # 解码邮件头
        email_data['subject'] = self._decode_mime_words(msg.get('Subject', ''))
        email_data['from'] = self._decode_mime_words(msg.get('From', ''))
        email_data['to'] = self._decode_mime_words(msg.get('To', ''))
        email_data['date'] = msg.get('Date', '')

        # 提取邮件正文
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get_content_disposition() or '')

                # 跳过附件
                if 'attachment' in content_disposition:
                    continue

                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        content = payload.decode(part.get_content_charset() or 'utf-8', errors='replace')

                        if content_type == 'text/plain':
                            email_data['body_text'] = content
                        elif content_type == 'text/html':
                            email_data['body_html'] = content
                except Exception:
                    continue
        else:
            try:
                payload = msg.get_payload(decode=True)
                if payload:
                    email_data['body_text'] = payload.decode(
                        msg.get_content_charset() or 'utf-8',
                        errors='replace'
                    )
            except Exception:
                email_data['body_text'] = str(msg.get_payload())

        return email_data

    # ==================== POP3 查询功能 ====================

    def connect_pop3(self) -> bool:
        """
        连接到 POP3 服务器

        Returns:
            连接是否成功
        """
        try:
            if self.config.get('use_ssl', True):
                self.pop3_conn = poplib.POP3_SSL(
                    self.config['host_pop3'],
                    self.config.get('port_pop3', 995)
                )
            else:
                self.pop3_conn = poplib.POP3(
                    self.config['host_pop3'],
                    self.config.get('port_pop3', 110)
                )

            # 登录
            self.pop3_conn.user(self.config['username'])
            self.pop3_conn.pass_(self.config['password'])

            return True
        except Exception as e:
            raise ConnectionError(f'POP3 连接失败：{str(e)}')

    def disconnect_pop3(self):
        """断开 POP3 连接"""
        if self.pop3_conn:
            try:
                self.pop3_conn.quit()
            except Exception:
                pass
            finally:
                self.pop3_conn = None

    def get_mail_count(self) -> int:
        """
        获取收件箱邮件数量

        Returns:
            邮件总数
        """
        if not self.pop3_conn:
            self.connect_pop3()

        try:
            return len(self.pop3_conn.list()[1])
        except Exception as e:
            raise RuntimeError(f'获取邮件数量失败：{str(e)}')

    def list_mails(self, limit: int = 10, unread_only: bool = False) -> List[Dict]:
        """
        获取邮件列表

        Args:
            limit: 最多返回多少封邮件
            unread_only: 是否只返回未读邮件（POP3 不支持标记已读/未读，此参数仅作兼容）

        Returns:
            邮件列表，每项包含：index, subject, from, date
        """
        if not self.pop3_conn:
            self.connect_pop3()

        try:
            messages = self.pop3_conn.list()[1]
            mail_list = []

            # 获取最近的邮件（倒序）
            for i, msg_info in enumerate(reversed(messages)):
                if len(mail_list) >= limit:
                    break

                # msg_info 格式：b'<index> <size>'
                parts = msg_info.decode().split()
                if len(parts) < 2:
                    continue

                index = int(parts[0])

                # 获取邮件头信息
                response, lines, size = self.pop3_conn.retr(index)
                raw_message = b'\r\n'.join(lines).decode('utf-8', errors='replace')
                msg = Parser().parsestr(raw_message)

                mail_list.append({
                    'index': index,
                    'subject': self._decode_mime_words(msg.get('Subject', '(无主题)')),
                    'from': self._decode_mime_words(msg.get('From', '')),
                    'date': msg.get('Date', ''),
                    'size': size
                })

            return mail_list
        except Exception as e:
            raise RuntimeError(f'获取邮件列表失败：{str(e)}')

    def read_mail(self, index: int) -> Dict[str, str]:
        """
        读取指定邮件的详细内容

        Args:
            index: 邮件序号（从 1 开始）

        Returns:
            邮件详细内容字典
        """
        try:
            # 如果是新连接，先获取邮件列表确认索引有效
            if not self.pop3_conn:
                self.connect_pop3()
                # 获取邮件列表以确认连接正常并验证索引
                messages = self.pop3_conn.list()[1]
                valid_indices = [int(msg.decode().split()[0]) for msg in messages]
                if index not in valid_indices:
                    raise ValueError(f'无效的邮件序号：{index}，有效范围：{valid_indices}')

            response, lines, size = self.pop3_conn.retr(index)
            raw_message = b'\r\n'.join(lines).decode('utf-8', errors='replace')
            msg = Parser().parsestr(raw_message)

            return self._get_email_content(msg)
        except poplib.error_proto as e:
            # POP3 协议错误，尝试重新连接后重试一次
            self.disconnect_pop3()
            self.connect_pop3()
            response, lines, size = self.pop3_conn.retr(index)
            raw_message = b'\r\n'.join(lines).decode('utf-8', errors='replace')
            msg = Parser().parsestr(raw_message)
            return self._get_email_content(msg)
        except Exception as e:
            raise RuntimeError(f'读取邮件失败：{str(e)}')

    def delete_mail(self, index: int) -> bool:
        """
        标记删除指定邮件

        Args:
            index: 邮件序号

        Returns:
            是否成功标记删除
        """
        if not self.pop3_conn:
            self.connect_pop3()

        try:
            self.pop3_conn.dele(index)
            return True
        except Exception as e:
            raise RuntimeError(f'删除邮件失败：{str(e)}')

    # ==================== SMTP 发送功能 ====================

    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        html: bool = False,
        cc: Optional[str] = None,
        bcc: Optional[str] = None
    ) -> bool:
        """
        发送邮件

        Args:
            to: 收件人邮箱
            subject: 邮件主题
            body: 邮件正文
            html: 正文是否为 HTML 格式
            cc: 抄送邮箱（逗号分隔多个）
            bcc: 密送邮箱（逗号分隔多个）

        Returns:
            是否发送成功
        """
        try:
            # 创建邮件
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.config['username']
            msg['To'] = to

            if cc:
                msg['Cc'] = cc

            # 收集所有收件人
            recipients = [to]
            if cc:
                recipients.extend([addr.strip() for addr in cc.split(',')])
            if bcc:
                recipients.extend([addr.strip() for addr in bcc.split(',')])

            # 添加正文
            if html:
                msg.attach(MIMEText(body, 'html', 'utf-8'))
            else:
                msg.attach(MIMEText(body, 'plain', 'utf-8'))

            # 连接 SMTP 服务器并发送
            if self.config.get('use_ssl', True):
                server = smtplib.SMTP_SSL(
                    self.config['host_smtp'],
                    self.config.get('port_smtp', 465)
                )
            else:
                server = smtplib.SMTP(
                    self.config['host_smtp'],
                    self.config.get('port_smtp', 587)
                )

            server.login(self.config['username'], self.config['password'])
            server.send_message(msg, to_addrs=recipients)
            server.quit()

            return True
        except Exception as e:
            raise RuntimeError(f'发送邮件失败：{str(e)}')

    def send_simple_email(self, to: str, subject: str, body: str) -> bool:
        """
        发送简单文本邮件（便捷方法）

        Args:
            to: 收件人邮箱
            subject: 邮件主题
            body: 邮件正文

        Returns:
            是否发送成功
        """
        return self.send_email(to, subject, body, html=False)


# ==================== CLI 入口（可选） ====================

if __name__ == '__main__':
    import sys

    manager = EmailManager()

    if len(sys.argv) < 2:
        print('用法:')
        print('  python email_manager.py list [count]     - 列出邮件')
        print('  python email_manager.py read <index>     - 读取邮件')
        print('  python email_manager.py count            - 邮件数量')
        print('  python email_manager.py send <to> <subject> <body> - 发送邮件')
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == 'count':
        manager.connect_pop3()
        count = manager.get_mail_count()
        print(f'收件箱共有 {count} 封邮件')
        manager.disconnect_pop3()

    elif cmd == 'list':
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        manager.connect_pop3()
        mails = manager.list_mails(limit=limit)
        for mail in mails:
            print(f"[{mail['index']}] {mail['subject']} - {mail['from']} ({mail['date']})")
        manager.disconnect_pop3()

    elif cmd == 'read':
        if len(sys.argv) < 3:
            print('请指定邮件序号：python email_manager.py read <index>')
            sys.exit(1)
        index = int(sys.argv[2])
        manager.connect_pop3()
        try:
            email = manager.read_mail(index)
            print(f"主题：{email['subject']}")
            print(f"发件人：{email['from']}")
            print(f"日期：{email['date']}")
            print("-" * 50)
            print(email['body_text'] or email['body_html'])
        except Exception as e:
            print(f"读取失败：{e}")
        manager.disconnect_pop3()

    elif cmd == 'send':
        if len(sys.argv) < 5:
            print('用法：python email_manager.py send <to> <subject> <body>')
            sys.exit(1)
        to = sys.argv[2]
        subject = sys.argv[3]
        body = ' '.join(sys.argv[4:])
        manager.send_email(to, subject, body)
        print('邮件发送成功!')

    else:
        print(f'未知命令：{cmd}')
        sys.exit(1)
