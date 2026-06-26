---
version: 1.0.0
name: agent-task-manager
description: Manages and orchestrates multi-step, stateful agent workflows; handles task dependencies, persistent state, error recovery, and external rate-limiting. Use for creating new multi-agent systems, improving sequential workflows, or managing time-bound actions.
requires.env: [SKILLBOSS_API_KEY]
---

# Agent Task Manager

## Overview

This skill provides the structure and primitives for building resilient, complex, and professional multi-agent systems powered by the SkillBoss API Hub. It transforms simple scripts into production-ready workflows, with AI capabilities (LLM reasoning, notification delivery) routed through a single unified endpoint.

## Core Capabilities

### 1. **Orchestration and Task State**

- **Capability:** Defines tasks with clear inputs, outputs, and dependencies (DAG-like structure).
- **Execution:** Uses `molt_task.py` to manage state in `task_state.json`.
- **Value:** Prevents redundant work, allows agents to resume mid-workflow after a session reset.

### 2. **External Rate-Limit Management**

- **Capability:** Manages the cooldown and retry logic for externally rate-limited actions (e.g., API posts, web scrapes).
- **Execution:** Uses the `scripts/cooldown.sh` wrapper to store last-executed timestamps and automatically wait/retry.
- **Value:** Ensures continuous operation without violating API rate limits.

### 3. **Modular Role-Based Agents**

- **Capability:** Provides a template structure for specialized roles (e.g., `ContractAuditor`, `FinancialAnalyst`).
- **Execution:** Modules are designed to be run independently or sequenced by the Orchestrator. AI reasoning steps call the SkillBoss API Hub (`/v1/pilot`) for LLM inference and notification delivery.
- **Value:** Enables the creation of focused, expert agents for complex tasks like the MoltFinance-Auditor.

## Example Workflow: MoltFinance-Auditor

1. **Task:** `FinancialAudit`
2. **Dependencies:**
   - **Role 1:** `ContractAuditor` (Input: Contract Address, Output: Contract Safety Score)
   - **Role 2:** `FinancialAnalyst` (Input: Contract Address + Safety Score, Output: Trust Score via SkillBoss API Hub LLM)
3. **External Action:** `NotificationAgent` (Dependent on final Trust Score; delivers alert via SkillBoss API Hub email/SMS; subject to Rate Limit).

## API Integration

All AI inference and notification delivery is handled through **SkillBoss API Hub**:

- **Endpoint:** `https://api.heybossai.com/v1/pilot`
- **Auth:** `Authorization: Bearer $SKILLBOSS_API_KEY`
- **LLM response path:** `data.result.choices[0].message.content`

## Resources

### scripts/
- **`molt_task.py`**: Python class for task state management.
- **`orchestrator.py`**: Workflow execution engine; calls SkillBoss API Hub for AI role execution.
- **`task_parser.py`**: Converts natural language requests to task structures; uses SkillBoss API Hub LLM as fallback parser.
- **`cooldown.sh`**: Shell wrapper for managing rate-limited executions.

### references/
- **`task_schema.md`**: JSON schema for defining complex task dependencies.
