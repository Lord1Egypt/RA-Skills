"""
认知力增强引擎（高性能优化版）
为AI Agent提供记忆、规划、推理、反思与元认知能力
"""
from __future__ import annotations
import hashlib
import heapq
import math
import re
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Deque, Dict, List, Optional, Set, Tuple, Union


# ======================= 分词器 =======================

class Tokenizer:
    """统一分词工具（中英文基础）"""
    @staticmethod
    def tokenize(text: str) -> List[str]:
        if not text:
            return []
        text = text.lower()
        words = re.findall(r"[a-zA-Z0-9\u4e00-\u9fa5]+", text)
        return [w for w in words if len(w) > 1 or w.isdigit()]


# ======================= 长期记忆（高性能向量检索）=======================

class VectorMemory:
    """
    基于TF-IDF和倒排索引的长期记忆存储
    - 添加时预处理tokens并预计算向量范数
    - 检索时仅扫描包含查询中任一token的候选记忆，大幅加速
    """
    def __init__(self, capacity: int = 1000, similarity_threshold: float = 0.15):
        self.capacity = capacity
        self.similarity_threshold = similarity_threshold
        self.memories: Dict[str, Dict] = {}  # id -> {content, metadata, importance, tokens, norm, ts, access}
        self.inverted_index: Dict[str, Set[str]] = defaultdict(set)
        self._idf_dirty = True
        self._idf_cache: Dict[str, float] = {}
        self.tokenizer = Tokenizer()

    def add(self, content: str, metadata: Optional[Dict] = None, importance: float = 1.0) -> str:
        """添加记忆，返回唯一标识"""
        if not content or not content.strip():
            raise ValueError("Memory content cannot be empty")
        if metadata is None:
            metadata = {}
        mem_id = hashlib.md5(f"{content}{time.time()}{id(self)}".encode()).hexdigest()[:12]

        token_list = self.tokenizer.tokenize(content)
        token_set = set(token_list)
        if not token_set:
            raise ValueError("Memory content has no valid tokens")

        if len(self.memories) >= self.capacity:
            self._evict()

        self.memories[mem_id] = {
            "content": content,
            "metadata": metadata,
            "importance": min(1.0, max(0.0, importance)),
            "timestamp": time.time(),
            "access_count": 0,
            "tokens": token_list,
            "norm": 0.0,  # 延迟计算（依赖于idf）
        }

        for token in token_set:
            self.inverted_index[token].add(mem_id)
        self._idf_dirty = True
        return mem_id

    def get(self, mem_id: str) -> Optional[Dict]:
        mem = self.memories.get(mem_id)
        if mem:
            mem["access_count"] += 1
        return mem

    def retrieve(self, query: str, top_k: int = 5) -> List[Tuple[Dict, float]]:
        """检索相似记忆，返回 (记忆内容, 相似度) 列表"""
        if not self.memories:
            return []

        query_tokens = set(self.tokenizer.tokenize(query))
        if not query_tokens:
            return []

        # 使用倒排索引缩小候选集：至少包含一个查询token的记忆
        candidate_ids = set()
        for token in query_tokens:
            candidate_ids.update(self.inverted_index.get(token, set()))
        if not candidate_ids:
            return []

        # 更新IDF并计算各记忆的范数（惰性计算）
        idf = self._get_idf()
        query_vec = {tok: idf.get(tok, 0.0) for tok in query_tokens}
        query_norm = math.sqrt(sum(v * v for v in query_vec.values()))

        scores = []
        for mem_id in candidate_ids:
            mem = self.memories[mem_id]
            # 计算该记忆的向量（基于当前idf）和范数
            mem_vec = {tok: idf.get(tok, 0.0) for tok in mem["tokens"]}
            if mem["norm"] == 0.0:
                mem["norm"] = math.sqrt(sum(v * v for v in mem_vec.values()))
            norm_mem = mem["norm"]
            if norm_mem == 0.0:
                continue

            # 余弦相似度
            dot = sum(query_vec.get(tok, 0.0) * mem_vec.get(tok, 0.0) for tok in set(query_vec) & set(mem_vec))
            raw_sim = dot / (query_norm * norm_mem) if query_norm > 0 else 0.0

            # 综合重要性与访问热度
            adjusted = raw_sim * (0.7 + 0.3 * mem["importance"]) * (0.9 + 0.1 * math.log(mem["access_count"] + 1))
            if adjusted > self.similarity_threshold:
                scores.append((mem, adjusted))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def _get_idf(self) -> Dict[str, float]:
        if not self._idf_dirty and self._idf_cache:
            return self._idf_cache
        n = len(self.memories)
        idf = {}
        for token, docs in self.inverted_index.items():
            idf[token] = math.log((n + 1) / (len(docs) + 1)) + 1
        self._idf_cache = idf
        self._idf_dirty = False
        return idf

    def _evict(self):
        """淘汰最不重要的记忆（基于重要性、访问次数、时效）"""
        if not self.memories:
            return
        now = time.time()
        scored = []
        for mem_id, mem in self.memories.items():
            age = now - mem["timestamp"]
            score = mem["importance"] * (mem["access_count"] + 1) / (age + 1)
            scored.append((score, mem_id))
        heapq.heapify(scored)
        _, worst_id = heapq.heappop(scored)
        self._remove(worst_id)

    def _remove(self, mem_id: str):
        if mem_id not in self.memories:
            return
        mem = self.memories[mem_id]
        for token in set(mem["tokens"]):
            docs = self.inverted_index.get(token)
            if docs:
                docs.discard(mem_id)
                if not docs:
                    del self.inverted_index[token]
        del self.memories[mem_id]
        self._idf_dirty = True


