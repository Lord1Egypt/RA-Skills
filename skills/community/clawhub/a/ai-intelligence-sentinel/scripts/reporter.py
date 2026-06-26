"""
AI前沿哨兵 - 报告生成模块
根据采集和分析的数据生成情报报告
"""
import argparse
import json
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from quality_scorer import QualityScorer


class ReportGenerator:
    """报告生成器"""
    
    def __init__(self, template_dir=None):
        self.template_dir = template_dir or Path(__file__).parent.parent / "templates"
        self.output_dir = Path(__file__).parent.parent / "output"
        self.output_dir.mkdir(exist_ok=True)
        
        # 初始化Jinja2环境
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )
        
        # 添加自定义过滤器
        self.env.filters['commalist'] = lambda x: f"{x:,}" if isinstance(x, (int, float)) else str(x)
    
    def generate(self, analyzed_data, report_type="morning"):
        """
        生成报告
        
        Args:
            analyzed_data: 分析后的数据
            report_type: 报告类型 (morning/evening)
        
        Returns:
            str: 生成的报告内容
        """
        template_name = f"{report_type}_report.md"
        
        try:
            template = self.env.get_template(template_name)
        except Exception:
            # 如果模板不存在，使用默认模板
            template = self._get_default_template(report_type)
        
        # 准备渲染数据
        context = self._prepare_context(analyzed_data, report_type)
        
        # 渲染报告
        report = template.render(**context)
        
        return report
    
    def generate_and_save(self, analyzed_data, report_type="morning"):
        """
        生成并保存报告
        
        Args:
            analyzed_data: 分析后的数据
            report_type: 报告类型
        
        Returns:
            Path: 报告文件路径
        """
        report = self.generate(analyzed_data, report_type)
        
        # 生成文件名
        date_str = datetime.now().strftime("%Y%m%d")
        time_str = datetime.now().strftime("%H%M")
        filename = f"{report_type}_report_{date_str}_{time_str}.md"
        output_path = self.output_dir / filename
        
        # 保存报告
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return output_path
    
    def _prepare_context(self, data, report_type):
        """准备渲染上下文"""
        timestamp = data.get("timestamp", datetime.now().isoformat())
        categorized = data.get("categorized", {})
        insights = data.get("insights", {})
        summary = data.get("summary", {})
        
        # 格式化时间
        try:
            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            date_str = dt.strftime("%Y年%m月%d日")
            time_str = dt.strftime("%H:%M")
        except:
            date_str = datetime.now().strftime("%Y年%m月%d日")
            time_str = datetime.now().strftime("%H:%M")
        
        # 生成今日摘要
        daily_summary = self._generate_daily_summary(categorized, insights, summary)
        
        # 问候语
        greetings = {
            "morning": "早安",
            "evening": "晚安"
        }
        
        # 质量评分
        scorer = QualityScorer()
        score_result = scorer.score_report(data)
        quality_card = scorer.generate_quality_card(score_result)
        
        return {
            "date_str": date_str,
            "time_str": time_str,
            "report_type": report_type,
            "greeting": greetings.get(report_type, "你好"),
            "total_items": data.get("total_items", 0),
            "summary": summary,
            "categorized": categorized,
            "insights": insights,
            "must_read": insights.get("must_read", [])[:10],
            "hot_topics": insights.get("hot_topics", []),
            "trending_projects": insights.get("trending_projects", [])[:5],
            "important_papers": insights.get("important_papers", [])[:2],  # 只展示最重要的2篇论文
            "top_picks": insights.get("must_read", [])[:5],  # 编辑精选
            "papers": categorized.get("papers", [])[:10],
            "projects": categorized.get("projects", [])[:10],
            "discussions": categorized.get("discussions", [])[:10],
            "news": categorized.get("news", [])[:10],
            "tweets": categorized.get("tweets", [])[:5],
            # 质量评分相关
            "daily_summary": daily_summary,
            "quality_score": score_result,
            "quality_card": quality_card
        }
    
    def _generate_daily_summary(self, categorized, insights, summary):
        """生成今日摘要"""
        summary_parts = []
        
        # 论文
        papers = categorized.get("papers", [])
        if papers:
            summary_parts.append(f"{len(papers)}篇学术论文")
        
        # 项目
        projects = categorized.get("projects", [])
        if projects:
            summary_parts.append(f"{len(projects)}个开源项目")
        
        # 讨论
        discussions = categorized.get("discussions", [])
        if discussions:
            summary_parts.append(f"{len(discussions)}条社区讨论")
        
        # 新闻
        news = categorized.get("news", [])
        if news:
            summary_parts.append(f"{len(news)}条行业动态")
        
        # 热词
        hot_topics = insights.get("hot_topics", [])
        if hot_topics:
            topics_str = "、".join(hot_topics[:3])
            summary_parts.append(f"热门话题：{topics_str}")
        
        if summary_parts:
            return "今日AI领域有新动态，涵盖" + "，".join(summary_parts)
        else:
            return "暂无重要更新"
    
    def _get_default_template(self, report_type):
        """获取默认模板"""
        if report_type == "morning":
            template_str = DEFAULT_MORNING_TEMPLATE
        else:
            template_str = DEFAULT_EVENING_TEMPLATE
        
        from jinja2 import Template
        return Template(template_str)


