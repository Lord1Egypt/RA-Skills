---
name: MODULE_03_ValidationAction
description: Contains the core decision logic (Step 3) and the subsequent execution/validation layer (Step 4). It determines *what* to do next based on search results, now incorporating L1 Error Analysis Loop.
---

# 🧠 Step 3 & 4: Synthesis, Decision, and Action Execution (Level 1 Enhanced)

**Goal:** To synthesize findings from the Search Chain (Module 02) into a concrete plan of action, and then execute that plan to validate the solution or gather more data.

## ⚖️ Step 3: Synthesis & Decision Making
Based on search results and evidence chain analysis (from Module 02), we decide the path:

| Scenario | Condition Met | Decision Path | Next Action (Step 4) |
| :--- | :--- | :--- | :--- |
| **Definitive Answer** | Docs provided a clear solution ($\ge 0.8$) AND GitHub confirms it. | Present Solution Directly. | **Path A: Direct Answer** |
| **Workaround Found** | GitHub provides a quick fix, but Docs are vague/outdated. | Propose Workaround + Suggest Official Fix. | **Path B: Code Verification (MRE)** $\rightarrow$ *进入 L1 错误分析循环* |
| **Ambiguous/Missing** | Both steps return low scores ($\le 0.5$) or contradictory info. | Formulate precise question for the user. | **Path C: Contextual Inquiry** |

## 🛠️ Step 4: Validation & Action Execution (Level 1 Loop)
This step executes the decision made in Step 3, with enhanced logic for Path B.

### Path A: Direct Answer (The Quick Win)
*   **Action:** Synthesize the best answer from Docs/GitHub into a clear, concise response for the user.
*   **Evidence:** The summary text itself is the primary evidence.
*   **Conclusion:** Proceed immediately to **Step 5 Finalization**.

### Path B: Code Verification (MRE - Minimal Reproducible Example) $\rightarrow$ L1 Loop
This path now includes a self-healing loop if the initial test fails!

1.  **Initial Test:** Proactively call `exec` with an MRE derived from search results.
2.  **Check Result:** Analyze the output:
    *   **Success (✅):** Proceed to **Step 5 Finalization**.
    *   **Failure (❌):** Trigger **Error Analysis Loop**:
        a. **Analyze Error:** Read `exec` output for error codes/messages.
        b. **Proactive Explanation & Proposal (新增核心步骤):** 基于错误分析，明确指出问题可能出在哪里（例如：“根据日志，问题很可能出在 Gateway 的配置加载环节”），并提出一个或多个建议的修复命令。
        c. **Await User Approval:** 暂停执行，等待用户通过 `/approve` 命令确认要运行哪个/哪些命令。
        d. **Execute & Re-Test:** 在获得同意后，调用 `exec` 执行选定的修复命令，然后**循环回到 Step 3 (Synthesis)** 进行重新决策（或直接进入下一步验证）。

### Path C: Contextual Inquiry (The Guided Conversation)
*   **Action:** Formulate a precise question for the user based on what is missing. This should be highly targeted.
*   **Evidence:** The formulated question itself, which serves as the prompt for the next turn.
*   **Conclusion:** Wait for user input, then loop back to **Step 1 (Primary Search)** with the new context。

## 🔗 Next Step Dependency
The outcome of this module determines whether we conclude the task (Path A), gather more data (Path B $\rightarrow$ Loop) 或等待用户输入 (Path C $\rightarrow$ Wait)。它直接驱动着 **Step 5 Finalization** 的执行！

### Path C: Contextual Inquiry (The Guided Conversation)
*   **Action:** Formulate a precise question for the user based on what is missing. This should be highly targeted.
*   **Evidence:** The formulated question itself, which serves as the prompt for the next turn.
*   **Conclusion:** Wait for user input, then loop back to **Step 1 (Primary Search)** with the new context。

## 🔗 Next Step Dependency
The outcome of this module determines whether we conclude the task (Path A), gather more data (Path B $\rightarrow$ Loop) 或等待用户输入 (Path C $\rightarrow$ Wait)。它直接驱动着 **Step 5 Finalization** 的执行！