# ======================= 工作记忆 =======================

class WorkingMemory:
    """短期上下文（FIFO）"""
    def __init__(self, capacity: int = 20):
        self.buffer: Deque[Dict] = deque(maxlen=capacity)

    def add(self, item: Dict):
        self.buffer.append(item)

    def get_recent(self, n: int = 10) -> List[Dict]:
        return list(self.buffer)[-n:]

    def clear(self):
        self.buffer.clear()


# ======================= 规划器 =======================

@dataclass
class PlanStep:
    description: str
    dependencies: List[int] = field(default_factory=list)
    status: str = "pending"  # pending, running, done, failed


class Planner:
    """将目标分解为可执行步骤，支持自定义分解器"""

    DEFAULT_KEYWORDS = {
        "calculate": ["calculate", "compute", "solve", "math"],
        "search": ["search", "find", "lookup", "query"],
        "summarize": ["summarize", "summary", "abstract"],
        "translate": ["translate", "language"],
        "write": ["write", "compose", "draft"],
    }

    def __init__(self, custom_decomposer: Optional[Callable[[str], List[str]]] = None):
        self.custom_decomposer = custom_decomposer

    def decompose(self, goal: str) -> List[PlanStep]:
        if self.custom_decomposer:
            return [PlanStep(desc) for desc in self.custom_decomposer(goal)]
        lower_goal = goal.lower()
        for category, keywords in self.DEFAULT_KEYWORDS.items():
            if any(kw in lower_goal for kw in keywords):
                return self._get_steps_for_category(category)
        return [PlanStep("Analyze problem"), PlanStep("Outline solution"), PlanStep("Execute"), PlanStep("Review")]

    def _get_steps_for_category(self, category: str) -> List[PlanStep]:
        steps_map = {
            "calculate": ["Gather data", "Perform calculation", "Verify result"],
            "search": ["Generate query", "Execute search", "Filter results"],
            "summarize": ["Read source", "Extract key points", "Write summary"],
            "translate": ["Detect language", "Translate text", "Proofread"],
            "write": ["Outline structure", "Draft content", "Revise and polish"],
        }
        return [PlanStep(desc) for desc in steps_map.get(category, ["Analyze", "Execute", "Evaluate"])]

    def validate_plan(self, plan: List[PlanStep]) -> bool:
        n = len(plan)
        indeg = [0] * n
        graph = defaultdict(list)
        for i, step in enumerate(plan):
            for dep in step.dependencies:
                if dep < 0 or dep >= n:
                    return False
                graph[dep].append(i)
                indeg[i] += 1
        q = deque([i for i in range(n) if indeg[i] == 0])
        visited = 0
        while q:
            u = q.popleft()
            visited += 1
            for v in graph[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return visited == n


# ======================= 推理器 =======================

class Reasoner:
    """基于记忆检索的简单问答引擎"""
    def __init__(self, memory: VectorMemory):
        self.memory = memory

    def query(self, question: str, context: Optional[List[str]] = None) -> List[str]:
        results = self.memory.retrieve(question, top_k=3)
        return [mem["content"] for mem, _ in results]


# ======================= 反思引擎 =======================

class ReflectionEngine:
    """记录成败并挖掘重复失败模式"""
    def __init__(self, memory: VectorMemory, max_failure_log: int = 50):
        self.memory = memory
        self.failure_log: Deque[Dict] = deque(maxlen=max_failure_log)

    def record_outcome(self, goal: str, plan: List[PlanStep], success: bool, feedback: str = ""):
        entry = {
            "goal": goal,
            "plan": [s.description for s in plan],
            "success": success,
            "feedback": feedback,
            "timestamp": datetime.now().isoformat(),
        }
        self.failure_log.append(entry)
        if not success:
            summary = f"Failed: '{goal}'. Reason: {feedback}. Avoid plan: {entry['plan']}"
            self.memory.add(summary, metadata={"type": "reflection", "success": False}, importance=0.8)

    def generate_insights(self) -> List[str]:
        failures = [e for e in self.failure_log if not e["success"]]
        if len(failures) < 2:
            return ["Not enough data for insights (need ≥2 failures)."]
        goal_counts = defaultdict(int)
        for f in failures:
            goal_counts[f["goal"]] += 1
        suggestions = []
        for goal, cnt in goal_counts.items():
            if cnt >= 2:
                suggestions.append(f"Goal '{goal}' failed {cnt} times → consider alternative strategy.")
        if not suggestions:
            suggestions.append("No recurring failure pattern; try adjusting memory/similarity threshold.")
        return suggestions


# ======================= 元认知监控 =======================

class MetaCognitiveMonitor:
    """监控任务耗时和错误率，动态建议参数调整"""
    def __init__(self, history_size: int = 100):
        self.history: Deque[float] = deque(maxlen=history_size)
        self.error_rate = 0.0
        self.consecutive_failures = 0

    def record_task_performance(self, duration: float, success: bool):
        self.history.append(duration)
        if not success:
            self.error_rate = 0.9 * self.error_rate + 0.1 * 1.0
            self.consecutive_failures += 1
        else:
            self.error_rate = 0.9 * self.error_rate + 0.0
            self.consecutive_failures = 0

    def suggest_adjustments(self) -> Dict[str, str]:
        adj = {}
        if len(self.history) >= 10 and sum(self.history) / len(self.history) > 5.0:
            adj["working_memory"] = "reduce capacity"
        if self.error_rate > 0.3:
            adj["reasoning"] = "increase depth"
            adj["reflection"] = "increase frequency"
        if self.consecutive_failures > 2:
            adj["planning"] = "use more cautious strategy"
        return adj


# ======================= 主引擎 =======================

class CognitiveEnhancer:
    """AI Agent认知力增强引擎（高性能版）"""
    def __init__(
        self,
        long_term_capacity: int = 1000,
        working_capacity: int = 20,
        similarity_threshold: float = 0.15,
        auto_reflect_interval: int = 10,
    ):
        self.long_term_memory = VectorMemory(long_term_capacity, similarity_threshold)
        self.working_memory = WorkingMemory(working_capacity)
        self.planner = Planner()
        self.reasoner = Reasoner(self.long_term_memory)
        self.reflection = ReflectionEngine(self.long_term_memory)
        self.meta_monitor = MetaCognitiveMonitor()
        self.auto_reflect_interval = auto_reflect_interval
        self._task_counter = 0

    def perceive(self, observation: Union[str, Dict]) -> None:
        """将感知信息存入工作记忆"""
        if isinstance(observation, str):
            obs = {"type": "observation", "content": observation, "timestamp": time.time()}
        else:
            obs = observation.copy()
            obs["timestamp"] = time.time()
        self.working_memory.add(obs)

    def recall(self, query: str, top_k: int = 3) -> List[Dict]:
        """从长期记忆中检索相关内容"""
        return [mem for mem, _ in self.long_term_memory.retrieve(query, top_k)]

    def memorize(self, content: str, importance: float = 1.0, metadata: Optional[Dict] = None) -> str:
        """存入长期记忆"""
        return self.long_term_memory.add(content, metadata, importance)

    def plan(self, goal: str) -> List[PlanStep]:
        """生成执行计划"""
        steps = self.planner.decompose(goal)
        if not self.planner.validate_plan(steps):
            raise ValueError("Invalid plan: circular dependency detected")
        self.working_memory.add({"type": "plan", "goal": goal, "steps": [s.description for s in steps]})
        return steps

    def reason(self, problem: str) -> List[str]:
        """基于记忆进行推理"""
        return self.reasoner.query(problem)

    def reflect(self) -> List[str]:
        """主动反思，生成改进建议"""
        insights = self.reflection.generate_insights()
        for ins in insights:
            if "Not enough" not in ins:
                self.memorize(f"Reflection: {ins}", importance=0.6, metadata={"type": "insight"})
        return insights

    def execute_task(self, goal: str, executor: Optional[Callable[[PlanStep], None]] = None) -> Dict[str, Any]:
        """
        完整执行一项任务：规划 → 执行（可注入执行器） → 记录 → 反思 → 元监控
        :param executor: 可选的可调用对象，接收PlanStep并执行实际动作
        """
        start = time.time()
        plan: List[PlanStep] = []
        success = True
        feedback = ""
        try:
            plan = self.plan(goal)
            for step in plan:
                step.status = "running"
                if executor:
                    executor(step)
                step.status = "done"
            self.working_memory.add({"type": "task_result", "goal": goal, "success": True})
        except Exception as e:
            success = False
            feedback = str(e)
            self.working_memory.add({"type": "task_result", "goal": goal, "success": False, "error": feedback})
        duration = time.time() - start
        self.meta_monitor.record_task_performance(duration, success)
        self.reflection.record_outcome(goal, plan, success, feedback)
        self._task_counter += 1
        if self._task_counter % self.auto_reflect_interval == 0:
            self.reflect()
        adjustments = self.meta_monitor.suggest_adjustments()
        if adjustments:
            self.working_memory.add({"type": "meta_suggestion", "adjustments": adjustments})
        return {
            "goal": goal,
            "success": success,
            "duration": round(duration, 3),
            "feedback": feedback,
            "meta_adjustments": adjustments,
        }

    def get_status(self) -> Dict:
        """返回引擎当前状态"""
        return {
            "long_term_memories": len(self.long_term_memory.memories),
            "working_memories": len(self.working_memory.buffer),
            "tasks_executed": self._task_counter,
            "error_rate": round(self.meta_monitor.error_rate, 3),
            "consecutive_failures": self.meta_monitor.consecutive_failures,
        }


# ======================= 演示与测试 =======================

if __name__ == "__main__":
    brain = CognitiveEnhancer(long_term_capacity=500, auto_reflect_interval=3)
    brain.perceive("User: What is the capital of France?")
    brain.memorize("Paris is the capital of France.", importance=0.9)
    recalled = brain.recall("France capital")
    print("Recalled:", [r["content"] for r in recalled])
    answers = brain.reason("capital of France")
    print("Reasoning result:", answers)
    result = brain.execute_task("Calculate 15% tip on $200 bill")
    print("Task result:", result)
    print("Reflection insights:", brain.reflect())
    print("Engine status:", brain.get_status())
    for i in range(3):
        brain.execute_task(f"Dummy task {i+1}")
    print("Final status:", brain.get_status())