# 默认晨报模板（需与 templates/morning_report.md 保持同步）
DEFAULT_MORNING_TEMPLATE = """# 🌅 AI前沿哨兵 - {{ date_str }}晨报

> **今日摘要**：{{ daily_summary }}

---

## ⭐ 编辑精选（Top 5）

{% for item in top_picks[:5] %}
### {{ loop.index }}. [{{ item.title }}]({{ item.url or item.hn_url or item.pdf_url or "#" }})

**一句话摘要**：{{ (item.summary or item.description or item.abstract or item.text or "暂无摘要")[:150] if (item.summary or item.description or item.abstract or item.text) else "暂无摘要" }}

**为什么重要**：
{% if item.stars %}- ⭐ 高热度开源项目（{{ item.stars }} stars）
{% elif item.score %}- 🔥 社区热议（{{ item.score }} 分）
{% else %}- 📚 重要学术贡献
{% endif %}

---

{% endfor %}

## 📚 学术前沿（arXiv）

{% if important_papers %}
{% for paper in important_papers[:2] %}
### [{{ paper.title }}]({{ paper.url }})

📝 **一句话描述**：{{ paper.title.split(":")[-1].strip() if ":" in paper.title else paper.abstract[:120] if paper.abstract else "重要AI研究论文" }}

| 信息 | 内容 |
|------|------|
| 👥 作者 | {{ paper.author_str or paper.authors[0] if paper.authors and paper.authors is iterable else "未知" }} |
| 🏷️ 分类 | {{ paper.primary_category or "Unknown" }} |
| 📅 发布 | {{ paper.published[:10] if paper.published else "未知" }} |

{% if paper.abstract %}
**摘要**：{{ paper.abstract[:250] }}...
{% endif %}

🔗 [阅读论文]({{ paper.url }})

---

{% endfor %}
{% else %}
暂无新论文
{% endif %}

## ⚡ 热门开源项目（GitHub）

{% if trending_projects %}
{% for project in trending_projects[:5] %}
### [{{ project.title }}]({{ project.url }})

{{ project.description[:150] if project.description and project.description != "无描述" else "热门AI开源项目" }}

| 指标 | 数值 |
|------|------|
| ⭐ Stars | {{ project.stars|default(0)|int|commalist }} |
| 🍴 Forks | {{ project.forks|default(0)|int|commalist }} |
| 🐙 语言 | {{ project.language or "Unknown" }} |
| 👤 作者 | [{{ project.author or "Unknown" }}]({{ project.author_url or "#" }}) |

---

{% endfor %}
{% else %}
暂无热门项目
{% endif %}

## 💬 社区热议（HackerNews）

{% if discussions %}
{% for item in discussions[:5] %}
### [{{ item.title }}]({{ item.hn_url or item.url or "#" }})

{{ item.text[:120] if item.text else (item.description[:120] if item.description else "社区热门讨论") }}...

| 信息 | 内容 |
|------|------|
| ⬆️ 得分 | {{ item.score|default(0) }} |
| 💬 评论 | {{ item.comments|default(0) }} |
| 👤 作者 | {{ item.author or "Unknown" }} |
| 🕐 时间 | {{ item.time or item.published or "未知" }} |

---

{% endfor %}
{% else %}
暂无社区讨论
{% endif %}

## 📰 行业动态（AI博客）

{% if news %}
{% for item in news[:5] %}
### [{{ item.title }}]({{ item.url or "#" }})

**来源**：{{ item.source or "AI博客" }} · {{ item.published or "未知" }}

{{ (item.summary or item.description or "行业动态")[:150] }}...

{% if item.categories %}
🏷️ 标签：{{ item.categories|join(', ') }}
{% endif %}

---

{% endfor %}
{% else %}
暂无新闻更新
{% endif %}

{% if tweets %}
## 🐦 大咖动态（Twitter）

{% for tweet in tweets[:3] %}
### [{{ tweet.author_name or tweet.author_username }}](https://twitter.com/{{ tweet.author_username }})

{{ tweet.text[:200] }}

| 指标 | 数值 |
|------|------|
| ❤️ 点赞 | {{ tweet.likes|default(0) }} |
| 🔁 转发 | {{ tweet.retweets|default(0) }} |
| 🔗 [查看原推]({{ tweet.url }}) |

---

{% endfor %}
{% endif %}

## 📊 今日数据

| 类型 | 数量 |
|------|------|
| 学术论文 | {{ summary.papers_count }} 篇 |
| 开源项目 | {{ summary.projects_count }} 个 |
| 社区讨论 | {{ summary.discussions_count }} 条 |
| 新闻动态 | {{ summary.news_count }} 条 |
| 社交动态 | {{ summary.tweets_count }} 条 |

### 🔥 今日热词

{% if hot_topics %}
{% for topic in hot_topics %}#{{ topic }} {% endfor %}
{% else %}
暂无热词分析
{% endif %}

---

## 💡 推荐阅读

- 🔍 持续关注 GitHub Trending 新上榜项目
- 📚 定期查看 arXiv 新提交的论文
- 💬 HackerNews 上的技术讨论往往预示趋势

---

{{ quality_card }}
"""


