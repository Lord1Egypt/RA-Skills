"""
immediate_skill_hook.py - 即时 Skill 生成钩子

参考 MaxHermes "任务完成 → 立即提炼" 机制，在任务完成后立即评估
并决定是否直接生成 Skill 文档，而非等待梦境周期（6-24小时延迟）。

与现有 persistent_store.py 完全解耦，作为独立 hook 层叠加。

核心流程:
  after_task_complete(task_result)
    → extract_skill_candidate()       # 候选提取（LLM 或规则兜底）
    → score_and_route()                # 置信度分流
        ├─ confidence >= 0.8  → write_skill_document()  # 高质量：直接写盘
        └─ confidence <  0.8  → add_to_dreaming_queue() # 低质量：入梦境队列

agentskills.io 兼容格式输出到 skills/ 目录。
"""

from __future__ import annotations

import json
import logging
import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

# =============================================================================
# 路径配置
# =============================================================================

DEFAULT_SKILLS_DIR = Path(__file__).parent.parent.parent / "data" / "skills"
DEFAULT_DREAM_QUEUE_PATH = Path(__file__).parent.parent.parent / "data" / "dream_queue.jsonl"


# =============================================================================
# 数据模型
# =============================================================================

class SkillConfidence(Enum):
    """Skill 候选置信度等级"""
    HIGH = "high"      # >= 0.8 → 直接写入
    MEDIUM = "medium"  # 0.5–0.8 → 入梦境队列
    LOW = "low"        # < 0.5 → 丢弃或标记低优先


@dataclass
class TaskResult:
    """
    任务执行结果 - after_task_complete 的输入类型。

    接受字典或 TaskResult 实例，字段宽松匹配。
    """
    task_id: str
    success: bool
    content: str                              # 任务描述
    result: str                               # 实际执行结果（文本）
    agent_id: str = ""
    session_id: str = ""
    duration_seconds: float = 0.0
    tools_used: list[str] = field(default_factory=list)  # 调用过的工具
    error: str = ""                            # 失败原因（如有）
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict) -> TaskResult:
        return cls(
            task_id=data.get("task_id", ""),
            success=data.get("success", False),
            content=data.get("content", ""),
            result=data.get("result", ""),
            agent_id=data.get("agent_id", ""),
            session_id=data.get("session_id", ""),
            duration_seconds=float(data.get("duration_seconds", 0.0)),
            tools_used=data.get("tools_used", []),
            error=data.get("error", ""),
            metadata=data.get("metadata", {}),
        )


@dataclass
class SkillCandidate:
    """
    Skill 候选 - 从任务结果中提取的半结构化 Skill 草稿。
    """
    # 基础信息
    name: str
    description: str                          # 一句话描述
    confidence: float                         # 0.0–1.0
    confidence_reason: str = ""               # 置信度来源说明

    # 核心字段（agentskills.io 标准）
    triggers: list[str] = field(default_factory=list)   # 触发场景关键词
    actions: list[str] = field(default_factory=list)    # 执行步骤列表
    examples: list[dict[str, str]] = field(default_factory=list)  # [{input, output}]
    version: str = "1.0.0"

    # 来源追溯
    source_task_id: str = ""
    source_agent_id: str = ""
    source_session_id: str = ""
    extracted_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    # 质量标记
    tags: list[str] = field(default_factory=list)
    notes: str = ""                            # 内部备注


# =============================================================================
# 规则兜底提取器（LLM 不可用时使用）
# =============================================================================

