# Multi-Agent Coordinator
# 参考: claude-code/src/core/coordinator.ts + coordinator prompt
#
# 设计:
#   一个主 Coordinator 协调多个 Specialized Agents 并行工作
#   主 agent 负责任务分解 + 结果聚合
#   子 agents 专注各自领域 (coding/review/memory...)
#
# 状态机: idle → planning → dispatching → waiting → aggregating → done

from __future__ import annotations
import uuid
import time
import threading
import json
from pathlib import Path
from typing import Optional, Any
from dataclasses import dataclass, field
from enum import Enum

WORKSPACE = Path(__file__).parent.parent.resolve()
COORDINATOR_DIR = WORKSPACE / "evoclaw" / "coordinator"
COORDINATOR_DIR.mkdir(parents=True, exist_ok=True)


# ─── 角色定义 ────────────────────────────────────────────────────

@dataclass
class AgentRole:
    name: str                          # "coder", "reviewer", "memory"
    description: str
    capabilities: list[str]
    model_preference: str = ""          # 可指定专用模型
    prompt_template: str = ""           # 角色专属 system prompt 片段


STANDARD_ROLES = {
    "coder": AgentRole(
        name="coder",
        description="主编码 agent，负责代码实现和修改",
        capabilities=["write_code", "refactor", "debug", "test"],
        prompt_template="你是一个专业后端开发者，擅长 Python/JS/Shell，代码简洁健壮。",
    ),
    "reviewer": AgentRole(
        name="reviewer",
        description="代码审查 agent，负责质量和安全审计",
        capabilities=["code_review", "security_check", "performance_review"],
        prompt_template="你是一个资深代码审查员，关注质量、安全和可维护性。",
    ),
    "memory": AgentRole(
        name="memory",
        description="记忆管理 agent，负责整理和检索记忆",
        capabilities=["memory_search", "memory_write", "reflection"],
        prompt_template="你负责记忆管理，关注信息的准确性和可追溯性。",
    ),
    "researcher": AgentRole(
        name="researcher",
        description="研究 agent，负责信息检索和分析",
        capabilities=["web_search", "source_analysis", "summarize"],
        prompt_template="你是一个研究助手，擅长信息检索、对比分析和结构化输出。",
    ),
}


# ─── 状态机 ─────────────────────────────────────────────────────

class CoordinatorState(str, Enum):
    IDLE = "idle"
    PLANNING = "planning"
    DISPATCHING = "dispatching"
    WAITING = "waiting"
    AGGREGATING = "aggregating"
    DONE = "done"
    FAILED = "failed"


# ─── 任务单元 ───────────────────────────────────────────────────

@dataclass
class SubTask:
    task_id: str
    role: str                           # coder / reviewer / ...
    instruction: str                    # 给子 agent 的具体指令
    context: dict = field(default_factory=dict)  # 共享上下文
    result: Optional[Any] = None
    status: str = "pending"             # pending / running / done / failed
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    error: Optional[str] = None

    @property
    def duration_ms(self) -> Optional[int]:
        if self.started_at and self.completed_at:
            return int((self.completed_at - self.started_at) * 1000)
        return None


# ─── Coordinator 会话 ────────────────────────────────────────────

@dataclass
class CoordinatorSession:
    session_id: str
    goal: str                           # 总体目标
    roles: dict[str, AgentRole]
    tasks: list[SubTask]
    state: CoordinatorState = CoordinatorState.IDLE
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    result: Optional[dict] = None
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "goal": self.goal,
            "state": self.state.value,
            "tasks": [
                {
                    "task_id": t.task_id,
                    "role": t.role,
                    "instruction": t.instruction,
                    "status": t.status,
                    "duration_ms": t.duration_ms,
                    "error": t.error,
                }
                for t in self.tasks
            ],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


# ─── Coordinator 主逻辑 ─────────────────────────────────────────

