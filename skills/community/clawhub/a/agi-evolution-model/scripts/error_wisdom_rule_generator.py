#!/usr/bin/env python3
"""
错误智慧库规则自动生成模块 (Error Wisdom Rule Generator)

功能：
- 相似错误聚合：基于多维度相似度计算
- 共性模式识别：从离散错误中提取抽象模式
- 预防规则生成：自动生成可执行的预防规则
- 规则验证与优化：基于验证历史调整规则

基于：error_wisdom_spec.md 规范
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ==================== 数据结构 ====================

@dataclass
class SimilarityScore:
    """相似度得分"""
    error_type_match: float      # 错误类型匹配度
    subtype_match: float         # 子类型匹配度
    pattern_match: float         # 触发模式匹配度
    root_cause_match: float      # 根因匹配度
    overall_score: float         # 综合得分


@dataclass
class ErrorPattern:
    """错误模式"""
    pattern_id: str
    pattern_type: str            # error_type/subtype/trigger/root_cause
    pattern_description: str
    occurrences: int             # 出现次数
    related_errors: List[str]    # 关联错误ID
    common_features: Dict[str, Any]


@dataclass
class GeneratedRule:
    """生成的预防规则"""
    rule_id: str
    rule_name: str
    source_patterns: List[str]   # 来源模式ID
    source_errors: List[str]     # 来源错误ID（至少3个）
    trigger_condition: Dict[str, Any]
    check_logic: Dict[str, Any]
    prevention_action: Dict[str, Any]
    confidence: float
    auto_fixable: bool
    applicability: Dict[str, Any]
    generation_time: str


# ==================== 相似度计算器 ====================

class SimilarityCalculator:
    """
    错误相似度计算器
    
    基于多维度计算错误之间的相似度
    """
    
    # 维度权重
    WEIGHTS = {
        "error_type": 0.25,
        "subtype": 0.20,
        "trigger_pattern": 0.25,
        "root_cause": 0.30
    }
    
    @staticmethod
    def calculate(entry1: Dict, entry2: Dict) -> SimilarityScore:
        """
        计算两个错误条目的相似度
        
        Args:
            entry1: 错误条目1
            entry2: 错误条目2
        
        Returns:
            相似度得分
        """
        # 错误类型匹配
        type1 = entry1.get("错误发现", {}).get("错误类型", "")
        type2 = entry2.get("错误发现", {}).get("错误类型", "")
        type_match = 1.0 if type1 == type2 else 0.0
        
        # 子类型匹配
        subtype1 = entry1.get("错误发现", {}).get("子类型", "")
        subtype2 = entry2.get("错误发现", {}).get("子类型", "")
        subtype_match = 1.0 if subtype1 == subtype2 else 0.0
        
        # 触发模式匹配（基于场景关键词）
        scene1 = entry1.get("错误发现", {}).get("触发场景", "")
        scene2 = entry2.get("错误发现", {}).get("触发场景", "")
        pattern_match = SimilarityCalculator._text_similarity(scene1, scene2)
        
        # 根因匹配
        cause1 = entry1.get("原因分析", {}).get("根本原因", "")
        cause2 = entry2.get("原因分析", {}).get("根本原因", "")
        cause_match = SimilarityCalculator._text_similarity(cause1, cause2)
        
        # 综合得分
        overall = (
            type_match * SimilarityCalculator.WEIGHTS["error_type"] +
            subtype_match * SimilarityCalculator.WEIGHTS["subtype"] +
            pattern_match * SimilarityCalculator.WEIGHTS["trigger_pattern"] +
            cause_match * SimilarityCalculator.WEIGHTS["root_cause"]
        )
        
        return SimilarityScore(
            error_type_match=type_match,
            subtype_match=subtype_match,
            pattern_match=pattern_match,
            root_cause_match=cause_match,
            overall_score=overall
        )
    
    @staticmethod
    def _text_similarity(text1: str, text2: str) -> float:
        """
        文本相似度（基于词重叠）
        
        Args:
            text1: 文本1
            text2: 文本2
        
        Returns:
            相似度 0.0-1.0
        """
        if not text1 or not text2:
            return 0.0
        
        # 简单分词（按空格和标点）
        import re
        words1 = set(re.findall(r'\w+', text1.lower()))
        words2 = set(re.findall(r'\w+', text2.lower()))
        
        if not words1 or not words2:
            return 0.0
        
        # Jaccard相似度
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0


# ==================== 错误聚合器 ====================

class ErrorCluster:
    """
    错误聚类
    
    管理一组相似的错误
    """
    
    def __init__(self, cluster_id: str):
        self.cluster_id = cluster_id
        self.entries: List[Dict] = []
        self.entry_ids: List[str] = []
        self.common_features: Dict[str, Any] = {}
    
    def add_entry(self, entry_id: str, entry: Dict):
        """添加错误条目"""
        self.entries.append(entry)
        self.entry_ids.append(entry_id)
    
    def size(self) -> int:
        """返回聚类大小"""
        return len(self.entries)
    
    def can_generate_rule(self, min_size: int = 3) -> bool:
        """判断是否可以生成规则"""
        return self.size() >= min_size
    
    def extract_common_features(self) -> Dict[str, Any]:
        """提取共性特征"""
        if not self.entries:
            return {}
        
        common = {}
        
        # 检查错误类型是否一致
        types = [e.get("错误发现", {}).get("错误类型", "") for e in self.entries]
        if len(set(types)) == 1:
            common["错误类型"] = types[0]
        
        # 检查子类型是否一致
        subtypes = [e.get("错误发现", {}).get("子类型", "") for e in self.entries]
        if len(set(subtypes)) == 1:
            common["子类型"] = subtypes[0]
        
        # 统计触发场景关键词
        triggers = [e.get("错误发现", {}).get("触发场景", "") for e in self.entries]
        common["触发场景关键词"] = self._extract_common_keywords(triggers)
        
        # 统计根因关键词
        causes = [e.get("原因分析", {}).get("根本原因", "") for e in self.entries]
        common["根因关键词"] = self._extract_common_keywords(causes)
        
        # 统计预防策略关键词
        preventions = [e.get("预防知识", {}).get("预防策略", "") for e in self.entries]
        common["预防策略关键词"] = self._extract_common_keywords(preventions)
        
        self.common_features = common
        return common
    
    def _extract_common_keywords(self, texts: List[str], min_freq: int = 2) -> List[str]:
        """提取高频关键词"""
        import re
        from collections import Counter
        
        all_words = []
        for text in texts:
            words = re.findall(r'\w+', text.lower())
            all_words.extend(words)
        
        # 过滤停用词（简化版）
        stopwords = {"的", "是", "在", "和", "了", "有", "为", "以", "及", "等", "中"}
        filtered = [w for w in all_words if w not in stopwords and len(w) > 1]
        
        # 统计频率
        counter = Counter(filtered)
        return [word for word, freq in counter.most_common(5) if freq >= min_freq]


class ErrorAggregator:
    """
    错误聚合器
    
    将相似的错误聚合成簇
    """
    
    # 相似度阈值
    SIMILARITY_THRESHOLD = 0.60
    
    def __init__(self):
        self.clusters: Dict[str, ErrorCluster] = {}
        self.cluster_counter = 0
    
    def aggregate(self, entries: Dict[str, Dict]) -> Dict[str, ErrorCluster]:
        """
        执行错误聚合
        
        Args:
            entries: 错误条目字典 {entry_id: entry_data}
        
        Returns:
            聚类字典 {cluster_id: ErrorCluster}
        """
        self.clusters = {}
        self.cluster_counter = 0
        
        entry_list = list(entries.items())
        
        for entry_id, entry_data in entry_list:
            # 寻找最相似的现有聚类
            best_cluster = None
            best_similarity = 0.0
            
            for cluster_id, cluster in self.clusters.items():
                # 计算与聚类中心条目的相似度
                if cluster.entries:
                    similarity = SimilarityCalculator.calculate(
                        entry_data,
                        cluster.entries[0]  # 以第一个条目为代表
                    )
                    if similarity.overall_score > best_similarity:
                        best_similarity = similarity.overall_score
                        best_cluster = cluster_id
            
            # 如果相似度足够高，加入现有聚类
            if best_cluster and best_similarity >= self.SIMILARITY_THRESHOLD:
                self.clusters[best_cluster].add_entry(entry_id, entry_data)
            else:
                # 创建新聚类
                self.cluster_counter += 1
                new_cluster_id = f"cluster_{self.cluster_counter:04d}"
                new_cluster = ErrorCluster(new_cluster_id)
                new_cluster.add_entry(entry_id, entry_data)
                self.clusters[new_cluster_id] = new_cluster
        
        # 提取所有聚类的共性特征
        for cluster in self.clusters.values():
            cluster.extract_common_features()
        
        logger.info(f"Aggregated {len(entry_list)} entries into {len(self.clusters)} clusters")
        
        return self.clusters
    
    def get_rule_ready_clusters(self, min_size: int = 3) -> List[ErrorCluster]:
        """获取可以生成规则的聚类"""
        return [c for c in self.clusters.values() if c.can_generate_rule(min_size)]


# ==================== 规则生成器 ====================

class RuleGenerator:
    """
    预防规则生成器
    
    从错误聚类中生成可执行的预防规则
    """
    
    # 规则模板
    RULE_TEMPLATES = {
        "工具性错误": {
            "参数构造错误": {
                "rule_name": "参数验证规则",
                "trigger_pattern": "工具调用前",
                "check_type": "parameter_validation"
            },
            "调用失败类": {
                "rule_name": "调用容错规则",
                "trigger_pattern": "调用失败时",
                "check_type": "retry_fallback"
            },
            "结果处理类": {
                "rule_name": "结果解析规则",
                "trigger_pattern": "结果返回后",
                "check_type": "result_validation"
            }
        },
        "认知性错误": {
            "幻觉倾向": {
                "rule_name": "幻觉检测规则",
                "trigger_pattern": "响应生成后",
                "check_type": "hallucination_check"
            },
            "推理跳跃": {
                "rule_name": "推理完整性规则",
                "trigger_pattern": "推理过程中",
                "check_type": "reasoning_chain_check"
            },
            "知识缺失": {
                "rule_name": "知识边界规则",
                "trigger_pattern": "知识检索时",
                "check_type": "knowledge_boundary_check"
            },
            "偏见影响": {
                "rule_name": "偏见检测规则",
                "trigger_pattern": "输出生成后",
                "check_type": "bias_detection"
            }
        }
    }
    
    def __init__(self, memory_dir: str = "./agi_memory"):
        """
        初始化
        
        Args:
            memory_dir: 记忆存储目录
        """
        self.memory_dir = memory_dir
        self.generated_rules_file = os.path.join(
            memory_dir, "error_wisdom_generated_rules.json"
        )
        self.generated_rules = self._load_generated_rules()
    
    def _load_generated_rules(self) -> Dict[str, Any]:
        """加载已生成的规则"""
        if os.path.exists(self.generated_rules_file):
            try:
                with open(self.generated_rules_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load generated rules: {e}")
        
        return {"rules": {}, "metadata": {"total_generated": 0}}
    
    def _save_generated_rules(self):
        """保存生成的规则"""
        try:
            os.makedirs(os.path.dirname(self.generated_rules_file), exist_ok=True)
            with open(self.generated_rules_file, 'w', encoding='utf-8') as f:
                json.dump(self.generated_rules, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Failed to save generated rules: {e}")
    
    def generate_rule(
        self,
        cluster: ErrorCluster,
        timeliness_manager = None
    ) -> Optional[GeneratedRule]:
        """
        从错误聚类生成预防规则
        
        Args:
            cluster: 错误聚类
            timeliness_manager: 时效性管理器（可选）
        
        Returns:
            生成的规则，如果无法生成则返回None
        """
        if not cluster.can_generate_rule():
            return None
        
        features = cluster.common_features
        
        # 获取规则模板
        error_type = features.get("错误类型", "")
        subtype = features.get("子类型", "")
        
        template = self.RULE_TEMPLATES.get(error_type, {}).get(subtype, {})
        
        if not template:
            # 使用通用模板
            template = {
                "rule_name": "通用预防规则",
                "trigger_pattern": "执行前",
                "check_type": "generic_validation"
            }
        
        # 生成规则ID
        rule_id = f"rule_auto_{int(time.time()*1000)}"
        
        # 构建触发条件
        trigger_condition = self._build_trigger_condition(cluster)
        
        # 构建检查逻辑
        check_logic = self._build_check_logic(cluster)
        
        # 构建预防动作
        prevention_action = self._build_prevention_action(cluster)
        
        # 计算置信度
        confidence = self._calculate_rule_confidence(cluster)
        
        # 判断是否可自动修正
        auto_fixable = self._determine_auto_fixable(cluster)
        
        # 构建适用范围
        applicability = self._build_applicability(cluster)
        
        rule = GeneratedRule(
            rule_id=rule_id,
            rule_name=template.get("rule_name", "自动生成规则"),
            source_patterns=[cluster.cluster_id],
            source_errors=cluster.entry_ids,
            trigger_condition=trigger_condition,
            check_logic=check_logic,
            prevention_action=prevention_action,
            confidence=confidence,
            auto_fixable=auto_fixable,
            applicability=applicability,
            generation_time=datetime.now().isoformat()
        )
        
        return rule
    
    def _build_trigger_condition(self, cluster: ErrorCluster) -> Dict[str, Any]:
        """构建触发条件"""
        features = cluster.common_features
        
        return {
            "error_type": features.get("错误类型", "any"),
            "subtype": features.get("子类型", "any"),
            "trigger_keywords": features.get("触发场景关键词", []),
            "min_occurrences": cluster.size()
        }
    
    def _build_check_logic(self, cluster: ErrorCluster) -> Dict[str, Any]:
        """构建检查逻辑"""
        features = cluster.common_features
        
        return {
            "check_type": "pattern_match",
            "patterns_to_check": features.get("触发场景关键词", []),
            "root_cause_indicators": features.get("根因关键词", []),
            "check_depth": "standard"
        }
    
    def _build_prevention_action(self, cluster: ErrorCluster) -> Dict[str, Any]:
        """构建预防动作"""
        features = cluster.common_features
        prevention_keywords = features.get("预防策略关键词", [])
        
        return {
            "action_type": "warn_and_suggest",
            "suggestions": prevention_keywords[:3],
            "fallback_strategy": "ask_user_confirmation",
            "log_level": "warning"
        }
    
    def _calculate_rule_confidence(self, cluster: ErrorCluster) -> float:
        """计算规则置信度"""
        # 基础置信度：聚类大小
        size_factor = min(1.0, cluster.size() / 5.0)  # 5个以上达到饱和
        
        # 特征一致性：共性特征越多越可信
        feature_factor = len(cluster.common_features) / 5.0
        
        # 综合置信度
        confidence = 0.5 + 0.3 * size_factor + 0.2 * min(1.0, feature_factor)
        
        return min(0.95, confidence)
    
    def _determine_auto_fixable(self, cluster: ErrorCluster) -> bool:
        """判断是否可自动修正"""
        error_type = cluster.common_features.get("错误类型", "")
        subtype = cluster.common_features.get("子类型", "")
        
        # 工具性错误中的参数构造错误通常可自动修正
        if error_type == "工具性错误" and subtype == "参数构造错误":
            return True
        
        return False
    
    def _build_applicability(self, cluster: ErrorCluster) -> Dict[str, Any]:
        """构建适用范围"""
        return {
            "error_types": [cluster.common_features.get("错误类型", "any")],
            "subtypes": [cluster.common_features.get("子类型", "any")],
            "contexts": cluster.common_features.get("触发场景关键词", [])[:5],
            "exclusions": []
        }
    
    def save_rule(self, rule: GeneratedRule):
        """保存生成的规则"""
        self.generated_rules["rules"][rule.rule_id] = asdict(rule)
        self.generated_rules["metadata"]["total_generated"] = \
            len(self.generated_rules["rules"])
        self._save_generated_rules()
        
        logger.info(f"Rule saved: {rule.rule_id} from {len(rule.source_errors)} errors")
    
    def generate_rules_from_clusters(
        self,
        clusters: List[ErrorCluster],
        timeliness_manager = None
    ) -> List[GeneratedRule]:
        """
        从多个聚类批量生成规则
        
        Args:
            clusters: 错误聚类列表
            timeliness_manager: 时效性管理器
        
        Returns:
            生成的规则列表
        """
        generated_rules = []
        
        for cluster in clusters:
            rule = self.generate_rule(cluster, timeliness_manager)
            if rule:
                self.save_rule(rule)
                generated_rules.append(rule)
        
        logger.info(f"Generated {len(generated_rules)} rules from {len(clusters)} clusters")
        
        return generated_rules
    
    def get_all_rules(self) -> Dict[str, Any]:
        """获取所有生成的规则"""
        return self.generated_rules["rules"]
    
    def get_rule(self, rule_id: str) -> Optional[Dict]:
        """获取特定规则"""
        return self.generated_rules["rules"].get(rule_id)


# ==================== 规则生成管理器 ====================

class RuleGenerationManager:
    """
    规则生成管理器
    
    协调错误聚合、模式识别和规则生成的完整流程
    """
    
    def __init__(self, memory_dir: str = "./agi_memory", timeliness_manager=None):
        """
        初始化
        
        Args:
            memory_dir: 记忆存储目录
            timeliness_manager: 时效性管理器
        """
        self.memory_dir = memory_dir
        self.timeliness_manager = timeliness_manager
        
        self.aggregator = ErrorAggregator()
        self.generator = RuleGenerator(memory_dir)
    
    def run_generation_pipeline(
        self,
        entries: Dict[str, Dict],
        min_cluster_size: int = 3
    ) -> Dict[str, Any]:
        """
        运行完整的规则生成流水线
        
        Args:
            entries: 错误智慧库条目
            min_cluster_size: 最小聚类大小
        
        Returns:
            生成报告
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_entries": len(entries),
            "clusters_formed": 0,
            "clusters_rule_ready": 0,
            "rules_generated": 0,
            "rules": []
        }
        
        # Step 1: 聚合错误
        clusters = self.aggregator.aggregate(entries)
        report["clusters_formed"] = len(clusters)
        
        # Step 2: 筛选可生成规则的聚类
        rule_ready_clusters = self.aggregator.get_rule_ready_clusters(min_cluster_size)
        report["clusters_rule_ready"] = len(rule_ready_clusters)
        
        # Step 3: 生成规则
        generated_rules = self.generator.generate_rules_from_clusters(
            rule_ready_clusters,
            self.timeliness_manager
        )
        report["rules_generated"] = len(generated_rules)
        report["rules"] = [
            {
                "rule_id": r.rule_id,
                "rule_name": r.rule_name,
                "confidence": r.confidence,
                "source_errors_count": len(r.source_errors)
            }
            for r in generated_rules
        ]
        
        logger.info(f"Rule generation pipeline completed: {report['rules_generated']} rules generated")
        
        return report


