# 类案检索与智能推送系统
# 度量衡商事调解智库 - 争议焦点→类案→裁判观点

import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field

# ============================================================
# 数据结构定义
# ============================================================

@dataclass
class CaseSummary:
    """类案摘要"""
    case_id: str
    title: str
    court: str
    date: str
    dispute_type: str  # 争议类型
    key_issue: str     # 关键争议点
    ruling: str        # 裁判结果
    main_reason: str   # 主要裁判理由
    amount: Optional[float] = None  # 涉及金额
    tags: List[str] = field(default_factory=list)


@dataclass
class DisputePattern:
    """争议模式"""
    pattern_id: str
    name: str
    description: str
    related_articles: List[str]  # 相关法条
    typical_cases: List[str]     # 典型案例ID
    mediation_tips: List[str]    # 调解建议


# ============================================================
# 内置类案数据库（示例）
# ============================================================

INTERNAL_CASE_DATABASE: List[CaseSummary] = [
    CaseSummary(
        case_id="CASE001",
        title="某建设公司与某房地产公司工程款纠纷案",
        court="某市中级人民法院",
        date="2024-03-15",
        dispute_type="工程款纠纷",
        key_issue="工程款支付条件是否成就",
        ruling="发包人应支付剩余工程款580万元",
        main_reason="工程已验收合格，付款条件已成就，发包人抗辩理由不成立",
        amount=5800000,
        tags=["验收合格", "付款条件", "抗辩不成立"]
    ),
    CaseSummary(
        case_id="CASE002",
        title="某建筑公司与某开发公司工期延误责任案",
        court="某省高级人民法院",
        date="2023-11-20",
        dispute_type="工期争议",
        key_issue="工期延误责任归属",
        ruling="承包人承担40%责任，设计变更影响60%",
        main_reason="承包人存在施工组织不当，但设计变更是主因",
        amount=12000000,
        tags=["工期延误", "责任划分", "设计变更"]
    ),
    CaseSummary(
        case_id="CASE003",
        title="某工程公司质量缺陷纠纷案",
        court="某市中级人民法院",
        date="2024-01-10",
        dispute_type="质量争议",
        key_issue="质量问题责任划分",
        ruling="承包人承担修复费用185万元",
        main_reason="质量问题主要由施工工艺不当导致",
        amount=1850000,
        tags=["质量缺陷", "修复费用", "责任划分"]
    ),
    CaseSummary(
        case_id="CASE004",
        title="某建设集团变更签证争议案",
        court="某仲裁委员会",
        date="2023-09-05",
        dispute_type="变更签证争议",
        key_issue="变更签证效力认定",
        ruling="发包人应支付签证价款210万元",
        main_reason="签证单有监理签字确认，应认定为有效变更",
        amount=2100000,
        tags=["签证效力", "监理确认", "变更认定"]
    ),
    CaseSummary(
        case_id="CASE005",
        title="某建筑公司工程款优先受偿权案",
        court="某市中级人民法院",
        date="2024-05-20",
        dispute_type="工程款纠纷",
        key_issue="优先受偿权行使期限",
        ruling="承包人享有优先受偿权",
        main_reason="未超过18个月行使期限",
        amount=3500000,
        tags=["优先受偿权", "期限", "建设工程"]
    ),
]


# ============================================================
# 争议模式库
# ============================================================

DISPUTE_PATTERNS: Dict[str, DisputePattern] = {
    "工程款支付": DisputePattern(
        pattern_id="P001",
        name="工程款支付争议",
        description="发包人拒绝或延迟支付工程款，承包人主张付款",
        related_articles=["民法典第807条", "建工解释一第21条", "GF-2017-0201第12条"],
        typical_cases=["CASE001", "CASE005"],
        mediation_tips=[
            "核查工程验收状态和付款节点",
            "梳理已付款项和欠付款项",
            "分析付款条件是否成就",
            "考虑工程款优先受偿权问题"
        ]
    ),
    "工期延误": DisputePattern(
        pattern_id="P002",
        name="工期延误责任争议",
        description="工期延误的责任归属和违约责任承担",
        related_articles=["民法典第584条", "GF-2017-0201第11条", "建工解释一第10条"],
        typical_cases=["CASE002"],
        mediation_tips=[
            "分析工期延误的原因（承包人/发包人/不可抗力）",
            "审查合同约定的工期和违约条款",
            "评估延误对项目的影响和损失",
            "考虑赶工费用的合理性"
        ]
    ),
    "质量问题": DisputePattern(
        pattern_id="P003",
        name="工程质量争议",
        description="工程质量缺陷的责任认定和修复费用",
        related_articles=["建筑法第60条", "民法典第801条", "GF-2017-0201第13条"],
        typical_cases=["CASE003"],
        mediation_tips=[
            "区分质量缺陷的责任主体（施工/设计/材料）",
            "审查验收程序是否合规",
            "确定修复方案和费用",
            "考虑质量保证金问题"
        ]
    ),
    "变更签证": DisputePattern(
        pattern_id="P004",
        name="变更签证争议",
        description="设计变更、施工变更的效力认定和价款确定",
        related_articles=["GF-2017-0201第10条", "建工解释一第19条", "GB/T 50500-2024第9条"],
        typical_cases=["CASE004"],
        mediation_tips=[
            "审查变更指令的书面形式",
            "核对签证单的签认情况",
            "确定计价依据和方式",
            "注意变更时效问题"
        ]
    ),
}


