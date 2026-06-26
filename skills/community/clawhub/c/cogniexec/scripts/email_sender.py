#!/usr/bin/env python3
"""
email_sender.py — 邮件发送工具（纯标准库 smtplib + email）
覆盖：SMTP发送/附件/HTML邮件/收件人管理/模板邮件/批量发送

用法：
  python email_sender.py send --to "user@example.com" --subject "测试" --body "Hello World"
  python email_sender.py send --to "a@x.com,b@x.com" --subject "报告" --html --body "<h1>Hi</h1>" --attach report.pdf
  python email_sender.py send --template email.jsonl --data users.json
  python email_sender.py send --to "test@example.com" --cc "cc@example.com" --bcc "hidden@x.com"
  python email_sender.py test-connection --host smtp.gmail.com --port 587
  python email_sender.py preview --html --body "<b>content</b>"
"""

import sys
import os
import json
import re
import mimetypes
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
from email.utils import formatdate, formataddr
from typing import Optional, List, Tuple


# ─── CLI ──────────────────────────────────────────────────────

def parse_args(argv=None):
    argv = argv or sys.argv[1:]
    if not argv or '-h' in argv or '--help' in argv:
        print(__doc__)
        sys.exit(0)
    cmd = argv[0]
    args = {'_cmd': cmd, '_pos': []}
    i = 1
    while i < len(argv):
        a = argv[i]
        if a.startswith('-'):
            key = a.lstrip('-').replace('-', '_')
            if i + 1 < len(argv) and not argv[i+1].startswith('-'):
                args[key] = argv[i + 1]
                i += 2
            else:
                args[key] = True
                i += 1
        else:
            args['_pos'].append(a)
            i += 1
    return args


def color(text: str, fg: str = '') -> str:
    codes = {'red': 31, 'green': 32, 'yellow': 33, 'blue': 34, 'cyan': 36}
    code = codes.get(fg, '')
    if not code:
        return text
    if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
        return f'\033[{code}m{text}\033[0m'
    return text


def echo(text: str, fg: str = ''):
    print(color(text, fg))


# ─── SMTP 配置（支持环境变量） ────────────────────────────────

def get_smtp_config(args: dict) -> dict:
    """获取 SMTP 配置，优先从参数，回退到环境变量"""
    config = {
        'host': args.get('smtp_host') or os.environ.get('SMTP_HOST', 'localhost'),
        'port': int(args.get('smtp_port') or os.environ.get('SMTP_PORT', '25')),
        'username': args.get('smtp_user') or os.environ.get('SMTP_USER', ''),
        'password': args.get('smtp_pass') or os.environ.get('SMTP_PASSWORD', ''),
        'use_tls': args.get('tls', False) or os.environ.get('SMTP_TLS', '').lower() in ('true', '1'),
        'use_ssl': args.get('ssl', False) or os.environ.get('SMTP_SSL', '').lower() in ('true', '1'),
        'sender_name': args.get('from_name') or os.environ.get('SENDER_NAME', ''),
        'sender_email': args.get('from') or os.environ.get('SENDER_EMAIL', ''),
        'reply_to': args.get('reply_to') or os.environ.get('REPLY_TO', ''),
    }
    return config


# ══════════════════════════════════════════════════════════════
#  邮件构建器
# ══════════════════════════════════════════════════════════════

