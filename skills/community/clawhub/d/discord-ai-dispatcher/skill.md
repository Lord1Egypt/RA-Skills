# Generic Webhook Notifier: Advanced Skill Guide

The **Webhook Notifier** skill provides a robust architecture that combines hard heuristics with local AI reasoning tools to ensure 100% routing accuracy and high-density visual formatting.

---

## 🚀 The High-Consistency Architecture: Deterministic Routing

Instead of relying solely on AI categorization, this dispatcher implements a **Deterministic Prefix Engine** to ensure 100% routing accuracy:
1.  **Prefix Identification**: An `updateId` (e.g., `systemevent00100`) directly dictates the target channel.
    - `systemevent` -> **Infrastructure Events**
    - `appalert` -> **Application Monitoring**
    - `userupdate` -> **User Activity**
2.  **Zero-Guessing**: This removes "Classification Drift" where an AI might misinterpret an update, ensuring data always reaches the correct stakeholders.

---

## 🔢 Deterministic Sequential Deduplication

To handle out-of-order API deliveries or network retries, the dispatcher uses a **Sequential State Tracker**:
- **Logic**: It extracts a numeric suffix from the ID (the `XXXXX` in `prefixXXXXX`).
- **State**: The highest seen ID for each category is stored locally.
- **Rule**: Use **Numeric Comparison** (`100 > 99`) instead of Alphabetical (`100 < 99`). Regex-extract digits `[^\d]` and cast to `[long]` to ensure the sequence advances even as ID lengths change.
- **Result**: You never see a stale update overwrite new data, and duplicate notifications are prevented.

---

## 🔒 Global Pipeline Locking (Self-Protection)

To prevent race conditions and file corruption when the AI takes longer than the polling interval:
1.  **Lock File**: Create a `dispatcher.lock` at the start of the orchestrator.
2.  **Abort Logic**: If a lock exists and is "fresh" (< 30 mins), the next pulse must exit immediately.
3.  **Atomic Recovery**: Always use `try/finally` blocks to ensure the lock is released even if the script crashes.

---

## 🏗️ Self-Healing JSON Recovery

State files can be corrupted by power loss or interrupted writes.
1.  **Integrity Checks**: Wrap every `ConvertFrom-Json` call in a `try/catch`.
2.  **Auto-Reset**: If parsing fails, log the corruption, delete the broken file, and re-initialize the state from the API source.
- **Benefit**: The system self-recovers from disk errors without manual developer intervention.

---

## 🩹 The "Healing Cleaner" Pattern

Instead of a "Negative Filter" (which deletes bad formatting), this skill uses a **Positive Healing** logic to repair inconsistent AI output:
1.  **Label Extraction**: It scans for colons and automatically wraps the text before them in `**Bold Labels**`.
2.  **Normalization**: It forcefully standardizes fluctuating terms to established vocabulary.
3.  **Noise Blacklist**: It aggressively strips AI conversational filler.
4.  **Artifact Stripping**: It cleans up redundant formatting artifacts (`** **`), escaped characters, and unwanted markdown blocks.
- **Result**: You get a professional, uniform feed even if the AI model gets "creative".

---

## 📊 Dashboard Mode (Clean Chat Strategy)

Prevent chat clutter by updating existing messages instead of posting new ones.
1.  **Logic**: Use `PATCH` (or corresponding update paradigm) instead of `POST` for webhooks.
2.  **State**: Store the created message ID in a local state file. 
- **Advantage**: Provides a single "Living" source of truth for your system status without generating unnecessary notification spam.

---

## 🪙 Token & Cost Optimization
...
- **Payload Pruning**: Strip all non-essential JSON keys before the AI sees them.
- **Compressed Instructions**: Use strict list-based prompts instead of paragraphs.
- **Low Effort Fallback**: If the AI is offline, use a hardcoded template for high availability.

---

## 🧠 The AI Improvement Layer: Learning From Gaps

The Webhook Notifier is built to be a self-improving system. When a gap is found, the agent must shift from **Monitor** to **Diagnostician**:

### 1. The RCA Feed (Log Diagnostics)
Instead of guessing, the agent must scan the `dispatcher.log` for the "Missing IDs":
-   **Skipped (`duplicate`) but not Delivered**: Indicates the deduplication logic was too aggressive (Historical Logic Flaw).
-   **Timeout**: Indicates the Local LLM needs a higher timeout or more GPU resources.
-   **No Log Record**: Indicates a failure at the Poller or API fetch stage.

### 2. Strategic Improvement Loop
When the user feeds you an RCA report, you should automatically suggest (or implement) one of the following:
1.  **State Realignment**: Resetting `last-seen-ids.json` or `polling-state.json` to the actual last-delivered marker to ensure the "Gaps" are re-sent.
2.  **Logic Tuning**: If sequential IDs are conflicting with timestamp IDs, adjust the `Test-IsSequentialDuplicate` helper to be more specific.
3.  **High-Precision Recovery**: Creating a one-time "Healing Queue" to force-inject missed notifications into Discord.

### 🛡️ Recovery Best Practices:
-   **Bypass Deduplication**: When in "Heal Mode", always bypass the `Test-IsSequentialDuplicate` filter to ensure recovery happens.
-   **Audit History**: Perform a "Log Audit" before making changes. Never assume a file is missing just because it's not in the DB—always check the logs to confirm if the Dispatcher ever saw it.

---

## 🎨 Best Practices for Professional Formatting

To maintain aesthetics and readability:
- **Mandatory Bolding**: Always wrap labels in visual emphasis (e.g., **Key**: Value).
- **Horizontal Dividers**: Every notification should logically separate from the next.
- **Tool-Calling First**: Calculate your metrics in code; use the AI *only* for the final beautification.

---

## ⚙️ Automation & Version Compatibility

- **Scheduling Reliability**: Use **Headless Discrete Execution** (Windows Task Scheduler / Cron). Avoid infinite `while($true)` loops to prevent memory leaks and handle system reboots gracefully.
- **PowerShell 5.1 Compatibility**: 
    - **Hashtables**: Modern PS 7.0 `-AsHashtable` fails in 5.1. Use manual property-looping to convert PSCustomObjects into Hashtables for reliable `$state[$key]` access.
    - **Encoding**: Always specify `-Encoding UTF8` on `Set-Content` to prevent character corruption in mixed-version environments.
- **Webhook First**: Always provide users the option to setup webhooks immediately after configuring the skill for instant "out-of-box" operation.

---

*Designed for extensible and robust notification pipelines.*
