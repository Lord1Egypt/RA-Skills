#!/usr/bin/env python3
"""
认知性错误分析器 (Cognitive Error Analyzer)

功能：
- 认知性错误识别与分类
- 根因分析（认知维度、情境维度、系统维度）
- 预防建议生成
- 与元认知检测集成
- 与错误智慧库联动

基于：error_wisdom_spec.md 规范
"""

import os
import json
import time
import re
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from collections import defaultdict


# ==================== 数据结构 ====================

@dataclass
class CognitiveDimension:
    """认知维度分析"""
    知识缺陷: str = ""  # 完全不知道/知道但不完整/知道但记错/无
    推理偏差: str = ""  # 过度推断/遗漏前提/逻辑跳跃/无
    注意力分配: str = ""  # 忽略关键信息/过度关注次要信息/正常
    记忆干扰: str = ""  # 近期干扰/相似干扰/无


@dataclass
class ContextDimension:
    """情境维度分析"""
    任务复杂性: str = "中等"  # 简单/中等/复杂
    信息完整性: str = "部分缺失"  # 充足/部分缺失/严重缺失
    时间压力: str = "适中"  # 宽松/适中/紧迫
    任务类型: str = "通用"  # 技术/创意/决策/通用


@dataclass
class SystemDimension:
    """系统维度分析"""
    人格特质影响: str = ""  # 谨慎型/激进型/平衡型
    学习阶段影响: str = ""  # 新手期/成长期/熟练期
    资源约束影响: str = ""  # 算力限制/上下文窗口限制/无
    上下文干扰: str = ""  # 前文干扰/主题切换/无


@dataclass
class CognitiveErrorAnalysis:
    """认知性错误分析结果"""
    错误类型: str  # 幻觉倾向类/推理跳跃类/知识缺失类/偏见影响类
    错误子类型: str
    错误描述: str
    严重程度: str  # mild/moderate/severe/critical
    
    认知维度: Optional[CognitiveDimension] = None
    情境维度: Optional[ContextDimension] = None
    系统维度: Optional[SystemDimension] = None
    
    根本原因: str = ""
    可预防性: str = "medium"  # high/medium/low
    
    预防建议: List[str] = field(default_factory=list)
    改进方向: List[str] = field(default_factory=list)


# ==================== 认知性错误模式库 ====================

