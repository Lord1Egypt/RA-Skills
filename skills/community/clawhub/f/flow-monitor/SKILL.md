---
name: flow-monitor
description: Universal flow tracer with cross-platform date support, latency calculation, and token estimation.
author: Zven
version: 1.3.0
---

# FlowMonitor Universal

Professional execution tracing for OpenClaw/MCP environments.

## Instructions
1. Call `get_trace` via `bash scripts/trace.sh`.
2. **Post-Processing**:
   - **Latency**: Calculate the difference between `unix_time` of the current step and the previous step. Display as `+Xs`.
   - **Resource**: Display `estimated_tokens` as a measure of cost.
3. **LangSmith Visualization**:
   - Create a **Trace Table**: | Step | Time | Skill | Latency | Est. Tokens |
   - Create a **Mermaid Flow**: Use `sequenceDiagram` to show the timeline.

## Metadata Rules
- If `unix_time` is missing or 0, skip latency for that specific step.
- Use a ⏱️ icon for latency and a 🪙 icon for tokens.

## Commands
- `get_trace`: Run the shell script to fetch raw telemetry.

