---
title: Gemma 4 Developer Tool
description: A development and orchestration skill for working with the Gemma 4 model family, supporting thinking modes and multi-step agentic workflows.
version: 1.0.0
authors:
  - OpenClaw Team
keywords:
  - gemma
  - gemma4
  - coding
  - agent
  - ai
license: MIT
---

# Gemma 4 Developer Tool

A comprehensive development and orchestration skill for working with the Gemma 4 model family. This skill provides specialized capabilities for complex coding tasks, long-context reasoning, and multi-step agentic workflows.

## Key Features
- **Model Selection**: Intelligent routing and configuration for different model sizes (e.g., Gemma 4 9B/12B).
- **Thinking Mode**: Enables high-inference "reasoning" steps before final output to solve complex logic or coding problems.
- **Advanced Coding**: Optimized instructions for system architecture, refactoring, and debugging.
- **Agentic Workflows**: Supports multi-turn planning and tool execution chains.

## Usage
Use this skill when requiring deep technical analysis, heavy coding implementation, or when the task requires the model to "think" through a problem before generating code.

## Configuration
- `thinking_mode`: boolean (default: true)
- `model_size`: string ("9b", "12b")
- `context_window`: auto (based on selected model)

## Security
This skill is designed to operate within the OpenClaw sandbox. It avoids direct raw shell evaluation where possible and validates agent inputs for tool calls.
