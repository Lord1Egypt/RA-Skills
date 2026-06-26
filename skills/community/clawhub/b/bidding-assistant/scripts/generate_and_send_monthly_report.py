#!/usr/bin/env python3
"""
生成并发送月报到飞书用户/群聊
支持发送PDF到用户个人或群聊
"""

import os
import sys
import logging
from datetime import datetime, timedelta

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.feishu_enterprise_app import FeishuEnterpriseApp
from scripts.pdf_generator import PDFGenerator

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """主函数：生成月报并发送"""
    print("=" * 60)
    print("招投标信息月报生成与发送")
    print("=" * 60)

    # 初始化
    app = FeishuEnterpriseApp()
    generator = PDFGenerator()

    # 检查配置
    if not app.app_id or not app.app_secret:
        print("❌ 未配置飞书应用凭证（appId/appSecret）")
        return False

    # 获取目标用户/群聊
    # 优先使用环境变量指定的接收者
    open_id = os.getenv('FEISHU_OPEN_ID')
    chat_id = os.getenv('FEISHU_CHAT_ID')

    if not open_id and not chat_id:
        print("⚠️ 未配置 FEISHU_OPEN_ID 或 FEISHU_CHAT_ID，将只生成PDF不发送")
        # 不直接退出，让后面可以生成PDF

    # 获取当前月份
    now = datetime.now()
    year = now.year
    month = now.month

    print(f"\n📅 正在生成 {year}年{month:02d}月 月报...")

    # 生成月度PDF（PDFGenerator默认输出到 daily 目录，需要改为 monthly）
    # 先生成到临时位置，然后再移动
    pdf_dir = os.path.join(os.path.dirname(generator.db_path), 'monthly')
    os.makedirs(pdf_dir, exist_ok=True)
    generator.output_dir = pdf_dir  # 临时修改输出目录

    pdf_file = generator.generate_monthly_report(year, month)
    if pdf_file:
        print(f"✅ PDF生成成功: {os.path.basename(pdf_file)} ({os.path.getsize(pdf_file) / 1024:.1f} KB)")
    else:
        print("❌ PDF生成失败")
        return False

    # 恢复输出目录
    generator.output_dir = os.path.join(os.path.dirname(generator.db_path), 'daily')

    # 查询月度数据
    first_day = datetime(year, month, 1).strftime('%Y-%m-%d')
    if month == 12:
        next_month_first_day = datetime(year + 1, 1, 1)
    else:
        next_month_first_day = datetime(year, month + 1, 1)
    last_day = (next_month_first_day - timedelta(days=1)).strftime('%Y-%m-%d')

    monthly_summary = generator._get_monthly_summary_data(first_day, last_day)
    if not monthly_summary:
        print("⚠️ 当月无数据")
        total = 0
    else:
        total = sum(monthly_summary.values())
        print(f"📊 查询到 {len(monthly_summary)} 个网站，共 {total} 条数据")

    # 发送PDF
    if open_id:
        print(f"\n📤 正在发送PDF到用户 {open_id}...")
        result = app.send_local_file(open_id, pdf_file, receive_id_type="open_id")
        if result:
            print(f"✅ 用户PDF发送成功！")
        else:
            print(f"❌ 用户PDF发送失败（详见日志）")

    if chat_id:
        print(f"\n📤 正在发送PDF到群聊 {chat_id}...")
        result = app.send_local_file(chat_id, pdf_file, receive_id_type="chat_id")
        if result:
            print(f"✅ 群聊PDF发送成功！")
        else:
            print(f"❌ 群聊PDF发送失败（详见日志）")

    if not open_id and not chat_id:
        print("\n📄 PDF已生成但未发送（未配置接收者）")

    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)