class RuleBasedExtractor:
    """
    基于规则的 Skill 候选提取器。

    在 LLM 不可用时，通过启发式规则从 TaskResult 中抽取：
    - 触发词（What/How/When/If ...）
    - 执行步骤（步骤编号、Markdown 列表）
    - 命名实体（工具名、文件路径）

    置信度说明：
    - 0.5：有成功结果 + 可提取步骤
    - 0.7：有成功结果 + 有触发词 + 有步骤
    - 0.85+：完美匹配 agentskills.io 字段
    """

    # 触发词正则（大小写不敏感）
    TRIGGER_PATTERNS = [
        re.compile(r'\b(how to|how do|how can)\b', re.I),
        re.compile(r'\b(when should|when to|when must)\b', re.I),
        re.compile(r'\b(if.*then|if.*occur)\b', re.I),
        re.compile(r'\b(what is|what are|which)\b', re.I),
        re.compile(r'\b(resolve|fix|debug|handle|detect)\b', re.I),
    ]

    # 步骤识别正则（Markdown 有序列表或无序列表）
    STEP_PATTERNS = [
        re.compile(r'^\s*(\d+)[.)].+\S', re.M),           # 1. 2. 或 1) 2)
        re.compile(r'^\s*[-*+]\s+.+\S', re.M),             # - * + 列表
        re.compile(r'\bstep\s+(\d+)\b', re.I),             # Step N
    ]

    # 工具名识别
    TOOL_PATTERNS = [
        re.compile(r'\b(read_file|write_file|bash|search_web|'
                    r'fetch_web|image_generate|create_podcast)\b'),
        re.compile(r'\b(skill_load|memory_search|persistent_store)\b'),
    ]

    def extract(self, task_result: TaskResult) -> SkillCandidate:
        """从 TaskResult 中提取 Skill 候选"""
        if not task_result.success:
            return self._extract_failed(task_result)

        # 合并 content + result 用于分析
        text = f"{task_result.content}\n\n{task_result.result}"
        steps = self._extract_steps(text)
        triggers = self._extract_triggers(text)
        tools = self._extract_tools(text)

        # 计算置信度
        confidence, reason = self._compute_confidence(
            success=task_result.success,
            steps=steps,
            triggers=triggers,
            tools=tools,
            has_examples=bool(task_result.metadata.get("examples")),
        )

        # 生成 name
        name = self._derive_name(task_result, triggers)

        candidate = SkillCandidate(
            name=name,
            description=self._summarize(text[:500]),
            confidence=confidence,
            confidence_reason=reason,
            triggers=triggers,
            actions=steps,
            examples=self._extract_examples(task_result),
            version="1.0.0",
            source_task_id=task_result.task_id,
            source_agent_id=task_result.agent_id,
            source_session_id=task_result.session_id,
            tags=["rule-extracted"] + tools,
        )
        return candidate

    def _extract_steps(self, text: str) -> list[str]:
        steps: list[str] = []
        seen: set[str] = set()
        for pattern in self.STEP_PATTERNS:
            for m in pattern.finditer(text):
                step = m.group(0).strip()
                # 去重
                if step not in seen:
                    seen.add(step)
                    steps.append(step)
        return steps[:10]   # 最多保留 10 步

    def _extract_triggers(self, text: str) -> list[str]:
        triggers: list[str] = []
        for pattern in self.TRIGGER_PATTERNS:
            m = pattern.search(text)
            if m:
                triggers.append(m.group(0).lower())
        # 去重
        return list(dict.fromkeys(triggers))[:5]

    def _extract_tools(self, text: str) -> list[str]:
        tools: list[str] = []
        for pattern in self.TOOL_PATTERNS:
            tools.extend(pattern.findall(text))
        return list(dict.fromkeys(tools))[:5]

    def _compute_confidence(
        self,
        success: bool,
        steps: list[str],
        triggers: list[str],
        tools: list[str],
        has_examples: bool,
    ) -> tuple[float, str]:
        if not success:
            return 0.2, "任务失败，无法生成 Skill"

        score = 0.3  # 基础分
        reasons: list[str] = []

        if steps:
            score += 0.25
            reasons.append(f"{len(steps)} 个执行步骤")
        if triggers:
            score += 0.15
            reasons.append(f"{len(triggers)} 个触发词")
        if tools:
            score += 0.1
            reasons.append(f"{len(tools)} 个工具引用")
        if has_examples:
            score += 0.15
            reasons.append("含示例数据")

        # 上限 0.95（规则提取器上限）
        score = min(score, 0.95)

        reason_str = f"规则提取：{', '.join(reasons) if reasons else '基础分'}"
        return round(score, 3), reason_str

    def _derive_name(self, task_result: TaskResult, triggers: list[str]) -> str:
        # 从 content 前 60 字符提取主语
        raw = task_result.content.strip()
        # 取第一个分句
        first_sentence = re.split(r'[.!?\n]', raw)[0].strip()
        name = first_sentence[:60].strip()
        # 清理特殊字符
        name = re.sub(r'\s+', '_', name)
        name = re.sub(r'[^\w_\-]', '', name)
        return name or f"skill_{task_result.task_id[:8]}"

    def _summarize(self, text: str, max_len: int = 200) -> str:
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) <= max_len:
            return text
        return text[:max_len].rsplit(' ', 1)[0] + "…"

    def _extract_examples(self, task_result: TaskResult) -> list[dict[str, str]]:
        """从 metadata 中提取示例，未找到则返回空"""
        examples = task_result.metadata.get("examples", [])
        if isinstance(examples, list) and examples:
            return [{"input": str(e.get("input", "")), "output": str(e.get("output", ""))}
                    for e in examples[:3]]
        return []

    def _extract_failed(self, task_result: TaskResult) -> SkillCandidate:
        """从失败任务中提取错误模式（作为反面 Skill 候选）"""
        return SkillCandidate(
            name=f"error_handler_{task_result.task_id[:8]}",
            description=f"处理错误：{self._summarize(task_result.error or 'unknown', 120)}",
            confidence=0.1,
            confidence_reason="任务失败，仅提取错误模式",
            triggers=["error", "failure", task_result.error[:30] if task_result.error else ""],
            actions=[f"错误信息：{task_result.error}"],
            source_task_id=task_result.task_id,
            source_agent_id=task_result.agent_id,
            tags=["error-case"],
        )