# 默认晚报模板
DEFAULT_EVENING_TEMPLATE = """# 🌙 AI前沿哨兵 - {{ date_str }}晚报

{{ greeting }}！以下是今日AI领域完整动态回顾。

## 📈 今日总结

| 类型 | 数量 |
|------|------|
| 学术论文 | {{ summary.papers_count }} 篇 |
| 开源项目 | {{ summary.projects_count }} 个 |
| 社区讨论 | {{ summary.discussions_count }} 条 |
| 新闻动态 | {{ summary.news_count }} 条 |

{% if hot_topics %}
## 🔥 今日热词

{% for topic in hot_topics %}
- **{{ topic }}**
{% endfor %}
{% endif %}

{% if projects %}
## 💻 开源项目

{% for item in projects %}
### [{{ item.title }}]({{ item.url }})
{{ item.get('description', '')[:150] }}
- ⭐ {{ item.stars }} | 🍴 {{ item.forks }} | 📝 {{ item.language }}
{% endfor %}
{% endif %}

{% if papers %}
## 📚 最新论文

{% for item in papers %}
### [{{ item.title }}]({{ item.url }})
- 👥 {{ item.author_str }}
- 🏷️ {{ item.primary_category }}
{{ item.abstract[:200] }}

{% endfor %}
{% endif %}

{% if discussions %}
## 💬 社区热议

{% for item in discussions %}
### [{{ item.title }}]({{ item.hn_url if item.hn_url else item.url }})
- ⬆️ {{ item.score }} | 💬 {{ item.comments }} | 👤 {{ item.author }}
{% endfor %}
{% endif %}

{% if news %}
## 📰 最新动态

{% for item in news %}
### [{{ item.title }}]({{ item.url }})
{{ item.summary[:200] }}
- 📅 {{ item.published }} | 👤 {{ item.author }}

{% endfor %}
{% endif %}

---
*报告生成时间: {{ date_str }} {{ time_str }}*
*由 AI前沿哨兵 自动生成*
"""