# ============================================================
# 类案检索核心类
# ============================================================

class CaseRetriever:
    """
    类案检索系统
    
    功能：
    1. 根据争议类型检索相似案例
    2. 提取关键争议点
    3. 推送裁判观点
    4. 生成调解建议
    """
    
    def __init__(self, case_database: Optional[List[CaseSummary]] = None):
        self.cases = case_database or INTERNAL_CASE_DATABASE
        self.patterns = DISPUTE_PATTERNS
        
    def search_by_dispute_type(self, dispute_type: str, limit: int = 5) -> List[CaseSummary]:
        """
        按争议类型检索类案
        
        Args:
            dispute_type: 争议类型（如：工程款纠纷、工期争议等）
            limit: 返回数量限制
            
        Returns:
            匹配的案例列表
        """
        results = []
        keywords = self._normalize_dispute_type(dispute_type)
        
        for case in self.cases:
            if any(kw in case.dispute_type for kw in keywords):
                results.append(case)
                
        return results[:limit]
    
    def search_by_key_issue(self, key_issue: str, limit: int = 3) -> List[CaseSummary]:
        """
        按关键争议点检索类案
        
        Args:
            key_issue: 关键争议点描述
            
        Returns:
            匹配的案例列表
        """
        results = []
        issue_keywords = key_issue.lower().split()
        
        for case in self.cases:
            # 计算关键词匹配度
            case_text = (case.key_issue + case.ruling).lower()
            match_count = sum(1 for kw in issue_keywords if kw in case_text)
            if match_count > 0:
                results.append((case, match_count))
        
        # 按匹配度排序
        results.sort(key=lambda x: x[1], reverse=True)
        return [case for case, _ in results[:limit]]
    
    def search_by_tags(self, tags: List[str], limit: int = 3) -> List[CaseSummary]:
        """
        按标签检索类案
        
        Args:
            tags: 标签列表
            
        Returns:
            匹配的案例列表
        """
        results = []
        
        for case in self.cases:
            if any(tag in case.tags for tag in tags):
                results.append(case)
                
        return results[:limit]
    
    def get_case_detail(self, case_id: str) -> Optional[CaseSummary]:
        """获取案例详情"""
        for case in self.cases:
            if case.case_id == case_id:
                return case
        return None
    
    def get_pattern_info(self, dispute_type: str) -> Optional[DisputePattern]:
        """获取争议模式信息"""
        # 模糊匹配
        for key, pattern in self.patterns.items():
            if key in dispute_type:
                return pattern
        return None
    
    def full_search(self, 
                   dispute_type: Optional[str] = None,
                   key_issue: Optional[str] = None,
                   tags: Optional[List[str]] = None,
                   amount_range: Optional[tuple] = None) -> Dict[str, Any]:
        """
        综合检索
        
        Args:
            dispute_type: 争议类型
            key_issue: 关键争议点
            tags: 标签
            amount_range: 金额范围 (min, max)
            
        Returns:
            检索结果
        """
        results = set()
        
        # 多条件组合检索
        if dispute_type:
            for case in self.search_by_dispute_type(dispute_type, limit=10):
                results.add(case.case_id)
                
        if key_issue:
            for case in self.search_by_key_issue(key_issue, limit=10):
                results.add(case.case_id)
                
        if tags:
            for case in self.search_by_tags(tags, limit=10):
                results.add(case.case_id)
        
        # 获取完整案例
        cases = []
        for case_id in results:
            case = self.get_case_detail(case_id)
            if case:
                # 金额过滤
                if amount_range:
                    if case.amount and amount_range[0] <= case.amount <= amount_range[1]:
                        cases.append(case)
                else:
                    cases.append(case)
        
        # 获取争议模式
        pattern = self.get_pattern_info(dispute_type or key_issue or "")
        
        return {
            "case_count": len(cases),
            "cases": cases,
            "pattern": pattern,
            "search_params": {
                "dispute_type": dispute_type,
                "key_issue": key_issue,
                "tags": tags,
                "amount_range": amount_range
            }
        }
    
    def generate_mediation_report(self, 
                                   dispute_type: str,
                                   key_issue: str,
                                   case_info: Optional[Dict] = None) -> str:
        """
        生成调解建议报告
        
        Args:
            dispute_type: 争议类型
            key_issue: 关键争议点
            case_info: 当前案件信息（可选）
            
        Returns:
            调解建议报告文本
        """
        # 检索类案
        search_result = self.full_search(
            dispute_type=dispute_type,
            key_issue=key_issue
        )
        
        # 获取争议模式
        pattern = search_result["pattern"]
        
        # 生成报告
        report_lines = [
            f"# 调解建议报告",
            "",
            f"**争议类型**：{dispute_type}",
            f"**关键争议点**：{key_issue}",
            "",
            "---",
            "",
            "## 一、相关法条",
        ]
        
        if pattern and pattern.related_articles:
            for article in pattern.related_articles:
                report_lines.append(f"- {article}")
        else:
            report_lines.append("- 暂无内置法规信息，建议使用通义法睿检索")
        
        report_lines.extend([
            "",
            "## 二、类案参考",
        ])
        
        if search_result["cases"]:
            for i, case in enumerate(search_result["cases"], 1):
                report_lines.extend([
                    f"### 案例{i}：{case.title}",
                    f"- 法院：{case.court}",
                    f"- 裁判日期：{case.date}",
                    f"- 争议焦点：{case.key_issue}",
                    f"- 裁判结果：{case.ruling}",
                    f"- 裁判理由：{case.main_reason}",
                    "",
                ])
        else:
            report_lines.append("暂无类案信息")
        
        report_lines.extend([
            "## 三、调解建议",
        ])
        
        if pattern and pattern.mediation_tips:
            for tip in pattern.mediation_tips:
                report_lines.append(f"- {tip}")
        else:
            report_lines.append("- 建议结合具体案情分析")
        
        return "\n".join(report_lines)
    
    @staticmethod
    def _normalize_dispute_type(dispute_type: str) -> List[str]:
        """标准化争议类型关键词"""
        mapping = {
            "工程款": ["工程款", "付款", "支付"],
            "工期": ["工期", "延误", "顺延"],
            "质量": ["质量", "缺陷", "验收"],
            "签证": ["签证", "变更", "调价"],
        }
        
        keywords = []
        for key, values in mapping.items():
            if key in dispute_type:
                keywords.extend(values)
        
        return keywords if keywords else [dispute_type]


