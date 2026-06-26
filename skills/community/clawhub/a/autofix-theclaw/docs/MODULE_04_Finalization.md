---
name: MODULE_04_Finalization
description: Handles the wrap-up of the resolution cycle (Step 5). This ensures that every interaction contributes to long-term knowledge by saving facts, learning lessons, and updating the session state. It now integrates L2 Hot Start Querying & L3 Skill Creation Suggestion.
---

# 💾 Step 5: Finalization & Memory Update (Level 2 & 3 Active)

**Goal:** To ensure continuity across sessions by persisting all relevant information derived from the problem-solving process into OpenClaw's memory structure, while proactively suggesting next steps and new tools.

## 📝 Action Sequence
This module executes a sequence of three critical memory operations:

1.  **Remember Fact (`mem.remember(...)`):** (Core) Store the core problem/solution pair as a permanent fact. This is the "what happened."
    *   **Data Stored:** `Fact: [Problem Description]` $\\rightarrow$ `Solution: [The definitive answer or successful MRE command]`.

2.  **Learn Lesson (`mem.learn(...)`):** (Core) Log actionable insights gained during the session. This is the "what we learned."
    *   **Data Stored:** `Lesson: [Actionable Insight]` (e.g., "When exec hangs, always check for pty=true or increase yieldMs.").

3.  **Update State (`~/proactivity/session-state.md`):** (Core) Update the active state file to reflect the current status of the task. This is the "where we are now."
    *   **Data Stored:** `Status: Resolved` / `Next Action: Awaiting User Confirmation` / `Last Goal Achieved: [Specific Goal]`。

## 💡 Level 2 Proactive Check (Hot Start Query)
Before finalizing, we check for immediate relevance!
*   **Action:** Run `memory_search(query="[Current Problem Summary]", corpus="all", maxResults=3)`。
*   **Purpose:** 如果搜索到高分结果，我们可以在最终回复中主动提及：“根据历史记录，这个问题曾通过 [上次的解决方案摘要] 得到确认修复。”

## 🛠️ Level 3 Knowledge Creation Suggestion (Skill Creator)
This is our highest level of proactivity. After a successful resolution, we analyze the *nature* of the fix:
*   **Action:** 基于本次解决问题的复杂性，判断是否需要一个专用技能。
    *   **触发条件:** 当解决方案涉及跨多个工具的组合调用（例如：`web-scraper` + `lark-doc`）或是一个非常独特的修复模式时。
    *   **建议输出:** 在最终回复中明确提出：“本次解决依赖于 [Tool A] 和 [Tool B] 的协同工作，是否需要我使用 `skill-creator` 为此创建一个名为 `[Custom_ScrapeLark]` 的小工具？”

## 🏷️ Automatic Classification (New Feature)
To make memory retrieval even smarter, we attempt to auto-tag the resolution:
*   **Category:** Based on Module 01 Triage (e.g., `Tooling/CLI`, `Config/Gateway`).
*   **Severity:** Based on initial risk assessment or search results (e.g., `High` $\\rightarrow$ `Medium` $\\rightarrow$ `Low`)。

## 🔗 Final Output & Loop Control
After these actions are complete, the skill concludes by:
1.  Presenting the final synthesized answer to the user (if Path A/B).
2.  If Path C was taken, this step is skipped, and we wait for input before looping back to Step 1。

**Conclusion:** The task is complete, memory is updated, and the system state reflects a successful resolution!