#!/usr/bin/env python3
"""
电子邮件发送模块
用于将 evolution-watcher 报告发送到指定邮箱
"""

import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class EmailSender:
    """电子邮件发送器"""
    
    def __init__(self, 
                 smtp_server: str = "smtp.gmail.com",
                 smtp_port: int = 587,
                 sender_email: Optional[str] = None,
                 sender_password: Optional[str] = None,
                 recipient_email: str = "johnson007.ye@gmail.com"):
        """
        初始化电子邮件发送器
        
        Args:
            smtp_server: SMTP服务器地址
            smtp_port: SMTP端口
            sender_email: 发件人邮箱（如未提供，尝试从环境变量读取）
            sender_password: 发件人密码（如未提供，尝试从环境变量读取）
            recipient_email: 收件人邮箱
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email or os.environ.get("EVOLUTION_WATCHER_SENDER_EMAIL")
        self.sender_password = sender_password or os.environ.get("EVOLUTION_WATCHER_SENDER_PASSWORD")
        self.recipient_email = recipient_email
        
        # 如果仍未设置发件人邮箱，使用默认值（需要用户配置）
        if not self.sender_email:
            self.sender_email = "your-email@gmail.com"  # 需要用户替换
        
        if not self.sender_password:
            self.sender_password = "your-app-password"  # 需要用户替换
    
    def send_report(self, subject: str, html_content: str, text_content: Optional[str] = None) -> bool:
        """
        发送报告邮件
        
        Args:
            subject: 邮件主题
            html_content: HTML内容
            text_content: 纯文本内容（可选）
        
        Returns:
            是否发送成功
        """
        if not text_content:
            # 从HTML内容生成简单文本
            import re
            text_content = re.sub(r'<[^>]+>', '', html_content)
            text_content = re.sub(r'\n\s*\n', '\n\n', text_content)
        
        # 创建邮件
        message = MIMEMultipart("alternative")
        message["Subject"] = f"[evolution-watcher] {subject}"
        message["From"] = self.sender_email
        message["To"] = self.recipient_email
        
        # 添加纯文本和HTML版本
        part1 = MIMEText(text_content, "plain", "utf-8")
        part2 = MIMEText(html_content, "html", "utf-8")
        
        message.attach(part1)
        message.attach(part2)
        
        try:
            # 创建安全SSL上下文
            context = ssl.create_default_context()
            
            # 连接到SMTP服务器并发送邮件
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()  # 向服务器标识自己
                server.starttls(context=context)  # 安全加密连接
                server.ehlo()  # 再次向服务器标识自己（TLS模式）
                
                # 登录（如果提供了凭据）
                if self.sender_email != "your-email@gmail.com" and self.sender_password != "your-app-password":
                    server.login(self.sender_email, self.sender_password)
                else:
                    logger.warning("使用默认邮箱凭据，邮件可能无法发送。请配置环境变量：")
                    logger.warning("  EVOLUTION_WATCHER_SENDER_EMAIL=your-email@gmail.com")
                    logger.warning("  EVOLUTION_WATCHER_SENDER_PASSWORD=your-app-password")
                    # 继续尝试发送，但可能失败
                
                server.sendmail(self.sender_email, self.recipient_email, message.as_string())
                logger.info(f"报告邮件已发送至 {self.recipient_email}")
                return True
                
        except Exception as e:
            logger.error(f"发送邮件失败: {e}")
            return False
    
    def send_markdown_report(self, subject: str, markdown_content: str) -> bool:
        """
        发送Markdown格式的报告邮件
        
        Args:
            subject: 邮件主题
            markdown_content: Markdown内容
        
        Returns:
            是否发送成功
        """
        # 将Markdown转换为HTML
        try:
            import markdown
            html_content = markdown.markdown(markdown_content, extensions=['extra', 'tables'])
        except ImportError:
            # 如果没有markdown库，使用简单转换
            html_content = f"<pre>{markdown_content}</pre>"
        
        return self.send_report(subject, html_content, markdown_content)


# 全局实例
_default_sender = None

def get_default_sender() -> EmailSender:
    """获取默认邮件发送器实例"""
    global _default_sender
    if _default_sender is None:
        _default_sender = EmailSender()
    return _default_sender


def send_report(subject: str, content: str, is_markdown: bool = True) -> bool:
    """
    发送报告的便捷函数
    
    Args:
        subject: 邮件主题
        content: 报告内容
        is_markdown: 是否为Markdown格式
    
    Returns:
        是否发送成功
    """
    sender = get_default_sender()
    if is_markdown:
        return sender.send_markdown_report(subject, content)
    else:
        return sender.send_report(subject, content, content)


if __name__ == "__main__":
    # 测试邮件发送
    import sys
    logging.basicConfig(level=logging.INFO)
    
    test_subject = "evolution-watcher 测试报告"
    test_content = """# evolution-watcher 测试报告

## 测试内容
这是一个测试邮件，用于验证邮件发送功能。

### 插件状态
- ✅ 插件 A: 正常
- ⚠️  插件 B: 需要更新
- ❌ 插件 C: 错误

**报告时间**: 2026-03-20 12:30:00
"""
    
    success = send_report(test_subject, test_content)
    if success:
        print("✅ 测试邮件发送成功")
        sys.exit(0)
    else:
        print("❌ 测试邮件发送失败")
        sys.exit(1)