class CognitiveErrorPatterns:
    """认知性错误模式库"""
    
    # 幻觉倾向模式
    HALLUCINATION_PATTERNS = {
        "虚构事实": {
            "keywords": ["编造", "虚构", "不存在", "imaginary", "fabricated"],
            "severity": "severe",
            "cause": "模型过度生成，缺乏事实验证",
            "prevention": ["增加事实核查步骤", "降低生成温度", "引用可信来源"]
        },
        "虚构API": {
            "keywords": ["API", "函数", "方法", "parameter", "method"],
            "patterns": [r"调用\s+\w+\s*\(.*\)", r"\w+\.api\."],
            "severity": "moderate",
            "cause": "知识混合，未验证API存在性",
            "prevention": ["API存在性验证", "查阅官方文档", "版本匹配检查"]
        },
        "虚构引用": {
            "keywords": ["根据", "引用", "研究显示", "文献"],
            "patterns": [r"根据.*研究", r"文献.*显示"],
            "severity": "moderate",
            "cause": "知识库中无确切来源，模型自行生成引用",
            "prevention": ["引用真实性验证", "标注来源不确定"]
        }
    }
    
    # 推理跳跃模式
    REASONING_JUMP_PATTERNS = {
        "遗漏前提": {
            "indicators": ["因此", "所以", "得出结论", "由此可见"],
            "severity": "moderate",
            "cause": "省略中间推理步骤，直接得出结论",
            "prevention": ["显式列出推理前提", "逐步推导", "前提验证"]
        },
        "逻辑跳跃": {
            "indicators": ["显然", "不难看出", "理所当然"],
            "severity": "mild",
            "cause": "假设听众已知中间逻辑，省略关键步骤",
            "prevention": ["补充中间推理", "避免过度假设", "显式连接"]
        },
        "因果误判": {
            "patterns": [r".*导致.*", r".*因为.*", r".*原因是.*"],
            "severity": "moderate",
            "cause": "错误建立因果关系，混淆相关与因果",
            "prevention": ["因果链验证", "排除他因", "相关性分析"]
        }
    }
    
    # 知识缺失模式
    KNOWLEDGE_GAP_PATTERNS = {
        "完全不知道": {
            "indicators": ["我不确定", "我不清楚", "没有相关信息"],
            "severity": "mild",
            "cause": "知识库中确实缺乏相关信息",
            "prevention": ["坦诚承认知识边界", "建议查询外部资源"]
        },
        "知道但不完整": {
            "indicators": ["可能", "大概", "似乎", "我记得"],
            "severity": "mild",
            "cause": "知识存在但不完整或有遗漏",
            "prevention": ["明确标注不确定性", "建议用户验证"]
        },
        "知道但记错": {
            "indicators": ["错误信息", "与事实不符"],
            "severity": "moderate",
            "cause": "记忆混淆，新旧知识冲突",
            "prevention": ["关键信息二次验证", "多源交叉验证"]
        }
    }
    
    # 偏见影响模式
    BIAS_PATTERNS = {
        "刻板印象": {
            "indicators": ["总是", "从来", "所有人都", "典型的"],
            "severity": "moderate",
            "cause": "过度泛化，忽视个体差异",
            "prevention": ["避免绝对化表述", "考虑例外情况", "个体化分析"]
        },
        "选择性注意": {
            "indicators": ["忽略", "只考虑", "片面"],
            "severity": "mild",
            "cause": "注意力集中在部分信息，忽略其他",
            "prevention": ["多角度分析", "主动寻找反例", "全面审查"]
        },
        "确认偏误": {
            "indicators": ["验证", "支持", "证明我的观点"],
            "severity": "mild",
            "cause": "只寻找支持已有观点的证据",
            "prevention": ["主动寻找反驳证据", "中立立场", "假设检验"]
        }
    }


# ==================== 认知性错误分析器 ====================