class EmailBuilder:
    """邮件构建与发送"""

    def __init__(self):
        self.to_addrs: List[str] = []
        self.cc_addrs: List[str] = []
        self.bcc_addrs: List[str] = []
        self.subject = ''
        self.body_text = ''
        self.body_html = ''
        self.attachments: List[str] = []
        self.inline_images: dict = {}  # cid -> path
        self.headers: dict = {}
        self.is_html = False

    def to(self, *addresses: str) -> 'EmailBuilder':
        """设置收件人"""
        for addr in addresses:
            self.to_addrs.extend(self._parse_addr_list(addr))
        return self

    def cc(self, *addresses: str) -> 'EmailBuilder':
        for addr in addresses:
            self.cc_addrs.extend(self._parse_addr_list(addr))
        return self

    def bcc(self, *addresses: str) -> 'EmailBuilder':
        for addr in addresses:
            self.bcc_addrs.extend(self._parse_addr_list(addr))
        return self

    def subject(self, subject: str) -> 'EmailBuilder':
        self.subject = subject
        return self

    def text_body(self, text: str) -> 'EmailBuilder':
        self.body_text = text
        return self

    def html_body(self, html: str) -> 'EmailBuilder':
        self.body_html = html
        self.is_html = True
        return self

    def attach(self, *file_paths: str) -> 'EmailBuilder':
        self.attachments.extend(file_paths)
        return self

    def header(self, key: str, value: str) -> 'EmailBuilder':
        self.headers[key] = value
        return self

    @staticmethod
    def _parse_addr_list(addr_str: str) -> List[str]:
        """解析逗号/分号分隔的地址列表"""
        if not addr_str:
            return []
        parts = re.split(r'[,;]', addr_str)
        return [a.strip().lower() for a in parts if a.strip() and '@' in a]

    def build(self, sender_email: str, sender_name: str = '',
               reply_to: str = None) -> MIMEMultipart:
        """构建完整的 MIME 消息"""

        # 根据内容类型选择根消息
        if self.body_html and not self.body_text:
            # 纯 HTML → 提取简单文本作为备用
            msg = MIMEMultipart('mixed')
            alt_part = MIMEMultipart('alternative')
            # 去除 HTML 标签作为纯文本
            plain_text = re.sub(r'<[^>]+>', '', self.body_html)
            plain_text = re.sub(r'\s+', ' ', plain_text).strip()
            alt_part.attach(MIMEText(plain_text, 'plain', 'utf-8'))
            alt_part.attach(MIMEText(self.body_html, 'html', 'utf-8'))
            msg.attach(alt_part)

        elif self.body_html and self.body_text:
            msg = MIMEMultipart('mixed')
            alt_part = MIMEMultipart('alternative')
            alt_part.attach(MIMEText(self.body_text, 'plain', 'utf-8'))
            alt_part.attach(MIMEText(self.body_html, 'html', 'utf-8'))
            msg.attach(alt_part)

        else:
            msg = MIMEMultipart('mixed')
            content_type = 'html' if self.is_html else 'plain'
            body = self.body_html if self.is_html else self.body_text
            main_part = MIMEText(body, content_type, 'utf-8')
            msg.attach(main_part)

        # 附件
        for file_path in self.attachments:
            if not os.path.isfile(file_path):
                echo(f'⚠️ 附件不存在: {file_path}', fg='yellow')
                continue
            try:
                self._attach_file(msg, file_path)
            except Exception as e:
                echo(f'⚠️ 附加失败 {file_path}: {e}', fg='yellow')

        # 头部信息
        from_name = sender_name or sender_email.split('@')[0]
        msg['From'] = formataddr((from_name, sender_email))
        msg['To'] = ', '.join(self.to_addrs) if self.to_addrs else ''
        msg['Cc'] = ', '.join(self.cc_addrs) if self.cc_addrs else ''
        msg['Subject'] = self.subject
        msg['Date'] = formatdate(localtime=True)
        msg['Message-ID'] = f'<{os.urandom(16).hex()}@email-sender>'
        if reply_to:
            msg['Reply-To'] = reply_to

        # 自定义头
        for k, v in self.headers.items():
            msg[k] = v

        return msg

    def _attach_file(self, msg: MIMEMultipart, file_path: str):
        """添加单个附件"""
        filename = os.path.basename(file_path)
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = 'application/octet-stream'

        maintype, subtype = mime_type.split('/', 1)

        with open(file_path, 'rb') as f:
            data = f.read()

        if maintype == 'text':
            att = MIMEText(data.decode('utf-8', errors='replace'), _subtype=subtype, _charset='utf-8')
        else:
            att = MIMEApplication(data, _subtype=subtype)

        att.add_header('Content-Disposition', 'attachment',
                       filename=('utf-8', '', filename))
        msg.attach(att)


# ─── SMTP 发送器 ─────────────────────────────────────────────

