#!/usr/bin/env python3
"""发送邮件（QQ邮箱）"""

import os
import sys
import json
import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email(to: str, subject: str, body: str, html: bool = False, attachment: str = None) -> dict:
    """发送邮件
    
    Args:
        to: 收件人
        subject: 邮件主题
        body: 邮件内容
        html: 是否为 HTML 格式
        attachment: 附件路径
    
    Returns:
        发送结果
    """
    user = os.environ.get("QQ_MAIL_USER")
    password = os.environ.get("QQ_MAIL_PASSWORD")
    
    if not user or not password:
        raise ValueError("未设置 QQ_MAIL_USER 或 QQ_MAIL_PASSWORD 环境变量")
    
    # 创建邮件
    msg = MIMEMultipart()
    msg["From"] = user
    msg["To"] = to
    msg["Subject"] = subject
    
    # 添加正文
    if html:
        msg.attach(MIMEText(body, "html", "utf-8"))
    else:
        msg.attach(MIMEText(body, "plain", "utf-8"))
    
    # 添加附件
    if attachment:
        with open(attachment, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment)}")
            msg.attach(part)
    
    # 发送邮件
    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(user, password)
        server.sendmail(user, to, msg.as_string())
        server.quit()
        
        return {
            "success": True,
            "message": "邮件发送成功"
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }

def main():
    parser = argparse.ArgumentParser(description="发送邮件")
    parser.add_argument("to", help="收件人")
    parser.add_argument("subject", help="邮件主题")
    parser.add_argument("body", help="邮件内容")
    parser.add_argument("--html", action="store_true", help="HTML 格式")
    parser.add_argument("--attachment", help="附件路径")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        result = send_email(args.to, args.subject, args.body, args.html, args.attachment)
        
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            if result["success"]:
                print("邮件发送成功")
            else:
                print(f"发送失败：{result['message']}")
                sys.exit(1)
    except Exception as e:
        print(f"发送失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
