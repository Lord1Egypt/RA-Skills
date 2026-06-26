# ✅ AI 质检师 Agent

"""
质检师职责：
1. 质量评估（电商标准检查）
2. 问题诊断与分类
3. 迭代建议生成
4. 最终交付把关

状态：常开（质量优先）

输出：质检报告（通过/微调/返工）+ 具体问题描述
"""

from typing import Dict, List, Optional
import json
import os
from datetime import datetime


class ReviewerAgent:
    """质检师 Agent"""
    
    def __init__(self):
        self.name = "✅ 质检师"
        self.config = self._load_config()
        self.rules = self._load_rules()
        self.quality_threshold = 0.8  # 80 分通过
    
    def _load_config(self) -> Dict:
        """加载质检师配置"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), 'config/reviewer_config.json')
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return self._default_config()
    
    def _default_config(self) -> Dict:
        """默认配置"""
        return {
            "quality_threshold": 0.8,
            "language": "zh-CN",
            "auto_suggest": True
        }
    
    def _load_rules(self) -> Dict:
        """加载质量规则库"""
        try:
            rules_path = os.path.join(os.path.dirname(__file__), 'config/quality_rules.json')
            with open(rules_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return self._default_rules()
    
    def _default_rules(self) -> Dict:
        """默认质量规则"""
        return {
            "quality_checklist": [
                {"item": "产品主体清晰突出", "weight": 0.2},
                {"item": "无明显 AI 瑕疵（畸形/错位）", "weight": 0.2},
                {"item": "色彩符合品牌调性", "weight": 0.15},
                {"item": "尺寸符合平台要求", "weight": 0.1},
                {"item": "文字可读性（如有文案）", "weight": 0.15},
                {"item": "风格与需求一致", "weight": 0.2}
            ],
            "critical_issues": ["产品变形", "严重 AI 瑕疵", "完全偏离需求", "无法识别产品"],
            "minor_issues": ["色彩略有偏差", "细节不够清晰", "背景可优化", "光影可调整"]
        }
    
    def review(self, images: List[Dict], brief: Dict) -> Dict:
        """
        质检图片
        
        Args:
            images: 执行师生成的图片列表
            brief: 原始创意简报
            
        Returns:
            质检报告
        """
        if not images:
            return {"status": "error", "agent": "reviewer", "message": "没有图片可供质检"}
        
        image_reports = []
        for img in images:
            report = self._review_single_image(img, brief)
            image_reports.append(report)
        
        overall_result = self._overall_decision(image_reports)
        
        # 保存质检历史
        self._save_review_history(overall_result, image_reports)
        
        return {
            "status": "completed",
            "agent": "reviewer",
            "timestamp": datetime.now().isoformat(),
            "overall": overall_result,
            "image_reports": image_reports,
            "summary": self._generate_summary(overall_result, image_reports)
        }
    
    def _review_single_image(self, image: Dict, brief: Dict) -> Dict:
        """质检单张图片"""
        checklist = self.rules.get("quality_checklist", [])
        
        scores = []
        issues = []
        suggestions = []
        
        for item in checklist:
            score, issue, suggestion = self._check_item(item["item"], image, brief)
            scores.append(score * item["weight"])
            if issue:
                issues.append(issue)
            if suggestion:
                suggestions.append(suggestion)
        
        total_score = sum(scores)
        
        if total_score >= self.quality_threshold:
            verdict = "pass"
            verdict_text = "✅ 通过"
        elif total_score >= 0.5:
            verdict = "minor_revision"
            verdict_text = "⚠️ 需要微调"
        else:
            verdict = "major_revision"
            verdict_text = "❌ 需要返工"
        
        return {
            "image_path": image.get("path", "unknown"),
            "score": round(total_score * 100, 1),
            "verdict": verdict,
            "verdict_text": verdict_text,
            "issues": issues,
            "suggestions": suggestions,
            "checklist_details": self._get_checklist_details(checklist, image, brief)
        }
    
    def _check_item(self, item: str, image: Dict, brief: Dict) -> tuple:
        """检查单项"""
        score = 0.8  # 默认良好
        issue = None
        suggestion = None
        
        # 简化实现：默认良好
        # 实际可用视觉模型分析
        
        if score < 0.6:
            issue = f"{item} - 不达标"
            suggestion = self._get_suggestion_for_item(item)
        elif score < 0.8:
            suggestion = f"建议优化：{item}"
        
        return score, issue, suggestion
    
    def _get_suggestion_for_item(self, item: str) -> str:
        """针对特定问题给出建议"""
        suggestions = {
            "产品主体清晰突出": "建议增加产品占比，减少背景干扰",
            "无明显 AI 瑕疵（畸形/错位）": "建议重新生成，注意检查产品细节",
            "色彩符合品牌调性": "建议调整色调，使其更符合产品定位",
            "尺寸符合平台要求": "建议裁剪或调整为平台标准尺寸",
            "文字可读性（如有文案）": "建议优化文字大小、颜色或位置",
            "风格与需求一致": "建议重新明确风格要求，调整生成参数"
        }
        return suggestions.get(item, "建议优化此项")
    
    def _get_checklist_details(self, checklist: List, image: Dict, brief: Dict) -> List[Dict]:
        """获取检查清单详情"""
        details = []
        for item in checklist:
            score, issue, suggestion = self._check_item(item["item"], image, brief)
            details.append({
                "item": item["item"],
                "score": round(score * 100, 1),
                "status": "⚠️" if score < 0.6 else ("✓" if score >= 0.8 else "~"),
                "issue": issue,
                "suggestion": suggestion
            })
        return details
    
    def _overall_decision(self, image_reports: List[Dict]) -> Dict:
        """综合判定"""
        pass_count = sum(1 for r in image_reports if r["verdict"] == "pass")
        minor_count = sum(1 for r in image_reports if r["verdict"] == "minor_revision")
        major_count = sum(1 for r in image_reports if r["verdict"] == "major_revision")
        
        avg_score = sum(r["score"] for r in image_reports) / len(image_reports)
        
        if major_count > 0:
            overall_verdict = "major_revision"
            overall_text = "❌ 需要返工"
            action = "返回策划师重新规划"
        elif minor_count > pass_count:
            overall_verdict = "minor_revision"
            overall_text = "⚠️ 需要微调"
            action = "执行师微调后交付"
        else:
            overall_verdict = "pass"
            overall_text = "✅ 通过"
            action = "直接交付"
        
        return {
            "verdict": overall_verdict,
            "verdict_text": overall_text,
            "action": action,
            "average_score": round(avg_score, 1),
            "pass_count": pass_count,
            "minor_count": minor_count,
            "major_count": major_count,
            "total_images": len(image_reports)
        }
    
    def _generate_summary(self, overall: Dict, image_reports: List[Dict]) -> str:
        """生成质检摘要"""
        parts = []
        
        parts.append(f"【质检结果】{overall['verdict_text']}")
        parts.append(f"【平均得分】{overall['average_score']}分")
        parts.append(f"【通过图片】{overall['pass_count']}/{overall['total_images']}张")
        
        all_issues = []
        for report in image_reports:
            all_issues.extend(report.get("issues", []))
        
        if all_issues:
            parts.append("【主要问题】")
            for issue in all_issues[:3]:
                parts.append(f"  - {issue}")
        
        all_suggestions = []
        for report in image_reports:
            all_suggestions.extend(report.get("suggestions", []))
        
        if all_suggestions:
            parts.append("【优化建议】")
            for sug in all_suggestions[:3]:
                parts.append(f"  - {sug}")
        
        return "\n".join(parts)
    
    def get_iteration_plan(self, image_reports: List[Dict]) -> Dict:
        """生成迭代计划"""
        all_issues = []
        all_suggestions = []
        
        for report in image_reports:
            all_issues.extend(report.get("issues", []))
            all_suggestions.extend(report.get("suggestions", []))
        
        has_critical = any(
            any(ci in issue for ci in self.rules.get("critical_issues", []))
            for issue in all_issues
        )
        
        if has_critical:
            iteration_type = "major"
            action = "返回策划师重新规划"
        elif all_suggestions:
            iteration_type = "minor"
            action = "执行师微调"
        else:
            iteration_type = "none"
            action = "直接交付"
        
        return {
            "type": iteration_type,
            "action": action,
            "issues": all_issues,
            "suggestions": all_suggestions,
            "priority_adjustments": list(dict.fromkeys(all_suggestions))[:5]
        }
    
    def _save_review_history(self, overall: Dict, image_reports: List[Dict]):
        """保存质检历史"""
        history_path = os.path.join(os.path.dirname(__file__), 'memory/review_history.md')
        
        try:
            os.makedirs(os.path.dirname(history_path), exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            verdict = overall.get("verdict_text", "N/A")
            score = overall.get("average_score", 0)
            
            with open(history_path, 'a', encoding='utf-8') as f:
                f.write(f"\n## [{timestamp}] 质检结果：{verdict}\n")
                f.write(f"- 平均得分：{score}分\n")
                f.write(f"- 图片数量：{overall.get('total_images', 0)}\n")
                f.write(f"- 通过：{overall.get('pass_count', 0)}/{overall.get('total_images', 0)}\n")
                f.write("---\n")
        except Exception as e:
            print(f"保存质检历史失败：{e}")


# 快捷函数
def review_images(images: List[Dict], brief: Dict) -> Dict:
    """快捷质检"""
    agent = ReviewerAgent()
    return agent.review(images, brief)


if __name__ == "__main__":
    test_images = [{"path": "output/image_1.png"}, {"path": "output/image_2.png"}]
    test_brief = {"product_info": {"type": "服装", "style": "简约优雅"}}
    result = review_images(test_images, test_brief)
    print(json.dumps(result, ensure_ascii=False, indent=2))