# =============================================================================
# LLM 增强提取器（可选，LLM 可用时调用）
# =============================================================================

class LLMExtractor:
    """
    基于 LLM 的 Skill 候选提取器。

    使用 LLM 对 TaskResult 进行结构化分析，输出 SkillCandidate。
    当 LLM 不可用或调用失败时，回退到 RuleBasedExtractor。
    """

    def __init__(self, llm_callable=None):
        """
        Args:
            llm_callable: 符合接口 (prompt: str) -> str 的 LLM 推理函数。
                          如 None，则内部禁用，强制回退。
        """
        self._llm = llm_callable

    async def extract(self, task_result: TaskResult) -> SkillCandidate:
        """异步 LLM 提取（内部同步调用 LLM）"""
        if not self._llm:
            return RuleBasedExtractor().extract(task_result)

        prompt = self._build_prompt(task_result)
        try:
            raw = self._llm(prompt)
            return self._parse_response(raw, task_result)
        except Exception as exc:
            logger.warning(f"LLM extraction failed, falling back to rules: {exc}")
            return RuleBasedExtractor().extract(task_result)

    def _build_prompt(self, task_result: TaskResult) -> str:
        return (
            "You are a skill distillation assistant. Given a task execution result, "
            "extract a reusable Skill candidate in JSON format.\n\n"
            "Task:\n" + task_result.content + "\n\n"
            "Result:\n" + task_result.result + "\n\n"
            "Tools used: " + ", ".join(task_result.tools_used) + "\n\n"
            "Output ONLY valid JSON with fields:\n"
            "  name (string, max 60 chars, use underscores)\n"
            "  description (string, max 200 chars)\n"
            "  triggers (list of strings, max 5)\n"
            "  actions (list of strings, max 10, each step one sentence)\n"
            "  examples (list of {input, output} objects, max 3)\n"
            "  tags (list of strings, max 5)\n"
            "Output JSON only, no markdown."
        )

    def _parse_response(self, raw: str, task_result: TaskResult) -> SkillCandidate:
        # 去掉 markdown 代码块
        raw = re.sub(r'^```json\s*', '', raw.strip(), flags=re.M)
        raw = re.sub(r'\s*```$', '', raw.strip())
        data = json.loads(raw)
        return SkillCandidate(
            name=data.get("name", f"skill_{task_result.task_id[:8]}"),
            description=data.get("description", ""),
            confidence=0.92,           # LLM 提取置信度默认高
            confidence_reason="LLM structured extraction",
            triggers=data.get("triggers", [])[:5],
            actions=data.get("actions", [])[:10],
            examples=data.get("examples", [])[:3],
            version="1.0.0",
            source_task_id=task_result.task_id,
            source_agent_id=task_result.agent_id,
            source_session_id=task_result.session_id,
            tags=data.get("tags", ["llm-extracted"])[:5],
        )


