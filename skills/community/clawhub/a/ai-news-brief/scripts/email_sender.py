#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮件推送模块
功能：读取邮件配置，将AI资讯简报发送到指定邮箱
"""

import sys
import io
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# 优先从 user_config 目录读取用户配置，如果没有则使用默认配置
USER_CONFIG_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "user_config")
CONFIG_FILE = os.path.join(USER_CONFIG_DIR, "email_config.json")
DEFAULT_CONFIG_FILE = os.path.join(SCRIPT_DIR, "email_config.json.default")


def load_email_config():
    """加载邮件配置（优先用户配置）"""
    # 优先读取用户配置目录
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARN] 读取用户配置失败: {e}")
    
    # 读取默认配置
    if os.path.exists(DEFAULT_CONFIG_FILE):
        try:
            with open(DEFAULT_CONFIG_FILE, 'r', encoding='utf-8') as f:
                print("[INFO] 使用默认邮件配置，请复制到 user_config 目录进行自定义")
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] 无法加载默认邮件配置: {e}")
            return None
    
    return None


def send_email(subject, html_content, config=None, attachment_path=None):
    """
    发送邮件
    attachment_path: 可选的 PDF 附件路径
    """
    if config is None:
        config = load_email_config()
        if config is None:
            return False, "配置加载失败"
    
    smtp_config = config.get('smtp_config', {})
    recipient_config = config.get('recipient_config', {})
    
    # 检查是否启用
    if not smtp_config.get('enabled', False):
        return False, "邮件推送未启用，请在 email_config.json 中设置 enabled: true"
    
    if not recipient_config.get('enabled', False):
        return False, "收件人未配置，请在 email_config.json 中设置 recipients"
    
    # 获取配置
    smtp_server = smtp_config.get('smtp_server', 'smtp.qq.com')
    smtp_port = smtp_config.get('smtp_port', 465)
    use_ssl = smtp_config.get('use_ssl', True)
    sender_email = smtp_config.get('sender_email', '')
    sender_password = smtp_config.get('sender_password', '')
    sender_name = smtp_config.get('sender_name', 'AI资讯小助手')
    recipients = recipient_config.get('recipients', [])
    
    # 验证配置
    if not sender_email or not sender_password:
        return False, "发件人邮箱或密码未配置"
    
    if not recipients:
        return False, "收件人列表为空"
    
    try:
        # 创建邮件
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{sender_name} <{sender_email}>"
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = Header(subject, 'utf-8')
        
        # 添加HTML内容
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        # 添加 PDF 附件（如果有）
        if attachment_path and os.path.exists(attachment_path):
            try:
                with open(attachment_path, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                filename = os.path.basename(attachment_path)
                part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                msg.attach(part)
                print(f"[INFO] 已添加附件: {filename}")
            except Exception as e:
                print(f"[WARN] 添加附件失败: {e}")
        
        # 连接SMTP服务器并发送
        if use_ssl:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
        
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipients, msg.as_string())
        server.quit()
        
        return True, f"邮件已发送到 {len(recipients)} 个收件人"
        
    except Exception as e:
        return False, f"发送失败: {str(e)}"


def generate_email_html(articles, date_range):
    """
    生成邮件HTML内容
    """
    template = config = load_email_config()
    email_template = template.get('email_template', {}) if template else {}
    
    subject_prefix = email_template.get('subject_prefix', '[AI资讯简报]')
    include_summary = email_template.get('include_summary', True)
    include_key_points = email_template.get('include_key_points', True)
    include_credibility = email_template.get('include_source_credibility', True)
    max_articles = email_template.get('max_articles', 15)
    
    articles = articles[:max_articles]
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #1a73e8; border-bottom: 2px solid #1a73e8; padding-bottom: 10px; }}
        h2 {{ color: #5f6368; margin-top: 30px; }}
        .article {{ background: #f8f9fa; border-radius: 8px; padding: 15px; margin: 15px 0; }}
        .article-title {{ font-size: 18px; font-weight: bold; color: #1a73e8; margin-bottom: 8px; }}
        .article-title a {{ color: inherit; text-decoration: none; }}
        .article-title a:hover {{ text-decoration: underline; }}
        .article-meta {{ font-size: 12px; color: #666; margin-bottom: 8px; }}
        .article-summary {{ color: #444; margin: 10px 0; }}
        .key-points {{ background: #e8f0fe; padding: 10px; border-radius: 4px; margin-top: 10px; }}
        .key-points-title {{ font-weight: bold; color: #1a73e8; font-size: 12px; }}
        .key-points ul {{ margin: 5px 0; padding-left: 20px; }}
        .key-points li {{ font-size: 13px; color: #333; }}
        .credibility {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; }}
        .credibility-A {{ background: #34a853; color: white; }}
        .credibility-B {{ background: #fbbc04; color: #333; }}
        .credibility-C {{ background: #ea4335; color: white; }}
        .credibility-D {{ background: #ccc; color: #333; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666; text-align: center; }}
        .hot-score {{ background: #ea4335; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px; margin-left: 8px; }}
    </style>
</head>
<body>
    <h1>🤖 AI 资讯简报</h1>
    <p style="color: #666;">📅 数据范围: {date_range}</p>
    
    <h2>📊 热点资讯 TOP {len(articles)}</h2>
"""
    
    for i, article in enumerate(articles, 1):
        title = article.get('title', '无标题')
        url = article.get('url', '#')
        source = article.get('source', '未知来源')
        summary = article.get('summary', '暂无摘要')
        key_points = article.get('key_points', [])
        credibility = article.get('credibility', {})
        hot_score = article.get('hot_score', 0)
        
        level = credibility.get('level', 'D')
        
        html += f"""
    <div class="article">
        <div class="article-title">
            <span class="hot-score">🔥 {hot_score}</span>
            <a href="{url}" target="_blank">{i}. {title}</a>
        </div>
        <div class="article-meta">
            📰 {source} 
            <span class="credibility credibility-{level}">可信度 {level}</span>
        </div>
"""
        
        if include_summary and summary:
            html += f'        <div class="article-summary">{summary[:200]}...</div>\n'
        
        if include_key_points and key_points:
            html += f"""
        <div class="key-points">
            <div class="key-points-title">📌 关键点</div>
            <ul>
"""
            for kp in key_points[:3]:
                html += f'                <li>{kp[:100]}</li>\n'
            html += """            </ul>
        </div>
"""
        
        html += """    </div>
"""
    
    html += f"""
    <div class="footer">
        <p>🤖 由 AI 资讯简报自动生成</p>
        <p>📧 此邮件由系统自动发送，请勿回复</p>
    </div>
</body>
</html>
"""
    
    return html


