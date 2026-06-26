#!/usr/bin/env python3
"""
飞书通知器
支持文本、Markdown、文件发送
"""

import os
import json
import logging
from datetime import datetime
from typing import Optional, List, Dict

logger = logging.getLogger(__name__)

try:
    import requests
except ImportError:
    import urllib.request as requests


class FeishuNotifier:
    """飞书通知器（支持Webhook和开放平台API）"""

    def __init__(self, webhook_url: Optional[str] = None):
        """
        初始化飞书通知器

        Args:
            webhook_url: 飞书机器人Webhook URL（可选，用于文本快捷发送）
        """
        self.webhook_url = webhook_url or os.getenv('FEISHU_WEBHOOK_URL')

    def send_text_message(self, text: str) -> bool:
        """发送文本消息（通过Webhook）"""
        if not self.webhook_url:
            logger.warning("未配置飞书Webhook URL")
            return False

        try:
            data = {"msg_type": "text", "content": {"text": text}}
            response = requests.post(
                self.webhook_url, json=data,
                headers={'Content-Type': 'application/json'}, timeout=10
            )
            result = response.json()
            if result.get('StatusCode') == 0:
                logger.info("文本消息发送成功")
                return True
            else:
                logger.error(f"发送失败: {result.get('StatusMessage')}")
                return False
        except Exception as e:
            logger.error(f"发送异常: {e}")
            return False

    def send_markdown_message(self, text: str) -> bool:
        """发送Markdown格式消息（通过Webhook）"""
        if not self.webhook_url:
            logger.warning("未配置飞书Webhook URL")
            return False

        try:
            data = {
                "msg_type": "interactive",
                "card": {
                    "config": {"wide_screen_mode": True},
                    "elements": [{"tag": "div", "text": {"tag": "lark_md", "content": text}}]
                }
            }
            response = requests.post(
                self.webhook_url, json=data,
                headers={'Content-Type': 'application/json'}, timeout=10
            )
            result = response.json()
            if result.get('StatusCode') == 0:
                logger.info("Markdown消息发送成功")
                return True
            else:
                logger.error(f"发送失败: {result.get('StatusMessage')}")
                return False
        except Exception as e:
            logger.error(f"发送异常: {e}")
            return False

    def send_daily_report(self, date: str, projects: List[Dict],
                          pdf_file: Optional[str] = None,
                          feishu_app=None) -> bool:
        """
        发送日报（先发统计文字，再发PDF文件）

        Args:
            date: 日期
            projects: 项目列表
            pdf_file: PDF文件路径（可选）
            feishu_app: FeishuEnterpriseApp实例（用于发送文件）
        """
        total = len(projects)
        yannan = len([p for p in projects if p.get('region') == '盐南高新区'])
        jingkai = len([p for p in projects if p.get('region') == '经开区'])
        regional = len([p for p in projects if p.get('region') == '区域内'])

        lines = [
            f"**招投标信息日报**",
            f"📅 日期：{date}",
            "",
            f"📊 数据统计：",
            f"- 总项目数：{total} 个",
            f"- 盐南高新区：{yannan} 个",
            f"- 经开区：{jingkai} 个",
            f"- 区域内：{regional} 个",
            ""
        ]

        if projects:
            lines.append("**项目列表：**\n")
            for i, p in enumerate(projects[:10], 1):
                lines.append(f"{i}. **{p['project_name']}**")
                lines.append(f"   区域：{p.get('region', 'N/A')} | 来源：{p.get('source_site', 'N/A')}")
                if p.get('budget_text'):
                    lines.append(f"   预算：{p['budget_text']}")
                lines.append("")

            if len(projects) > 10:
                lines.append(f"... 还有 {len(projects) - 10} 个项目，详见PDF报告\n")

        if pdf_file:
            lines.append(f"📄 详细报告已生成")

        return self.send_markdown_message("\n".join(lines))


# 兼容旧代码的类名
class FeishuOpenAPI:
    """飞书开放平台API（已废弃，请使用 FeishuEnterpriseApp）"""
    pass