# =============================================================================
# Skill 文档写入器
# =============================================================================

class SkillDocumentWriter:
    """
    将 SkillCandidate 写入 agentskills.io 兼容的 Markdown 文档。

    输出格式：
      data/skills/{name}/{name}.md
      data/skills/{name}/metadata.json
    """

    def __init__(self, skills_dir: Path | str = DEFAULT_SKILLS_DIR):
        self.skills_dir = Path(skills_dir)

    def write(self, candidate: SkillCandidate) -> Path:
        """写入 Skill 文档，返回文档路径"""
        self.skills_dir.mkdir(parents=True, exist_ok=True)

        # 安全化目录名（只允许字母数字下划线短横）
        safe_name = re.sub(r'[^\w\-]', '_', candidate.name)[:60]
        skill_dir = self.skills_dir / safe_name
        skill_dir.mkdir(parents=True, exist_ok=True)

        # 1. 主文档
        doc_path = skill_dir / f"{safe_name}.md"
        doc_path.write_text(self._render_markdown(candidate), encoding="utf-8")

        # 2. 元数据
        meta_path = skill_dir / "metadata.json"
        meta_path.write_text(json.dumps({
            "name": candidate.name,
            "version": candidate.version,
            "confidence": candidate.confidence,
            "confidence_reason": candidate.confidence_reason,
            "source_task_id": candidate.source_task_id,
            "source_agent_id": candidate.source_agent_id,
            "source_session_id": candidate.source_session_id,
            "extracted_at": candidate.extracted_at,
            "tags": candidate.tags,
            "notes": candidate.notes,
        }, ensure_ascii=False, indent=2), encoding="utf-8")

        logger.info(f"Skill document written: {doc_path}")
        return doc_path

    def _render_markdown(self, candidate: SkillCandidate) -> str:
        """渲染 agentskills.io 兼容的 Markdown 文档"""
        lines = [
            f"# {candidate.name}",
            "",
            f"> {candidate.description}",
            "",
            "---",
            "",
            "## Metadata",
            "",
            f"- **Version**: `{candidate.version}`",
            f"- **Confidence**: `{candidate.confidence}` ({candidate.confidence_reason})",
            f"- **Extracted at**: {candidate.extracted_at}",
            f"- **Source task**: `{candidate.source_task_id}`",
            "",
            "## Triggers",
            "",
        ]
        for t in candidate.triggers:
            lines.append(f"- `{t}`")

        lines += [
            "",
            "## Actions",
            "",
        ]
        for i, action in enumerate(candidate.actions, 1):
            lines.append(f"{i}. {action}")

        if candidate.examples:
            lines += [
                "",
                "## Examples",
                "",
            ]
            for ex in candidate.examples:
                lines.append(f"**Input:** {ex.get('input', '')}")
                lines.append(f"**Output:** {ex.get('output', '')}")
                lines.append("")

        if candidate.tags:
            lines += [
                "",
                "## Tags",
                "",
                ", ".join(f"`{t}`" for t in candidate.tags),
            ]

        if candidate.notes:
            lines += [
                "",
                "## Notes",
                "",
                candidate.notes,
            ]

        lines.append("")
        return "\n".join(lines)


# =============================================================================
# 梦境队列管理
# =============================================================================