class SMTPSender:
    """SMTP 发送封装"""

    def __init__(self, host: str, port: int, username: str = '',
                 password: str = '', use_tls: bool = False,
                 use_ssl: bool = False, timeout: int = 30):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.use_ssl = use_ssl
        self.timeout = timeout
        self.server = None

    def connect(self) -> bool:
        try:
            if self.use_ssl:
                self.server = smtplib.SMTP_SSL(self.host, self.port, timeout=self.timeout)
            else:
                self.server = smtplib.SMTP(self.host, self.port, timeout=self.timeout)

            # 调试输出
            if os.environ.get('EMAIL_DEBUG'):
                self.server.set_debuglevel(2)

            # TLS 启动
            if self.use_tls and not self.use_ssl:
                self.server.starttls()

            # 认证
            if self.username and self.password:
                self.server.login(self.username, self.password)

            echo(f'✅ 已连接到 {self.host}:{self.port}', fg='green')
            return True

        except smtplib.SMTPAuthenticationError:
            echo('❌ SMTP 认证失败（用户名或密码错误）', fg='red')
            return False
        except smtplib.SMTPConnectError as e:
            echo(f'❌ 连接失败: {e}', fg='red')
            return False
        except Exception as e:
            echo(f'❌ 错误: {e}', fg='red')
            return False

    def send_message(self, message: MIMEMultipart,
                      to_addrs: List[str], cc_addrs: List[str],
                      bcc_addrs: List[str]) -> Tuple[bool, str]:
        """发送消息"""
        all_recipients = list(set(
            to_addrs + cc_addrs + bcc_addrs
        ))

        if not all_recipients:
            return False, '无收件人'

        try:
            failed = self.server.sendmail(
                message['From'],
                all_recipients,
                message.as_string()
            )
            if failed:
                return False, f'部分发送失败: {failed}'
            return True, f'成功发送给 {len(all_recipients)} 个收件人'
        except Exception as e:
            return False, str(e)

    def close(self):
        if self.server:
            try:
                server = self.server
                self.server = None
                server.quit()
            except Exception:
                pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.close()


# ══════════════════════════════════════════════════════════════
#  命令实现
# ══════════════════════════════════════════════════════════════

def cmd_send(args):
    """发送邮件主命令"""
    dry_run = args.get('dry_run', False)

    # 收件人
    to_raw = args.get('to', '')
    cc_raw = args.get('cc', '')
    bcc_raw = args.get('bcc', '')

    # 内容
    subject = args.get('subject', '(无主题)')
    body = args.get('body', '')
    is_html = args.get('html', False)

    # 附件
    attach_arg = args.get('attach', '')

    # 模板模式
    template_file = args.get('template', '')
    data_source = args.get('data', '')

    # SMTP 配置
    smtp_config = get_smtp_config(args)

    # 构建邮件
    builder = EmailBuilder()
    builder.subject(subject)

    if to_raw:
        builder.to(to_raw)
    if cc_raw:
        builder.cc(cc_raw)
    if bcc_raw:
        builder.bcc(bcc_raw)

    if is_html:
        builder.html_body(body)
    else:
        builder.text_body(body)

    if attach_arg:
        for fp in attach_arg.split(','):
            fp = fp.strip()
            if fp and os.path.isfile(fp):
                builder.attach(fp)

    # 批量模板模式
    if template_file and data_source:
        return _batch_send(template_file, data_source, smtp_config, dry_run)

    # 单封发送
    sender_email = smtp_config['sender_email']
    if not sender_email:
        echo('❌ 请指定发件人地址 (--from 或 SENDER_EMAIL)', fg='red')
        sys.exit(1)

    if not builder.to_addrs and not dry_run:
        echo('⚠️ 未指定收件人', fg='yellow')

    message = builder.build(sender_email,
                            smtp_config['sender_name'],
                            smtp_config.get('reply_to'))

    echo(f'📧 邮件预览:', fg='cyan', bold=True)
    echo(f'   From:    {message["From"]}')
    echo(f'   To:      {message["To"]}')
    if cc_raw:
        echo(f'   Cc:      {message["Cc"]}')
    echo(f'   Subject: {message["Subject"]}')
    echo(f'   Body:    {len(body)} 字符 ({("HTML" if is_html else "文本")})')
    if attach_arg:
        files = [f.strip() for f in attach_arg.split(',') if f.strip()]
        echo(f'   Attach: {len(files)} 个文件')

    if dry_run:
        echo('\n🔍 Dry-run 模式，未发送', fg='yellow')
        return

    # 连接并发送
    sender = SMTPSender(
        host=smtp_config['host'],
        port=smtp_config['port'],
        username=smtp_config['username'],
        password=smtp_config['password'],
        use_tls=smtp_config['use_tls'],
        use_ssl=smtp_config['use_ssl'],
    )

    try:
        if not sender.connect():
            sys.exit(1)

        ok, info = sender.send_message(
            message,
            builder.to_addrs, builder.cc_addrs, builder.bcc_addrs
        )
        if ok:
            echo(f'✅ {info}', fg='green')
        else:
            echo(f'❌ {info}', fg='red')

    finally:
        sender.close()


