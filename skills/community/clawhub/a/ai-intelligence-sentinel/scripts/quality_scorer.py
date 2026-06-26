"""
AI前沿哨兵 - 报告质量评分系统
自动评估生成报告的质量
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any


class QualityScorer:
    """报告质量评分器"""
    
    def __init__(self):
        self.weights = {
            "information_density": 25,   # 信息密度
            "timeliness": 25,            # 时效性
            "diversity": 20,             # 多样性
            "readability": 15,           # 可读性
            "practicality": 15           # 实用性
        }
    
    def score_report(self, data: Dict[str, Any], report_content: str = "") -> Dict[str, Any]:
        """
        对报告进行全面评分
        
        Args:
            data: 报告数据（包含采集和分析结果）
            report_content: 报告原文（用于分析可读性）
        
        Returns:
            dict: 评分结果
        """
        scores = {}
        details = {}
        
        # 1. 信息密度评分（25分）
        info_score, info_detail = self._score_information_density(data)
        scores["information_density"] = info_score
        details["information_density"] = info_detail
        
        # 2. 时效性评分（25分）
        time_score, time_detail = self._score_timeliness(data)
        scores["timeliness"] = time_score
        details["timeliness"] = time_detail
        
        # 3. 多样性评分（20分）
        div_score, div_detail = self._score_diversity(data)
        scores["diversity"] = div_score
        details["diversity"] = div_detail
        
        # 4. 可读性评分（15分）
        read_score, read_detail = self._score_readability(data, report_content)
        scores["readability"] = read_score
        details["readability"] = read_detail
        
        # 5. 实用性评分（15分）
        prac_score, prac_detail = self._score_practicality(data)
        scores["practicality"] = prac_score
        details["practicality"] = prac_detail
        
        # 计算总分
        total = sum(scores.values())
        max_total = sum(self.weights.values())
        percentage = (total / max_total) * 100
        
        # 星级评分
        stars = self._get_stars(percentage)
        
        return {
            "scores": scores,
            "details": details,
            "total": total,
            "max_total": max_total,
            "percentage": round(percentage, 1),
            "stars": stars,
            "grade": self._get_grade(percentage)
        }
    
    def _score_information_density(self, data: Dict) -> tuple:
        """信息密度评分（25分）"""
        categorized = data.get("categorized", {})
        insights = data.get("insights", {})
        
        total_items = 0
        total_content_length = 0
        meaningful_items = 0
        
        # 统计各类内容
        for key, items in categorized.items():
            if isinstance(items, list):
                total_items += len(items)
                for item in items:
                    # 检查是否有有效内容
                    content = ""
                    if isinstance(item, dict):
                        content = (item.get("description", "") or 
                                  item.get("abstract", "") or 
                                  item.get("summary", "") or "")
                        if len(content) > 20:  # 有实质内容
                            meaningful_items += 1
                    total_content_length += len(str(content))
        
        # 统计编辑精选
        must_read = insights.get("must_read", [])
        total_items += len(must_read)
        meaningful_items += len([m for m in must_read if m.get("description") or m.get("abstract")])
        
        # 计算评分
        # 基础分：内容数量（10分）
        item_score = min(10, total_items * 0.5)
        
        # 内容质量：平均内容长度（10分）
        if total_items > 0:
            avg_length = total_content_length / total_items
            quality_score = min(10, avg_length / 30)  # 平均30字符/项为满分
        else:
            quality_score = 0
        
        # 有意义内容占比（5分）
        if total_items > 0:
            ratio_score = (meaningful_items / total_items) * 5
        else:
            ratio_score = 0
        
        total_score = round(item_score + quality_score + ratio_score)
        
        # 生成评价
        if total_items >= 20:
            detail = f"内容丰富，共{total_items}条有效信息"
        elif total_items >= 10:
            detail = f"内容适中，共{total_items}条信息"
        else:
            detail = f"内容较少，仅{total_items}条信息"
        
        return total_score, detail
    
    def _score_timeliness(self, data: Dict) -> tuple:
        """时效性评分（25分）"""
        categorized = data.get("categorized", {})
        
        now = datetime.now()
        recent_count = 0
        total_count = 0
        
        for key, items in categorized.items():
            if isinstance(items, list):
                for item in items:
                    total_count += 1
                    published = item.get("published", "") or item.get("created_at", "") or item.get("updated", "")
                    
                    if published:
                        try:
                            # 尝试解析日期
                            if isinstance(published, str):
                                if "T" in published:
                                    item_date = datetime.fromisoformat(published.replace("Z", "+00:00"))
                                else:
                                    item_date = datetime.strptime(published[:10], "%Y-%m-%d")
                            else:
                                continue
                            
                            # 24小时内为新鲜
                            if (now - item_date).total_seconds() < 86400:
                                recent_count += 1
                        except:
                            pass
        
        # 计算评分
        if total_count == 0:
            timeliness_score = 15  # 无数据时给基础分
            detail = "无法判断时效性"
        else:
            ratio = recent_count / total_count
            timeliness_score = round(min(25, ratio * 30))  # 80%以上新鲜内容为满分
            
            if ratio >= 0.8:
                detail = f"内容新鲜，{int(ratio*100)}%为24小时内发布"
            elif ratio >= 0.5:
                detail = f"时效性良好，{int(ratio*100)}%为近期内容"
            else:
                detail = f"部分内容较旧，仅{int(ratio*100)}%为24小时内"
        
        return timeliness_score, detail
    
    def _score_diversity(self, data: Dict) -> tuple:
        """多样性评分（20分）"""
        categorized = data.get("categorized", {})
        insights = data.get("insights", {})
        
        # 来源多样性
        sources = set()
        for key, items in categorized.items():
            if isinstance(items, list):
                for item in items:
                    source = item.get("source", "") or item.get("_source_name", "")
                    if source:
                        sources.add(source)
        
        # 类型多样性
        content_types = set(categorized.keys())
        
        # 话题多样性
        topics = insights.get("hot_topics", [])
        topic_count = len(topics)
        
        # 计算评分
        source_score = min(8, len(sources) * 1.5)  # 来源多样性（8分）
        type_score = min(7, len(content_types) * 2)  # 类型多样性（7分）
        topic_score = min(5, len(topics) * 1)  # 话题多样性（5分）
        
        total_score = round(source_score + type_score + topic_score)
        
        if len(sources) >= 5 and len(content_types) >= 4:
            detail = f"来源丰富，覆盖{len(sources)}个来源，{len(content_types)}种内容类型"
        else:
            detail = f"覆盖{len(sources)}个来源，{len(content_types)}种内容类型"
        
        return total_score, detail
    
    def _score_readability(self, data: Dict, report_content: str) -> tuple:
        """可读性评分（15分）"""
        if not report_content:
            return 12, "报告结构基本清晰"  # 无内容时给基础分
        
        # 检查结构元素
        has_summary = "## " in report_content and len(report_content.split("## ")) > 3  # 至少3个章节
        has_emoji = any(emoji in report_content for emoji in ["📚", "⭐", "🔥", "📊", "🔗"])
        has_links = "[" in report_content and "](" in report_content
        has_tables = "|" in report_content and "---" in report_content
        has_divider = "---" in report_content
        
        # 计算评分
        structure_score = 4 if has_summary else 2
        formatting_score = 4 if has_emoji else 2
        navigation_score = 4 if has_links else 2
        separation_score = 3 if has_divider else 1
        
        total_score = structure_score + formatting_score + navigation_score + separation_score
        
        # 生成评价
        positive = []
        if has_summary:
            positive.append("结构清晰")
        if has_emoji:
            positive.append("格式美观")
        if has_links:
            positive.append("导航完善")
        if has_tables:
            positive.append("数据规整")
        
        detail = "，".join(positive) if positive else "结构可进一步优化"
        
        return total_score, detail
    
    def _score_practicality(self, data: Dict) -> tuple:
        """实用性评分（15分）"""
        insights = data.get("insights", {})
        categorized = data.get("categorized", {})
        
        practical_count = 0
        total_count = 0
        
        # 检查是否有可操作的链接
        all_items = []
        for key, items in categorized.items():
            if isinstance(items, list):
                all_items.extend(items)
        
        # 有URL/链接的条目
        items_with_urls = [i for i in all_items if i.get("url") or i.get("pdf_url") or i.get("hn_url")]
        practical_count += len(items_with_urls)
        total_count += len(all_items)
        
        # 有摘要/描述的条目
        items_with_desc = [i for i in all_items if i.get("description") or i.get("abstract") or i.get("summary")]
        practical_count += len(items_with_desc)
        
        # 编辑精选质量
        must_read = insights.get("must_read", [])
        if len(must_read) >= 3:
            practical_count += 2
        if len(must_read) >= 5:
            practical_count += 1
        
        # 计算评分
        if total_count > 0:
            url_ratio = len(items_with_urls) / total_count
            desc_ratio = len(items_with_desc) / total_count
            
            action_score = min(8, url_ratio * 10)  # 可操作内容（8分）
            insight_score = min(7, desc_ratio * 8)  # 有洞察内容（7分）
        else:
            action_score = 5
            insight_score = 5
        
        total_score = round(action_score + insight_score)
        
        actionable = len(items_with_urls)
        detail = f"有{actionable}条可立即访问的资源"
        
        return total_score, detail
    
    def _get_stars(self, percentage: float) -> str:
        """根据百分比获取星级"""
        if percentage >= 90:
            return "⭐⭐⭐⭐⭐"
        elif percentage >= 80:
            return "⭐⭐⭐⭐"
        elif percentage >= 70:
            return "⭐⭐⭐"
        elif percentage >= 60:
            return "⭐⭐"
        else:
            return "⭐"
    
    def _get_grade(self, percentage: float) -> str:
        """获取评级"""
        if percentage >= 95:
            return "卓越"
        elif percentage >= 90:
            return "优秀"
        elif percentage >= 80:
            return "良好"
        elif percentage >= 70:
            return "中等"
        elif percentage >= 60:
            return "及格"
        else:
            return "待改进"
    
    def generate_quality_card(self, score_result: Dict) -> str:
        """生成质量评分卡片（Markdown格式）"""
        scores = score_result["scores"]
        details = score_result["details"]
        
        card = """

