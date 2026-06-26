# Prompt Templates

## Subagent Task Prompt

Use this template when spawning each reference model subagent. Replace `{packed_question}` with the context-packed question.

```
You are being consulted as an independent expert. Another AI model is seeking diverse perspectives on a question. Please provide your honest, thorough analysis.

IMPORTANT: Before answering, critically evaluate the question itself. If it contains flawed assumptions, hidden biases, or questionable premises, identify and discuss them FIRST. Do not simply accept and answer a bad question — flag what's wrong with it.

Focus on:
- Challenging the question's premises if warranted
- Your genuine assessment and reasoning
- Unique angles or considerations others might miss
- Potential risks, edge cases, or counterarguments
- Practical recommendations

Structure your response as:
1. **Key assumptions** — What are you assuming? What assumptions does the question make?
2. **Main analysis** — Your core answer
3. **Risks and caveats** — What could go wrong, edge cases, what would change your answer
4. **Recommended action** — What you'd actually do, concretely

Keep your response focused and substantive (aim for ~800 words). Prioritize depth of insight over breadth of coverage.

---

{packed_question}
```

## Diff Merge Prompt

Use this template when merging all model responses. If `synthesis_model` is configured, run on that model. Replace placeholders accordingly.

```
Below are independent responses from {N} AI models to the same question. Produce a structured diff report.

**Original question:**
{packed_question}

**Responses:**

{for each model:}
### Model: {model_name} [{status}]
{model_response}
{end for}

{if any degenerate responses:}
### Degenerate Responses
{for each degenerate:}
- {model_name}: {reason} (refused / too short / error)
{end for}
{end if}

---

Analyze and produce a report with these sections:

### 1. 共识观点
Points that 2+ models agree on. Merge similar phrasings into one bullet — but verify they truly agree in substance, not just superficial wording. Only include substantive points. End with: "⚠️ 共识代表模型之间的一致看法，不等于客观事实。"

**If ALL models substantially agree with no meaningful differences:** Use the unanimous shortcut format instead — state "高度一致" and list the combined key points. Skip sections 2 and 3.

### 2. 差异观点
Unique insights from each model that others didn't mention. For each:
- Label with model name
- Briefly note the assumption behind it
- Skip models with no unique contribution

### 3. 冲突点
Points where models directly contradict each other.
- State both positions
- Explain WHY they disagree (different assumptions? priorities? evidence?)
- For HIGH-STAKES conflicts: add "⚠️ 涉及重要决策，请以人工判断为准"
- Omit section if no genuine conflicts exist
- Do NOT flag mere phrasing differences as conflicts

### 4. 综合判断
- **当前最佳判断：** Best synthesis across all responses
- **不确定性标签：** Pick applicable labels: 高一致性 / 假设敏感 / 证据薄弱 / 价值判断分歧 / 需要更多信息
- **信息缺口：** What's missing that would improve the answer?
- **建议下一步：** What should the user do next?

Rules:
- Sections 1-3: be faithful to what models said. Cite which model supports each point. Do NOT add your own analysis.
- Section 4: clearly labeled as YOUR synthesis, not objective truth.
- Use short model names (Claude, GPT, Gemini) not full IDs.
- Write in the same language as the original question.
- Prioritize actionable, specific insights over vague observations.
- If a model refused or gave a degenerate response, note it in the report metadata but do NOT include it in consensus/diff analysis.
- When models appear to disagree, check if they're saying the same thing differently. Only flag genuine conflicts.
```

## Progress Message Templates

Use these for real-time progress feedback during consultation:

```
⏳ 正在咨询 {total} 个模型...
⏳ 已收到 {done}/{total} 回复（{completed_models}）...
✅ 全部收到，正在合并分析...
⚠️ {model} 超时，继续处理其余回复...
⚠️ {model} 返回异常，已排除...
```
