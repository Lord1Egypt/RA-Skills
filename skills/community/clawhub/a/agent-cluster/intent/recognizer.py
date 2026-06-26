"""
Intent Recognizer - 意图识别器

支持 5 大意图类型：
    INFORMATIONAL  - 信息查询
    OPERATIONAL     - 执行操作
    ANALYTICAL      - 数据分析
    CREATIVE        - 内容创作
    COLLABORATIVE   - 多Agent协作

功能：
    - 语义理解与意图分类
    - 置信度评估
    - 实体提取
    - 子任务候选提取
    - 降级到关键词匹配（无LLM时）

Change Log:
    2026-04-14: 初始版本，对标 QClaw 主Agent意图识别
"""

from __future__ import annotations

import re
import time
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

logger = logging.getLogger(__name__)


# =============================================================================
# 意图类型枚举
# =============================================================================

class IntentType(Enum):
    """意图分类体系"""
    INFORMATIONAL = "informational"   # 信息查询：查库存、查物流、查预算
    OPERATIONAL   = "operational"     # 执行操作：下单、补货、审批、发货
    ANALYTICAL    = "analytical"      # 数据分析：趋势分析、利润优化、库存预测
    CREATIVE      = "creative"        # 内容创作：生成报表、生成文档、生成PPT
    COLLABORATIVE = "collaborative"   # 多Agent协作：复杂任务需要多个专业Agent联动


# =============================================================================
# 数据模型
# =============================================================================

@dataclass
class Intent:
    """
    用户意图结构体

    Attributes:
        raw_input: 原始用户输入
        intent_type: 意图类型
        sub_intent: 子意图（辅助分类）
        entities: 提取的实体字典
        confidence: 置信度 [0.0, 1.0]
        required_agents: 需要调用的Agent列表
        sub_task_candidates: 子任务候选列表
        reasoning: 推理过程描述
        latency_ms: 识别耗时（毫秒）
    """
    raw_input: str
    intent_type: IntentType
    sub_intent: str = ""
    entities: dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    required_agents: list[str] = field(default_factory=list)
    sub_task_candidates: list[dict] = field(default_factory=list)
    reasoning: str = ""
    latency_ms: float = 0.0

    def to_dict(self) -> dict:
        return {
            "intent_type": self.intent_type.value,
            "sub_intent": self.sub_intent,
            "entities": self.entities,
            "confidence": round(self.confidence, 4),
            "required_agents": self.required_agents,
            "sub_task_candidates": self.sub_task_candidates,
            "reasoning": self.reasoning,
            "latency_ms": round(self.latency_ms, 2),
        }


@dataclass
class SubTask:
    """
    子任务结构体

    Attributes:
        task_id: 子任务唯一ID
        action: 操作名称
        description: 任务描述
        parameters: 任务参数
        depends_on: 依赖的子任务ID列表
        parallel_group: 并行组标识（同一组内可并行执行）
        priority: 优先级
        estimated_cost: 预估消耗
    """
    task_id: str
    action: str
    description: str
    parameters: dict = field(default_factory=dict)
    depends_on: list[str] = field(default_factory=list)
    parallel_group: Optional[str] = None
    priority: int = 50   # 0-100, 越高越优先
    estimated_cost: float = 1.0  # 相对消耗单位

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "action": self.action,
            "description": self.description,
            "parameters": self.parameters,
            "depends_on": self.depends_on,
            "parallel_group": self.parallel_group,
            "priority": self.priority,
            "estimated_cost": self.estimated_cost,
        }


# =============================================================================
# 意图识别器
# =============================================================================

