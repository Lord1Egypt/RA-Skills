"""Output formatter for ChatBI Agent results.

Author: ChatBI Skills
Created: 2026-04-01
"""

from __future__ import annotations

import json
from typing import Optional, List

from chatbi.models import ChatBIResponse
from chatbi.parser import FilteredResult


class ResultFormatter:
    """格式化 ChatBI 结果输出."""

    def __init__(self, output_mode: str = "summary"):
        self.output_mode = output_mode

    def format_event(self, result: FilteredResult) -> Optional[str]:
        """格式化单个过滤结果为终端输出文本."""
        if self.output_mode == "sql-only":
            if result.category == "sql" and result.data.get("sql_executed"):
                return result.data["sql_executed"]
            return None

        if self.output_mode == "raw":
            return json.dumps(result.data, ensure_ascii=False, indent=2)

        # summary / detail 模式
        if result.category == "intent":
            thinking = result.data.get("understanding_thinking", "")
            question = result.data.get("original_question", "")
            lines = [f"\n{'=' * 60}", "  🧠 意图理解", "=" * 60]
            if question:
                lines.append(f"  原始问题: {question}")
            lines.append(f"  {thinking}")
            return "\n".join(lines)

        elif result.category == "table_select":
            names = result.data.get("table_names", [])
            reason = result.data.get("table_selected_reason", "")
            lines = [f"\n{'─' * 60}", "  📋 选表结果", "─" * 60]
            for name in names:
                lines.append(f"  表名: {name}")
            if reason:
                lines.append(f"  原因: {reason}")
            return "\n".join(lines)

        elif result.category == "sql":
            return self._format_sql_event(result)

        elif result.category == "final_answer":
            content = result.data.get("content", "")
            lines = [f"\n{'=' * 60}", "  ✅ 最终回答", "=" * 60, f"  {content}"]
            return "\n".join(lines)

        return None

    def _format_sql_event(self, result: FilteredResult) -> Optional[str]:
        """格式化 SQL 事件（区分 stage=1 和 stage=2）."""
        stage = result.data.get("stage", "")
        sql = result.data.get("sql_executed", "")
        plan = result.data.get("execution_plan", "")
        result_raw = result.data.get("result_raw", "")
        preview = result.data.get("data_preview_info")

        parts: List[str] = []

        if stage == "1":
            # Stage 1: SQL 生成 + 执行计划
            parts.append(f"\n{'=' * 60}")
            parts.append("  🔍 SQL 生成 (stage=1)")
            parts.append("=" * 60)
            if sql:
                parts.append(f"```sql\n{sql}\n```")
            if plan:
                parts.append(f"\n  📊 执行计划: {plan}")

        elif stage == "2":
            # Stage 2: 执行结果
            parts.append(f"\n{'─' * 60}")
            parts.append("  📦 SQL 执行结果 (stage=2)")
            parts.append("─" * 60)

            # 解析 result_raw 为表格
            if result_raw:
                table_str = self._format_result_table(result_raw)
                if table_str:
                    parts.append(table_str)

            # detail 模式才显示 data_preview_info
            if self.output_mode == "detail" and preview:
                if isinstance(preview, (dict, list)):
                    parts.append(f"\n  数据预览详情:\n{json.dumps(preview, ensure_ascii=False, indent=2)}")
                else:
                    parts.append(f"\n  数据预览: {str(preview)[:500]}")
        else:
            # 未知 stage
            if sql:
                parts.append(f"\n  🔍 SQL: {sql}")

        return "\n".join(parts) if parts else None

    def _format_result_table(self, result_raw: str) -> Optional[str]:
        """将 result_raw 格式化为 ASCII 表格.

        result_raw 格式: [["col1","col2",...], ["val1","val2",...], ...]
        第一行是表头，后续行是数据。
        """
        try:
            rows = json.loads(result_raw) if isinstance(result_raw, str) else result_raw
        except (json.JSONDecodeError, TypeError):
            return f"  (原始数据: {str(result_raw)[:200]})"

        if not isinstance(rows, list) or len(rows) < 2:
            return None

        headers = [str(h) for h in rows[0]]
        data_rows = rows[1:]

        # 计算列宽
        col_widths = [len(h) for h in headers]
        for row in data_rows:
            for i, val in enumerate(row):
                if i < len(col_widths):
                    col_widths[i] = max(col_widths[i], len(str(val)))

        # 构建表格
        def _fmt_row(vals: list) -> str:
            # 补齐列数不足的行
            padded = []
            for i in range(len(col_widths)):
                v = str(vals[i]) if i < len(vals) else ""
                padded.append(v.ljust(col_widths[i]))
            return "  " + " | ".join(padded)

        lines = []
        lines.append(_fmt_row(headers))
        lines.append("  " + "-+-".join("-" * w for w in col_widths))
        for row in data_rows:
            lines.append(_fmt_row(row))

        return "\n".join(lines)

    def format_raw_event(self, event: dict) -> str:
        """格式化原始事件."""
        return json.dumps(event, ensure_ascii=False, indent=2)

    def format_response(self, response: ChatBIResponse) -> str:
        """格式化完整响应."""
        if self.output_mode == "sql-only":
            return response.sql.sql_executed if response.has_sql else "(未生成 SQL)"
        return response.summary()

    def format_stream_header(self, question: str) -> str:
        return (
            f"\n{'=' * 60}\n"
            f"  ChatBI 问数 Agent\n"
            f"  问题: {question}\n"
            f"{'=' * 60}"
        )

    def format_stream_footer(self, response: ChatBIResponse) -> str:
        parts = [f"\n{'=' * 60}", "  📋 执行摘要", "─" * 60]
        parts.append(f"  意图理解: {'✅' if response.intent else '❌'}")
        parts.append(f"  选表数量: {len(response.table_selections)}")
        parts.append(f"  SQL 生成: {'✅' if response.has_sql else '❌'}")
        parts.append(f"  最终回答: {'✅' if response.has_answer else '❌'}")
        parts.append(f"  总事件数: {len(response.raw_events)}")
        parts.append("=" * 60)
        return "\n".join(parts)