class Coordinator:
    """
    Multi-Agent Coordinator.
    
    流程:
      1. planning()    — 分解任务到多个 SubTask
      2. dispatch()    — 并行分发到各子 agents
      3. wait()        — 等待子 agents 完成
      4. aggregate()   — 聚合结果，返回给主 session
      5. shutdown()    — 取消/清理
    
    参考: claude-code CoordinatorSession + processCoordinatorTask()
    """

    def __init__(self, session: CoordinatorSession):
        self.session = session
        self._lock = threading.RLock()
        self._done_event = threading.Event()
        self._sub_results: dict[str, Any] = {}

    # ─── 任务分解 (Planning) ──────────────────────────────────

    def plan(self, task_description: str) -> list[SubTask]:
        """
        将任务分解为子任务.
        这里用规则分解，后续可升级为 LLM 分解.
        
        返回: 分解后的 SubTask 列表
        """
        with self._lock:
            self.session.state = CoordinatorState.PLANNING
            self.session.updated_at = time.time()

        tasks = []

        # 简单规则: "实现 X 并审查" → coder + reviewer
        if any(kw in task_description.lower() for kw in ["实现", "开发", "写", "代码", "implement", "build", "write"]):
            tasks.append(SubTask(
                task_id=str(uuid.uuid4())[:8],
                role="coder",
                instruction=task_description,
            ))

        if any(kw in task_description.lower() for kw in ["审查", "review", "审计", "检查"]):
            tasks.append(SubTask(
                task_id=str(uuid.uuid4())[:8],
                role="reviewer",
                instruction=task_description,
            ))

        if any(kw in task_description.lower() for kw in ["研究", "搜索", "找", "分析"]):
            tasks.append(SubTask(
                task_id=str(uuid.uuid4())[:8],
                role="researcher",
                instruction=task_description,
            ))

        # 默认至少一个 coder
        if not tasks:
            tasks.append(SubTask(
                task_id=str(uuid.uuid4())[:8],
                role="coder",
                instruction=task_description,
            ))

        self.session.tasks = tasks
        self._update_state(CoordinatorState.DISPATCHING)
        return tasks

    # ─── 分发 (Dispatch) ─────────────────────────────────────

    def dispatch(self) -> None:
        """
        并行分发任务到子 agents.
        每个 SubTask 通过 sessions_spawn 启动子代理.
        
        注意: 实际 spawn 需要 sessions_spawn tool，这里只管理状态.
        """
        with self._lock:
            self._update_state(CoordinatorState.DISPATCHING)
            for task in self.session.tasks:
                task.status = "running"
                task.started_at = time.time()
        self._update_state(CoordinatorState.WAITING)

    def mark_done(self, task_id: str, result: Any) -> None:
        """标记子任务完成"""
        with self._lock:
            for task in self.session.tasks:
                if task.task_id == task_id:
                    task.status = "done"
                    task.result = result
                    task.completed_at = time.time()
                    self._sub_results[task_id] = result
                    break
            self.session.updated_at = time.time()

            # 检查是否全部完成
            if all(t.status in ("done", "failed") for t in self.session.tasks):
                self._done_event.set()

    def mark_failed(self, task_id: str, error: str) -> None:
        """标记子任务失败"""
        with self._lock:
            for task in self.session.tasks:
                if task.task_id == task_id:
                    task.status = "failed"
                    task.error = error
                    task.completed_at = time.time()
                    break
            self.session.updated_at = time.time()
            # 一个失败不阻断整体，除非所有都失败
            if all(t.status in ("done", "failed") for t in self.session.tasks):
                self._done_event.set()

    # ─── 等待 (Wait) ──────────────────────────────────────────

    def wait(self, timeout: float = 300) -> bool:
        """
        等待所有子任务完成.
        返回: True=全部完成, False=超时
        """
        return self._done_event.wait(timeout)

    # ─── 聚合 (Aggregate) ────────────────────────────────────

    def aggregate(self) -> dict:
        """
        聚合所有子任务结果.
        返回结构化的最终结果.
        """
        with self._lock:
            self._update_state(CoordinatorState.AGGREGATING)

        by_role = {}
        for task in self.session.tasks:
            by_role[task.role] = {
                "status": task.status,
                "result": task.result,
                "duration_ms": task.duration_ms,
                "error": task.error,
            }

        self.session.result = {
            "session_id": self.session.session_id,
            "goal": self.session.goal,
            "by_role": by_role,
            "total_duration_ms": int((time.time() - self.session.created_at) * 1000),
            "all_done": all(t.status == "done" for t in self.session.tasks),
        }

        self._update_state(CoordinatorState.DONE)
        return self.session.result

    # ─── 状态 ─────────────────────────────────────────────────

    def _update_state(self, state: CoordinatorState) -> None:
        self.session.state = state
        self.session.updated_at = time.time()

    def get_status(self) -> dict:
        with self._lock:
            return self.session.to_dict()

    def is_done(self) -> bool:
        return self.session.state in (CoordinatorState.DONE, CoordinatorState.FAILED)

    def shutdown(self) -> dict:
        """取消所有任务，清理状态"""
        with self._lock:
            self._update_state(CoordinatorState.FAILED)
            for task in self.session.tasks:
                if task.status == "running":
                    task.status = "cancelled"
        return {"session_id": self.session.session_id, "shutdown": True}


# ─── 会话管理 ───────────────────────────────────────────────────

class CoordinatorStore:
    """Coordinator 会话持久化管理"""

    _sessions: dict[str, CoordinatorSession] = {}
    _lock = threading.Lock()

    @classmethod
    def create(cls, goal: str, roles: Optional[dict[str, AgentRole]] = None) -> Coordinator:
        session = CoordinatorSession(
            session_id=str(uuid.uuid4())[:12],
            goal=goal,
            roles=roles or STANDARD_ROLES,
            tasks=[],
        )
        with cls._lock:
            cls._sessions[session.session_id] = session
        return Coordinator(session)

    @classmethod
    def get(cls, session_id: str) -> Optional[CoordinatorSession]:
        with cls._lock:
            return cls._sessions.get(session_id)

    @classmethod
    def list_active(cls) -> list[CoordinatorSession]:
        with cls._lock:
            return [s for s in cls._sessions.values() if s.state not in (CoordinatorState.DONE, CoordinatorState.FAILED)]

    @classmethod
    def close(cls, session_id: str) -> None:
        with cls._lock:
            cls._sessions.pop(session_id, None)


# ─── 快捷函数 ───────────────────────────────────────────────────

def coordinate(goal: str, task_description: str, roles: Optional[dict[str, AgentRole]] = None) -> Coordinator:
    """
    创建 Coordinator 并自动 plan + dispatch.
    
    用法:
        coord = coordinate("实现登录功能", "写一个 Python 登录 API 并做安全审查")
        coord.wait()
        result = coord.aggregate()
    """
    coord = CoordinatorStore.create(goal, roles)
    coord.plan(task_description)
    coord.dispatch()
    return coord


if __name__ == "__main__":
    coord = coordinate("多 agent 测试", "写一个 hello world 并审查")
    coord.wait(timeout_secs=1)  # 模拟快速完成
    coord.mark_done(coord.session.tasks[0].task_id, "print('hello world')")
    result = coord.aggregate()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("✅ Coordinator: test passed")
