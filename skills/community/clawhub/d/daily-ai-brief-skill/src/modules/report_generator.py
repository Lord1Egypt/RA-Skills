"""
报告生成器
将抓取结果保存为文件
"""
import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any

from .base_fetcher import NewsItem


class ReportGenerator:
    """报告生成器"""

    def __init__(self, output_dir: str = None):
        """
        初始化报告生成器

        Args:
            output_dir: 输出目录，默认为项目根目录下的reports目录
        """
        if output_dir is None:
            # 默认输出目录
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.output_dir = os.path.join(current_dir, "..", "reports")
        else:
            self.output_dir = output_dir

        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)

        self.logger = logging.getLogger(__name__)


    def generate_json_report(self, items: List[NewsItem]) -> str:
        """
        生成JSON格式报告

        Args:
            items: 新闻条目列表

        Returns:
            JSON报告文件路径
        """
        # 按发布时间降序排序
        sorted_items = sorted(items, key=lambda x: x.publish_date, reverse=True)

        # 生成报告文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H")
        filename = f"ai_news_report_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)

        # 转换为字典列表
        items_dict = [item.to_dict() for item in sorted_items]

        # 添加元数据
        report_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_items": len(items_dict),
                "source_count": len(set(item["source"] for item in items_dict)),
            },
            "items": items_dict
        }

        # 保存JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2, default=str)

        self.logger.info(f"JSON报告已保存: {filepath}")
        return filepath

    def _get_channel(self, item: NewsItem) -> str:
        """
        根据新闻条目属性确定频道分组

        Args:
            item: 新闻条目

        Returns:
            频道名称
        """
        source_type = item.source_type.lower() if item.source_type else ""
        source = item.source.lower() if item.source else ""

        # 根据source_type判断频道
        if source_type == "rss":
            # 根据来源名称判断是国内还是国际媒体
            if any(kw in source for kw in ["36kr", "36氪", "qbitai", "量子位"]):
                return "国内媒体"
            elif "arxiv" in source:
                return "学术研究"
            elif any(kw in source for kw in ["openai", "anthropic", "google", "deepmind", "meta", "microsoft"]):
                return "官方博客"
            elif any(kw in source for kw in ["mit", "techcrunch", "theverge", "arstechnica"]):
                return "国际媒体"
            else:
                return "其他RSS源"
        elif source_type == "twitter" or source_type == "x":
            return "社交媒体 (X/Twitter)"
        elif source_type == "web_scraper":
            return "网页爬虫"
        elif source_type == "api":
            return "API数据"
        elif source_type == "hackernews":
            return "社区讨论 (Hacker News)"
        else:
            return "其他来源"

    def _get_category(self, item: NewsItem) -> str:
        """
        根据新闻内容确定分类

        Args:
            item: 新闻条目

        Returns:
            分类名称
        """
        text = f"{item.title} {item.summary} {item.content}".lower()

        # 技术突破关键词
        breakthrough_keywords = [
            "breakthrough", "state of the art", "sota", "record", "里程碑",
            "革命性", "颠覆", "重大突破", "突破性", "创新", "novel", "innovative",
            "groundbreaking", "pioneering", "新模型", "算法改进", "性能提升"
        ]

        # 产品动态关键词
        product_keywords = [
            "product", "产品", "update", "更新", "上线", "launch", "发布",
            "feature", "功能", "用户体验", "user experience", "改进", "改进版"
        ]

        # 行业应用关键词
        industry_keywords = [
            "industry", "行业", "application", "应用", "落地", "case", "案例",
            "商业合作", "合作", "partnership", "enterprise", "企业", "制造业",
            "医疗", "教育", "金融", "finance", "healthcare", "education"
        ]

        # 开源项目关键词
        open_source_keywords = [
            "open source", "开源", "github", "repo", "repository", "project",
            "项目", "version", "版本", "release", "发布", "contribute", "贡献"
        ]

        # 学术前沿关键词
        academic_keywords = [
            "paper", "论文", "research", "研究", "academic", "学术", "conference",
            "会议", "预印本", "preprint", "arxiv", "期刊", "journal", "发表"
        ]

        # 政策监管关键词
        policy_keywords = [
            "policy", "政策", "regulation", "监管", "law", "法律", "法规",
            "合规", "compliance", "标准", "standard", "治理", "governance"
        ]

        # 投融资讯关键词
        funding_keywords = [
            "funding", "融资", "investment", "投资", "并购", "acquisition",
            "ipo", "上市", "venture", "风投", "capital", "资本", "融资轮",
            "seed", "series", "round", "估值", "valuation"
        ]

        # 专家观点关键词
        expert_keywords = [
            "expert", "专家", "opinion", "观点", "commentary", "评论",
            "interview", "访谈", "speech", "演讲", "statement", "声明",
            "分析", "analysis", "perspective", "视角"
        ]

        # 检查每个类别的关键词匹配数
        category_scores = {
            "技术突破": sum(1 for kw in breakthrough_keywords if kw in text),
            "产品动态": sum(1 for kw in product_keywords if kw in text),
            "行业应用": sum(1 for kw in industry_keywords if kw in text),
            "开源项目": sum(1 for kw in open_source_keywords if kw in text),
            "学术前沿": sum(1 for kw in academic_keywords if kw in text),
            "政策监管": sum(1 for kw in policy_keywords if kw in text),
            "投融资讯": sum(1 for kw in funding_keywords if kw in text),
            "专家观点": sum(1 for kw in expert_keywords if kw in text),
        }

        # 找到分数最高的类别
        max_score = max(category_scores.values())
        if max_score > 0:
            # 返回分数最高的类别
            for category, score in category_scores.items():
                if score == max_score:
                    return category

        # 默认类别
        return "行业动态"


    def generate_structured_report(self, items: List[NewsItem], orchestrator=None) -> str:
        """
        生成结构化报告，按照用户建议的每日简报结构组织

        Args:
            items: 新闻条目列表
            orchestrator: 协调器对象（可选），用于获取统计信息

        Returns:
            结构化报告文件路径
        """
        # 按发布时间降序排序
        sorted_items = sorted(items, key=lambda x: x.publish_date, reverse=True)

        # 生成报告文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H")
        filename = f"ai_news_report_{timestamp}.md"
        filepath = os.path.join(self.output_dir, filename)

        # 生成报告内容
        report_lines = []
        # 获取当前日期
        current_date = datetime.now()
        # 格式化为"年月日 今日AI简报"
        date_str = current_date.strftime("%Y年%m月%d日")
        report_lines.append(f"# {date_str} 行业简报")
        report_lines.append("")

        # 按分类分组
        categories = {
            "今日头条": [],
            "技术突破": [],
            "产品动态": [],
            "行业应用": [],
            "开源项目": [],
            "学术前沿": [],
            "政策监管": [],
            "投融资讯": [],
            "专家观点": [],
        }

        # 首先找出今日头条（最新的1-2条）
        if sorted_items:
            # 取最新的2条作为今日头条
            top_items = sorted_items[:2]
            categories["今日头条"] = top_items

            # 其他新闻按分类分组
            other_items = sorted_items[2:]
            for item in other_items:
                category = self._get_category(item)
                # 如果分类不在预定义列表中，放入技术突破
                if category not in categories:
                    category = "技术突破"
                categories[category].append(item)

        # 生成每个分类的内容
        for category_name, category_items in categories.items():
            if not category_items:
                continue

            report_lines.append(f"## {category_name}")
            report_lines.append("")

            for i, item in enumerate(category_items, 1):
                report_lines.append(f"### {i}. {item.title}")
                report_lines.append(f"**来源**: {item.source}")
                report_lines.append(f"**发布时间**: {item.publish_date.strftime('%Y-%m-%d %H:%M') if item.publish_date else '未知'}")
                report_lines.append(f"**链接**: [阅读原文]({item.url})")
                if item.summary:
                    report_lines.append(f"**摘要**:")
                    report_lines.append(f"{item.summary[:250]}...")
                report_lines.append("")

        # 保存报告
        report_content = "\n".join(report_lines)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)

        self.logger.info(f"结构化报告已保存: {filepath}")
        return filepath


    def generate_all_reports(self, items: List[NewsItem], orchestrator=None) -> Dict[str, str]:
        """
        生成所有类型的报告

        Args:
            items: 新闻条目列表
            orchestrator: 协调器对象（可选），用于获取统计信息

        Returns:
            报告文件路径字典
        """
        reports = {}

        try:
            # 只生成结构化报告（最全最优的Markdown报告）
            reports["structured"] = self.generate_structured_report(items, orchestrator)
        except Exception as e:
            self.logger.error(f"生成结构化报告失败: {e}")

        try:
            # 保留JSON报告作为机器可读格式
            reports["json"] = self.generate_json_report(items)
        except Exception as e:
            self.logger.error(f"生成JSON报告失败: {e}")

        return reports