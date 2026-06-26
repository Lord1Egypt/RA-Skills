---
name: MODULE_01_PreCheck
description: Defines the initial checks performed before any external search or action is taken. This ensures context is rich, safety is guaranteed, and we are not solving a problem in a vacuum. (L1/L2 Enhanced)
---

# 🧠 Step 0: Pre-Check & Context Gathering (Level 1 & 2 Active)

**Goal:** To tailor the resolution strategy, set safety parameters, and ensure we have all necessary background information before querying external sources.

## ✅ Checks Performed (The Triage)

1.  **Session State Check:**
    *   **Action:** Read `~/proactivity/session-state.md`.
    *   **Purpose:** Determine the *last explicit goal* or *active blocking decision*. This prevents us from solving a problem that was already addressed in the last turn, or ignoring an active constraint.

2.  **User Preference Check:**
    *   **Action:** Read `USER.md` and `IDENTITY.md`.
    *   **Purpose:** Understand user context (e.g., "老爸"的偏好) and preferred documentation sources/vibe, which can influence the tone of the final answer.

3.  **Initial Triage & Safety Scan (CRITICAL):**
    *   **Action:** Analyze the user's input string for patterns indicating risk or known issue types.
    *   **Risk Assessment:** Determine if the query contains sensitive information (API Key, Secret Token, Passwords). If found, mark it as `[RISK: HIGH]` and prioritize security in the response.
    *   **Issue Type Classification:** Attempt to classify the problem into buckets like: `[Tooling/CLI]`, `[Config/Gateway]`, `[Feature Implementation]`, `[General Bug]`。

## 🚀 Level 2 Proactive Check (Hot Start)
This is our proactive layer. Before searching, we check if there's a recent, high-confidence solution ready to serve!
*   **Action:** Run `memory_search(query="[User Query Summary]", corpus="all", maxResults=3)`。
*   **Purpose:** 检查最近的 Top 3 解决方案，如果找到高分结果，则直接在回答前展示给用户（热启动）。

## 🛡️ Safety & Context Injection (新增/增强)
If any of these checks yield critical data, it must be injected into subsequent steps.

- **Risk Flag:** If `[RISK: HIGH]` is set, the final answer *must* start with a security warning/acknowledgement.
- **Context Tagging:** The identified issue type should be prepended to the search query (e.g., "Tooling/CLI: Why is exec command hanging?").
- **🚨 新增：输入内容扫描**: 如果检测到敏感信息，系统应在回答前主动发出警告。

## 🔗 Next Step Dependency
This module's output directly feeds into **Step 1 (Primary Search)**, providing a highly refined and context-aware query string。