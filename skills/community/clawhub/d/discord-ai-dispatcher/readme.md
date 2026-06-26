# Generic AI Dispatcher: The Official Guide

A high-precision, AI-augmented notification engine built for mission-critical pipelines. This repository contains the learnings of deploying local-AI dispatchers in production environments.

---

> [!CAUTION]
> **Operational Note**: This skill uses an "Automatic Healing" pattern. If state files are corrupted, the system repairs them immediately to maintain uptime. This is internally consistent with its goal of a persistent headless worker, but users should be aware that recovery often includes a "Backlog Re-sync" of recent history. Webhook secrets are stored locally in the `config/` directory.

*Designed for extensible and robust notification pipelines.*

---

## 🏗️ The "Zero-Leak" Architecture: Deterministic Sequential IDs

One of the most persistent challenges in AI notifications is **Classification Drift**—where the LLM incorrectly routes a high-priority update to the wrong channel. This dispatcher solves this by moving from AI-guessing to **Deterministic Routing & Sequential Tracking**.

### 🛑 Tier 1: Pattern-Based Routing (The "Prefix Pass")
Instead of letting the AI guess the channel, the dispatcher uses an ID prefix to force-route messages with 100% accuracy.
- **Prefixes**: Customizable prefixes (e.g., `systemupdate`, `appalert`, `user-notification`).
- **Logic**: Each prefix is hard-mapped to a specific webhook in `config/webhooks.json`.
- **Benefit**: Zero misrouted alerts for mission-critical data.

### 🔢 Tier 2: Sequential Deduplication (The "Numeric Pass")
To prevent duplicate notifications or out-of-order data overwrites:
1.  **Extract**: The script parses a numeric suffix from the ID (e.g., `10001`).
2.  **Compare**: Use **Numeric Comparison** (`[long]$curr -gt [long]$last`). Do NOT use string comparison (`CompareTo`), as it will fail on digits (e.g., it thinks `100` is smaller than `99`).
- **Benefit**: Ensures only the latest, most accurate sequence of events is broadcast, even if the API delivers old history during retries.

### 🛡️ Tier 3: Hardened Reliability & Locking
To ensure the dispatcher runs 24/7 without corruption:
1.  **Global Locking**: Implement an `orchestrator.lock` file. If a previous pulse is still formatting (due to AI latency), the next pulse will exit instead of starting a second conflicting process.
2.  **Corruption Recovery**: Wrap file-read operations in `try/catch` logic. If a state file is corrupted during a power loss, the script deletes it and re-initializes from the source.
3.  **Headless Cadence**: Use **Discrete Pulses** (Trigger -> Poll -> Dispatch -> Exit) via Windows Task Scheduler. This prevents memory bloat from long-running loops.

### 🎨 Phase 3: AI Formatting (The "Beautification Pass")
Once correctly routed and validated, a dedicated formatting call uses category-specific prompts to transform raw JSON into professional, bold-labeled messages.
- **Healing Cleaner**: Automatically repairs inconsistent AI output (missing bolding, bad colons) to maintain a premium visual feed.

---

## 📊 Dashboard Mode: "Self-Editing" Messages

Prevent chat clutter by transforming your channel into a living dashboard. Instead of posting new messages constantly, the dispatcher can **PATCH** an existing post to update it in real-time.

### Implementation Pattern:
1.  **Initialize**: The script checks a local state configuration for a stored message ID.
2.  **Post**: If no ID exists, it `POST`s a new message and saves the ID.
3.  **Update**: If an ID exists, it sends an `HTTP PATCH` to the relevant messaging API.
- **Advantage**: Chat history stays clean, providing a single "Source of Truth" for your system status.

---

## 🪙 Low AI COST Mode: Token Optimization
...
- **Pruning**: Use your script to strip irrelevant JSON keys (debug logs, internal UUIDs) before sending to the LLM.
- **Compressed Context**: Minimize the prompt by using strict list-based instructions instead of paragraphs.
- **Fallback Flow**: If the AI model is offline, the script uses a hard-coded fallback template, ensuring 0% downtime.