# ============================================================
# 便捷函数
# ============================================================

def search_similar_cases(dispute_type: str, key_issue: str = "", limit: int = 3) -> List[CaseSummary]:
    """快速类案检索"""
    retriever = CaseRetriever()
    return retriever.search_by_dispute_type(dispute_type, limit)


def get_mediation_advice(dispute_type: str, key_issue: str) -> str:
    """获取调解建议报告"""
    retriever = CaseRetriever()
    return retriever.generate_mediation_report(dispute_type, key_issue)


# ============================================================
# 使用示例
# ============================================================

if __name__ == "__main__":
    retriever = CaseRetriever()
    
    # 示例1：按争议类型检索
    print("=== 示例1：工程款纠纷类案检索 ===")
    cases = retriever.search_by_dispute_type("工程款纠纷")
    for case in cases:
        print(f"- {case.title} | {case.ruling[:30]}...")
    
    # 示例2：生成调解报告
    print("\n=== 示例2：调解建议报告 ===")
    report = get_mediation_advice("工期延误", "工期延误责任划分")
    print(report[:500] + "...")
    
    # 示例3：综合检索
    print("\n=== 示例3：综合检索 ===")
    result = retriever.full_search(
        dispute_type="工程款",
        key_issue="优先受偿权",
        amount_range=(1000000, 10000000)
    )
    print(f"找到 {result['case_count']} 个相关案例")