def main():
    parser = argparse.ArgumentParser(description="AI前沿哨兵 - 报告生成工具")
    parser.add_argument("--type", type=str, default="morning", choices=["morning", "evening", "full"],
                        help="报告类型: morning(晨报), evening(晚报), full(完整报告-自动采集)")
    parser.add_argument("--input", type=str, help="分析结果JSON文件路径")
    parser.add_argument("--output", type=str, help="输出文件路径")
    
    args = parser.parse_args()
    
    # 如果是full类型，先执行采集和分析
    if args.type == "full":
        print("🚀 执行完整报告生成流程...")
        print("\n📋 Step 1: 采集所有信息源")
        
        # 导入collect模块
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        from collect import DataCollector
        
        # 执行采集
        collector = DataCollector()
        collect_result = collector.collect_all()
        
        if not collect_result or collect_result.get("total_items", 0) == 0:
            print("❌ 采集失败或无数据")
            return
        
        print(f"✅ 采集完成: {collect_result.get('total_items', 0)} 条数据")
        
        # 执行分析
        print("\n📊 Step 2: 智能分析数据")
        from analyzer import DataAnalyzer
        analyzer = DataAnalyzer()
        
        # 加载最新采集的数据
        output_dir = Path(__file__).parent.parent / "output"
        raw_files = list(output_dir.glob("raw_data_*.json"))
        if raw_files:
            latest_raw = max(raw_files, key=lambda f: f.stat().st_mtime)
            with open(latest_raw, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            analyzed_data = analyzer.analyze(raw_data)
            print("✅ 分析完成")
        else:
            print("❌ 未找到采集数据")
            return
        
        # 生成完整报告
        print("\n📄 Step 3: 生成完整报告")
        generator = ReportGenerator()
        report = generator.generate(analyzed_data, "evening")  # 使用晚报模板生成完整报告
        
        # 保存报告
        date_str = datetime.now().strftime("%Y-%m-%d")
        time_str = datetime.now().strftime("%H%M")
        reports_dir = Path(__file__).parent.parent / "reports" / date_str
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = reports_dir / f"full_report_{time_str}.md"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ 完整报告已保存到: {output_path}")
        print(f"\n📈 报告统计:")
        print(f"   - 总条目数: {analyzed_data.get('total_items', 0)}")
        print(f"   - 分类数: {len(analyzed_data.get('categorized', {}))}")
        return
    
    # 加载分析数据
    if args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            analyzed_data = json.load(f)
    else:
        # 尝试加载最新的分析结果
        output_dir = Path(__file__).parent.parent / "output"
        files = list(output_dir.glob("analyzed_*.json"))
        if files:
            latest = max(files, key=lambda f: f.stat().st_mtime)
            with open(latest, 'r', encoding='utf-8') as f:
                analyzed_data = json.load(f)
        else:
            print("❌ 未找到分析数据文件")
            return
    
    # 生成报告
    generator = ReportGenerator()
    report = generator.generate(analyzed_data, args.type)
    
    # 输出或保存
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✅ 报告已保存到: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