---

## 📊 报告质量评分

| 维度 | 得分 | 说明 |
|------|------|------|
"""
        
        dimensions = [
            ("information_density", "信息密度", 25),
            ("timeliness", "时效性", 25),
            ("diversity", "多样性", 20),
            ("readability", "可读性", 15),
            ("practicality", "实用性", 15)
        ]
        
        for key, name, max_score in dimensions:
            score = scores.get(key, 0)
            detail = details.get(key, "")
            card += f"| {name} | {score}/{max_score} | {detail} |\n"
        
        card += f"""
**总分：{score_result['total']}/{score_result['max_total']}** ({score_result['percentage']}%)
**评级：{score_result['grade']}** {score_result['stars']}

> 💡 本评分由 AI前沿哨兵 自动生成，仅供参考
"""
        
        return card


# 全局实例
_scorer = None

def get_scorer() -> QualityScorer:
    """获取评分器实例"""
    global _scorer
    if _scorer is None:
        _scorer = QualityScorer()
    return _scorer


def quick_score(data: Dict) -> Dict:
    """快速评分"""
    return get_scorer().score_report(data)


if __name__ == "__main__":
    # 测试代码
    test_data = {
        "categorized": {
            "papers": [
                {"title": "Test Paper 1", "abstract": "A" * 200, "url": "http://test.com"},
                {"title": "Test Paper 2", "abstract": "B" * 200, "url": "http://test.com"}
            ],
            "projects": [
                {"title": "Test Project", "description": "A" * 100, "url": "http://test.com"}
            ]
        },
        "insights": {
            "must_read": [
                {"title": "Important 1", "description": "Key insight"}
            ],
            "hot_topics": ["AI", "ML", "LLM"]
        }
    }
    
    scorer = QualityScorer()
    result = scorer.score_report(test_data)
    print(f"评分结果：{result['total']}/{result['max_total']}")
    print(f"评级：{result['grade']} {result['stars']}")
    print(scorer.generate_quality_card(result))
