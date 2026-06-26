---
name: task-graph-executor
description: Decompose complex user tasks into multi-step workflows using DAG-based execution.
version: 1.0.0
---

# Task Graph Executor

## When to use

Use this skill when tasks involve multiple steps or dependencies.

Examples:
- Analyze a repo and summarize it
- Research a topic and generate a report
- Process data and visualize results

---

## What this skill does

This skill enables the AI to:

1. Break down complex tasks
2. Build a dependency graph (DAG)
3. Execute tasks in order
4. Parallelize independent steps
5. Return structured results

---

## Execution Strategy

### Step 1: Decompose Task

Convert user request into subtasks.

Example:

User: "Analyze repo and summarize"

Tasks:
- clone repo
- analyze code
- generate summary

---

### Step 2: Build DAG

- Identify dependencies
- Ensure correct execution order

---

### Step 3: Execute

- Run independent tasks first
- Wait for dependencies
- Execute in parallel when possible

---

### Step 4: Output

Return structured result:

{
  "tasks": [],
  "result": "",
  "status": "success"
}

---

## Goal

Enable multi-step task execution instead of single tool calls.
