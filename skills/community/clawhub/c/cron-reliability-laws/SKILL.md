---
name: "cron-reliability-laws"
description: "Hard rules for Cron reliability: Shell-First architecture, mandatory wrappers (flock/logging), and LLM constraints to prevent timeouts and token-waste."
---

# 🛡️ The Laws of Cron Reliability (LCR)
**Purpose:** To eliminate stochastic failures (timeouts, LLM hallucinations) and token-waste in scheduled tasks.

## ⚖️ Law I: The Determinism Mandate (Shell-First)
**Any task that can be executed via a deterministic script MUST be a `systemEvent` calling a Shell-Wrapper.**
- ❌ **Forbidden:** Using `agentTurn` to "Run a script and tell me if it failed."
- ✅ **Required:** Use `systemEvent` → `Wrapper.sh` → `Logic.py/sh`.
- **Logic:** If the outcome is binary (Success/Failure) or data-driven, the LLM is a liability, not an asset.

## ⚖️ Law II: The Wrapper Standard (The Holy Trinity)
Every shell-based cron job MUST be wrapped in a standardized handler that implements:
1. **Atomic Locking (`flock`):** Prevent job overlap and resource exhaustion.
2. **Absolute Environment:** Explicit `PATH` and `.env` sourcing to prevent "Command not found".
3. **Centralized Logging:** All output must be redirected to `logs/cron/<job_name>.log`.

## ⚖️ Law III: The Reasoning Constraint (LLM-Sizing)
LLMs are permitted in crons ONLY for high-level reasoning (e.g., Reflection, Optimization).
- **Constraint A:** Must use `isolated` session target.
- **Constraint B:** Must use `lightContext: true` to prevent token-bloat.
- **Constraint C:** Must be assigned to the smallest capable model (e.g., a small model for simple formatting, a large model only for complex analysis).

## ⚖️ Law IV: The Silent-by-Default Principle
Cron jobs must remain silent unless a failure occurs.
- **Success:** Log to file → Exit 0 → No notification.
- **Failure:** Log to file → Exit 1 → Trigger alert to your alert channel.

## ⚖️ Law V: The Audit Requirement
Every recurring task must be measurable.
- **Requirement:** An audit script calculates the **Success Rate** and **Token-Impact** per job.
- **Review:** Stability reports must be generated and reviewed periodically to identify "Degrading Jobs".