class DreamingQueue:
    """
    低置信度 Skill 候选的梦境队列。

    以 JSONL（每行一条 JSON）追加写入，支持后续 Dreaming 引擎批量处理。
    """

    def __init__(self, queue_path: Path | str = DEFAULT_DREAM_QUEUE_PATH):
        self.queue_path = Path(queue_path)

    def add(self, candidate: SkillCandidate) -> None:
        """追加候选到梦境队列"""
        self.queue_path.parent.mkdir(parents=True, exist_ok=True)
        with self.queue_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({
                "name": candidate.name,
                "description": candidate.description,
                "confidence": candidate.confidence,
                "confidence_reason": candidate.confidence_reason,
                "triggers": candidate.triggers,
                "actions": candidate.actions,
                "examples": candidate.examples,
                "version": candidate.version,
                "source_task_id": candidate.source_task_id,
                "source_agent_id": candidate.source_agent_id,
                "source_session_id": candidate.source_session_id,
                "extracted_at": candidate.extracted_at,
                "tags": candidate.tags,
                "notes": candidate.notes,
                "dream_status": "pending",          # pending | dreaming | refined | discarded
                "dream_attempts": 0,
            }, ensure_ascii=False) + "\n")
        logger.debug(f"Added to dreaming queue: {candidate.name} (conf={candidate.confidence})")

    def read_pending(self, limit: int = 50) -> list[SkillCandidate]:
        """读取待处理的梦境候选"""
        if not self.queue_path.exists():
            return []
        candidates = []
        with self.queue_path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    if data.get("dream_status") == "pending":
                        candidates.append(SkillCandidate(
                            name=data["name"],
                            description=data.get("description", ""),
                            confidence=data.get("confidence", 0.0),
                            confidence_reason=data.get("confidence_reason", ""),
                            triggers=data.get("triggers", []),
                            actions=data.get("actions", []),
                            examples=data.get("examples", []),
                            version=data.get("version", "1.0.0"),
                            source_task_id=data.get("source_task_id", ""),
                            source_agent_id=data.get("source_agent_id", ""),
                            source_session_id=data.get("source_session_id", ""),
                            extracted_at=data.get("extracted_at", ""),
                            tags=data.get("tags", []),
                            notes=data.get("notes", ""),
                        ))
                        if len(candidates) >= limit:
                            break
                except json.JSONDecodeError:
                    continue
        return candidates


# =============================================================================
# 主钩子类
# =============================================================================

