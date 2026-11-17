#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发送邮件 - SMTP 协议
用法：python3 send_email.py "收件人" "主题" "正文" [附件路径]
"""

import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def get_env():
    """从环境变量获取配置"""
    return {
        'smtp_server': os.environ.get('EMAIL_SMTP_SERVER', ''),
        'smtp_port': int(os.environ.get('EMAIL_SMTP_PORT', '465')),
        'email_user': os.environ.get('EMAIL_USER', ''),
        'email_password': os.environ.get('EMAIL_PASSWORD', '')
    }

def send_email(to_address, subject, body, attachment_path=None):
    """发送邮件"""
    config = get_env()
    
    if not config['smtp_server']:
        print("❌ 错误：EMAIL_SMTP_SERVER 未配置")
        sys.exit(1)
    if not config['email_user']:
        print("❌ 错误：EMAIL_USER 未配置")
        sys.exit(1)
    if not config['email_password']:
        print("❌ 错误：EMAIL_PASSWORD 未配置")
        sys.exit(1)
    
    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = config['email_user']
    msg['To'] = to_address
    msg['Subject'] = subject
    
    # 添加正文
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # 添加附件
    if attachment_path and os.path.exists(attachment_path):
        try:
            with open(attachment_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                filename = os.path.basename(attachment_path)
                part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                msg.attach(part)
            print(f"✅ 附件已添加：{filename}")
        except Exception as e:
            print(f"⚠️ 附件添加失败：{e}")
    
    # 发送邮件
    try:
        print(f"📧 正在发送邮件到：{to_address}")
        print(f"📤 主题：{subject}")
        
        # 根据端口选择连接方式：465 用 SSL，587 用 TLS
        if config['smtp_port'] == 465:
            server = smtplib.SMTP_SSL(config['smtp_server'], config['smtp_port'])
        else:
            server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
            server.starttls()
        
        server.login(config['email_user'], config['email_password'])
        server.sendmail(config['email_user'], to_address.split(','), msg.as_string())
        server.quit()
        
        print("✅ 邮件发送成功！")
        return True
    except smtplib.SMTPAuthenticationError:
        print("❌ 认证失败：请检查邮箱账号和授权码")
        return False
    except smtplib.SMTPConnectError:
        print("❌ 连接失败：请检查 SMTP 服务器和端口")
        return False
    except Exception as e:
        print(f"❌ 发送失败：{e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("用法：python3 send_email.py \"收件人\" \"主题\" \"正文\" [附件路径]")
        print("示例：python3 send_email.py \"test@example.com\" \"测试\" \"你好\"")
        sys.exit(1)
    
    to_addr = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    attachment = sys.argv[4] if len(sys.argv) > 4 else None
    
    success = send_email(to_addr, subject, body, attachment)
    sys.exit(0 if success else 1)
