"""Data models for ChatBI Agent responses.

Author: ChatBI Skills
Created: 2026-04-01
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class IntentResult:
    """意图理解结果 — 来自 intent_tool."""

    understanding_thinking: str = ""
    raw_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TableSelectResult:
    """选表结果 — 来自 table_select_tool."""

    table_name: str = ""
    table_selected_reason: str = ""
    raw_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SQLResult:
    """SQL 执行结果 — 来自 tool 事件中的 sql_executed 等."""

    sql_executed: str = ""
    execution_plan: str = ""
    data_preview_info: Any = None
    result_raw: Any = None
    raw_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FinalAnswer:
    """最终回答 — is_final_answer=true 且 type=answer."""

    content: str = ""
    raw_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChatBIResponse:
    """完整的 ChatBI 问数响应，聚合所有关键信息."""

    intent: Optional[IntentResult] = None
    table_selections: List[TableSelectResult] = field(default_factory=list)
    sql: Optional[SQLResult] = None
    final_answer: Optional[FinalAnswer] = None

    # 原始事件列表（调试用）
    raw_events: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def has_sql(self) -> bool:
        return self.sql is not None and bool(self.sql.sql_executed)

    @property
    def has_answer(self) -> bool:
        return self.final_answer is not None and bool(self.final_answer.content)

    def summary(self) -> str:
        """生成简洁的摘要文本."""
        parts = []

        if self.intent and self.intent.understanding_thinking:
            parts.append(f"【意图理解】\n{self.intent.understanding_thinking}")

        if self.table_selections:
            parts.append("【选表结果】")
            for ts in self.table_selections:
                parts.append(f"  表名: {ts.table_name}")
                if ts.table_selected_reason:
                    parts.append(f"  原因: {ts.table_selected_reason}")

        if self.sql and self.sql.sql_executed:
            parts.append(f"【SQL】\n{self.sql.sql_executed}")
            if self.sql.execution_plan:
                parts.append(f"【执行计划】\n{self.sql.execution_plan}")

        if self.final_answer and self.final_answer.content:
            parts.append(f"【最终回答】\n{self.final_answer.content}")

        return "\n\n".join(parts) if parts else "(无有效结果)"