class CognitiveErrorAnalyzer:
    """
    认知性错误分析器
    
    负责：
    - 识别和分类认知性错误
    - 多维度根因分析
    - 生成预防建议
    - 与错误智慧库联动
    """
    
    def __init__(self, memory_dir: str = "./agi_memory"):
        """
        初始化
        
        Args:
            memory_dir: 记忆存储目录
        """
        self.memory_dir = memory_dir
        self.patterns = CognitiveErrorPatterns()
        
        # 错误类型到模式的映射
        self.error_type_patterns = {
            "幻觉倾向类": self.patterns.HALLUCINATION_PATTERNS,
            "推理跳跃类": self.patterns.REASONING_JUMP_PATTERNS,
            "知识缺失类": self.patterns.KNOWLEDGE_GAP_PATTERNS,
            "偏见影响类": self.patterns.BIAS_PATTERNS
        }
    
    def analyze(
        self,
        response: str,
        context: dict = None,
        objectivity_metrics: dict = None,
        personality: dict = None,
        learning_stage: str = "成长期"
    ) -> CognitiveErrorAnalysis:
        """
        分析认知性错误
        
        Args:
            response: 智能体响应内容
            context: 上下文信息
            objectivity_metrics: 客观性评估指标（来自元认知检测）
            personality: 人格配置
            learning_stage: 学习阶段
        
        Returns:
            认知性错误分析结果
        """
        # 1. 错误识别
        error_type, error_subtype, error_desc = self._identify_error(
            response, objectivity_metrics
        )
        
        if not error_type:
            # 无认知性错误
            return CognitiveErrorAnalysis(
                错误类型="无",
                错误子类型="无",
                错误描述="未检测到显著认知性错误",
                严重程度="none"
            )
        
        # 2. 严重程度评估
        severity = self._assess_severity(error_type, error_subtype, objectivity_metrics)
        
        # 3. 多维度根因分析
        cognitive_dim = self._analyze_cognitive_dimension(
            response, error_type, error_subtype, objectivity_metrics
        )
        context_dim = self._analyze_context_dimension(context)
        system_dim = self._analyze_system_dimension(personality, learning_stage)
        
        # 4. 综合根本原因
        root_cause = self._synthesize_root_cause(
            cognitive_dim, context_dim, system_dim, error_type
        )
        
        # 5. 可预防性评估
        preventability = self._assess_preventability(error_type, severity)
        
        # 6. 生成预防建议
        prevention_suggestions = self._generate_prevention_suggestions(
            error_type, error_subtype, cognitive_dim, context_dim
        )
        
        # 7. 改进方向
        improvement_directions = self._generate_improvement_directions(
            error_type, cognitive_dim, system_dim
        )
        
        return CognitiveErrorAnalysis(
            错误类型=error_type,
            错误子类型=error_subtype,
            错误描述=error_desc,
            严重程度=severity,
            认知维度=cognitive_dim,
            情境维度=context_dim,
            系统维度=system_dim,
            根本原因=root_cause,
            可预防性=preventability,
            预防建议=prevention_suggestions,
            改进方向=improvement_directions
        )
    
    def _identify_error(
        self,
        response: str,
        objectivity_metrics: dict
    ) -> Tuple[str, str, str]:
        """
        识别错误类型
        
        Returns:
            (错误类型, 错误子类型, 错误描述)
        """
        # 如果有客观性评估结果，优先使用
        if objectivity_metrics:
            subjectivity_dims = objectivity_metrics.get("subjectivity_dimensions", {})
            
            # 幻觉检测
            if subjectivity_dims.get("hallucination", 0) > 0.5:
                return "幻觉倾向类", "虚构事实", "检测到幻觉倾向，可能包含虚构信息"
            
            # 推测性检测
            if subjectivity_dims.get("speculation", 0) > 0.6:
                return "推理跳跃类", "过度推断", "推测性过高，可能存在逻辑跳跃"
            
            # 假设性检测
            if subjectivity_dims.get("assumption", 0) > 0.6:
                return "推理跳跃类", "遗漏前提", "基于过多假设，前提可能不完整"
        
        # 基于模式匹配识别
        response_lower = response.lower()
        
        for error_type, patterns in self.error_type_patterns.items():
            for subtype, pattern_info in patterns.items():
                # 关键词匹配
                keywords = pattern_info.get("keywords", [])
                if any(kw in response_lower for kw in keywords):
                    return error_type, subtype, f"检测到{error_type}模式：{subtype}"
                
                # 正则模式匹配
                regex_patterns = pattern_info.get("patterns", [])
                for pattern in regex_patterns:
                    if re.search(pattern, response, re.IGNORECASE):
                        return error_type, subtype, f"检测到{error_type}模式：{subtype}"
        
        # 无显著错误
        return None, None, None
    
    def _assess_severity(
        self,
        error_type: str,
        error_subtype: str,
        objectivity_metrics: dict
    ) -> str:
        """评估严重程度"""
        # 基于错误类型的基础严重程度
        base_severity = {
            "幻觉倾向类": "severe",
            "推理跳跃类": "moderate",
            "知识缺失类": "mild",
            "偏见影响类": "mild"
        }
        
        severity = base_severity.get(error_type, "mild")
        
        # 根据客观性指标调整
        if objectivity_metrics:
            gap = objectivity_metrics.get("gap", 0)
            if gap > 0.4:
                # 适切性差距大，提升严重程度
                severity_map = {"mild": "moderate", "moderate": "severe", "severe": "critical"}
                severity = severity_map.get(severity, severity)
        
        return severity
    
    def _analyze_cognitive_dimension(
        self,
        response: str,
        error_type: str,
        error_subtype: str,
        objectivity_metrics: dict
    ) -> CognitiveDimension:
        """分析认知维度"""
        dim = CognitiveDimension()
        
        # 知识缺陷分析
        if error_type == "知识缺失类":
            if "不确定" in response or "不清楚" in response:
                dim.知识缺陷 = "完全不知道"
            elif "可能" in response or "大概" in response:
                dim.知识缺陷 = "知道但不完整"
            else:
                dim.知识缺陷 = "知道但记错"
        else:
            dim.知识缺陷 = "无"
        
        # 推理偏差分析
        if error_type == "推理跳跃类":
            if error_subtype == "过度推断":
                dim.推理偏差 = "过度推断"
            elif error_subtype == "遗漏前提":
                dim.推理偏差 = "遗漏前提"
            else:
                dim.推理偏差 = "逻辑跳跃"
        else:
            dim.推理偏差 = "无"
        
        # 注意力分配分析
        if error_type == "偏见影响类":
            if error_subtype == "选择性注意":
                dim.注意力分配 = "忽略关键信息"
            else:
                dim.注意力分配 = "过度关注次要信息"
        else:
            dim.注意力分配 = "正常"
        
        # 记忆干扰分析（基于幻觉类型）
        if error_type == "幻觉倾向类":
            dim.记忆干扰 = "相似干扰"
        else:
            dim.记忆干扰 = "无"
        
        return dim
    
    def _analyze_context_dimension(self, context: dict) -> ContextDimension:
        """分析情境维度"""
        dim = ContextDimension()
        
        if not context:
            return dim
        
        # 任务复杂性
        dim.任务复杂性 = context.get("complexity", "中等")
        
        # 信息完整性
        dim.信息完整性 = context.get("information_completeness", "部分缺失")
        
        # 时间压力
        dim.时间压力 = context.get("time_pressure", "适中")
        
        # 任务类型
        dim.任务类型 = context.get("task_type", "通用")
        
        return dim
    
    def _analyze_system_dimension(
        self,
        personality: dict,
        learning_stage: str
    ) -> SystemDimension:
        """分析系统维度"""
        dim = SystemDimension()
        
        # 人格特质影响
        if personality:
            # 基于人格向量判断
            caution = personality.get("caution", 0.5)
            if caution > 0.7:
                dim.人格特质影响 = "谨慎型"
            elif caution < 0.3:
                dim.人格特质影响 = "激进型"
            else:
                dim.人格特质影响 = "平衡型"
        
        # 学习阶段影响
        dim.学习阶段影响 = learning_stage
        
        # 资源约束影响（暂时设为无）
        dim.资源约束影响 = "无"
        
        # 上下文干扰（暂时设为无）
        dim.上下文干扰 = "无"
        
        return dim
    
    def _synthesize_root_cause(
        self,
        cognitive_dim: CognitiveDimension,
        context_dim: ContextDimension,
        system_dim: SystemDimension,
        error_type: str
    ) -> str:
        """综合根本原因"""
        causes = []
        
        # 认知维度原因
        if cognitive_dim.知识缺陷 != "无":
            causes.append(f"知识层面：{cognitive_dim.知识缺陷}")
        
        if cognitive_dim.推理偏差 != "无":
            causes.append(f"推理层面：{cognitive_dim.推理偏差}")
        
        if cognitive_dim.注意力分配 != "正常":
            causes.append(f"注意力层面：{cognitive_dim.注意力分配}")
        
        if cognitive_dim.记忆干扰 != "无":
            causes.append(f"记忆层面：{cognitive_dim.记忆干扰}")
        
        # 情境维度原因
        if context_dim.信息完整性 in ["部分缺失", "严重缺失"]:
            causes.append(f"信息层面：{context_dim.信息完整性}")
        
        if context_dim.时间压力 == "紧迫":
            causes.append("时间压力导致分析不充分")
        
        # 系统维度原因
        if system_dim.学习阶段影响 == "新手期":
            causes.append("新手期经验不足")
        
        if system_dim.人格特质影响 == "激进型" and error_type == "幻觉倾向类":
            causes.append("激进型人格易产生过度生成")
        
        if not causes:
            return "未明确识别根本原因"
        
        return "；".join(causes)
    
    def _assess_preventability(self, error_type: str, severity: str) -> str:
        """评估可预防性"""
        # 幻觉类较难预防（需要模型改进）
        if error_type == "幻觉倾向类":
            if severity in ["severe", "critical"]:
                return "low"
            return "medium"
        
        # 偏见类需要长期调整
        if error_type == "偏见影响类":
            return "medium"
        
        # 推理和知识类相对容易预防
        return "high"
    
    def _generate_prevention_suggestions(
        self,
        error_type: str,
        error_subtype: str,
        cognitive_dim: CognitiveDimension,
        context_dim: ContextDimension
    ) -> List[str]:
        """生成预防建议"""
        suggestions = []
        
        # 从模式库获取基础建议
        if error_type in self.error_type_patterns:
            patterns = self.error_type_patterns[error_type]
            if error_subtype in patterns:
                base_suggestions = patterns[error_subtype].get("prevention", [])
                suggestions.extend(base_suggestions)
        
        # 基于认知维度补充建议
        if cognitive_dim.知识缺陷 != "无":
            suggestions.append("明确标注知识边界和不确定性")
            suggestions.append("建议用户通过外部资源验证")
        
        if cognitive_dim.推理偏差 != "无":
            suggestions.append("显式展示推理步骤和前提")
            suggestions.append("在关键推理点进行自我验证")
        
        if cognitive_dim.注意力分配 != "normal":
            suggestions.append("主动寻找被忽略的关键信息")
            suggestions.append("进行多角度分析")
        
        # 基于情境维度补充建议
        if context_dim.信息完整性 in ["部分缺失", "严重缺失"]:
            suggestions.append("明确告知用户信息缺失情况")
            suggestions.append("请求补充必要信息")
        
        if context_dim.时间压力 == "紧迫":
            suggestions.append("在时间压力下优先保证关键信息的准确性")
        
        return list(set(suggestions))  # 去重
    
    def _generate_improvement_directions(
        self,
        error_type: str,
        cognitive_dim: CognitiveDimension,
        system_dim: SystemDimension
    ) -> List[str]:
        """生成改进方向"""
        directions = []
        
        # 基于错误类型
        if error_type == "幻觉倾向类":
            directions.append("加强事实验证机制")
            directions.append("优化生成温度参数")
        
        if error_type == "推理跳跃类":
            directions.append("完善推理链显式化")
            directions.append("增加前提验证步骤")
        
        if error_type == "知识缺失类":
            directions.append("扩充知识库覆盖范围")
            directions.append("建立知识边界识别机制")
        
        if error_type == "偏见影响类":
            directions.append("增加偏见检测模块")
            directions.append("建立多元化视角")
        
        # 基于系统维度
        if system_dim.学习阶段影响 == "新手期":
            directions.append("通过更多交互积累经验")
            directions.append("参考成熟案例进行学习")
        
        return directions
    
    def to_error_wisdom_entry(
        self,
        analysis: CognitiveErrorAnalysis,
        trace_id: str,
        response: str = ""
    ) -> dict:
        """
        转换为错误智慧库条目格式
        
        Args:
            analysis: 认知性错误分析结果
            trace_id: 追踪ID
            response: 响应内容（可选）
        
        Returns:
            错误智慧库条目字典
        """
        if analysis.错误类型 == "无":
            return None
        
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        entry = {
            "id": f"ew_{datetime.utcnow().strftime('%Y%m%d')}_{int(time.time()*1000)%1000000:06d}",
            "timestamp": timestamp,
            "trace_id": trace_id,
            "version": "1.0",
            
            "错误发现": {
                "错误类型": "认知性错误",
                "子类型": f"{analysis.错误类型}-{analysis.错误子类型}",
                "错误码": f"COG_{analysis.错误类型[:2].upper()}_{analysis.错误子类型[:2].upper()}",
                "错误描述": analysis.错误描述,
                "严重程度": analysis.严重程度,
                "触发场景": "元认知检测触发",
                "影响范围": "响应质量"
            },
            
            "原因分析": {
                "根本原因": analysis.根本原因,
                "认知维度": asdict(analysis.认知维度) if analysis.认知维度 else {},
                "情境维度": asdict(analysis.情境维度) if analysis.情境维度 else {},
                "系统维度": asdict(analysis.系统维度) if analysis.系统维度 else {},
                "可预防性": analysis.可预防性
            },
            
            "解决方案": {
                "即时纠错": "触发自我纠错流程",
                "纠错成本": "medium",
                "有效性": "待验证",
                "预防建议": analysis.预防建议
            },
            
            "预防知识": {
                "预防策略": "；".join(analysis.预防建议[:3]) if analysis.预防建议 else "",
                "改进方向": analysis.改进方向,
                "适用场景": ["认知性错误预防"],
                "预防优先级": "medium" if analysis.可预防性 == "high" else "low",
                "预防成本": "medium"
            },
            
            "验证历史": [],
            
            "关联错误": {
                "相似错误ID": [],
                "共性模式": analysis.错误类型,
                "抽象规则ID": ""
            },
            
            "元数据": {
                "创建时间": timestamp,
                "最后更新": timestamp,
                "验证次数": 0,
                "成功预防次数": 0,
                "置信度": 0.7,
                "时效性标记": "active",
                "响应片段": response[:500] if response else ""
            }
        }
        
        return entry


