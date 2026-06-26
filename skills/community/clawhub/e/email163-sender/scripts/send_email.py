#!/usr/bin/env python3
"""
163邮箱发送工具

环境变量:
    EMAIL_163_USER: 163邮箱地址
    EMAIL_163_AUTH_CODE: 授权密码(授权码)
"""

import argparse
import json
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
from datetime import datetime
from typing import List, Dict, Optional
import mimetypes
import uuid
import sys

# SMTP配置
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465


def get_config_dir() -> str:
    """获取配置目录"""
    workspace = os.environ.get('WORKSPACE', os.getcwd())
    config_dir = os.path.join(workspace, '.email_history')
    os.makedirs(config_dir, exist_ok=True)
    return config_dir


def get_history_file() -> str:
    """获取历史记录文件路径"""
    return os.path.join(get_config_dir(), 'sent_emails.json')


def load_history() -> List[Dict]:
    """加载发送历史"""
    history_file = get_history_file()
    if not os.path.exists(history_file):
        return []
    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def save_history(email_data: Dict) -> None:
    """保存发送记录到历史文件"""
    history = load_history()
    email_id = email_data.get('email_id')
    if email_id:
        for record in history:
            if record.get('email_id') == email_id:
                return
    history.append(email_data)
    try:
        with open(get_history_file(), 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def parse_recipients(recipients_str: str) -> List[str]:
    """解析收件人列表"""
    if not recipients_str:
        return []
    return [r.strip() for r in recipients_str.split(',') if r.strip()]


def send_email(
    to: str,
    subject: str,
    body: str,
    from_email: str = None,
    auth_code: str = None,
    cc: str = None,
    bcc: str = None,
    reply_to: str = None,
    attachments: List[str] = None,
    html: bool = False
) -> Dict:
    """发送邮件"""
    # 从环境变量获取配置
    if from_email is None:
        from_email = os.environ.get('EMAIL_163_USER')
    if auth_code is None:
        auth_code = os.environ.get('EMAIL_163_AUTH_CODE')
    
    if not from_email or not auth_code:
        return {
            'success': False,
            'error': 'Missing email configuration. Set EMAIL_163_USER and EMAIL_163_AUTH_CODE',
            'error_type': 'config_error'
        }
    
    # 解析收件人
    to_list = parse_recipients(to)
    cc_list = parse_recipients(cc) if cc else []
    bcc_list = parse_recipients(bcc) if bcc else []
    all_recipients = to_list + cc_list + bcc_list
    
    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ', '.join(to_list)
    msg['Subject'] = subject
    
    if cc_list:
        msg['Cc'] = ', '.join(cc_list)
    if reply_to:
        msg['Reply-To'] = reply_to
    
    # 添加正文
    content_type = 'html' if html else 'plain'
    msg.attach(MIMEText(body, content_type, 'utf-8'))
    
    # 添加附件
    if attachments:
        for att_path in attachments:
            if not os.path.exists(att_path):
                return {
                    'success': False,
                    'error': f'Attachment not found: {att_path}',
                    'error_type': 'attachment_error'
                }
            
            try:
                file_name = os.path.basename(att_path)
                mime_type, _ = mimetypes.guess_type(att_path)
                if mime_type is None:
                    mime_type = 'application/octet-stream'
                
                with open(att_path, 'rb') as f:
                    file_data = f.read()
                
                attachment = MIMEBase(*mime_type.split('/'))
                attachment.set_payload(file_data)
                encoders.encode_base64(attachment)
                attachment.add_header('Content-Disposition', 'attachment', filename=file_name)
                msg.attach(attachment)
            except Exception as e:
                return {
                    'success': False,
                    'error': f'Attachment error: {str(e)}',
                    'error_type': 'attachment_error'
                }
    
    # 发送邮件
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(from_email, auth_code)
            server.sendmail(from_email, all_recipients, msg.as_string())
        
        # 保存记录
        sent_time = datetime.now().isoformat()
        email_id = str(uuid.uuid4())[:8]
        
        save_history({
            'email_id': email_id,
            'sender': from_email,
            'recipients': to_list,
            'cc': cc_list,
            'bcc': bcc_list,
            'subject': subject,
            'sent_at': sent_time,
            'status': 'sent'
        })
        
        return {
            'success': True,
            'email_id': email_id,
            'sent_at': sent_time,
            'recipients': to_list,
            'cc': cc_list,
            'message': 'Email sent successfully'
        }
        
    except smtplib.SMTPAuthenticationError as e:
        return {'success': False, 'error': f'认证失败: {str(e)}', 'error_type': 'smtp_auth_error'}
    except smtplib.SMTPException as e:
        return {'success': False, 'error': f'SMTP错误: {str(e)}', 'error_type': 'smtp_error'}
    except Exception as e:
        return {'success': False, 'error': f'未知错误: {str(e)}', 'error_type': 'unknown_error'}


def list_sent_emails(limit: int = 10) -> List[Dict]:
    """列出已发送邮件"""
    history = load_history()
    return history[-limit:] if limit > 0 and len(history) > limit else history


def get_email_status(email_id: str) -> Optional[Dict]:
    """获取邮件状态"""
    for email in load_history():
        if email.get('email_id') == email_id:
            return email
    return None


def clear_history() -> bool:
    """清空发送历史"""
    history_file = get_history_file()
    if os.path.exists(history_file):
        os.remove(history_file)
        return True
    return False


def main():
    parser = argparse.ArgumentParser(
        description='163邮箱发送工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 发送简单邮件
  python3 send_email.py --to recipient@example.com --subject "测试" --body "内容"
  
  # 发送带附件邮件
  python3 send_email.py --to recipient@example.com --subject "报告" --body "请查收" -a report.pdf
  
  # 发送HTML邮件
  python3 send_email.py --to recipient@example.com --subject "周报" --html --body "<h1>周报</h1>"
  
  # 查看发送历史
  python3 send_email.py --list
        """
    )
    
    send_group = parser.add_argument_group('发送邮件')
    send_group.add_argument('--to', '-t', help='收件人邮箱')
    send_group.add_argument('--subject', '-s', help='邮件主题')
    send_group.add_argument('--body', '-b', help='邮件正文')
    send_group.add_argument('--html', action='store_true', help='HTML格式')
    send_group.add_argument('-a', '--attachment', action='append', help='附件路径')
    send_group.add_argument('--cc', help='抄送')
    send_group.add_argument('--bcc', help='密送')
    send_group.add_argument('--from', '-f', dest='from_email', help='发件人邮箱')
    send_group.add_argument('--auth-code', help='授权密码')
    
    manage_group = parser.add_argument_group('管理')
    manage_group.add_argument('--list', '-l', action='store_true', help='列出已发送邮件')
    manage_group.add_argument('--limit', type=int, default=10, help='显示数量')
    manage_group.add_argument('--status', help='查看邮件状态')
    manage_group.add_argument('--clear-history', action='store_true', help='清空历史')
    
    args = parser.parse_args()
    
    if args.list:
        emails = list_sent_emails(args.limit)
        if emails:
            print(f"已发送邮件记录 ({len(emails)} 条):")
            for email in emails:
                print(f"  [{email['email_id']}] {email['sent_at']}")
                print(f"      主题: {email['subject']}")
                print(f"      收件人: {', '.join(email['recipients'])}")
        else:
            print("暂无发送记录")
        return
    
    if args.status:
        email_data = get_email_status(args.status)
        if email_data:
            print(json.dumps(email_data, indent=2, ensure_ascii=False))
        else:
            print(f"未找到邮件: {args.status}")
        return
    
    if args.clear_history:
        if clear_history():
            print("发送历史已清空")
        else:
            print("发送历史为空")
        return
    
    # 发送邮件
    if not args.to or not args.subject or not args.body:
        print("错误: 发送邮件需要 --to, --subject, --body 参数")
        sys.exit(1)
    
    from_email = args.from_email or os.environ.get('EMAIL_163_USER')
    auth_code = args.auth_code or os.environ.get('EMAIL_163_AUTH_CODE')
    
    if not from_email:
        print("错误: 未设置发件人邮箱 (EMAIL_163_USER 或 --from)")
        sys.exit(1)
    if not auth_code:
        print("错误: 未设置授权密码 (EMAIL_163_AUTH_CODE 或 --auth-code)")
        sys.exit(1)
    
    result = send_email(
        to=args.to,
        subject=args.subject,
        body=args.body,
        from_email=from_email,
        auth_code=auth_code,
        cc=args.cc,
        bcc=args.bcc,
        attachments=args.attachment,
        html=args.html
    )
    
    if result['success']:
        print(f"✅ 邮件发送成功!")
        print(f"   邮件ID: {result['email_id']}")
        print(f"   发送时间: {result['sent_at']}")
        print(f"   收件人: {', '.join(result['recipients'])}")
    else:
        print(f"❌ 发送失败: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