class ImmediateSkillHook:
    """
    即时 Skill 生成钩子 - 核心入口。

    使用方式：
        hook = ImmediateSkillHook(agent_id="agent-001")
        await hook.after_task_complete(task_result_dict)

    集成方式（在 Agent 执行完任务后调用）：
        async def run_task(task):
            result = await agent.execute(task)
            await hook.after_task_complete(result)   # <-- 即时钩子
            return result
    """

    HIGH_CONFIDENCE_THRESHOLD = 0.8  # 阈值可配置
    MEDIUM_CONFIDENCE_THRESHOLD = 0.5  # MEDIUM 入梦境队列，LOW 直接丢弃

    def __init__(
        self,
        agent_id: str = "",
        skills_dir: Path | str | None = None,
        dream_queue_path: Path | str | None = None,
        llm_callable=None,
        persist_to_memory: bool = True,
    ):
        """
        Args:
            agent_id: 当前 Agent ID（用于记录来源）
            skills_dir: Skill 文档输出目录
            dream_queue_path: 梦境队列文件路径
            llm_callable: LLM 推理函数，None 则强制规则提取
            persist_to_memory: 是否将候选同步写入 persistent_store（供 FTS 检索）
        """
        self.agent_id = agent_id
        self.skills_dir = skills_dir or DEFAULT_SKILLS_DIR
        self.dream_queue_path = dream_queue_path or DEFAULT_DREAM_QUEUE_PATH
        self.persist_to_memory = persist_to_memory

        self._writer = SkillDocumentWriter(self.skills_dir)
        self._queue = DreamingQueue(self.dream_queue_path)
        self._rule_extractor = RuleBasedExtractor()
        self._llm_extractor = LLMExtractor(llm_callable)

    async def after_task_complete(self, task_result: TaskResult | dict) -> SkillCandidate | None:
        """
        任务完成后的即时钩子。

        在任务成功完成后调用，立即触发 Skill 候选提取和分流逻辑。

        Args:
            task_result: TaskResult 实例或等效字典

        Returns:
            提取的 SkillCandidate，或 None（任务明显无价值时）
        """
        # 标准化输入
        if isinstance(task_result, dict):
            task_result = TaskResult.from_dict(task_result)
        if not task_result.content and not task_result.result:
            logger.debug("Empty task result, skipping skill extraction")
            return None

        # ---- Step 1: 提取候选 ----
        candidate = await self._extract_candidate(task_result)

        # ---- Step 2: 过滤极低价值任务 ----
        if candidate.confidence < 0.2:
            logger.debug(f"Confidence too low ({candidate.confidence}), discarding")
            return None

        # ---- Step 3: 分流路由 ----
        await self._route_candidate(candidate)

        # ---- Step 4: 可选：写入记忆系统（供后续 FTS 检索）----
        if self.persist_to_memory:
            await self._persist_candidate_memory(candidate)

        return candidate

    async def _extract_candidate(self, task_result: TaskResult) -> SkillCandidate:
        """提取 Skill 候选（LLM 优先，规则兜底）"""
        return await self._llm_extractor.extract(task_result)

    async def _route_candidate(self, candidate: SkillCandidate) -> None:
        """根据置信度路由到不同处理管道"""
        if candidate.confidence >= self.HIGH_CONFIDENCE_THRESHOLD:
            # 高置信度：直接写入 Skill 文档
            try:
                path = self._writer.write(candidate)
                candidate.notes = f"Written to {path}"
                logger.info(
                    f"[HIGH] Skill '{candidate.name}' written directly "
                    f"(conf={candidate.confidence})"
                )
            except Exception as exc:
                logger.error(f"Failed to write skill document: {exc}")
                # 写失败时降级到梦境队列
                self._queue.add(candidate)

        elif candidate.confidence >= self.MEDIUM_CONFIDENCE_THRESHOLD:
            # 中置信度：进入梦境队列
            self._queue.add(candidate)
            logger.debug(
                f"[MEDIUM] Candidate '{candidate.name}' queued for dreaming "
                f"(conf={candidate.confidence})"
            )
        else:
            # 低置信度：仅记录，不写入
            logger.debug(
                f"[LOW] Candidate '{candidate.name}' discarded "
                f"(conf={candidate.confidence})"
            )

    async def _persist_candidate_memory(self, candidate: SkillCandidate) -> None:
        """将候选信息持久化到记忆系统（供 FTS 检索）"""
        try:
            from .persistent_store import PersistentStore
            from .memory_core import (
                MemoryEntry,
                MemoryImportance,
                MemoryScope,
                MemoryType,
            )
            store = PersistentStore()

            entry = MemoryEntry(
                content=f"Skill: {candidate.name}\n{candidate.description}\n"
                        f"Actions: {' | '.join(candidate.actions)}",
                memory_type=MemoryType.PROCEDURE,
                scope=MemoryScope.SHARED,
                importance=MemoryImportance.HIGH if candidate.confidence >= 0.8
                           else MemoryImportance.MEDIUM,
                agent_id=candidate.source_agent_id or self.agent_id,
                tags=["skill-candidate", f"confidence:{candidate.confidence:.2f}"] + candidate.tags,
                summary=candidate.description,
                source="immediate_skill_hook",
            )
            store.store(entry)
            logger.debug(f"Skill candidate persisted to memory: {entry.entry_id}")
        except Exception as exc:
            # 记忆写入失败不影响 Skill 提取主流程
            logger.warning(f"Failed to persist skill candidate to memory: {exc}")


# =============================================================================
# 便捷工厂函数
# =============================================================================

def create_hook(
    agent_id: str = "",
    skills_dir: str | None = None,
    llm_callable=None,
) -> ImmediateSkillHook:
    """
    快速创建即时 Skill 钩子实例。

    Example:
        hook = create_hook(agent_id="agent-001")
        candidate = await hook.after_task_complete({"task_id": "t1", ...})
    """
    return ImmediateSkillHook(
        agent_id=agent_id,
        skills_dir=Path(skills_dir) if skills_dir else None,
        llm_callable=llm_callable,
    )
