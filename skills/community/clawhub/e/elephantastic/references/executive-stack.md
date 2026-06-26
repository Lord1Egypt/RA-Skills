---
version: 1.0.0
last_updated: 2026-03-28
status: experimental
---

# Sovereign Agent Executive Stack (v1)

## Overview
The Sovereign Agent Executive Stack is a local-first, privacy-respecting system for managing AI agency. It uses **Taskwarrior** as the "Cognitive Brain" (Goal Management) and **Pueue** as the "Worker Body" (Execution Queue).

## Core Philosophy: The Parallel Mind
Most agents are blocking—they can't do two things at once. This stack enables **Asynchronous Agency**. The agent decides on a goal, offloads the heavy lifting to a background queue, and remains available for new instructions or strategic pivots.

## Components

### 1. Taskwarrior (The Executive Brain)
- **Role:** Goal tracking, urgency weighting, and project management.
- **Benefit:** Provides a persistent "memory" of what needs to be done, even across session restarts.
- **Workflow:** Agents triage incoming requests into Taskwarrior to prevent "Digital Amnesia."

### 2. Pueue (The Executioner)
- **Role:** Background task runner and log streamer.
- **Benefit:** Allows the agent to run long-running tasks (scraping, coding, data processing) without blocking the main interaction loop.
- **Safety:** Built-in resource management (parallel execution limits) prevents the agent from overwhelming the host system.

### 3. The Bridge (Automation Hook)
- **Role:** A Python-based hook (`on-modify`) that monitors Taskwarrior state changes.
- **Logic:** Marking a task as `active` in Taskwarrior automatically injects its `pueue_cmd` into the Pueue queue.

## Value Proposition for Customers
1. **Durable Agency:** Work survives system crashes and agent restarts.
2. **Transparent Operations:** High-fidelity "Flight Recorder" logs for auditing AI activity.
3. **Total Privacy:** Zero reliance on cloud-based task managers (Zapier, Trello, etc.).
4. **Efficiency:** Minimal effort, maximum leverage (The Judo Principle).

## Next Steps for Development
- [ ] Implement `pueue_cmd` auto-generation based on task description.
- [ ] Create a "Heartbeat" skill that pings the user when a background Pueue task fails.
- [ ] Develop a "Digest" function that summarizes Pueue execution logs back into Taskwarrior annotations.

---
*Created by Talena for the Sovereign Agent Project | 2026-02-17*
