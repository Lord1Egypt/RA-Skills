"""
AI Model Steward - 周度部署建议模块

功能:
1. 读取本周情报数据
2. AI 分析并生成部署建议
3. 输出报告（Markdown / 飞书文档）
"""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional

CACHE_DIR = Path.home() / ".openclaw" / ".ai-model-steward"
DAILY_CACHE_FILE = CACHE_DIR / "daily_intelligence.json"
REPORTS_DIR = CACHE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)


def load_weekly_data() -> list:
    """加载最近 7 天的情报数据"""
    if not DAILY_CACHE_FILE.exists():
        return []
    
    try:
        data = json.loads(DAILY_CACHE_FILE.read_text())
    except Exception:
        return []
    
    cutoff = datetime.now() - timedelta(days=7)
    week_data = []
    for item in data:
        fetched = item.get("fetched_at", "")
        if fetched:
            try:
                # 支持 ISO 格式
                dt = datetime.fromisoformat(fetched.replace('Z', '+00:00'))
                if dt > cutoff - timedelta(days=1):
                    week_data.append(item)
            except Exception:
                pass
    
    return week_data


def generate_weekly_report(data: list, output_format: str = "markdown") -> dict:
    """
    生成周度部署建议报告
    
    参数:
        data: 情报数据列表
        output_format: 'markdown' 或 'feishu'
    返回:
        报告内容和元数据
    """
    report_date = datetime.now().strftime("%Y-%m-%d")
    week_start = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    # 简单分析
    free_items = [i for i in data if i.get("is_free") or i.get("is_free_related")]
    news_items = [i for i in data if i.get("type") == "model_news"]
    
    # 按来源统计
    source_stats = {}
    for item in data:
        src = item.get("source", "unknown")
        source_stats[src] = source_stats.get(src, 0) + 1
    
    # ====== 生成建议报告 ======
    report_content = f"""# 🤖 AI 模型智能管家 - 周度部署建议报告

**报告周期**: {week_start} ~ {report_date}
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**数据源数量**: {len(source_stats)}
**情报总量**: {len(data)} 条

---

## 📊 本周情报概览

| 指标 | 数值 |
|------|------|
| 情报总量 | {len(data)} 条 |
| 免费/Tokens 相关 | {len(free_items)} 条 |
| 新模型发布 | {len(news_items)} 条 |
| 数据来源 | {len(source_stats)} 个 |

### 数据源分布
"""
    for src, count in sorted(source_stats.items(), key=lambda x: -x[1]):
        report_content += f"- **{src}**: {count} 条\n"

    report_content += f"""
---

## 🎁 免费 Tokens 信息汇总
"""
    if free_items:
        for item in free_items[:10]:  # 最多展示10条
            report_content += f"""
### {item.get('title', '未知')}
- 来源: {item.get('source', '-')}
- 摘要: {item.get('description', item.get('context_preview', '-'))[:200]}
- 链接: {item.get('url', '-')}
"""
    else:
        report_content += "\n本周未发现新的免费 Tokens 信息。\n"

    report_content += """
---

## 📰 新模型发布会

"""
    if news_items:
        for item in news_items[:10]:
            report_content += f"""
### {item.get('title', '未知')}
- 来源: {item.get('source', '-')}
- 摘要: {item.get('context_preview', '-')[:200]}
- 链接: {item.get('url', '-')}
"""
    else:
        report_content += "\n本周未发现新的模型发布会。\n"

    report_content += f"""
---

## 💡 部署建议

> ⚠️ 以下建议由 AI 基于本周情报自动生成，请审批后执行。

### 建议新增模型

> 基于本周免费发布的新模型或免费额度变动

待分析...

### 建议替换/调整

> 质量明显提升的模型替代建议

待分析...

### 建议保留

> 当前部署模型评估

待分析...

---

## 🔧 下一步

- [ ] 审批上述建议
- [ ] 执行模型部署 `ai-model-steward deploy`
- [ ] 验证模型可用性
- [ ] 回滚机制测试

---

*报告由 AI 模型智能管家自动生成*
"""

    # 保存文件
    report_filename = f"weekly_{report_date}.md"
    report_path = REPORTS_DIR / report_filename
    report_path.write_text(report_content, encoding='utf-8')

    return {
        "status": "success",
        "report_date": report_date,
        "week_start": week_start,
        "data_count": len(data),
        "free_count": len(free_items),
        "news_count": len(news_items),
        "report_file": str(report_path),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AI 模型智能管家 - 周度部署建议")
    parser.add_argument("--format", default="markdown", choices=["markdown", "feishu"])
    parser.add_argument("--bitable-app", help="飞书多维表格 App Token")
    args = parser.parse_args()

    print("=" * 50)
    print("📊 AI 模型智能管家 - 周度部署建议")
    print("=" * 50)

    data = load_weekly_data()
    print(f"\n📥 加载了 {len(data)} 条情报数据")

    result = generate_weekly_report(data, args.format)
    print(f"\n✅ 报告已生成: {result['report_file']}")
    print(f"📅 报告周期: {result['week_start']} ~ {result['report_date']}")
    print(f"🎁 免费 Tokens 相关: {result['free_count']} 条")
    print(f"📰 新模型发布: {result['news_count']} 条")