# ==================== 便捷函数 ====================

def analyze_cognitive_error(
    response: str,
    context: dict = None,
    objectivity_metrics: dict = None,
    memory_dir: str = "./agi_memory"
) -> CognitiveErrorAnalysis:
    """
    分析认知性错误（便捷函数）
    
    Args:
        response: 智能体响应内容
        context: 上下文信息
        objectivity_metrics: 客观性评估指标
        memory_dir: 记忆存储目录
    
    Returns:
        认知性错误分析结果
    """
    analyzer = CognitiveErrorAnalyzer(memory_dir)
    return analyzer.analyze(response, context, objectivity_metrics)


# ==================== CLI 接口 ====================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="认知性错误分析器")
    parser.add_argument("--memory-dir", default="./agi_memory", help="记忆存储目录")
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # analyze 命令
    analyze_parser = subparsers.add_parser("analyze", help="分析认知性错误")
    analyze_parser.add_argument("--response", required=True, help="响应内容")
    analyze_parser.add_argument("--context", help="上下文（JSON格式）")
    analyze_parser.add_argument("--objectivity", help="客观性指标（JSON格式）")
    
    # test 命令
    subparsers.add_parser("test", help="运行测试案例")
    
    args = parser.parse_args()
    
    analyzer = CognitiveErrorAnalyzer(args.memory_dir)
    
    if args.command == "analyze":
        context = json.loads(args.context) if args.context else None
        objectivity = json.loads(args.objectivity) if args.objectivity else None
        
        result = analyzer.analyze(args.response, context, objectivity)
        
        print("=== 认知性错误分析结果 ===\n")
        print(f"错误类型: {result.错误类型}")
        print(f"错误子类型: {result.错误子类型}")
        print(f"严重程度: {result.严重程度}")
        print(f"根本原因: {result.根本原因}")
        print(f"可预防性: {result.可预防性}")
        print(f"\n预防建议:")
        for i, suggestion in enumerate(result.预防建议, 1):
            print(f"  {i}. {suggestion}")
    
    elif args.command == "test":
        # 测试案例
        test_cases = [
            {
                "response": "根据最近的研究显示，每天喝三杯咖啡可以有效预防癌症。",
                "description": "虚构引用测试"
            },
            {
                "response": "这个项目失败的原因肯定是团队不努力，因为他们从来都不认真对待任务。",
                "description": "刻板印象测试"
            },
            {
                "response": "这个数据显然是错误的，所以结论也不成立。",
                "description": "推理跳跃测试"
            }
        ]
        
        for i, case in enumerate(test_cases, 1):
            print(f"\n--- 测试案例 {i}: {case['description']} ---")
            result = analyzer.analyze(case["response"])
            print(f"错误类型: {result.错误类型}")
            print(f"错误子类型: {result.错误子类型}")
            print(f"严重程度: {result.严重程度}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
