#!/usr/bin/env python3
"""
Agent化身控制器
让Agent真正主导大模型调用，如臂驱使
- 真人思维模式
- 上下文完全隔离
- 智能意图理解
- 自主决策框架
"""

import os
import json
import logging
import asyncio
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import hashlib
import uuid
from queue import Queue
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IntentType(Enum):
    CODE_GENERATION = "code_generation"
    ARCHITECTURE_DESIGN = "architecture_design"
    PRD_GENERRATION = "prd_generation"
    TECH_CONSULTATION = "tech_consultation"
    DEBUG_ANALYSIS = "debug_analysis"
    KNOWLEDGE_QUERY = "knowledge_query"
    PROJECT_PLANNING = "project_planning"
    CODE_REVIEW = "code_review"

class ContextScope(Enum):
    ISOLATED = "isolated"
    SHARED = "shared"
    PERSISTENT = "persistent"

@dataclass
class UserIntent:
    """用户意图解析结果"""
    raw_input: str
    intent_type: IntentType
    core_question: str
    constraints: Dict[str, Any]
    expected_output: str
    urgency: int = 5
    context_needed: bool = True

@dataclass
class ThinkingStep:
    """思维步骤"""
    step_name: str
    reasoning: str
    decision: str
    confidence: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class ContextSpace:
    """隔离的上下文空间"""
    space_id: str
    task_id: str
    created_at: str
    data: Dict[str, Any]
    memory_refs: List[str]
    is_active: bool = True
    parent_space: Optional[str] = None

