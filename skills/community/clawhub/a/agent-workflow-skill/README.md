# Agent Workflow Skill

A modular AI agent runtime that converts natural language into a DAG (task graph) and executes it with parallel scheduling, tool-based execution, and context propagation.

---

## Overview

This project implements a simplified AI Agent execution system with:

- LLM-based task planning (natural language → structured DAG)
- Dependency-aware scheduling
- Parallel execution with thread pools
- Tool-based execution layer
- Context propagation between tasks

Unlike typical AI applications that only call APIs, this project focuses on the **execution layer of AI agents**.

---

## Architecture

```
+------------------+
|   User Input     |
+------------------+
          ↓
+------------------+
|   LLM Planner    |
|  (planner.py)    |
+------------------+
          ↓
+------------------+
|   Task Graph     |
|      (DAG)       |
+------------------+
          ↓
+------------------+
|    Executor      |
| (executor.py)    |
+------------------+
          ↓
+------------------+
|   Tool System    |
|  (tools.py)      |
+------------------+
          ↓
+------------------+
| Execution Output |
+------------------+
```

---

## Components

### planner.py
- Converts natural language into structured task graphs (DAG)
- Ensures valid JSON output via cleaning + validation

### executor.py
- DAG-based scheduler
- Parallel execution using ThreadPoolExecutor
- Dependency resolution
- Context propagation between tasks

### tools.py
- Modular tool registry system
- Decouples execution logic from scheduler

### utils.py
- Output cleaning (handles LLM formatting issues)
- Task validation (structure + dependency correctness)

---

## Example

### Input

```
Research AI agents and write a structured report
```

---

### Generated Task Graph

```json
[
  {"id": 1, "task": "search AI agents", "depends_on": []},
  {"id": 2, "task": "analyze results", "depends_on": [1]},
  {"id": 3, "task": "generate report", "depends_on": [2]}
]
```

---

### Execution Flow

```
Running: search ai agents
Completed: [SEARCH] result ...

Running: analyze results | [SEARCH result]
Completed: [ANALYZE] result ...

Running: generate report | [ANALYZE result]
Completed: [GENERATE] result ...
```

---

## Key Features

- DAG-based task orchestration  
- Parallel execution (multi-threading)  
- Tool-based execution system  
- Context-aware task chaining  
- LLM output cleaning + validation  
- Retry and fallback mechanisms  

---

## Design Highlights

### 1. DAG Execution Model
Tasks are executed only when dependencies are satisfied.

### 2. Parallel Scheduling
Independent tasks run concurrently, improving throughput.

### 3. Tool Registry System
Execution logic is modular and easily extensible.

### 4. Context Propagation
Each task consumes outputs from previous tasks.

### 5. Robust LLM Handling
Handles:
- markdown-wrapped outputs
- invalid JSON
- API failures

---

## Installation

```bash
git clone https://github.com/your-username/agent-workflow-skill
cd agent-workflow-skill
pip install -r requirements.txt
```

---

## Setup

Create `.env` file:

```
OPENAI_API_KEY=your_key_here
```

---

## Usage

```bash
python examples/demo_llm.py
```

---

## Why This Project

Most AI projects stop at calling APIs.

This project demonstrates:

- how agents plan tasks  
- how systems execute tasks  
- how to design scalable AI architecture  

---

## Future Work

- Integrate real tools (GitHub, Web APIs)
- Add memory (long-term context)
- Distributed execution (Celery / queue system)
- Async execution support

---

## Tech Stack

- Python
- OpenAI API
- ThreadPoolExecutor
- dotenv

---

## Author

Kewei Zhan  
USC MS Computer Engineering

---

## License

MIT