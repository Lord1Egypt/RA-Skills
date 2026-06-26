"""
Article Taster - 主入口
帮助用户提前品尝文章可读性，过滤低质量内容
"""

import argparse
import sys
from typing import Optional

from .article_classifier import ArticleClassifier
from .tech_analyzer import TechAnalyzer
from .creative_analyzer import CreativeAnalyzer
from .novel_analyzer import NovelAnalyzer, SpoilerLevel
from .ai_detector import AIDetector
from .scorer import QualityScorer
from .report_generator import ReportGenerator


class ArticleTaster:
    """
    文章品鉴师 - 主分析器

    工作流程:
    1. 类型识别 (M1)
    2. 专业分析 (M2)
    3. AI检测 (M3)
    4. 综合评分 (M4)
    5. 报告生成
    """

    def __init__(self, spoiler_tolerance: str = "low"):
        self.classifier = ArticleClassifier()
        self.tech_analyzer = TechAnalyzer()
        self.creative_analyzer = CreativeAnalyzer()
        self.novel_analyzer = NovelAnalyzer(
            spoiler_tolerance=SpoilerLevel[spoiler_tolerance.upper()]
        )
        self.ai_detector = AIDetector()
        self.scorer = QualityScorer()
        self.report_generator = ReportGenerator()

    def analyze(
        self,
        text: str,
        title: str = None,
        article_type: str = None,
        user_hint: str = None,
        output_format: str = "markdown"
    ) -> dict:
        """
        分析文章

        Args:
            text: 文章内容
            title: 文章标题 (可选)
            article_type: 指定文章类型 (可选)
            user_hint: 用户提示的类型 (可选)
            output_format: 输出格式 (json/markdown)

        Returns:
            分析报告
        """
        title = title or self._extract_title(text)
        text = text.strip()

        # M1: 类型识别
        if article_type:
            detected_type = article_type
            type_confidence = 1.0
        elif user_hint:
            detected_type, type_confidence, _ = self.classifier.classify_with_hints(
                title, text, user_hint
            )
        else:
            detected_type, type_confidence = self.classifier.classify(title, text)

        # M2: 专业分析
        if detected_type == "technical_article":
            analysis_result = self.tech_analyzer.analyze(title, text)
            dimension_scores = analysis_result["dimension_scores"]
            weights = analysis_result["weights"]
            details = {
                "indicators": analysis_result.get("indicators", {}),
                "issues": analysis_result.get("issues", []),
                "strengths": analysis_result.get("strengths", [])
            }

        elif detected_type == "essay":
            analysis_result = self.creative_analyzer.analyze(title, text, "essay")
            dimension_scores = analysis_result["dimension_scores"]
            weights = analysis_result["weights"]
            details = {
                "emotional_curve": analysis_result.get("emotional_curve", {}),
                "indicators": analysis_result.get("indicators", {}),
                "strengths": analysis_result.get("strengths", []),
                "improvements": analysis_result.get("improvements", [])
            }

        elif detected_type == "novel":
            analysis_result = self.novel_analyzer.analyze(title, text)
            dimension_scores = analysis_result["dimension_scores"]
            weights = analysis_result["weights"]
            details = {
                "plot_analysis": analysis_result.get("plot_analysis", {}),
                "character_profiles": analysis_result.get("character_profiles", []),
                "spoiler_warnings": analysis_result.get("spoiler_warnings", []),
                "reader_experience": analysis_result.get("reader_experience", {}),
                "strengths": analysis_result.get("spoiler_free_summary", {}).get("key_strengths", [])
            }

        else:
            # other: 使用通用分析
            analysis_result = self.creative_analyzer.analyze(title, text, "other")
            dimension_scores = analysis_result["dimension_scores"]
            weights = analysis_result["weights"]
            details = {"indicators": analysis_result.get("indicators", {})}

        # M3: AI检测
        ai_result = self.ai_detector.detect(text)

        # M4: 综合评分
        overall_score, grade, score_breakdown = self.scorer.calculate_overall_score(
            dimension_scores,
            weights,
            ai_result["ai_probability"],
            detected_type
        )

        # 生成阅读建议
        reading_advice = self.scorer.generate_reading_advice(
            detected_type,
            grade,
            dimension_scores,
            text
        )

        # 生成报告
        ai_detection_summary = {
            "ai_probability": ai_result["ai_probability"],
            "is_ai_generated": ai_result["is_ai_generated"],
            "confidence_label": ai_result["confidence_label"],
            "originality_score": ai_result.get("originality_score", 0),
            "exemption_type": ai_result.get("exemption_type"),
            "exemption_confidence": ai_result.get("exemption_confidence", 0)
        }

        report = self.report_generator.generate(
            title=title,
            article_type=detected_type,
            type_confidence=type_confidence,
            overall_score=overall_score,
            grade=grade,
            reading_advice=reading_advice,
            dimension_scores=[
                {"dimension": k, "score": v, "weight": weights.get(k, 0)}
                for k, v in dimension_scores.items()
            ] if isinstance(list(dimension_scores.keys())[0], str) else
                {k: {"score": v, "weight": weights.get(k, 0)} for k, v in dimension_scores.items()},
            ai_detection=ai_detection_summary,
            analysis_details=details
        )

        # 格式化维度评分
        if isinstance(report["dimension_scores"], dict):
            report["dimension_scores"] = {
                k: {"score": v, "weight": weights.get(k, 0)}
                for k, v in dimension_scores.items()
            }

        # 输出格式
        if output_format == "markdown":
            report["_markdown"] = self.report_generator.to_markdown(report)

        return report

    def quick_score(self, text: str) -> dict:
        """
        快速评分 (简化版)

        Returns:
            简化报告，仅包含核心信息
        """
        title = self._extract_title(text)

        # 快速类型识别
        article_type, _ = self.classifier.classify(title, text)

        # 快速AI检测
        ai_result = self.ai_detector.detect(text)

        # 简化评分
        if article_type == "technical_article":
            analyzer = self.tech_analyzer
        else:
            analyzer = self.creative_analyzer

        result = analyzer.analyze(title, text)

        overall_score, grade, _ = self.scorer.calculate_overall_score(
            result["dimension_scores"],
            result["weights"],
            ai_result["ai_probability"],
            article_type
        )

        return {
            "score": overall_score,
            "grade": grade,
            "type": article_type,
            "ai_probability": ai_result["ai_probability"],
            "is_recommended": overall_score >= 70
        }

    def _extract_title(self, text: str) -> str:
        """从文本中提取标题"""
        lines = text.strip().split("\n")
        first_line = lines[0].strip() if lines else ""

        # 如果第一行很短 (< 50字符) 且没有明显的内容标记，则认为是标题
        if len(first_line) < 50 and not any(
            marker in first_line for marker in ["#", "```", "http"]
        ):
            return first_line

        return "未命名文章"