def _batch_send(template_file: str, data_source: str,
                 smtp_config: dict, dry_run=False):
    """批量模板发送"""
    # 加载模板
    with open(template_file, 'r', encoding='utf-8') as f:
        templates = []
        for line in f:
            line = line.strip()
            if line:
                try:
                    templates.append(json.loads(line))
                except json.JSONDecodeError:
                    pass

    # 加载数据
    with open(data_source, 'r', encoding='utf-8') as f:
        data_list = json.load(f)
    if isinstance(data_list, dict):
        data_list = [data_list]

    echo(f'📧 批量发送: {len(data_list)} 封邮件 (模板: {len(templates)})', fg='cyan')

    sent_count = 0
    fail_count = 0

    for idx, record in enumerate(data_list):
        tmpl = templates[idx % len(templates)] if templates else {}

        # 渲染模板
        subject = _render_template(tmpl.get('subject', ''), record)
        body = _render_template(tmpl.get('body', ''), record)
        html_body = _render_template(tmpl.get('html_body', ''), record)
        to_addr = _render_template(tmpl.get('to', ''), record)
        cc_addr = _render_template(tmpl.get('cc', ''), record)

        builder = EmailBuilder()
        builder.subject(subject)
        if to_addr:
            builder.to(to_addr)
        if cc_addr:
            builder.cc(cc_addr)
        if html_body and html_body != tmpl.get('html_body', ''):
            builder.html_body(html_body)
        else:
            builder.text_body(body)

        # 处理附件模板
        attachments = tmpl.get('attachments', [])
        for att in attachments:
            att_path = _render_template(att, record)
            if os.path.isfile(att_path):
                builder.attach(att_path)

        sender_email = smtp_config['sender_email']
        if not sender_email:
            echo(f'  ❌ #{idx+1}: 缺少发件人配置', fg='red')
            fail_count += 1
            continue

        message = builder.build(sender_email,
                                smtp_config['sender_name'])

        if dry_run:
            echo(f'  [DRY] #{idx+1}: {message["To"]} | {subject}', fg='cyan')
            sent_count += 1
            continue

        sender = SMTPSender(
            host=smtp_config['host'], port=smtp_config['port'],
            username=smtp_config['username'], password=smtp_config['password'],
            use_tls=smtp_config['use_tls'], use_ssl=smtp_config['use_ssl'],
        )
        try:
            if sender.connect():
                ok, info = sender.send_message(
                    message, builder.to_addrs, builder.cc_addrs, [])
                if ok:
                    echo(f'  ✅ #{idx+1}: {info}', fg='green')
                    sent_count += 1
                else:
                    echo(f'  ❌ #{idx+1}: {info}', fg='red')
                    fail_count += 1
            else:
                fail_count += 1
        finally:
            sender.close()

    echo(f'\n📊 结果: ✅{sent_count} ❌{fail_count} (共{len(data_list)})',
         fg='green' if fail_count == 0 else 'yellow')


def _render_template(template_str: str, context: dict) -> str:
    """简单 {{key}} 模板渲染"""
    if not template_str:
        return ''

    result = template_str

    # 支持嵌套键: {{user.name}} 和 {{user.name}}
    def replacer(match):
        expr = match.group(1).strip()
        keys = expr.split('.')
        val = context
        try:
            for k in keys:
                val = val[k]
            return str(val)
        except (KeyError, TypeError, IndexError):
            return match.group(0)

    result = re.sub(r'\{\{(.+?)\}\}', replacer, result)
    return result