def send_ai_news_email(articles, date_range, config=None, pdf_path=None):
    """
    发送AI资讯简报邮件
    pdf_path: 可选的 PDF 附件路径
    """
    # 生成HTML内容
    html_content = generate_email_html(articles, date_range)
    
    # 生成主题
    template = config if config else load_email_config()
    email_template = template.get('email_template', {}) if template else {}
    subject_prefix = email_template.get('subject_prefix', '[AI资讯简报]')
    subject = f"{subject_prefix} {date_range} - 共{len(articles)}条"
    
    # 发送邮件（带上 PDF 附件）
    return send_email(subject, html_content, config, attachment_path=pdf_path)


def test_email_config():
    """测试邮件配置"""
    config = load_email_config()
    
    if not config:
        print("❌ 配置加载失败")
        return
    
    smtp = config.get('smtp_config', {})
    recipient = config.get('recipient_config', {})
    
    print("=" * 50)
    print("邮件配置检查")
    print("=" * 50)
    print(f"SMTP服务器: {smtp.get('smtp_server', '未配置')}")
    print(f"SMTP端口: {smtp.get('smtp_port', '未配置')}")
    print(f"发件人: {smtp.get('sender_email', '未配置')}")
    print(f"收件人: {recipient.get('recipients', [])[0] if recipient.get('recipients') else '未配置'}")
    print(f"推送状态: {'✅ 已启用' if smtp.get('enabled') else '❌ 未启用'}")
    print("=" * 50)
    
    if not smtp.get('enabled'):
        print("\n⚠️ 邮件推送未启用!")
        print("请编辑 email_config.json，设置 enabled: true 并填写邮箱配置")
    else:
        print("\n正在发送测试邮件...")
        test_html = "<h1>测试邮件</h1><p>如果收到这封邮件，说明配置正确!</p>"
        success, msg = send_email("AI资讯简报 - 测试邮件", test_html, config)
        if success:
            print(f"✅ {msg}")
        else:
            print(f"❌ {msg}")


if __name__ == "__main__":
    test_email_config()