---

## 🧠 Smart Fidelity: Self-Correction & Auto-Healing

To ensure 100% notification delivery in production, the dispatcher includes an **Automated Fidelity Monitor** that audits the pipeline every 24 hours.

### 1. Gap Detection (Audit Mode)
The system performs a cross-reference between the **Database (Source of Truth)** and the **Dispatcher Log (Delivery Receipt)**.
- **Logic**: It fetches all IDs triggered today from the DB and checks if a corresponding "Delivered" entry exists in the log.
- **Goal**: Identify exactly which updates were missed, even if the poller thinks it finished successfully.

### 2. Self-Diagnostics: Root Cause Analysis (RCA)
For every detected gap, the system performs an automated RCA:
- **Logic Flaw**: Detects if an entry was "Skipped as Duplicate" but never actually delivered (indicating an ID state desync).
- **Transient Fault**: Detects LLM timeouts, network errors, or "Ollama busy" states.
- **Credential Fault**: Detects expired webhooks or 403 Forbidden errors.

### 3. The Healing Queue (Auto-Heal)
Once a gap is diagnosed, the system triggers a **Healing Pulse**:
1. **Fetch**: It re-fetches the original alert data from the source API.
2. **Inject**: It places the alerts into a specialized `healing-queue.json`.
3. **Bypass**: The dispatcher reads this queue and **force-delivers** the alerts, bypassing the standard duplicate filter for these specific IDs.

### 4. Emoji-Safe Transmission (UTF-8 Bytes)
To prevent character corruption (e.g., emojis turning into `??` or mangled symbols), always transmit webhook payloads as **UTF-8 Byte Streams** rather than raw strings, specifically in mixed PowerShell 5.1/7.0 environments.

---

## ⚙️ Automation & Reliability

---

## 💻 Environment Compatibility (PowerShell 5.1 vs 7.0)

When deploying on standard Windows Server or Desktop environments:
1.  **Hashtable Safety**: Avoid `-AsHashtable` (PS 6.0+). Use a recursive property-looping helper to load JSON state into Hashtables for reliable key-based access.
2.  **UT8 Enforcement**: Explicitly use `-Encoding UTF8` when saving state files to prevent character corruption.
3.  **Automation**: Run the orchestrator as a **Background Task** (`schtasks`) to ensure persistence across reboots.

---

## 📝 The "Do's and Don'ts" of Notification Engineering

### ✅ DO:
- **Bold Everything**: Property labels must always be bolded for high-density scanning.
- **Use Dividers**: Always end messages with visual separators for readability.
- **Tool-Calling First**: Use smart scripting for data fetching; use AI *only* for formatting.

### ❌ DON'T:
- **Don't Assume**: Never let the AI guess a channel based on unknown variables—hardcode it!
- **Avoid Preamble**: Use a cleaning pass to forcefully strip AI conversational filler ("Here is your alert", "Note:").
- **Heal the Output**: If the AI forgets to bold a label, use regex-based 'healing' to re-force standard formatting.

---

## 🐍 Smart Scripting Strategy

For advanced use cases, we recommend using scripts (Python/Node/PowerShell) for the "Intelligence" layer:
1.  **Logic**: Fetch data, join multiple API results, and calculate metrics.
2.  **AI Formatting**: Pass the *fully calculated* data to an LLM for final beautification only. This reduces the reasoning burden on the model and significantly speeds up delivery.

---

## 🛡️ Security & Operational Notes

The dispatcher follows a **Local-First** security model:
- **Secrets Storage**: All webhook URLs and configuration secrets are stored locally in `config/webhooks.json`. No external credential managers are used.
- **Auto-Repair Notice**: The system is designed for **High Availability**. If it detects a corrupted JSON state file (due to a crash or power loss), it will **automatically delete and re-initialize** the file. 
    - *Caveat*: This may trigger a one-time "Recovery Surge" where the system re-sends notifications from the last 24 hours to ensure no data was missed during the downtime. Review state files manually if you wish to skip historical re-syncs.

---

*Built for reliability and flexibility.*
