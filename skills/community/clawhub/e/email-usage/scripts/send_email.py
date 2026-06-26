#!/usr/bin/env python3
"""发送邮件脚本。直接执行即可，无需修改。"""
import smtplib, sys, email.mime.text, email.header

def send_email(to_addr: str, subject: str, body: str,
               from_addr: str = 'noreply@axelhu.com',
               username: str = None,
               password: str = None,
               host: str = 'localhost',
               port: int = 587):
    msg = email.mime.text.MIMEText(body, 'plain', 'utf-8')
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = email.header.Header(subject, 'utf-8').encode()
    s = smtplib.SMTP(host, port, timeout=10)
    if username and password:
        try:
            s.login(username, password)
        except smtplib.SMTPAuthenticationError:
            # 认证失败，尝试无认证发送（仅限信任网络）
            pass
    s.sendmail(from_addr, [to_addr], msg.as_string())
    s.quit()
    return True

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("用法: python3 send_email.py <收件人> <主题> <正文> <发件邮箱> <密码>")
        sys.exit(1)
    to_addr = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    from_addr = sys.argv[4]
    password = sys.argv[5]
    username = from_addr
    send_email(to_addr, subject, body, from_addr, username, password)
    print(f"邮件已发送至 {to_addr}")
