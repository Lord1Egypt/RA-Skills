#!/usr/bin/env python3
"""
生物信息学日报搜索脚本
搜索并汇总最新的生物信息学、肿瘤学研究进展
"""

import subprocess
import json
import sys
import urllib.request
import urllib.parse
from datetime import datetime

def search_topic(topic, count=5):
    """搜索特定主题的最新研究"""
    try:
        # 使用 web_search 工具搜索
        result = subprocess.run(
            ['openclaw', 'web_search', f'{topic} 最新研究'],
            capture_output=True,
            text=True,
            timeout=60
        )
        # 提取实际的搜索结果
        output = result.stdout
        # 过滤掉插件注册信息
        lines = [line for line in output.split('\n') if not line.startswith('[')]
        return '\n'.join(lines[:30])  # 返回前30行
    except Exception as e:
        return f"搜索失败: {e}"

def main():
    """主函数：搜索并汇总生物信息学日报"""
    
    print("🔬 正在搜索今日生物信息学与肿瘤学研究进展...\n")
    
    # 定义搜索主题
    topics = [
        ("生物信息学 最新算法", "🧬 算法与工具"),
        ("肿瘤免疫学 最新研究", "🦠 肿瘤免疫"),
        ("单细胞测序 最新论文", "🔬 单细胞测序"),
        ("癌症免疫治疗 临床试验", "💊 临床进展"),
        ("空间转录组 技术进展", "🧪 空间组学"),
    ]
    
    daily_report = []
    daily_report.append("=" * 50)
    daily_report.append("📰 生物信息学日报")
    daily_report.append(f"📅 {datetime.now().strftime('%Y年%m月%d日')}")
    daily_report.append("=" * 50)
    daily_report.append("")
    
    for query, category in topics:
        print(f"正在搜索: {category}...")
        results = search_topic(query)
        
        daily_report.append(f"\n{category}")
        daily_report.append("-" * 40)
        daily_report.append(results[:500] if len(results) > 500 else results)
        daily_report.append("")
    
    daily_report.append("\n" + "=" * 50)
    daily_report.append("💡 提示：使用 openclaw bioinfo-daily search --topic [关键词] 查询特定主题")
    daily_report.append("=" * 50)
    
    report_text = "\n".join(daily_report)
    print(report_text)
    
    # 保存到文件
    output_file = f"/tmp/bioinfo_daily_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(f"\n📄 报告已保存: {output_file}")
    
    return report_text

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--topic":
        # 搜索特定主题
        topic = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "生物信息学"
        print(search_topic(topic))
    else:
        # 生成完整日报
        main()
