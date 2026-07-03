"""
SMTP 邮件发送器
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from .config_loader import get_config


class EmailSender:
    """SMTP 邮件发送器"""

    def __init__(self, config: dict = None):
        cfg = config or get_config()
        smtp_cfg = cfg["smtp"]
        self.server = smtp_cfg["server"]
        self.port = smtp_cfg["port"]
        self.username = smtp_cfg["username"]
        self.password = smtp_cfg["password"]
        self.use_tls = smtp_cfg.get("use_tls", True)
        self.sender_name = smtp_cfg.get("sender_name", "AI 客服助手")

    def send(
        self,
        to_email: str,
        subject: str,
        body: str,
        in_reply_to: str = "",
        references: str = "",
        cc: list[str] = None,
        bcc: list[str] = None,
    ) -> dict:
        """
        发送邮件
        返回 {"success": bool, "message": str, "message_id": str}
        """
        try:
            msg = MIMEMultipart("alternative")
            msg["From"] = f"{self.sender_name} <{self.username}>"
            msg["To"] = to_email
            msg["Subject"] = subject

            if in_reply_to:
                msg["In-Reply-To"] = in_reply_to
            if references:
                msg["References"] = references

            if cc:
                msg["Cc"] = ", ".join(cc)
            if bcc:
                msg["Bcc"] = ", ".join(bcc)

            # 纯文本 + HTML 双版本
            msg.attach(MIMEText(body, "plain", "utf-8"))

            html_body = self._plain_to_html(body)
            msg.attach(MIMEText(html_body, "html", "utf-8"))

            # 连接并发送
            with smtplib.SMTP(self.server, self.port, timeout=30) as smtp:
                smtp.ehlo()
                if self.use_tls:
                    smtp.starttls()
                    smtp.ehlo()
                smtp.login(self.username, self.password)
                smtp.send_message(msg)

            return {"success": True, "message": "发送成功", "message_id": msg["Message-ID"]}

        except smtplib.SMTPAuthenticationError:
            return {"success": False, "message": "SMTP 认证失败，请检查用户名和密码", "message_id": ""}
        except smtplib.SMTPConnectError:
            return {"success": False, "message": f"无法连接 SMTP 服务器 {self.server}:{self.port}", "message_id": ""}
        except Exception as e:
            return {"success": False, "message": f"发送失败: {str(e)}", "message_id": ""}

    def send_test(self, to_email: str) -> dict:
        """发送测试邮件"""
        return self.send(
            to_email=to_email,
            subject="[AI Email Agent] 测试邮件",
            body="这是一封来自 AI Email Agent 系统的测试邮件。\n\n如果您收到此邮件，说明邮件发送配置正确。\n\nThis is a test email from the AI Email Agent system.",
        )

    @staticmethod
    def _plain_to_html(text: str) -> str:
        """纯文本转简易 HTML"""
        # 转义 HTML
        import html
        text = html.escape(text)

        # 换行 → <br>
        text = text.replace("\n", "<br>\n")

        # 加粗 **text** → <b>text</b>
        import re
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)

        return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; line-height: 1.8; color: #333;">
{text}
</body>
</html>"""