def main():
    parser = argparse.ArgumentParser(
        description="Article Taster - 文章品鉴师",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python -m article_taster analyze --text "文章内容..."
  python -m article_taster analyze --file article.txt
  python -m article_taster quick --text "文章内容..."
  python -m article_taster batch --dir ./articles
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # analyze 命令
    analyze_parser = subparsers.add_parser("analyze", help="分析单篇文章")
    analyze_parser.add_argument("--text", type=str, help="文章文本内容")
    analyze_parser.add_argument("--file", type=str, help="文章文件路径")
    analyze_parser.add_argument("--title", type=str, help="文章标题")
    analyze_parser.add_argument("--type", type=str, choices=[
        "technical_article", "essay", "novel", "other"
    ], help="指定文章类型")
    analyze_parser.add_argument("--output", type=str, choices=["json", "markdown"],
        default="markdown", help="输出格式")

    # quick 命令
    quick_parser = subparsers.add_parser("quick", help="快速评分")
    quick_parser.add_argument("--text", type=str, required=True, help="文章文本内容")

    # batch 命令
    batch_parser = subparsers.add_parser("batch", help="批量分析")
    batch_parser.add_argument("--dir", type=str, required=True, help="文章目录")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    taster = ArticleTaster()

    if args.command == "analyze":
        text = args.text
        if not text and args.file:
            with open(args.file, "r", encoding="utf-8") as f:
                text = f.read()
        elif not text:
            print("错误: 请提供 --text 或 --file 参数")
            return

        report = taster.analyze(
            text=text,
            title=args.title,
            article_type=args.type,
            output_format=args.output
        )

        if args.output == "markdown":
            print(report["_markdown"])
        else:
            print(taster.report_generator.to_json_string(report))

    elif args.command == "quick":
        result = taster.quick_score(args.text)
        print(f"评分: {result['score']}分 ({result['grade']})")
        print(f"类型: {result['type']}")
        print(f"AI概率: {result['ai_probability']:.0%}")
        print(f"推荐: {'是' if result['is_recommended'] else '否'}")

    elif args.command == "batch":
        print("批量分析功能开发中...")


if __name__ == "__main__":
    main()