def cmd_test_connection(args):
    """测试 SMTP 连接"""
    host = args.get('host', 'localhost')
    port = int(args.get('port', 587))
    username = args.get('user', os.environ.get('SMTP_USER', ''))
    password = args.get('pass', os.environ.get('SMTP_PASSWORD', ''))
    use_tls = args.get('tls', True)
    use_ssl = args.get('ssl', False)

    echo(f'🔗 测试连接: {host}:{port} (TLS={use_tls}, SSL={use_ssl})', fg='cyan')

    try:
        if use_ssl:
            server = smtplib.SMTP_SSL(host, port, timeout=15)
        else:
            server = smtplib.SMTP(host, port, timeout=15)

        # EHLO
        ehlo_response = server.ehlo()
        echo(f'  EHLO: OK (server: {server.ehlo_resp.decode()[:60]}...)' if hasattr(server, 'ehlo_resp') else '  EHLO: OK', fg='green')

        if use_tls and not use_ssl:
            server.starttls()
            echo('  STARTTLS: OK', fg='green')
            server.ehlo()

        if username and password:
            server.login(username, password)
            echo(f'  认证: ✅ ({username})', fg='green')
        else:
            echo('  认证: 跳过 (无凭据)', fg='yellow')

        echo(f'✅ 连接正常!', fg='green', bold=True)
        server.quit()

    except smtplib.SMTPAuthenticationError:
        echo('❌ 认证失败 (检查用户名/密码)', fg='red')
    except smtplib.SMTPConnectError as e:
        echo(f'❌ 连接拒绝: {e}', fg='red')
    except TimeoutError:
        echo('❌ 连接超时', fg='red')
    except Exception as e:
        echo(f'❌ 错误: {e}', fg='red')


def cmd_preview(args):
    """预览 HTML 邮件内容"""
    html_content = args.get('body', '')
    output = args.get('o', '')

    if html_content.startswith('@') or os.path.isfile(html_content):
        with open(html_content, 'r', encoding='utf-8') as f:
            html_content = f.read()

    # 包装为完整 HTML 以便预览
    full_html = f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
body {{ font-family: -apple-system, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }}
</style></head><body>{html_content}</body></html>'''

    dest = output or '_email_preview.html'
    with open(dest, 'w', encoding='utf-8') as f:
        f.write(full_html)
    echo(f'📄 预览已生成: {dest}', fg='green')
    echo(f'   在浏览器中打开查看效果', fg='cyan')


def cmd_validate_addresses(args):
    """验证邮箱地址格式"""
    source = args['_pos'][0] if args.get('_pos') else ''

    # 从文件或直接输入
    if os.path.isfile(source):
        with open(source, 'r', encoding='utf-8') as f:
            raw = f.read()
    else:
        raw = source

    addresses = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', raw)

    # 格式校验
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    valid = []
    invalid = []

    for addr in set(addresses):
        if re.match(pattern, addr.strip()):
            valid.append(addr)
        else:
            invalid.append(addr)

    domain_counts: dict = {}
    for addr in valid:
        domain = addr.split('@')[1]
        domain_counts[domain] = domain_counts.get(domain, 0) + 1

    from scripts.table_format import tabulate
    echo(f'📧 地址验证结果:', fg='cyan', bold=True)
    print(tabulate([
        ['有效地址数', str(len(valid))],
        ['无效地址数', str(len(invalid))],
        ['不同域名数', str(len(domain_counts))],
    ], tablefmt='grid'))

    if invalid:
        echo(f'\n⚠️ 无效地址:', fg='yellow')
        for addr in invalid[:20]:
            echo(f'  - {addr}')

    if domain_counts:
        echo(f'\n📊 域名分布 TOP 15:', fg='cyan')
        rows = [{'域名': d, '数量': c} for d, c in sorted(domain_counts.items(),
                                                       key=lambda x: x[1], reverse=True)[:15]]
        print(tabulate(rows, tablefmt='grid'))


# ══════════════════════════════════════════════════════════════
#  主入口
# ══════════════════════════════════════════════════════════════

COMMANDS = {
    'send': cmd_send,
    'test-connection': cmd_test_connection,
    'preview': cmd_preview,
    'validate': cmd_validate_addresses,
}

ALIASES = {
    'mail': 'send', 'email': 'send',
    'test': 'test-connection', 'ping': 'test-connection',
    'preview-html': 'preview', 'view': 'preview',
    'check-emails': 'validate', 'verify': 'validate',
}


def main():
    args = parse_args()
    cmd = args['_cmd']
    cmd = ALIASES.get(cmd, cmd)

    if cmd not in COMMANDS:
        available = ', '.join(sorted(set(list(COMMANDS.keys()) + list(ALIASES.keys()))))
        echo(f'❌ 未知命令: {cmd}', fg='red')
        echo(f'可用命令: {available}', fg='cyan')
        sys.exit(1)

    COMMANDS[cmd](args)


if __name__ == '__main__':
    main()