class ContextManager:
    """上下文管理器 - 确保完全隔离"""
    
    def __init__(self, max_spaces: int = 100):
        self.spaces: Dict[str, ContextSpace] = {}
        self.active_space: Optional[str] = None
        self.max_spaces = max_spaces
        self._lock = threading.RLock()
    
    def create_space(self, task_id: str, parent: Optional[str] = None) -> str:
        """创建新的隔离上下文空间"""
        with self._lock:
            space_id = f"ctx_{uuid.uuid4().hex[:8]}"
            
            space = ContextSpace(
                space_id=space_id,
                task_id=task_id,
                created_at=datetime.now().isoformat(),
                data={},
                memory_refs=[],
                parent_space=parent
            )
            
            self.spaces[space_id] = space
            self.active_space = space_id
            
            if len(self.spaces) > self.max_spaces:
                self._cleanup_old_spaces()
            
            logger.info(f"创建上下文空间: {space_id} for task: {task_id}")
            return space_id
    
    def get_space(self, space_id: str) -> Optional[ContextSpace]:
        with self._lock:
            return self.spaces.get(space_id)
    
    def write_to_space(self, space_id: str, key: str, value: Any):
        """写入上下文（完全隔离）"""
        with self._lock:
            if space_id in self.spaces:
                self.spaces[space_id].data[key] = value
                logger.debug(f"写入上下文: {space_id}.{key}")
    
    def read_from_space(self, space_id: str, key: str) -> Optional[Any]:
        """读取上下文"""
        with self._lock:
            space = self.spaces.get(space_id)
            if space and key in space.data:
                return space.data[key]
            if space and space.parent_space:
                return self.read_from_space(space.parent_space, key)
            return None
    
    def close_space(self, space_id: str):
        """关闭上下文空间"""
        with self._lock:
            if space_id in self.spaces:
                self.spaces[space_id].is_active = False
                logger.info(f"关闭上下文空间: {space_id}")
    
    def _cleanup_old_spaces(self):
        """清理旧空间"""
        inactive = [s for s in self.spaces.values() if not s.is_active]
        for space in inactive[:len(inactive)//2]:
            del self.spaces[space.space_id]

class ThinkingEngine:
    """真人思维引擎"""
    
    def __init__(self):
        self.thinking_history: List[ThinkingStep] = []
        self.decision_patterns = self._load_decision_patterns()
    
    def _load_decision_patterns(self) -> Dict:
        """加载决策模式 - 蒸馏自顶级架构师"""
        return {
            "problem_analysis": {
                "steps": ["理解本质", "识别约束", "分解问题", "优先级排序"],
                "questions": [
                    "用户真正想要解决什么问题？",
                    "有什么技术和资源限制？",
                    "问题可以分解成哪些子问题？",
                    "哪些部分最关键？"
                ]
            },
            "solution_design": {
                "steps": ["方案构思", "对比分析", "风险评估", "最优选择"],
                "questions": [
                    "有哪些可行的解决方案？",
                    "各方案的优缺点是什么？",
                    "每个方案有什么风险？",
                    "综合考虑哪个方案最优？"
                ]
            },
            "implementation": {
                "steps": ["架构设计", "技术选型", "实现规划", "验证方案"],
                "questions": [
                    "系统架构应该如何设计？",
                    "选择什么技术栈？",
                    "如何分阶段实现？",
                    "如何验证正确性？"
                ]
            }
        }
    
    def think(self, intent: UserIntent) -> List[ThinkingStep]:
        """按照真人思维模式思考"""
        steps = []
        
        analysis_pattern = self.decision_patterns["problem_analysis"]
        for i, step_name in enumerate(analysis_pattern["steps"]):
            step = ThinkingStep(
                step_name=step_name,
                reasoning=self._reason_about(intent, i),
                decision=self._make_decision(intent, step_name),
                confidence=self._calculate_confidence(intent, i)
            )
            steps.append(step)
            self.thinking_history.append(step)
        
        return steps
    
    def _reason_about(self, intent: UserIntent, step_index: int) -> str:
        """推理过程"""
        reasonings = {
            0: f"分析用户输入: {intent.raw_input[:100]}... 核心问题是: {intent.core_question}",
            1: f"识别到的约束条件: {json.dumps(intent.constraints, ensure_ascii=False)}",
            2: f"将问题分解为: {intent.intent_type.value} 类型的任务",
            3: f"根据紧急程度 {intent.urgency}/10 确定处理优先级"
        }
        return reasonings.get(step_index, "继续分析...")
    
    def _make_decision(self, intent: UserIntent, step_name: str) -> str:
        """做出决策"""
        decisions = {
            "理解本质": f"确定核心需求: {intent.core_question}",
            "识别约束": f"应用约束: {list(intent.constraints.keys())}",
            "分解问题": f"任务类型: {intent.intent_type.value}",
            "优先级排序": f"优先级: {intent.urgency}/10"
        }
        return decisions.get(step_name, "决策中...")
    
    def _calculate_confidence(self, intent: UserIntent, step_index: int) -> float:
        """计算置信度"""
        base_confidence = 0.8
        if intent.constraints:
            base_confidence += 0.05
        if intent.expected_output:
            base_confidence += 0.05
        return min(base_confidence + step_index * 0.02, 0.98)

class IntentParser:
    """意图解析器 - 听懂人话"""
    
    def __init__(self):
        self.intent_keywords = {
            IntentType.CODE_GENERATION: ["写代码", "生成代码", "实现", "编程", "code", "function"],
            IntentType.ARCHITECTURE_DESIGN: ["架构", "设计", "系统设计", "架构设计", "architecture"],
            IntentType.PRD_GENERRATION: ["PRD", "需求文档", "产品需求", "prd"],
            IntentType.TECH_CONSULTATION: ["咨询", "建议", "推荐", "选型", "怎么选"],
            IntentType.DEBUG_ANALYSIS: ["报错", "错误", "bug", "问题", "调试", "debug"],
            IntentType.KNOWLEDGE_QUERY: ["什么是", "解释", "介绍", "讲解", "查询"],
            IntentType.PROJECT_PLANNING: ["规划", "计划", "排期", "里程碑", "项目"],
            IntentType.CODE_REVIEW: ["审查", "review", "检查代码", "代码质量"]
        }
    
    def parse(self, user_input: str, context: Optional[Dict] = None) -> UserIntent:
        """解析用户意图"""
        intent_type = self._classify_intent(user_input)
        core_question = self._extract_core_question(user_input)
        constraints = self._extract_constraints(user_input, context)
        expected_output = self._infer_expected_output(intent_type)
        urgency = self._assess_urgency(user_input)
        
        return UserIntent(
            raw_input=user_input,
            intent_type=intent_type,
            core_question=core_question,
            constraints=constraints,
            expected_output=expected_output,
            urgency=urgency
        )
    
    def _classify_intent(self, text: str) -> IntentType:
        """分类意图"""
        text_lower = text.lower()
        for intent_type, keywords in self.intent_keywords.items():
            if any(kw in text_lower for kw in keywords):
                return intent_type
        return IntentType.TECH_CONSULTATION
    
    def _extract_core_question(self, text: str) -> str:
        """提取核心问题"""
        question_markers = ["帮我", "请", "需要", "想要", "如何", "怎么"]
        for marker in question_markers:
            if marker in text:
                parts = text.split(marker, 1)
                if len(parts) > 1:
                    return parts[1].strip()
        return text
    
    def _extract_constraints(self, text: str, context: Optional[Dict]) -> Dict:
        """提取约束条件"""
        constraints = {}
        
        tech_keywords = ["React", "Vue", "Python", "Go", "Node", "Java", "TypeScript"]
        for tech in tech_keywords:
            if tech.lower() in text.lower():
                constraints["tech_stack"] = constraints.get("tech_stack", [])
                constraints["tech_stack"].append(tech)
        
        scale_keywords = ["高并发", "分布式", "微服务", "单体", "小型", "大型"]
        for scale in scale_keywords:
            if scale in text:
                constraints["scale"] = scale
        
        if context:
            constraints.update({k: v for k, v in context.items() if v is not None})
        
        return constraints
    
    def _infer_expected_output(self, intent_type: IntentType) -> str:
        """推断期望输出"""
        outputs = {
            IntentType.CODE_GENERATION: "可运行的代码",
            IntentType.ARCHITECTURE_DESIGN: "架构设计文档",
            IntentType.PRD_GENERRATION: "PRD文档",
            IntentType.TECH_CONSULTATION: "专业建议",
            IntentType.DEBUG_ANALYSIS: "问题分析和解决方案",
            IntentType.KNOWLEDGE_QUERY: "详细解释",
            IntentType.PROJECT_PLANNING: "项目计划",
            IntentType.CODE_REVIEW: "代码审查报告"
        }
        return outputs.get(intent_type, "专业回答")
    
    def _assess_urgency(self, text: str) -> int:
        """评估紧急程度"""
        high_urgency = ["紧急", "立刻", "马上", " ASAP", "急"]
        low_urgency = ["有空", "不急", "慢慢", "有时间"]
        
        if any(kw in text for kw in high_urgency):
            return 9
        if any(kw in text for kw in low_urgency):
            return 3
        return 5

class ModelOrchestrator:
    """大模型编排器 - Agent主导调用"""
    
    def __init__(self):
        self.model_configs = {
            "openai": {"strengths": ["快速响应", "通用任务"], "cost": "medium"},
            "claude": {"strengths": ["代码质量", "推理能力", "长文本"], "cost": "high"},
            "gemini": {"strengths": ["多模态", "文档生成"], "cost": "low"},
            "local": {"strengths": ["隐私", "离线"], "cost": "free"}
        }
        self.call_history: List[Dict] = []
    
    def select_model(self, intent: UserIntent) -> str:
        """智能选择最优模型"""
        model_scores = {"claude": 0, "openai": 0, "gemini": 0, "local": 0}
        
        if intent.intent_type == IntentType.CODE_GENERATION:
            model_scores["claude"] += 3
        elif intent.intent_type == IntentType.ARCHITECTURE_DESIGN:
            model_scores["claude"] += 2
            model_scores["openai"] += 1
        elif intent.intent_type == IntentType.KNOWLEDGE_QUERY:
            model_scores["gemini"] += 2
            model_scores["openai"] += 1
        
        if intent.urgency >= 8:
            model_scores["openai"] += 2
        
        if len(intent.raw_input) > 5000:
            model_scores["claude"] += 2
        
        return max(model_scores, key=model_scores.get)
    
    def build_prompt(self, intent: UserIntent, thinking_steps: List[ThinkingStep]) -> str:
        """构建提示词"""
        prompt_parts = [
            f"【任务类型】{intent.intent_type.value}",
            f"【核心问题】{intent.core_question}",
            f"【约束条件】{json.dumps(intent.constraints, ensure_ascii=False)}",
            f"【期望输出】{intent.expected_output}",
            "",
            "【思维过程】"
        ]
        
        for step in thinking_steps:
            prompt_parts.append(f"- {step.step_name}: {step.decision} (置信度: {step.confidence:.0%})")
        
        prompt_parts.extend([
            "",
            "请按照上述思维过程，给出专业、详细的回答。"
        ])
        
        return "\n".join(prompt_parts)
    
    def record_call(self, model: str, prompt: str, response: str, success: bool):
        """记录调用历史"""
        self.call_history.append({
            "model": model,
            "prompt_hash": hashlib.md5(prompt.encode()).hexdigest()[:8],
            "response_length": len(response),
            "success": success,
            "timestamp": datetime.now().isoformat()
        })

class AvatarController:
    """Agent化身控制器 - 核心类"""
    
    def __init__(self, name: str = "架构师"):
        self.name = name
        self.context_manager = ContextManager()
        self.thinking_engine = ThinkingEngine()
        self.intent_parser = IntentParser()
        self.model_orchestrator = ModelOrchestrator()
        
        self.current_task_id: Optional[str] = None
        self.current_space_id: Optional[str] = None
        self.task_queue: Queue = Queue()
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        self.personality = {
            "name": name,
            "tone": "专业严谨",
            "style": "结构化表达",
            "values": ["质量", "效率", "可维护性"]
        }
    
    def understand(self, user_input: str, context: Optional[Dict] = None) -> UserIntent:
        """理解用户意图"""
        logger.info(f"[{self.name}] 正在理解用户输入...")
        intent = self.intent_parser.parse(user_input, context)
        logger.info(f"[{self.name}] 意图识别: {intent.intent_type.value}")
        return intent
    
    def think(self, intent: UserIntent) -> List[ThinkingStep]:
        """真人思维过程"""
        logger.info(f"[{self.name}] 正在思考...")
        steps = self.thinking_engine.think(intent)
        for step in steps:
            logger.info(f"[{self.name}] {step.step_name}: {step.decision}")
        return steps
    
    def decide(self, intent: UserIntent, thinking_steps: List[ThinkingStep]) -> Dict:
        """做出决策"""
        selected_model = self.model_orchestrator.select_model(intent)
        prompt = self.model_orchestrator.build_prompt(intent, thinking_steps)
        
        decision = {
            "selected_model": selected_model,
            "prompt": prompt,
            "reasoning": f"基于任务类型 {intent.intent_type.value} 和紧急程度 {intent.urgency}/10",
            "confidence": sum(s.confidence for s in thinking_steps) / len(thinking_steps)
        }
        
        logger.info(f"[{self.name}] 决策: 使用 {selected_model} 模型")
        return decision
    
    def execute(self, decision: Dict, platform_adapter: Optional[Any] = None) -> str:
        """执行决策"""
        logger.info(f"[{self.name}] 正在执行...")
        
        if platform_adapter:
            try:
                response = platform_adapter.generate(decision["prompt"])
                self.model_orchestrator.record_call(
                    decision["selected_model"],
                    decision["prompt"],
                    response,
                    success=True
                )
                return response
            except Exception as e:
                logger.error(f"[{self.name}] 执行失败: {str(e)}")
                return f"执行出错: {str(e)}"
        
        return f"[{self.name}] 模拟执行: {decision['selected_model']}"
    
    def think_and_execute(self, user_input: str, context: Optional[Dict] = None, 
                          platform_adapter: Optional[Any] = None) -> Dict[str, Any]:
        """完整的思考-执行流程"""
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        self.current_task_id = task_id
        
        self.current_space_id = self.context_manager.create_space(task_id)
        
        self.context_manager.write_to_space(
            self.current_space_id, 
            "user_input", 
            user_input
        )
        
        intent = self.understand(user_input, context)
        self.context_manager.write_to_space(
            self.current_space_id, 
            "intent", 
            intent.__dict__
        )
        
        thinking_steps = self.think(intent)
        self.context_manager.write_to_space(
            self.current_space_id, 
            "thinking_steps", 
            [s.__dict__ for s in thinking_steps]
        )
        
        decision = self.decide(intent, thinking_steps)
        self.context_manager.write_to_space(
            self.current_space_id, 
            "decision", 
            decision
        )
        
        response = self.execute(decision, platform_adapter)
        self.context_manager.write_to_space(
            self.current_space_id, 
            "response", 
            response
        )
        
        self.context_manager.close_space(self.current_space_id)
        
        return {
            "task_id": task_id,
            "intent": intent.intent_type.value,
            "thinking": [s.step_name for s in thinking_steps],
            "model": decision["selected_model"],
            "confidence": decision["confidence"],
            "response": response
        }
    
    def get_status(self) -> Dict:
        """获取当前状态"""
        return {
            "name": self.name,
            "current_task": self.current_task_id,
            "active_context": self.current_space_id,
            "total_contexts": len(self.context_manager.spaces),
            "thinking_history": len(self.thinking_engine.thinking_history),
            "model_calls": len(self.model_orchestrator.call_history)
        }

class AvatarManager:
    """化身管理器 - 管理多个Agent化身"""
    
    def __init__(self):
        self.avatars: Dict[str, AvatarController] = {}
        self._lock = threading.RLock()
    
    def create_avatar(self, name: str, personality: Optional[Dict] = None) -> AvatarController:
        """创建新的Agent化身"""
        with self._lock:
            avatar = AvatarController(name)
            if personality:
                avatar.personality.update(personality)
            self.avatars[name] = avatar
            logger.info(f"创建Agent化身: {name}")
            return avatar
    
    def get_avatar(self, name: str) -> Optional[AvatarController]:
        """获取Agent化身"""
        return self.avatars.get(name)
    
    def list_avatars(self) -> List[str]:
        """列出所有化身"""
        return list(self.avatars.keys())
    
    def dispatch_task(self, task: str, avatar_name: Optional[str] = None) -> Dict:
        """分发任务到合适的化身"""
        if avatar_name and avatar_name in self.avatars:
            return self.avatars[avatar_name].think_and_execute(task)
        
        for avatar in self.avatars.values():
            if not avatar.current_task_id:
                return avatar.think_and_execute(task)
        
        default_avatar = list(self.avatars.values())[0] if self.avatars else AvatarController()
        return default_avatar.think_and_execute(task)

if __name__ == "__main__":
    print("="*60)
    print("Agent化身控制器测试")
    print("="*60)
    
    avatar = AvatarController("架构师小明")
    
    print("\n【测试1: 理解用户意图】")
    intent = avatar.understand("帮我用React设计一个高并发的电商秒杀系统")
    print(f"   意图类型: {intent.intent_type.value}")
    print(f"   核心问题: {intent.core_question}")
    print(f"   约束条件: {intent.constraints}")
    
    print("\n【测试2: 真人思维过程】")
    steps = avatar.think(intent)
    for step in steps:
        print(f"   {step.step_name}: {step.decision} ({step.confidence:.0%})")
    
    print("\n【测试3: 智能决策】")
    decision = avatar.decide(intent, steps)
    print(f"   选择模型: {decision['selected_model']}")
    print(f"   决策理由: {decision['reasoning']}")
    
    print("\n【测试4: 完整流程】")
    result = avatar.think_and_execute("设计一个用户认证系统，要求安全可靠")
    print(f"   任务ID: {result['task_id']}")
    print(f"   意图: {result['intent']}")
    print(f"   思维步骤: {result['thinking']}")
    print(f"   选择模型: {result['model']}")
    print(f"   置信度: {result['confidence']:.0%}")
    
    print("\n【测试5: 化身状态】")
    print(avatar.get_status())
    
    print("\n" + "="*60)
    print("Agent化身控制器测试完成 ✅")
    print("="*60)