# ==================== 命令行接口 ====================

def main():
    """命令行测试接口"""
    print("=== 错误智慧库规则自动生成模块（测试模式） ===\n")
    
    # 创建模拟数据
    test_entries = {
        "ew_001": {
            "错误发现": {
                "错误类型": "工具性错误",
                "子类型": "参数构造错误",
                "触发场景": "调用天气API时使用无效温度单位"
            },
            "原因分析": {
                "根本原因": "枚举参数未验证"
            },
            "预防知识": {
                "预防策略": "调用前验证枚举参数"
            }
        },
        "ew_002": {
            "错误发现": {
                "错误类型": "工具性错误",
                "子类型": "参数构造错误",
                "触发场景": "调用日历API时日期格式错误"
            },
            "原因分析": {
                "根本原因": "日期格式未标准化"
            },
            "预防知识": {
                "预防策略": "调用前标准化日期格式"
            }
        },
        "ew_003": {
            "错误发现": {
                "错误类型": "工具性错误",
                "子类型": "参数构造错误",
                "触发场景": "调用翻译API时语言代码错误"
            },
            "原因分析": {
                "根本原因": "参数格式未验证"
            },
            "预防知识": {
                "预防策略": "调用前验证参数格式"
            }
        },
        "ew_004": {
            "错误发现": {
                "错误类型": "认知性错误",
                "子类型": "幻觉倾向",
                "触发场景": "回答问题时虚构API函数"
            },
            "原因分析": {
                "根本原因": "未验证API存在性"
            },
            "预防知识": {
                "预防策略": "提及API前验证其存在"
            }
        },
        "ew_005": {
            "错误发现": {
                "错误类型": "认知性错误",
                "子类型": "幻觉倾向",
                "触发场景": "生成代码时虚构库函数"
            },
            "原因分析": {
                "根本原因": "未验证函数存在性"
            },
            "预防知识": {
                "预防策略": "引用函数前验证其存在"
            }
        }
    }
    
    manager = RuleGenerationManager("./agi_memory")
    
    # 测试1：错误聚合
    print("测试1：错误聚合")
    report = manager.run_generation_pipeline(test_entries, min_cluster_size=2)
    print(f"  总条目数: {report['total_entries']}")
    print(f"  形成聚类: {report['clusters_formed']}")
    print(f"  可生成规则聚类: {report['clusters_rule_ready']}")
    print(f"  生成规则数: {report['rules_generated']}\n")
    
    # 测试2：相似度计算
    print("测试2：相似度计算")
    similarity = SimilarityCalculator.calculate(test_entries["ew_001"], test_entries["ew_002"])
    print(f"  ew_001 vs ew_002:")
    print(f"    类型匹配: {similarity.error_type_match:.2f}")
    print(f"    子类型匹配: {similarity.subtype_match:.2f}")
    print(f"    触发模式匹配: {similarity.pattern_match:.2f}")
    print(f"    根因匹配: {similarity.root_cause_match:.2f}")
    print(f"    综合得分: {similarity.overall_score:.2f}\n")
    
    # 测试3：生成的规则
    print("测试3：生成的规则")
    for rule_info in report["rules"]:
        print(f"  规则ID: {rule_info['rule_id']}")
        print(f"    名称: {rule_info['rule_name']}")
        print(f"    置信度: {rule_info['confidence']:.3f}")
        print(f"    来源错误数: {rule_info['source_errors_count']}\n")
    
    print("=== 所有测试完成 ===")


if __name__ == "__main__":
    main()
