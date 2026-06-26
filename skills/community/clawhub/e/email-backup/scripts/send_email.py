#!/usr/bin/env python3
"""
QQ邮箱SMTP发送脚本
支持发送带附件的邮件
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import datetime

def send_email_with_attachment(
    to_email,
    subject,
    body,
    attachment_path,
    smtp_server='smtp.qq.com',
    smtp_port=465,
    username=None,
    password=None
):
    """
    发送带附件的邮件
    
    Args:
        to_email: 收件人邮箱
        subject: 邮件主题
        body: 邮件正文
        attachment_path: 附件路径
        smtp_server: SMTP服务器地址
        smtp_port: SMTP服务器端口
        username: 发件人邮箱
        password: SMTP密码/授权码
    
    Returns:
        bool: 是否成功
    """
    try:
        # 检查附件是否存在
        if not os.path.exists(attachment_path):
            print(f"❌ 附件文件不存在: {attachment_path}")
            return False
        
        # 创建邮件对象
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # 添加正文
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # 添加附件
        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        
        # 获取文件名
        filename = os.path.basename(attachment_path)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {filename}',
        )
        
        msg.attach(part)
        print(f"✅ 附件已添加: {filename}")
        
        # 发送邮件
        print(f"📧 正在连接SMTP服务器: {smtp_server}:{smtp_port}")
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        
        print(f"🔐 正在登录: {username}")
        server.login(username, password)
        
        print(f"📤 正在发送邮件到: {to_email}")
        server.send_message(msg)
        server.quit()
        
        print(f"✅ 邮件发送成功！")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("❌ SMTP认证失败，请检查邮箱和授权码")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ SMTP错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 发送邮件失败: {e}")
        return False

def main():
    """主函数（用于测试）"""
    import argparse
    
    parser = argparse.ArgumentParser(description='QQ邮箱SMTP发送工具')
    parser.add_argument('--to', required=True, help='收件人邮箱')
    parser.add_argument('--subject', required=True, help='邮件主题')
    parser.add_argument('--body', required=True, help='邮件正文')
    parser.add_argument('--attachment', required=True, help='附件路径')
    parser.add_argument('--username', help='发件人邮箱')
    parser.add_argument('--password', help='SMTP密码/授权码')
    
    args = parser.parse_args()
    
    # 从环境变量获取配置
    username = args.username or os.getenv('QQ_EMAIL', 'your-email@example.com')
    password = args.password or os.getenv('QQ_SMTP_PASSWORD', 'your-auth-code')
    
    success = send_email_with_attachment(
        to_email=args.to,
        subject=args.subject,
        body=args.body,
        attachment_path=args.attachment,
        username=username,
        password=password
    )
    
    if not success:
        exit(1)

if __name__ == "__main__":
    main()