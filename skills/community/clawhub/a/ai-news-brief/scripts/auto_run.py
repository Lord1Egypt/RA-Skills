#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 资讯简报 - 自动执行脚本
功能：获取资讯 → 生成报告 → 发送邮件
"""

import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 添加 scripts 目录到路径
sys.path.insert(0, SCRIPT_DIR)

def main():
    print("=" * 50)
    print("AI 资讯简报 - 自动执行")
    print("=" * 50)
    
    # 1. 获取资讯
    print("\n[1/4] 正在获取AI资讯...")
    from fetch_ai_news import fetch_all_news
    articles = fetch_all_news()
    print(f"    获取到 {len(articles)} 条资讯")
    
    if not articles:
        print("    警告：未获取到任何资讯")
        articles = []
    
    # 2. 生成 HTML 报告（暂时跳过，有bug）
    print("\n[2/4] 正在生成报告...")
    html_path = None
    try:
        # 暂时跳过 HTML 报告生成，等待修复
        print("    HTML报告: 暂时跳过")
    except Exception as e:
        print(f"    HTML报告跳过: {e}")
    
    # 3. 生成 PDF（如启用）
    pdf_path = None
    from pdf_generator import generate_pdf_with_attachment
    try:
        from pdf_config import load_pdf_config
        pdf_config = load_pdf_config()
        if pdf_config and pdf_config.get('config', {}).get('enabled', False):
            print("\n[3/4] 正在生成PDF...")
            pdf_path, pdf_msg = generate_pdf_with_attachment(articles, date_range, pdf_config)
            print(f"    PDF生成: {pdf_msg}")
    except Exception as e:
        print(f"    PDF生成跳过: {e}")
    
    # 4. 发送邮件（如启用）
    try:
        from email_sender import send_ai_news_email
        try:
            from email_config import load_email_config
            email_config = load_email_config()
        except:
            email_config = None
        
        if email_config:
            smtp = email_config.get('smtp_config', {})
            recipient = email_config.get('recipient_config', {})
            
            if smtp.get('enabled', False) and recipient.get('enabled', False):
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__
                print("\n[4/4] 正在发送邮件...")
                success, msg = send_ai_news_email(articles, date_range, email_config, pdf_path)
                print(f"    邮件发送: {msg}")
            else:
                print("\n[4/4] 邮件未启用")
        else:
            print("\n[4/4] 邮件配置未找到")
    except Exception as e:
        print(f"    邮件发送跳过: {e}")
    
    print("\n" + "=" * 50)
    print("执行完成!")
    print("=" * 50)
    
    return articles


if __name__ == "__main__":
    main()