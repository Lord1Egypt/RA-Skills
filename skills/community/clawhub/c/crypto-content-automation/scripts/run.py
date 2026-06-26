#!/usr/bin/env python3
"""
Crypto Content Automation - 整合版
"""

import sys
import os
import json
from datetime import datetime

# 添加workspace的scripts目录到路径
WORKSPACE = '/Users/youyou/.openclaw/workspace'
SCRIPTS_DIR = os.path.join(WORKSPACE, 'scripts')
sys.path.insert(0, SCRIPTS_DIR)

def run_hot_topic_scan():
    """运行热点扫描"""
    print("🔥 开始热点扫描...")
    from hot_topic_scanner import scan_ai_news, scan_crypto_news, scan_ai_crypto
    
    ai_news = scan_ai_news()
    crypto_news = scan_crypto_news()
    ai_crypto = scan_ai_crypto()
    
    report = {
        "time": datetime.now().isoformat(),
        "ai_news": [{"title": r['title'], "url": r['url']} for r in ai_news],
        "crypto_news": [{"title": r['title'], "url": r['url']} for r in crypto_news],
        "ai_crypto": [{"title": r['title'], "url": r['url']} for r in ai_crypto]
    }
    
    # 保存报告
    log_dir = os.path.join(WORKSPACE, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    report_file = f"{log_dir}/hot_topics_{datetime.now().strftime('%Y%m%d')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 热点扫描完成！报告: {report_file}")
    return report

def run_content_planning(hot_topics=None):
    """运行内容策划"""
    print("📝 开始内容策划...")
    
    if hot_topics is None:
        # 尝试读取今日热点
        log_dir = os.path.join(WORKSPACE, 'logs')
        report_file = f"{log_dir}/hot_topics_{datetime.now().strftime('%Y%m%d')}.json"
        if os.path.exists(report_file):
            with open(report_file, 'r', encoding='utf-8') as f:
                hot_topics = json.load(f)
    
    # 生成策划
    planning = f"""# 📝 内容策划案 - {datetime.now().strftime('%Y-%m-%d')}

## 🎯 今日核心选题

### 选题1：AI Agent + Crypto
**热点来源**：AI Agent正在改变Crypto生态

#### 1️⃣ 反直觉视角
- 大众认知：AI只是辅助工具
- 反向切入：AI Agent将成为Crypto的主要用户群体

#### 2️⃣ 落地操作指南
1. 了解AI Agent项目
2. 学习如何参与
3. 关注赛道发展

#### 3️⃣ 风险提示
- 项目风险
- 技术不确定性

---

## 📊 今日最佳选题

**推荐**：AI Agent赛道分析

---
*策划生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    # 保存策划
    log_dir = os.path.join(WORKSPACE, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    planning_file = f"{log_dir}/content_planning_{datetime.now().strftime('%Y%m%d')}.md"
    with open(planning_file, 'w', encoding='utf-8') as f:
        f.write(planning)
    
    print(f"✅ 内容策划完成！策划案: {planning_file}")
    return planning

def run_all():
    """完整流程"""
    print("🚀 开始完整内容运营流程...")
    topics = run_hot_topic_scan()
    planning = run_content_planning(topics)
    print("✅ 全部完成！")

def main():
    if len(sys.argv) < 2:
        print("""
╔════════════════════════════════════════╗
║  Crypto Content Automation           ║
╠════════════════════════════════════════╣
║  scan   - 热点扫描                  ║
║  plan   - 内容策划                  ║
║  all    - 完整流程                  ║
╚════════════════════════════════════════╝
        """)
        return
    
    cmd = sys.argv[1].lower()
    if cmd == 'scan':
        run_hot_topic_scan()
    elif cmd == 'plan':
        run_content_planning()
    elif cmd == 'all':
        run_all()
    else:
        print(f"未知命令: {cmd}")

if __name__ == '__main__':
    main()