class IntentRecognizer:
    """
    意图识别引擎

    使用混合策略（规则 + 语义向量 + 可选LLM）识别用户意图：

    Level 1: 关键词+正则规则匹配（始终可用）
    Level 2: 语义模式匹配（短语模板）
    Level 3: LLM调用（如配置了 API_KEY，可选）

    识别流程：
        1. 文本预处理（分词、去噪）
        2. 多策略并行识别
        3. 置信度融合
        4. 实体提取
        5. 子任务候选生成
    """

    # -------------------------------------------------------------------
    # 意图分类规则
    # -------------------------------------------------------------------

    INTENT_RULES: dict[str, dict] = {
        # ---- INFORMATIONAL ----
        "stock_query": {
            "intent_type": IntentType.INFORMATIONAL,
            "keywords": [
                "库存", "库存量", "还有多少", "查库存", "库存情况",
                "stock", "查一下库存", "有没有货", "缺货", "安全水位",
                "SKU001", "SKU002", "SKU003", "剩余", "当前库存",
            ],
            "pattern": r"(?:查询?|查|看)\s*(?:.*?的?\s*)?(?:库存|货|-stock)",
            "agents": ["inventory_agent"],
            "sub_intent": "库存查询",
        },
        "logistics_query": {
            "intent_type": IntentType.INFORMATIONAL,
            "keywords": [
                "物流", "运费", "配送", "快递", "追踪", "tracking",
                "物流查询", "到货", "发货", "运输", "路线", "时效",
            ],
            "pattern": r"(?:物流|运费|配送|快递|追踪|tracking|到货|发货)",
            "agents": ["logistics_agent"],
            "sub_intent": "物流查询",
        },
        "finance_query": {
            "intent_type": IntentType.INFORMATIONAL,
            "keywords": [
                "预算", "付款", "报销", "发票", "成本", "费用",
                "财务查询", "budget", "付款审核", "账期", "账单",
            ],
            "pattern": r"(?:预算|付款|报销|发票|成本|费用|财务|budget)",
            "agents": ["finance_agent"],
            "sub_intent": "财务查询",
        },
        "supplier_query": {
            "intent_type": IntentType.INFORMATIONAL,
            "keywords": [
                "供应商", "供应商查询", "supplier", "厂商", "采购渠道",
                "有哪些供应商", "合格供应商",
            ],
            "pattern": r"(?:供应商|supplier|厂商|采购渠道)",
            "agents": ["procurement_agent"],
            "sub_intent": "供应商查询",
        },

        # ---- OPERATIONAL ----
        "purchase_order": {
            "intent_type": IntentType.OPERATIONAL,
            "keywords": [
                "采购", "下单", "订货", "进货", "订购", "supplier",
                "采购订单", "向.*采购", "询价", "报价", "签订合同",
            ],
            "pattern": r"(?:采购|下单|订货|进货|订购|询价|报价|签订合同)",
            "agents": ["procurement_agent", "finance_agent"],
            "sub_intent": "采购下单",
        },
        "replenishment": {
            "intent_type": IntentType.OPERATIONAL,
            "keywords": [
                "补货", "补仓", "补库存", "补充库存", "补采",
                "触发补货", "安全库存", "自动补货",
            ],
            "pattern": r"(?:补货|补仓|补库存|补充库存|触发补货)",
            "agents": ["inventory_agent", "procurement_agent", "finance_agent"],
            "sub_intent": "库存补货",
        },
        "payment_approval": {
            "intent_type": IntentType.OPERATIONAL,
            "keywords": [
                "付款", "付款审核", "审批", "费用审批", "报销审批",
                "approve", "通过", "驳回",
            ],
            "pattern": r"(?:付款|审批|approve|通过|驳回)",
            "agents": ["finance_agent"],
            "sub_intent": "付款审批",
        },
        "shipping": {
            "intent_type": IntentType.OPERATIONAL,
            "keywords": [
                "发货", "安排发货", "发出", "出库", " shipment",
            ],
            "pattern": r"(?:发货|安排发货|发出|出库|shipment)",
            "agents": ["logistics_agent"],
            "sub_intent": "发货操作",
        },

        # ---- ANALYTICAL ----
        "stock_forecast": {
            "intent_type": IntentType.ANALYTICAL,
            "keywords": [
                "预测", "趋势", "forecast", "库存预测", "需求预测",
                "分析", "分析.*库存", "未来.*库存",
            ],
            "pattern": r"(?:预测|趋势|forecast|分析|未来)",
            "agents": ["inventory_agent"],
            "sub_intent": "库存预测分析",
        },
        "profit_optimization": {
            "intent_type": IntentType.ANALYTICAL,
            "keywords": [
                "利润", "盈利", "优化", "利润优化", "profit",
                "ACOS", "TACOS", "广告优化", "定价策略",
            ],
            "pattern": r"(?:利润|盈利|优化|profit|ACOS|TACOS|定价)",
            "agents": ["finance_agent"],
            "sub_intent": "利润分析优化",
        },
        "cost_analysis": {
            "intent_type": IntentType.ANALYTICAL,
            "keywords": [
                "成本分析", "费用分析", "成本结构", "cost",
                "降本", "节流", "节省成本",
            ],
            "pattern": r"(?:成本|费用|降本|节流|cost)",
            "agents": ["finance_agent"],
            "sub_intent": "成本分析",
        },
        "logistics_optimization": {
            "intent_type": IntentType.ANALYTICAL,
            "keywords": [
                "路线优化", "物流优化", "最优路线", "运费优化",
                "配送效率", "路径规划", "route.*optim",
            ],
            "pattern": r"(?:路线优化|物流优化|最优路线|路径规划)",
            "agents": ["logistics_agent"],
            "sub_intent": "物流优化分析",
        },

        # ---- CREATIVE ----
        "document_generation": {
            "intent_type": IntentType.CREATIVE,
            "keywords": [
                "文档", "报表", "工艺", "BOM", "工艺卡", "导出",
                "PDF", "报告", "申请单", "doc", "生成.*文档",
                "生成.*报表", "生成.*工艺",
            ],
            "pattern": r"(?:文档|报表|工艺|BOM|工艺卡|导出|PDF|报告|申请单|doc)",
            "agents": ["doc_agent"],
            "sub_intent": "文档生成",
        },
        "ppt_generation": {
            "intent_type": IntentType.CREATIVE,
            "keywords": [
                "PPT", "幻灯片", "演示", "presentation", "pptx",
                "生成PPT", "做PPT", "生成幻灯片",
            ],
            "pattern": r"(?:PPT|幻灯片|演示|presentation|pptx)",
            "agents": ["doc_agent"],
            "sub_intent": "PPT生成",
        },

        # ---- COLLABORATIVE ----
        "cross_department_workflow": {
            "intent_type": IntentType.COLLABORATIVE,
            "keywords": [
                "全程", "一体化", "端到端", "end.to.end",
                "帮我", "帮我.*采购", "帮我.*物流", "帮我.*库存",
                "全流程", "跨部门",
            ],
            "pattern": r"(?:全程|一体化|端到端|end.to.end|全流程|跨部门)",
            "agents": ["inventory_agent", "procurement_agent", "logistics_agent", "finance_agent"],
            "sub_intent": "跨部门协作",
        },
        "supplier_procurement_logistics": {
            "intent_type": IntentType.COLLABORATIVE,
            "keywords": [
                "采购.*物流", "供应商.*发货", "到货.*采购",
                "全程.*采购",
            ],
            "pattern": r"(?:采购.*物流|供应商.*发货|全程.*采购)",
            "agents": ["procurement_agent", "logistics_agent", "finance_agent"],
            "sub_intent": "采供销联动",
        },
    }

    # 实体提取正则
    ENTITY_PATTERNS: dict[str, tuple[str, str]] = {
        "sku":        (r"SKU\d{3}",                                  "SKU编号"),
        "sku_fuzzy":  (r"[A-Z]{2,3}-\d{3}",                          "SKU编号"),
        "supplier":   (r"SUP\d{3}",                                  "供应商编号"),
        "warehouse":  (r"华东仓|华北仓|华南仓|WH\d{3}|中心仓",        "仓库名称"),
        "amount":     (r"(\d+(?:\.\d+)?)\s*(?:万|千|元|件|套|箱)?",   "数量金额"),
        "priority":   (r"紧急|加急|urgent|急件",                    "优先级"),
        "date":       (r"\d{4}[-/]\d{1,2}[-/]\d{1,2}",               "日期"),
        "product":    (r"(?:轴承|电机|电缆|变压器|开关|阀门|泵).*?", "产品名称"),
        "region":     (r"(?:华东|华北|华南|华中|西南|西北|东北)",    "地区"),
    }

    # 复合意图信号词（触发 COLLABORATIVE）
    COLLABORATIVE_SIGNALS = [
        "帮我", "帮我查", "帮我做", "帮我执行", "帮我看看",
        "全程", "一体化", "端到端", "全流程",
    ]

    # 辅助意图（辅助识别主意图）
    AUX_INTENT_KEYWORDS = {
        "with_approval":  ["审批", "审核", "approve", "通过", "确认"],
        "with_analysis":  ["分析", "分析一下", "看看趋势", "预测一下"],
        "with_notification": ["通知", "提醒", "alert", "告警"],
        "with_export":    ["导出", "下载", "生成文件", "保存"],
    }

    def __init__(
        self,
        llm_provider: Optional[Any] = None,
        use_llm_fallback: bool = False,
    ):
        """
        初始化意图识别器

        Args:
            llm_provider: LLM提供者（如 OpenAI / Claude 客户端），可选
            use_llm_fallback: 当规则置信度 < threshold 时是否降级到LLM
        """
        self.llm_provider = llm_provider
        self.use_llm_fallback = use_llm_fallback
        self._stats = {"total": 0, "avg_confidence": 0.0}

    # -------------------------------------------------------------------
    # 主识别入口
    # -------------------------------------------------------------------

    def recognize(self, user_input: str) -> Intent:
        """
        识别用户意图

        Args:
            user_input: 用户自然语言输入

        Returns:
            Intent 对象
        """
        t0 = time.perf_counter()

        # Step 1: 规则匹配
        rule_intent, rule_score = self._rule_based_recognize(user_input)

        # Step 2: 辅助意图识别
        aux_intents = self._recognize_aux_intents(user_input)

        # Step 3: 实体提取
        entities = self._extract_entities(user_input)

        # Step 4: 子任务候选
        sub_task_candidates = self._generate_sub_task_candidates(
            rule_intent, entities, user_input
        )

        # Step 5: 置信度评估
        confidence = self._compute_confidence(rule_score, rule_intent, aux_intents)

        # Step 6: 推理过程
        reasoning = self._build_reasoning(rule_intent, rule_score, aux_intents, entities)

        intent = Intent(
            raw_input=user_input,
            intent_type=(rule_intent.get("intent_type") if rule_intent
                         else IntentType.INFORMATIONAL),
            sub_intent=(rule_intent.get("sub_intent", "") if rule_intent
                        else "通用查询"),
            entities=entities,
            confidence=confidence,
            required_agents=(rule_intent.get("agents", []) if rule_intent
                             else []),
            sub_task_candidates=sub_task_candidates,
            reasoning=reasoning,
            latency_ms=(time.perf_counter() - t0) * 1000,
        )

        # 更新统计
        self._update_stats(confidence)

        logger.info(
            f"[IntentRecognizer] input='{user_input[:40]}...' "
            f"→ type={intent.intent_type.value}, "
            f"sub_intent={intent.sub_intent}, "
            f"confidence={intent.confidence:.2%}, "
            f"latency={intent.latency_ms:.1f}ms"
        )

        return intent

    # -------------------------------------------------------------------
    # 规则匹配
    # -------------------------------------------------------------------

    def _rule_based_recognize(self, user_input: str) -> tuple[Optional[dict], float]:
        """基于规则的意图识别，返回(匹配的规则配置, 匹配分数)"""
        text_lower = user_input.lower()

        # --- 优先级1: CREATIVE 信号词（"PPT"/"幻灯片"/"文档"等）---
        # 短词优先检测，避免被 precision_signals 中的通用词覆盖
        if any(sig in text_lower for sig in ["ppt", "幻灯片", "演示", "presentation"]):
            config = self.INTENT_RULES["ppt_generation"]
            return {"name": "ppt_generation", **config, "agents": config["agents"]}, 2.5
        if any(sig in text_lower for sig in ["导出", "生成文档", "生成报表", "生成工艺",
                                               "生成BOM", "doc", "报表", "工艺", "BOM", "pdf"]):
            config = self.INTENT_RULES["document_generation"]
            return {"name": "document_generation", **config, "agents": config["agents"]}, 2.5

        # --- 优先级2: 精确关键词匹配（按特定性递减，列表保证顺序）---
        # 优先级: 协作复合词 > 分析复合词 > 创意复合词 > 操作词
        precision_signals = [
            # 协作类（最高优先）
            ("全程跟踪",            "cross_department_workflow"),
            ("全程处理",            "cross_department_workflow"),
            ("全程",                "cross_department_workflow"),
            ("端到端",              "cross_department_workflow"),
            ("全流程",              "cross_department_workflow"),
            ("采供销",              "supplier_procurement_logistics"),
            ("一体化",              "supplier_procurement_logistics"),
            # 分析类
            ("利润分析",            "profit_optimization"),
            ("盈利分析",            "profit_optimization"),
            ("利润优化",            "profit_optimization"),
            ("盈利优化",            "profit_optimization"),
            ("成本分析",            "cost_analysis"),
            ("成本结构",            "cost_analysis"),
            ("降本",                "cost_analysis"),
            ("路线优化",            "logistics_optimization"),
            ("物流优化",            "logistics_optimization"),
            ("路径规划",            "logistics_optimization"),
            ("物流路线",            "logistics_optimization"),
            ("分析",                "profit_optimization"),
            ("优化",                "profit_optimization"),
            ("预测",                "stock_forecast"),
            ("forecast",            "stock_forecast"),
            # 创意类
            ("生成BOM",             "document_generation"),
            ("生成工艺",            "document_generation"),
            ("生成报表",            "document_generation"),
            ("生成文档",            "document_generation"),
            ("导出PDF",             "document_generation"),
            # 操作类
            ("触发补货",            "replenishment"),
            ("补库存",              "replenishment"),
            ("补仓",                "replenishment"),
            ("补货",                "replenishment"),
            ("付款审核",            "payment_approval"),
            ("approve",             "payment_approval"),
            ("审批",                "payment_approval"),
            ("安排发货",            "shipping"),
            ("发货",                "shipping"),
            ("下单",                "purchase_order"),
            ("订货",                "purchase_order"),
            ("采购",                "purchase_order"),
            ("供应商",              "supplier_query"),
        ]
        for kw, rule_name in precision_signals:
            if kw in text_lower:
                config = self.INTENT_RULES.get(rule_name)
                if config:
                    return {"name": rule_name, **config, "agents": config["agents"]}, 2.0

        # --- 优先级3: 通用协作信号词（需要结合多动作词）---
        # "帮我"+具体动作词 才触发协作
        collab_action_words = ["看看", "搞定", "完成"]
        if any(sig in text_lower for sig in collab_action_words) and \
           any(kw in text_lower for kw in ["库存", "采购", "物流", "发货", "补货"]):
            config = self.INTENT_RULES["cross_department_workflow"]
            return {"name": "cross_department_workflow", **config, "agents": config["agents"]}, 1.5

        # --- 优先级4: 通用规则匹配（关键词+正则）---
        best_rule: Optional[dict] = None
        best_score = 0.0

        for rule_name, config in self.INTENT_RULES.items():
            score = 0.0

            # 关键词匹配
            for kw in config["keywords"]:
                if kw.lower() in text_lower:
                    score += 1.0

            # 正则匹配
            pattern = config.get("pattern", "")
            if pattern and re.search(pattern, user_input):
                score += 2.0  # 正则匹配权重更高

            if score > best_score:
                best_score = score
                best_rule = {
                    "name": rule_name,
                    **config,
                    "agents": config["agents"],
                }

        return best_rule, best_score

    def _recognize_aux_intents(self, user_input: str) -> list[str]:
        """识别辅助意图"""
        aux = []
        text_lower = user_input.lower()
        for aux_name, keywords in self.AUX_INTENT_KEYWORDS.items():
            if any(kw.lower() in text_lower for kw in keywords):
                aux.append(aux_name)
        return aux

    # -------------------------------------------------------------------
    # 实体提取
    # -------------------------------------------------------------------

    def _extract_entities(self, user_input: str) -> dict[str, Any]:
        """从用户输入中提取结构化实体"""
        entities: dict[str, Any] = {}

        for entity_name, (pattern, label) in self.ENTITY_PATTERNS.items():
            matches = re.findall(pattern, user_input, re.IGNORECASE)
            if matches:
                entities[entity_name] = matches if len(matches) > 1 else matches[0]

        # 金额换算
        amount_str = entities.get("amount", "")
        if isinstance(amount_str, str):
            try:
                val = float(re.search(r"\d+(?:\.\d+)?", amount_str).group())
                if "万" in user_input:
                    val *= 10000
                elif "千" in user_input:
                    val *= 1000
                entities["amount_value"] = val
            except (ValueError, AttributeError):
                pass

        # 优先级
        if any(kw in user_input for kw in ["紧急", "加急", "urgent"]):
            entities["priority"] = "high"

        return entities

    # -------------------------------------------------------------------
    # 子任务候选生成
    # -------------------------------------------------------------------

    def _generate_sub_task_candidates(
        self,
        rule: Optional[dict],
        entities: dict,
        user_input: str,
    ) -> list[dict]:
        """根据意图类型生成子任务候选"""
        candidates = []

        if not rule:
            return [{
                "action": "general_query",
                "description": "通用查询",
                "agents": ["inventory_agent"],
            }]

        sub_intent = rule.get("sub_intent", "")

        TASK_TEMPLATES: dict[str, list[dict]] = {
            "库存查询": [
                {"action": "query_stock", "description": "查询库存", "agents": ["inventory_agent"]},
            ],
            "物流查询": [
                {"action": "query_logistics", "description": "查询物流", "agents": ["logistics_agent"]},
            ],
            "财务查询": [
                {"action": "query_finance", "description": "查询财务", "agents": ["finance_agent"]},
            ],
            "采购下单": [
                {"action": "query_supplier", "description": "查询供应商", "agents": ["procurement_agent"]},
                {"action": "place_order", "description": "创建采购订单", "agents": ["procurement_agent"]},
                {"action": "approve_payment", "description": "财务审批", "agents": ["finance_agent"]},
            ],
            "库存补货": [
                {"action": "check_stock", "description": "检查库存", "agents": ["inventory_agent"]},
                {"action": "calc_replenishment", "description": "计算补货量", "agents": ["inventory_agent"]},
                {"action": "place_order", "description": "生成采购订单", "agents": ["procurement_agent"]},
                {"action": "approve_payment", "description": "财务审批", "agents": ["finance_agent"]},
            ],
            "付款审批": [
                {"action": "approve_payment", "description": "付款审批", "agents": ["finance_agent"]},
            ],
            "发货操作": [
                {"action": "shipping_notify", "description": "发货通知", "agents": ["logistics_agent"]},
            ],
            "文档生成": [
                {"action": "generate_document", "description": "生成文档", "agents": ["doc_agent"]},
                {"action": "export_pdf", "description": "导出PDF", "agents": ["doc_agent"]},
            ],
            "PPT生成": [
                {"action": "generate_ppt", "description": "生成PPT", "agents": ["doc_agent"]},
            ],
            "利润分析优化": [
                {"action": "analyze_profit", "description": "利润分析", "agents": ["finance_agent"]},
                {"action": "optimize_pricing", "description": "优化定价", "agents": ["finance_agent"]},
            ],
            "库存预测分析": [
                {"action": "forecast_stock", "description": "库存预测", "agents": ["inventory_agent"]},
                {"action": "trend_analysis", "description": "趋势分析", "agents": ["inventory_agent"]},
            ],
            "跨部门协作": [
                {"action": "check_stock", "description": "库存检查", "agents": ["inventory_agent"]},
                {"action": "place_order", "description": "采购下单", "agents": ["procurement_agent"]},
                {"action": "query_logistics", "description": "物流查询", "agents": ["logistics_agent"]},
                {"action": "approve_payment", "description": "财务审批", "agents": ["finance_agent"]},
            ],
            "采供销联动": [
                {"action": "query_supplier", "description": "供应商查询", "agents": ["procurement_agent"]},
                {"action": "place_order", "description": "采购下单", "agents": ["procurement_agent"]},
                {"action": "query_logistics", "description": "物流追踪", "agents": ["logistics_agent"]},
                {"action": "approve_payment", "description": "付款审核", "agents": ["finance_agent"]},
            ],
        }

        templates = TASK_TEMPLATES.get(sub_intent, [])
        for tmpl in templates:
            candidates.append(tmpl)

        return candidates

    # -------------------------------------------------------------------
    # 置信度评估
    # -------------------------------------------------------------------

    def _compute_confidence(
        self,
        rule_score: float,
        rule: Optional[dict],
        aux_intents: list[str],
    ) -> float:
        """
        计算最终置信度

        策略：
            - rule_score = 0  → 基础置信度 0.5
            - rule_score >= 3 → 置信度 >= 0.8（强匹配）
            - 有辅助意图     → 置信度 + 0.05
            - 上限 1.0
        """
        if rule_score == 0:
            base = 0.5
        elif rule_score <= 1:
            base = 0.6
        elif rule_score <= 2:
            base = 0.75
        else:
            base = min(0.85 + (rule_score - 3) * 0.05, 0.98)

        # 辅助意图加成
        bonus = len(aux_intents) * 0.05

        # 目标：意图识别准确率 > 80%，低置信度时应触发降级或追问
        confidence = min(base + bonus, 1.0)

        # 低置信度标记（< 0.6 需要追问或降级）
        if confidence < 0.6:
            logger.warning(f"[IntentRecognizer] 低置信度 {confidence:.2%}，建议追问用户")

        return confidence

    # -------------------------------------------------------------------
    # 推理过程构建
    # -------------------------------------------------------------------

    def _build_reasoning(
        self,
        rule: Optional[dict],
        rule_score: float,
        aux_intents: list[str],
        entities: dict,
    ) -> str:
        """生成推理过程描述"""
        parts = []

        if rule:
            parts.append(f"匹配规则: {rule['name']}（得分 {rule_score:.1f}）")
            parts.append(f"子意图: {rule.get('sub_intent', 'N/A')}）")
        else:
            parts.append("未匹配预设规则，使用默认通用查询")

        if aux_intents:
            parts.append(f"检测到辅助意图: {', '.join(aux_intents)}")

        if entities:
            entity_keys = list(entities.keys())[:4]
            parts.append(f"提取实体: {', '.join(entity_keys)}")

        return " | ".join(parts)

    # -------------------------------------------------------------------
    # 统计
    # -------------------------------------------------------------------

    def _update_stats(self, confidence: float) -> None:
        n = self._stats["total"]
        old_avg = self._stats["avg_confidence"]
        self._stats["total"] = n + 1
        self._stats["avg_confidence"] = (old_avg * n + confidence) / (n + 1)

    def get_stats(self) -> dict:
        return {
            **self._stats,
            "avg_confidence": round(self._stats["avg_confidence"], 4),
        }
