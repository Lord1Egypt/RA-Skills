# Drift Guard — Limitations

This document honestly describes what Drift Guard **does not** do.

---

## What Drift Guard Does NOT Do

### 1. **Automatic Remediation**
Drift Guard **detects** drift. It does not automatically fix it.

- It will not restore your agent from checkpoint
- It will not modify memory files
- It will not rollback context changes
- It will not reset configurations

**Why:** Automatic remediation is dangerous. Different situations require different fixes. Detection and action are kept separate intentionally.

**Pairing:** Use CPR (Context Preservation & Restore) for remediation after Drift Guard detects the problem.

---

### 2. **Root Cause Analysis**
Drift Guard tells you **that** drift happened and **what** changed. It does not tell you **why**.

- It will not identify which memory file caused the drift
- It will not pinpoint which conversation corrupted context
- It will not tell you which config change triggered the problem

**Why:** Root cause analysis requires context beyond text metrics—file histories, conversation logs, user interactions.

**Workaround:** Correlate drift timestamps with your agent's activity logs to identify causes.

---

### 3. **Semantic Understanding**
Drift Guard analyzes **patterns**, not **meaning**.

- It counts words, not ideas
- It detects phrase patterns, not intent
- It measures vocabulary, not correctness

**Why:** Semantic analysis requires large language models or complex NLP libraries. Drift Guard is stdlib-only and lightweight.

**Implication:** False positives are possible. A legitimately helpful response might trigger sycophancy alerts if it uses validation language appropriately.

---

### 4. **Real-Time Inline Monitoring**
Drift Guard requires you to **explicitly** analyze responses. It does not hook into your agent runtime.

- It will not automatically intercept agent responses
- It will not run in the background without being called
- It will not monitor agents you don't explicitly point it at

**Why:** Runtime hooks are invasive and platform-specific. Drift Guard is designed as a standalone tool you control.

**Workaround:** Integrate via cron jobs, wrapper scripts, or manual analysis.

---

### 5. **HTTP Webhooks (in stdlib-only version)**
The configuration includes `webhook_url`, but **HTTP POST is not implemented** in the stdlib-only version.

**Why:** Python's stdlib `urllib` can do HTTP, but adding full webhook support (retries, authentication, error handling) would balloon the codebase.

**Workaround:** Monitor `current_alert.json` or `drift_alerts.log` with external tools, or extend Drift Guard with `requests` library for production webhook use.

---

### 6. **Multi-Language Support**
Drift Guard's patterns are **English-centric**.

- Sycophancy patterns assume English phrasing
- Hedging patterns assume English grammar
- Vocabulary analysis assumes Latin script

**Why:** Internationalization requires language-specific pattern libraries and tokenization.

**Workaround:** Customize patterns in `config.py` for your language, or use Drift Guard as a template and adapt the pattern logic.

---

### 7. **Baseline Recommendation**
Drift Guard will not tell you **when** to capture a new baseline or **which** responses make a good baseline.

**Why:** "Healthy" behavior is user-defined and context-specific. Only you know what your agent should sound like.

**Guidance:** Capture baseline from 10-20 responses when your agent is performing well and behaving as intended. Recapture when you deliberately change agent personality or capabilities.

---

### 8. **Drift Prevention**
Drift Guard **detects** drift after it happens. It does not **prevent** drift from happening.

**Why:** Prevention requires controlling the agent's context, memory, and training—well outside Drift Guard's scope.

**Complementary tools:**
- **Canary** (safety tripwires) prevents unauthorized file access
- **CPR** (checkpoints) enables quick recovery
- **Forge** (workspace hygiene) prevents context corruption

---

### 9. **Performance Optimization**
Drift Guard is **not optimized** for high-throughput or low-latency analysis.

- It processes one response at a time
- It writes to disk on every measurement
- It loads full history for reporting

**Why:** Optimization adds complexity. Drift Guard prioritizes simplicity and reliability over speed.

**Implication:** Fine for human-scale agent monitoring. May not scale to analyzing thousands of responses per second.

---

### 10. **Model-Specific Tuning**
Drift Guard does not know which AI model your agent uses and does not adjust its analysis accordingly.

- GPT-4 vs Claude vs Llama: all analyzed the same way
- Fine-tuned models: treated like base models
- Model version changes: not detected automatically

**Why:** Model-agnostic design keeps Drift Guard portable and simple.

**Implication:** You may need to adjust thresholds and patterns when changing models.

---

## What You Should Combine It With

| Tool | Purpose | Pairing Benefit |
|------|---------|-----------------|
| **CPR** | Checkpoint & restore | Detect drift (Drift Guard) → Restore (CPR) |
| **Canary** | Safety boundaries | Prevent bad behavior → Detect personality change |
| **Forge** | Workspace cleanup | Clean workspace → Monitor for re-contamination |
| **Manual review** | Human judgment | Metrics show drift → You decide if it's bad |

---

## Philosophy

Drift Guard does **one thing well**: quantify behavior change over time.

It does not try to be an all-in-one agent management suite. It does not replace human judgment. It is a measurement tool, not a decision-maker.

Use it as part of a broader agent health monitoring strategy, not as the entire strategy.
