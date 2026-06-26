#!/usr/bin/env python3
"""
顾问会诊验证器

验证会诊输出是否符合顾问的核心理念
提供透明度和可追溯性
"""

import json
from datetime import datetime
from pathlib import Path

# 顾问核心理念数据库
ADVISOR_CORE_PRINCIPLES = {
    "德鲁克": {
        "核心问题": ["客户是谁", "价值主张", "业务是什么"],
        "关键词": ["客户", "价值", "目标", "管理", "组织", "贡献"],
        "思维特征": "本质导向、目标驱动、价值创造",
        "最低匹配": 2  # 至少匹配 2 个核心问题/关键词
    },
    "Jobs": {
        "核心问题": ["最好的体验", "简化", "爱上"],
        "关键词": ["体验", "简洁", "完美", "细节", "用户", "设计", "简洁"],
        "思维特征": "极致体验、简化、直觉",
        "最低匹配": 2
    },
    "原研哉": {
        "核心问题": ["有必要存在", "空", "本质"],
        "关键词": ["存在", "必要", "简约", "空", "本质", "去掉"],
        "思维特征": "极简、本质、空",
        "最低匹配": 2
    },
    "芒格": {
        "核心问题": ["反过来想", "学科框架", "能力圈"],
        "关键词": ["逆向", "模型", "框架", "能力圈", "心理学", "误判"],
        "思维特征": "多元思维、逆向思考",
        "最低匹配": 2
    },
    "巴菲特": {
        "核心问题": ["护城河", "10 年后", "安全边际"],
        "关键词": ["护城河", "长期", "价值", "安全", "竞争优势"],
        "思维特征": "长期主义、价值投资",
        "最低匹配": 2
    },
    "马斯克": {
        "核心问题": ["为什么还没开始", "第一性原理", "最小行动"],
        "关键词": ["开始", "行动", "第一性", "原理", "最小", "本周"],
        "思维特征": "第一性原理、快速行动",
        "最低匹配": 2
    },
    "维特根斯坦": {
        "核心问题": ["语言污染", "概念澄清", "逻辑边界"],
        "关键词": ["语言", "概念", "定义", "意义", "边界", "说清楚"],
        "思维特征": "语言分析、概念澄清",
        "最低匹配": 2
    },
    "弗洛伊德": {
        "核心问题": ["真实动机", "潜意识", "防御机制"],
        "关键词": ["动机", "潜意识", "欲望", "恐惧", "防御", "真正"],
        "思维特征": "潜意识分析、动机挖掘",
        "最低匹配": 2
    },
    "Bowen": {
        "核心问题": ["匹配度", "长期回报", "机会成本"],
        "关键词": ["匹配", "教育", "回报", "成本", "选择", "学校"],
        "思维特征": "教育经济学、匹配理论",
        "最低匹配": 2
    }
}


class ConsultationValidator:
    def __init__(self):
        self.validation_results = []
    
    def validate_advisor_response(self, advisor_name: str, response_text: str) -> dict:
        """验证某个顾问的回答是否符合其核心理念"""
        
        if advisor_name not in ADVISOR_CORE_PRINCIPLES:
            return {
                "advisor": advisor_name,
                "status": "unknown_advisor",
                "score": 0,
                "message": "未知顾问"
            }
        
        principles = ADVISOR_CORE_PRINCIPLES[advisor_name]
        
        # 计算匹配度
        core_matches = sum(1 for q in principles["核心问题"] if q in response_text)
        keyword_matches = sum(1 for k in principles["关键词"] if k in response_text)
        
        total_matches = core_matches + keyword_matches
        min_required = principles["最低匹配"]
        
        # 计算分数 (0-100)
        max_possible = len(principles["核心问题"]) + len(principles["关键词"])
        score = int((total_matches / max_possible) * 100)
        
        # 判定状态
        if total_matches >= min_required:
            status = "passed"
        elif total_matches >= min_required - 1:
            status = "warning"
        else:
            status = "failed"
        
        result = {
            "advisor": advisor_name,
            "status": status,
            "score": score,
            "core_matches": core_matches,
            "keyword_matches": keyword_matches,
            "total_matches": total_matches,
            "min_required": min_required,
            "matched_questions": [q for q in principles["核心问题"] if q in response_text],
            "matched_keywords": [k for k in principles["关键词"] if k in response_text],
            "思维特征": principles["思维特征"]
        }
        
        self.validation_results.append(result)
        return result
    
    def validate_consultation(self, consultation_text: str, advisors_used: list) -> dict:
        """验证整体会诊质量"""
        
        # 解析每个顾问的回答
        overall_score = 0
        passed_count = 0
        failed_advisors = []
        
        for advisor in advisors_used:
            # 简单分割（实际应该更智能）
            result = self.validate_advisor_response(advisor, consultation_text)
            overall_score += result["score"]
            
            if result["status"] == "passed":
                passed_count += 1
            elif result["status"] == "failed":
                failed_advisors.append(advisor)
        
        avg_score = overall_score / len(advisors_used) if advisors_used else 0
        
        return {
            "overall_score": int(avg_score),
            "passed_advisors": passed_count,
            "total_advisors": len(advisors_used),
            "failed_advisors": failed_advisors,
            "status": "passed" if not failed_advisors else "needs_review",
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_validation_report(self) -> str:
        """生成验证报告"""
        report = []
        report.append("## 顾问思维验证报告\n")
        
        for result in self.validation_results:
            status_emoji = {"passed": "✅", "warning": "⚠️", "failed": "❌"}.get(result["status"], "❓")
            report.append(f"### {status_emoji} {result['advisor']}")
            report.append(f"- 匹配分数：{result['score']}/100")
            report.append(f"- 核心问题匹配：{result['core_matches']}")
            report.append(f"- 关键词匹配：{result['keyword_matches']}")
            if result.get('matched_questions'):
                report.append(f"- 匹配问题：{', '.join(result['matched_questions'])}")
            if result.get('matched_keywords'):
                report.append(f"- 匹配关键词：{', '.join(result['matched_keywords'][:5])}")
            report.append(f"- 思维特征：{result['思维特征']}")
            report.append("")
        
        return "\n".join(report)


def main():
    """测试用"""
    validator = ConsultationValidator()
    
    # 测试用例
    test_response = """
    德鲁克观点：
    你的客户是谁？是团长还是最终消费者？
    你为他们创造什么价值？价格优势还是选品优势？
    你的业务本质是什么？是供货商还是服务商？
    """
    
    result = validator.validate_advisor_response("德鲁克", test_response)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
