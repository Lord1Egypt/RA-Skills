"""SSE event parser and filter for ChatBI Agent.

基于 242 个真实事件的完整分析，精确提取关键信息。

真实数据结构要点：
- 格式: NDJSON（每行一个 JSON），非标准 SSE
- type="tool" 的关键数据在 data.payload 下
- type="answer" 是逐 token 流式碎片，需拼接
- is_final_answer 在 event.extra.is_final_answer 而非顶层
- sql_execution_tool 分两阶段: stage=1(SQL+计划), stage=2(结果数据)

Author: ChatBI Skills
Created: 2026-04-01
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from chatbi.models import (
    IntentResult,
    TableSelectResult,
    SQLResult,
    FinalAnswer,
    ChatBIResponse,
)


@dataclass
class FilteredResult:
    """单个被过滤出的关键事件."""

    category: str  # "intent" | "table_select" | "sql" | "final_answer"
    data: Dict[str, Any] = field(default_factory=dict)
    summary: str = ""


class SSEEventParser:
    """解析 ChatBI Agent 的流式事件，提取关键信息.

    Usage::

        parser = SSEEventParser()
        for event in client.stream_query("查询销售情况"):
            results = parser.process_event(event)
            for r in results:
                print(r.category, r.summary)

        response = parser.get_response()
    """

    def __init__(self):
        self._response = ChatBIResponse()
        self._raw_events: List[Dict[str, Any]] = []
        self._answer_chunks: List[str] = []  # 拼接 answer 流式碎片
        self._answer_finished = False

    def process_event(self, event: Dict[str, Any]) -> List[FilteredResult]:
        """处理单个流式事件，返回提取出的关键结果（可能为空列表）."""
        self._raw_events.append(event)
        results: List[FilteredResult] = []

        event_type = event.get("type", "")

        # ---- type="tool" ----
        if event_type == "tool":
            results.extend(self._process_tool_event(event))

        # ---- type="answer" → 流式碎片，逐块拼接 ----
        #   仅处理 extra.is_final_answer == "true" 的 answer 事件
        elif event_type == "answer":
            extra = event.get("extra", {})
            is_final = extra.get("is_final_answer") if isinstance(extra, dict) else None
            if is_final is True or str(is_final).lower() == "true":
                results.extend(self._process_answer_chunk(event))

        # ---- type="final" → 流结束标记 ----
        elif event_type == "final":
            # 如果有未 flush 的 answer，现在 flush
            if self._answer_chunks and not self._answer_finished:
                results.extend(self._flush_answer())

        return results

    def _process_tool_event(self, event: Dict[str, Any]) -> List[FilteredResult]:
        """处理 type="tool" 事件.

        真实结构:
            event.data = {
                "tool_name": "xxx",
                "status": "success",
                "payload": { ... 关键数据 ... },
                ...
            }
        """
        results: List[FilteredResult] = []

        data = event.get("data", {})
        if not isinstance(data, dict):
            return results

        tool_name = data.get("tool_name", "")
        payload = data.get("payload", {})
        if not isinstance(payload, dict):
            payload = {}

        # --- intent_tool ---
        if tool_name == "intent_tool":
            thinking = payload.get("understanding_thinking", "")
            if thinking:
                intent = IntentResult(
                    understanding_thinking=thinking,
                    raw_data=event,
                )
                self._response.intent = intent
                results.append(FilteredResult(
                    category="intent",
                    data={
                        "understanding_thinking": thinking,
                        "original_question": payload.get("original_question", ""),
                    },
                    summary=f"意图理解: {thinking}",
                ))

        # --- table_select_tool ---
        elif tool_name == "table_select_tool":
            reason = payload.get("table_selected_reason", "")
            selected_tables = payload.get("selected_tables", [])

            table_names = []
            for t in selected_tables:
                name = t.get("table_name", "") if isinstance(t, dict) else ""
                if name:
                    table_names.append(name)

            if table_names or reason:
                for name in (table_names or [""]):
                    ts = TableSelectResult(
                        table_name=name,
                        table_selected_reason=reason,
                        raw_data=event,
                    )
                    self._response.table_selections.append(ts)

                results.append(FilteredResult(
                    category="table_select",
                    data={
                        "table_names": table_names,
                        "table_selected_reason": reason,
                    },
                    summary=f"选表: {', '.join(table_names)} — {reason}",
                ))

        # --- sql_execution_tool (stage=1 和 stage=2) ---
        elif tool_name == "sql_execution_tool":
            stage = str(payload.get("stage", ""))
            sql_executed = payload.get("sql_executed", "")
            execution_plan = payload.get("execution_plan", "")
            data_preview_info = payload.get("data_preview_info")
            result_raw = payload.get("result_raw", "")

            sql_result = self._response.sql or SQLResult()

            if sql_executed:
                sql_result.sql_executed = sql_executed
            if execution_plan:
                sql_result.execution_plan = execution_plan
            if data_preview_info:
                sql_result.data_preview_info = data_preview_info
            if result_raw:
                sql_result.result_raw = result_raw
            sql_result.raw_data = event

            # stage=2 包含查询结果
            if stage == "2" and result_raw:
                sql_result.raw_data = event  # stage=2 优先

            self._response.sql = sql_result

            # 构建摘要
            if stage == "1":
                summary = f"SQL(stage=1): {sql_executed[:120]}..." if len(sql_executed) > 120 else f"SQL(stage=1): {sql_executed}"
            else:
                summary = f"SQL(stage=2): 执行完成，获得查询结果"
                if result_raw:
                    try:
                        rows = json.loads(result_raw) if isinstance(result_raw, str) else result_raw
                        if isinstance(rows, list) and len(rows) > 1:
                            summary += f"，{len(rows)-1} 行数据"
                    except (json.JSONDecodeError, TypeError):
                        pass

            results.append(FilteredResult(
                category="sql",
                data={
                    "stage": stage,
                    "sql_executed": sql_executed,
                    "execution_plan": execution_plan,
                    "data_preview_info": data_preview_info,
                    "result_raw": result_raw,
                },
                summary=summary,
            ))

        return results

    def _process_answer_chunk(self, event: Dict[str, Any]) -> List[FilteredResult]:
        """处理 type="answer" 流式碎片.

        真实结构:
            {"type": "answer", "data": "Fin", "finish_reason": "", "extra": {"is_final_answer": "true"}}
            ...
            {"type": "answer", "data": "的销售额对比。", "finish_reason": "stop", "extra": {...}}

        answer 是逐 token 输出，data 是文本碎片，需拼接。
        最后一条 finish_reason="stop" 标志结束。
        """
        chunk = event.get("data", "")
        if isinstance(chunk, str):
            self._answer_chunks.append(chunk)

        finish_reason = event.get("finish_reason", "")
        if finish_reason == "stop":
            return self._flush_answer()

        return []

    def _flush_answer(self) -> List[FilteredResult]:
        """拼接并输出完整的最终回答."""
        if self._answer_finished:
            return []

        self._answer_finished = True
        full_text = "".join(self._answer_chunks)

        # 去掉 "Final Answer: " 前缀（如有）
        clean_text = full_text
        for prefix in ["Final Answer: ", "Final Answer:", "final answer: "]:
            if clean_text.startswith(prefix):
                clean_text = clean_text[len(prefix):]
                break

        if clean_text.strip():
            answer = FinalAnswer(content=clean_text.strip(), raw_data={"full_text": full_text})
            self._response.final_answer = answer
            return [FilteredResult(
                category="final_answer",
                data={"content": clean_text.strip(), "raw_text": full_text},
                summary=f"最终回答: {clean_text.strip()[:200]}{'...' if len(clean_text.strip()) > 200 else ''}",
            )]

        return []

    def get_response(self) -> ChatBIResponse:
        """获取聚合后的完整响应.

        如果 answer 流没有收到 finish_reason=stop，也会尝试拼接已有碎片。
        """
        # 确保未 flush 的 answer 碎片被处理
        if self._answer_chunks and not self._answer_finished:
            self._flush_answer()

        self._response.raw_events = self._raw_events
        return self._response

    def reset(self) -> None:
        """重置解析器状态."""
        self._response = ChatBIResponse()
        self._raw_events = []
        self._answer_chunks = []
        self._answer_finished = False
