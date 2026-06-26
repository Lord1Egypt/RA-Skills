#!/usr/bin/env python3
"""
论文推荐报告生成器
整合 arXiv 搜索、GitHub 验证、智能分析
"""

import os
import json
from datetime import datetime
from search import find_papers_with_code
from analyze import analyze_paper, format_analysis_report

HISTORY_FILE = os.path.expanduser("~/papers/history.json")
OUTPUT_DIR = os.path.expanduser("~/papers/recommendations")

TOPIC_NAMES = {
    'agent-eval': 'Agent测评',
    'rag-eval': 'RAG测评',
    'agent-arch': 'Agent架构',
    'rag-arch': 'RAG架构'
}

def load_history() -> list:
    """加载已推荐论文历史"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f).get('recommended', [])
    return []

def save_to_history(paper: dict):
    """保存到历史记录"""
    history = load_history()
    history.append({
        'arxiv_id': paper['id'],
        'title': paper['title'],
        'date': datetime.now().strftime('%Y-%m-%d'),
        'topic': paper.get('topic', 'unknown')
    })
    
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, 'w') as f:
        json.dump({'recommended': history}, f, indent=2, ensure_ascii=False)

def is_already_recommended(arxiv_id: str) -> bool:
    """检查是否已推荐过"""
    history = load_history()
    return any(h['arxiv_id'] == arxiv_id for h in history)

def generate_report(paper: dict, analysis: dict) -> str:
    """生成 Markdown 报告"""
    
    github = paper.get('github', {})
    stars = github.get('stars', 0)
    updated = github.get('updated_at', 'N/A')
    language = github.get('language', 'Unknown')
    github_url = github.get('url', '')
    
    # 计算更新天数
    try:
        update_days = (datetime.now() - datetime.strptime(updated, '%Y-%m-%d')).days
    except:
        update_days = 'N/A'
    
    # 格式化建议列表（更清晰的格式）
    suggestions = analysis.get('practice_suggestions', [])
    if suggestions:
        suggestions_md = '\n'.join([f"- 💡 {s}" for s in suggestions])
    else:
        suggestions_md = "- 💡 建议阅读论文实验部分，了解具体应用场景"
    
    # 亮点
    highlights = analysis.get('highlights', [])
    highlights_str = '、'.join(highlights) if highlights else '方法创新'
    
    report = f"""# 📄 {paper['title']}

> **一句话摘要**：{analysis.get('one_line_summary', '待分析')}

## 📊 基本信息

| 项目 | 内容 |
|------|------|
| arXiv ID | {paper['id']} |
| 发布日期 | {paper['published']} |
| 作者 | {', '.join(paper['authors'][:3])}{'...' if len(paper['authors']) > 3 else ''} |
| 主题 | {paper.get('topic', '未知')} |
| 🔗 arXiv | [{paper['link']}]({paper['link']}) |
| 📥 PDF | [{paper['pdf_link']}]({paper['pdf_link']}) |
| 💻 GitHub | [{github_url}]({github_url}) (⭐ {stars} stars) |

---

## 📝 摘要

{paper['summary'][:600]}{'...' if len(paper['summary']) > 600 else ''}

---

## 🎯 推荐理由

### 1. 解决了什么问题？

{analysis.get('problem_solved', '待进一步阅读论文确定')}

**结论**：{analysis.get('conclusion', '待进一步阅读论文确定')}

### 2. 使用了什么方法？

{analysis.get('method_used', '待进一步阅读论文确定')}

**亮点**：{highlights_str}

### 3. 工程实践建议

{ suggestions_md }

### 4. 代码质量评估

| 指标 | 评价 |
|------|------|
| ⭐ Stars | {stars} 个 |
| 📅 最近更新 | {update_days} 天前 |
| 🔧 语言 | {language or '未指定'} |
| 📖 README | [需访问查看] |
| ✅ 可复现性 | {'高' if stars > 100 else '中' if stars > 20 else '待验证'} |

---

## ⏱️ 1分钟速览

**如果你只有1分钟，看这里：**

> {analysis.get('one_line_summary', '待分析')}

---

## 🔗 快速链接

- 📥 [下载 PDF]({paper['pdf_link']})
- 💻 [GitHub 代码]({github_url})
- 🌐 [arXiv 页面]({paper['link']})

---

*推荐时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} | 主题：{paper.get('topic', '未知')}*
"""
    return report

def recommend_paper(topic: str = None) -> dict:
    """推荐一篇论文"""
    import random
    
    topics = list(TOPIC_NAMES.keys())
    
    if topic not in topics:
        topic = random.choice(topics)
    
    topic_display = TOPIC_NAMES.get(topic, topic)
    print(f"🔍 搜索主题: {topic_display}")
    
    papers = find_papers_with_code(topic, max_results=20)
    
    # 过滤已推荐过的
    new_papers = [p for p in papers if not is_already_recommended(p['id'])]
    
    if not new_papers:
        print("没有找到新的符合条件的论文")
        # 如果没有新的，就用所有找到的
        new_papers = papers
    
    if not new_papers:
        return None
    
    # 选择 star 数最高的
    best = new_papers[0]
    best['topic'] = topic_display
    
    # 分析论文
    print(f"\n📊 分析论文...")
    analysis_result = analyze_paper(best)
    analysis = format_analysis_report(best, analysis_result)
    
    # 生成报告
    report = generate_report(best, analysis)
    
    # 保存报告
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, f"{datetime.now().strftime('%Y-%m-%d')}_{best['id'].replace('v1', '')}.md")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 保存到历史
    save_to_history(best)
    
    return {
        'paper': best,
        'analysis': analysis,
        'report_file': output_file,
        'report': report
    }

def main():
    import sys
    
    topic = sys.argv[1] if len(sys.argv) > 1 else None
    
    result = recommend_paper(topic)
    
    if result:
        p = result['paper']
        a = result['analysis']
        
        print(f"\n{'='*60}")
        print(f"📄 推荐论文：{p['title']}")
        print(f"{'='*60}")
        print(f"🎯 主题：{p['topic']}")
        print(f"📅 发布：{p['published']}")
        print(f"⭐ GitHub：{p['github']['stars']} stars")
        print(f"\n📝 一句话：{a.get('one_line_summary', '')[:100]}...")
        print(f"\n🔗 arXiv: {p['link']}")
        print(f"💻 GitHub: {p['github']['url']}")
        print(f"\n📄 完整报告：{result['report_file']}")

if __name__ == '__main__':
    main()
