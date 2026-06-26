"""
claw-reliability: Gateway event parser.
Reads OpenClaw session transcripts (.jsonl) to extract metrics.
"""

import json
import os
import glob
from pathlib import Path
from datetime import datetime
from typing import Generator


class EventParser:
    def __init__(self, openclaw_state_dir="~/.openclaw"):
        self.state_dir = Path(os.path.expanduser(openclaw_state_dir))
        self.agents_dir = self.state_dir / "agents"
        self._last_positions = {}

    def discover_agents(self):
        if not self.agents_dir.exists():
            return []
        return [d.name for d in self.agents_dir.iterdir() if d.is_dir()]

    def discover_sessions(self, agent_id):
        sessions_dir = self.agents_dir / agent_id / "sessions"
        if not sessions_dir.exists():
            return []
        return sorted(glob.glob(str(sessions_dir / "*.jsonl")))

    def parse_transcript_incremental(self, filepath) -> Generator[dict, None, None]:
        last_pos = self._last_positions.get(filepath, 0)
        try:
            with open(filepath, 'r') as f:
                f.seek(last_pos)
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        raw = json.loads(line)
                        for parsed in self._classify_event(raw):
                            yield parsed
                    except json.JSONDecodeError:
                        continue
                self._last_positions[filepath] = f.tell()
        except (FileNotFoundError, PermissionError):
            pass

    def _classify_event(self, raw):
        """Classify a raw JSONL line into metric events. May yield multiple."""
        events = []
        raw_type = raw.get("type", "")

        # Session start
        if raw_type == "session":
            events.append({
                "event_type": "session_start",
                "timestamp": raw.get("timestamp", ""),
                "session_id": raw.get("id", ""),
                "agent_id": None,
            })
            return events

        # Message events contain the real data
        if raw_type != "message":
            return events

        msg = raw.get("message", {})
        role = msg.get("role", "")
        content = msg.get("content", [])
        timestamp = raw.get("timestamp", "")
        session_id = None  # We track this from the session event

        # Assistant messages: look for tool calls AND usage data
        if role == "assistant":
            # Extract tool calls
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "toolCall":
                        events.append({
                            "event_type": "tool_call_start",
                            "timestamp": timestamp,
                            "tool_name": block.get("name", "unknown"),
                            "tool_id": block.get("id", ""),
                            "params_summary": self._summarize_params(block.get("arguments", {})),
                            "session_id": session_id,
                            "agent_id": None,
                        })

            # Extract LLM usage (present on assistant messages)
            usage = msg.get("usage", {})
            if usage:
                tokens_in = (usage.get("input", 0) or 0) + (usage.get("cacheRead", 0) or 0)
                tokens_out = usage.get("output", 0) or 0
                cost_data = usage.get("cost", {})
                total_cost = cost_data.get("total", 0) if isinstance(cost_data, dict) else 0
                model = msg.get("model", "unknown")

                events.append({
                    "event_type": "llm_call",
                    "timestamp": timestamp,
                    "model": model,
                    "tokens_in": tokens_in,
                    "tokens_out": tokens_out,
                    "total_cost": total_cost,
                    "session_id": session_id,
                    "agent_id": None,
                })

        # Tool results
        if role == "toolResult":
            tool_name = msg.get("toolName", "unknown")
            tool_call_id = msg.get("toolCallId", "")
            is_error = msg.get("isError", False)
            content_text = ""

            if isinstance(content, list):
                content_text = " ".join(
                    b.get("text", "") for b in content if isinstance(b, dict))
            elif isinstance(content, str):
                content_text = content

            # Heuristic error detection
            if not is_error and content_text:
                error_signals = ["error", "failed", "exception", "traceback", "errno"]
                is_error = any(s in content_text.lower()[:300] for s in error_signals)

            events.append({
                "event_type": "tool_call_end",
                "timestamp": timestamp,
                "tool_name": tool_name,
                "tool_id": tool_call_id,
                "success": not is_error,
                "error_message": content_text[:500] if is_error else None,
                "session_id": session_id,
                "agent_id": None,
            })

        return events

    def _summarize_params(self, params, max_length=200):
        if not params:
            return ""
        try:
            s = json.dumps(params)
            return s[:max_length] + "..." if len(s) > max_length else s
        except (TypeError, ValueError):
            return str(params)[:max_length]

    def scan_all(self) -> Generator[dict, None, None]:
        for agent_id in self.discover_agents():
            for session_file in self.discover_sessions(agent_id):
                for event in self.parse_transcript_incremental(session_file):
                    yield event
