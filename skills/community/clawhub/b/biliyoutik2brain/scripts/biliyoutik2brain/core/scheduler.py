"""
资源感知调度器 (v3.0)

基于环境画像 + ASR/LLM 成本模型，动态决策任务执行策略。

核心决策:
  1. 并行 vs 串行: 根据 CPU/内存/GPU 决定同时能跑几个任务
  2. 任务优先级: 长视频优先 or 短视频优先（取决于环境）
  3. 引擎选择: 本地ASR(yes) vs 云端ASR(no) → 影响成本和速度
  4. 模型降级: 资源不足时自动下调 ASR 模型大小

集成: 替换现有 slots.py 的简单并发控制，增强 config.py 的 assess_and_route。
"""

import os, time, json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from .env import EnvProfile, detect, AgentType, ASREngine, LLMBackend


# ═══════════════════════════════════════════════════════════════
#  数据类型
# ═══════════════════════════════════════════════════════════════

class TaskPriority(Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3


@dataclass
class Task:
    """调度任务"""
    url: str
    video_id: str
    title: str = ""
    duration_s: int = 0          # 视频时长(秒)
    uploader: str = ""
    platform: str = ""
    priority: TaskPriority = TaskPriority.MEDIUM
    subtitles_available: bool = False  # 是否有API字幕

    @property
    def estimated_minutes(self) -> float:
        """预估处理时长(分钟)"""
        return max(1, self.duration_s / 60)


@dataclass
class SchedulerDecision:
    """调度决策输出"""
    # 并发控制
    max_parallel_tasks: int = 1
    can_async: bool = False       # 是否可以异步并行

    # 引擎选择
    asr_engine: str = "auto"
    asr_model: str = "base"
    llm_backend: str = "auto"

    # 策略
    reason: str = ""
    estimated_time_per_task: float = 0.0  # 预估单任务耗时(分钟)
    estimated_cost_per_task: float = 0.0  # 预估单任务成本(元)


# ═══════════════════════════════════════════════════════════════
#  成本模型
# ═══════════════════════════════════════════════════════════════

def _estimate_cost(
    duration_minutes: float,
    asr_engine: str,
    llm_backend: str,
    env: EnvProfile,
) -> Tuple[float, str]:
    """估算单任务成本(元)"""
    if env.agent_type in (AgentType.WORKBUDDY_LOCAL,):
        if "faster_whisper" in [e.value for e in env.asr.engines]:
            # 本地 ASR + 本地 LLM → 免费
            if not env.llm.is_paid:
                return 0.0, "本地全链路, 免费"

    # 云端 or 混合
    cost = 0.0
    details = []

    # ASR 成本
    if asr_engine in ("bailian",):
        # 百炼ASR 对音频时长计费 (约 ¥0.003/分钟)
        cost += duration_minutes * 0.003
        details.append(f"ASR ¥{duration_minutes * 0.003:.4f}")
    elif asr_engine in ("faster_whisper", "openai_whisper"):
        details.append("ASR 本地免费")
    else:
        cost += duration_minutes * 0.01  # 保守估算
        details.append(f"ASR 估 ¥{duration_minutes * 0.01:.4f}")

    # LLM 成本
    if llm_backend == "deepseek":
        # DeepSeek: ¥0.001/1K tokens, 估算 3K tokens/分钟视频
        tokens = duration_minutes * 3000
        cost += tokens / 1000 * 0.001
        details.append(f"LLM ¥{tokens/1000*0.001:.4f}")
    elif llm_backend == "openai":
        tokens = duration_minutes * 3000
        cost += tokens / 1000 * 0.01  # OpenAI 贵10倍
        details.append(f"LLM ¥{tokens/1000*0.01:.4f}")
    elif llm_backend in ("ollama", "vllm"):
        details.append("LLM 本地免费")
    else:
        cost += duration_minutes * 0.005
        details.append(f"LLM 估 ¥{duration_minutes * 0.005:.4f}")

    return round(cost, 4), " + ".join(details)


# ═══════════════════════════════════════════════════════════════
#  调度决策
# ═══════════════════════════════════════════════════════════════

def decide(
    tasks: List[Task],
    env: Optional[EnvProfile] = None,
    prefer_cost_saving: bool = False,
) -> SchedulerDecision:
    """根据环境和任务列表，输出调度决策

    Args:
        tasks: 待处理的任务列表
        env: 环境画像 (自动检测)
        prefer_cost_saving: 是否优先省钱 (True=本地免费, False=云端快)

    Returns:
        SchedulerDecision
    """
    if env is None:
        env = detect()

    decision = SchedulerDecision()
    cpu = env.cpu_cores
    ram = env.ram_gb
    agent = env.agent_type

    task_count = len(tasks)

    # ── 并发决策 ──
    if agent == AgentType.WORKBUDDY_CLOUD:
        # 云端: 资源受限，串行为主
        decision.max_parallel_tasks = min(2, max(1, cpu // 4))
        decision.can_async = (task_count > 1 and cpu >= 4)

    elif agent == AgentType.WORKBUDDY_LOCAL:
        # 本地NUC: 资源充足，可并行
        decision.max_parallel_tasks = min(6, max(1, cpu // 2))
        decision.can_async = (task_count > 1 and cpu >= 4)

    elif agent in (AgentType.OPENCLAW_PIP, AgentType.OPENCLAW_DOCKER, AgentType.OPENCLAW_SOURCE):
        decision.max_parallel_tasks = min(4, max(1, cpu // 2))
        decision.can_async = task_count > 1

    else:
        # Hermes / Generic
        decision.max_parallel_tasks = min(3, max(1, cpu // 3))
        decision.can_async = task_count > 1

    # ── ASR 引擎选择 ──
    asr_available = env.asr

    if "faster_whisper" in [e.value for e in asr_available.engines]:
        # 本地 faster-whisper → 首选
        decision.asr_engine = "faster_whisper"
        # 根据资源选模型
        if env.gpu_available:
            decision.asr_model = "small"  # 有GPU可用大模型
        elif cpu >= 8 and ram > 16:
            decision.asr_model = "base"
        else:
            decision.asr_model = "tiny"
    elif "bailian" in [e.value for e in asr_available.engines]:
        decision.asr_engine = "bailian"
        decision.asr_model = "paraformer-v2"
    elif "openai_whisper" in [e.value for e in asr_available.engines]:
        decision.asr_engine = "openai_whisper"
        decision.asr_model = "base"
    else:
        # 回退
        decision.asr_engine = "faster_whisper"
        decision.asr_model = "base"

    # ── LLM 后端选择 ──
    llm = env.llm

    if prefer_cost_saving and "ollama" in [b.value for b in llm.backends]:
        decision.llm_backend = "ollama"
    elif prefer_cost_saving and "vllm" in [b.value for b in llm.backends]:
        decision.llm_backend = "vllm"
    elif "deepseek" in [b.value for b in llm.backends]:
        decision.llm_backend = "deepseek"
    elif "openai" in [b.value for b in llm.backends]:
        decision.llm_backend = "openai"
    elif "ollama" in [b.value for b in llm.backends]:
        decision.llm_backend = "ollama"
    else:
        decision.llm_backend = "deepseek"  # 乐观

    # ── 成本估算 ──
    avg_duration = sum(t.duration_s for t in tasks) / max(task_count, 1) / 60
    cost, cost_detail = _estimate_cost(
        avg_duration, decision.asr_engine, decision.llm_backend, env
    )
    decision.estimated_cost_per_task = cost
    decision.estimated_time_per_task = avg_duration * 0.8  # 约80%实时

    # ── 决策理由 ──
    parts = []
    parts.append(f"平台={agent.value}")
    parts.append(f"ASR={decision.asr_engine}/{decision.asr_model}")
    parts.append(f"LLM={decision.llm_backend}")
    parts.append(f"并发={decision.max_parallel_tasks}")
    parts.append(f"成本={cost_detail}=¥{cost:.4f}/任务")
    if decision.can_async:
        parts.append("可并行")
    decision.reason = " | ".join(parts)

    return decision


# ═══════════════════════════════════════════════════════════════
#  任务排序
# ═══════════════════════════════════════════════════════════════

def prioritize(tasks: List[Task], env: Optional[EnvProfile] = None) -> List[Task]:
    """对任务列表排序

    策略:
    - 有API字幕的优先 (零成本处理)
    - 云端: 短视频优先 (快速周转)
    - 本地: 长视频优先 (充分利用空闲算力)
    """
    if env is None:
        env = detect()

    # 副本，避免修改原列表
    sorted_tasks = list(tasks)

    if env.agent_type == AgentType.WORKBUDDY_CLOUD:
        # 云端: 有字幕最优先, 然后短视频优先
        sorted_tasks.sort(key=lambda t: (0 if t.subtitles_available else 1, t.duration_s))
    else:
        # 本地: 有字幕最优先, 然后长视频优先
        sorted_tasks.sort(key=lambda t: (0 if t.subtitles_available else 1, -t.duration_s))

    return sorted_tasks


# ═══════════════════════════════════════════════════════════════
#  诊断
# ═══════════════════════════════════════════════════════════════

def diagnose(env: Optional[EnvProfile] = None):
    """打印调度诊断信息"""
    if env is None:
        env = detect()

    print("=" * 55)
    print("  调度器诊断")
    print("=" * 55)

    dummy_tasks = [
        Task(url="dummy", video_id="BV001", title="10分钟视频", duration_s=600),
        Task(url="dummy", video_id="BV002", title="30分钟视频", duration_s=1800),
        Task(url="dummy", video_id="BV003", title="60分钟视频", duration_s=3600),
    ]

    decision = decide(dummy_tasks, env, prefer_cost_saving=False)
    print(f"  决策: {decision.reason}")

    print(f"\n  排序测试:")
    sorted_tasks = prioritize(dummy_tasks, env)
    for i, t in enumerate(sorted_tasks):
        print(f"    {i+1}. {t.title} ({t.duration_s//60}分)")

    print("\n  省钱模式:")
    decision2 = decide(dummy_tasks, env, prefer_cost_saving=True)
    print(f"  决策: {decision2.reason}")

    print("=" * 55)


# ═══════════════════════════════════════════════════════════════
#  异步并行执行
# ═══════════════════════════════════════════════════════════════

def run_parallel(
    tasks: List[Task],
    processor_func,
    env: Optional[EnvProfile] = None,
    max_workers: int = None,
):
    """多线程并行执行任务队列

    Args:
        tasks: 任务列表
        processor_func: 处理函数 func(task) -> result
        env: 环境画像
        max_workers: 最大并发数 (None=auto from scheduler)

    Example:
        results = run_parallel(tasks, lambda t: process_video(t.url))
    """
    if env is None:
        env = detect()

    decision = decide(tasks, env)
    workers = max_workers or decision.max_parallel_tasks
    workers = min(workers, len(tasks))

    print(f"\n🚀 并行执行: {len(tasks)}个任务, {workers}线程")
    print(f"   策略: {decision.reason}")

    from concurrent.futures import ThreadPoolExecutor, as_completed
    from threading import Lock

    results = []
    errors = []
    lock = Lock()

    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_task = {
            executor.submit(processor_func, task): task
            for task in tasks
        }

        for future in as_completed(future_to_task):
            task = future_to_task[future]
            try:
                result = future.result()
                with lock:
                    results.append((task, result))
                    print(f"  ✅ {task.title[:30]} ({task.duration_s//60}分)")
            except Exception as e:
                with lock:
                    errors.append((task, str(e)))
                    print(f"  ❌ {task.title[:30]}: {e}")

    print(f"\n📊 完成: {len(results)}/{len(tasks)}, 失败: {len(errors)}")
    return results, errors
