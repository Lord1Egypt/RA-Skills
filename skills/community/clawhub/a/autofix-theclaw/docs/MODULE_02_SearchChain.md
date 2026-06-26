---
name: MODULE_02_SearchChain
description: Details the sequential search strategy used to find solutions, prioritizing official documentation before falling back to community reports (GitHub Issues). It now includes Evidence Chain Analysis (L1).
---

# 🔍 Step 1 & 2: Search Chain Execution (Level 1 Enhanced)

**Goal:** To systematically locate the most authoritative and relevant solution for the user's problem. We follow a strict hierarchy: **Official Docs $\\rightarrow$ GitHub Issues**.

## 🥇 Step 1: Primary Search - Official Documentation (docs.openclaw.ai)
This is our first line of defense, as documentation represents the intended behavior of OpenClaw.

**Tool Used:** `tavily_search`
**Query Focus:** The user's problem description, refined by context from **MODULE_01_PreCheck**.
**Parameters:**
- `query`: [User's Problem Description + Context Tags] (e.g., "Tooling/CLI: Why is exec command hanging?")
- `include_answer`: true (Crucial for immediate summary)
- `search_depth`: "advanced"

**Goal:** Find a direct, authoritative answer or a link to the relevant documentation page. If this step returns high confidence results, we may stop here and proceed directly to Step 3 Synthesis.

## 🥈 Step 2: Fallback Search - GitHub Issues (Fallback A)
If Step 1 yields no satisfactory result or provides only partial context, we check community reports for existing bug discussions.

**Tool Used:** `tavily_search`
**Query Focus:** The user's exact problem description, prefixed to signal a bug report context.
**Parameters:**
- `query`: "[User's Problem Description] OpenClaw issue" (e.g., "exec command hanging OpenClaw issue")
- `include_answer`: true (To get a summary of the best matching issue)
- `search_depth`: "advanced"

**Goal:** Find an existing, reported bug or discussion thread that mirrors the user's problem. This provides community-vetted workarounds.

## 🥉 Step 3: Ultimate Fallback Search - General Web/Community (Fallback B - New!)
如果步骤 1 和步骤 2 都未能提供明确答案，系统将激活广域网络搜索作为最后的诊断手段。这一步用于查找最新的行业共识、博客文章或非结构化的讨论记录。

**Tool Used:** `tavily_search` 或 `searxng` (根据配置切换)
**Query Focus:** 扩大查询范围，使用更宽泛但相关的关键词组合。
**Parameters:**
- `query`: [User's Problem Description] OR "OpenClaw best practice"
- `include_answer`: true
- `search_depth`: "advanced"

**Goal:** 作为终极的兜底网络搜索，尽可能多地收集信息碎片。结果应被标记为“外部参考信息”，其权威性需由人工判断。

## 🔗 Level 1: Evidence Chain Analysis (New!)
When results are returned from Step 1 and/or Step 2, we don't just trust the summary; we verify the evidence trail!
*   **Action:** For the top N results, we extract not just the snippet, but also the **URL link**.
*   **Verification:** We check if the solution is supported by *both* Docs (Step 1) AND GitHub (Step 2).
    *   **High Confidence:** Doc + GH Match. $\\rightarrow$ Proceed to Synthesis with strong evidence.
    *   **Medium Confidence:** Only one source matches, or sources conflict slightly. $\\rightarrow$ Proceed to Synthesis with caution.
    *   **Low Confidence:** Both are weak/contradictory. $\\rightarrow$ Proceed to Contextual Inquiry (Step 5C).

## 🔗 Next Step Dependency
The output of this module dictates which path is taken in **Step 3 (Synthesis & Decision)**, now backed by a verifiable evidence trail。