---
name: emergence-diagram-rendering
slug: emergence
title: Emergence Diagram Rendering
description: High-fidelity diagram generation (Mermaid, D2, Graphviz) for autonomous agents. Supports local-first rendering and persistent run history.
version: 1.1.0
author: Emergence Science
site: https://emergence.science
repository: https://github.com/emergencescience/emergence-diagram-rendering
requires:
  env:
    - EMERGENCE_API_KEY
  bin:
    - dot
    - d2
    - npm
---

# Diagram Rendering Skill (Internal Monologue)

You are an autonomous solver agent capable of transforming natural language into technical visuals. You prioritize **Local Rendering** for speed and privacy, using the Cloud API only as a fallback.

## 1. Activation Triggers
**Invoke this skill when the user asks to:**
- "Draw," "map out," or "diagram" a system.
- "Visualize" an architecture or cloud infrastructure.
- "Create a flowchart" or "sequence diagram."
- "Show me an ERD" or "database schema."

## 2. Decision Reasoning
- **D2**: Use for complex architecture, nested containers, and high-fidelity layouts.
- **Mermaid**: Use for standard flowcharts, sequence diagrams, and simple logic paths.
- **Graphviz (DOT)**: Use for mathematical graphs, network topologies, and relational ERDs.

## 3. Template-Assisted Generation
Before generating from scratch, check `./templates/`. 
- These are "Gold Standard" examples. 
- You can inject data into templates using the `--inject '{"key": "value"}'` flag in `local_render.py`.

## 4. Persistent Execution & Self-Correction
Your rendering attempts are stored in `./runs/<run_id>/`.
1. **Attempt Render**: Call `./.venv/bin/python3 scripts/local_render.py <engine> "<code>"`.
2. **Handle Failure**: If the output is an error, **open the `metadata.json`** in the specific run directory.
3. **Parse Stderr**: Read the compiler's `stderr`. It will pinpoint the exact line and character of your syntax error.
4. **Recursive Fix**: Use the error feedback to fix your code and re-run. Do not give up until the `status` is `"success"`.

## 5. Visual Verification (Vision Agents)
If you have a Vision Language Model (VLM) capability:
- Inspect the generated PNG/SVG in the run folder.
- Compare the visual output against the logical intent of the prompt.
- If the layout is confusing or logically incorrect, refine the code and re-render.
