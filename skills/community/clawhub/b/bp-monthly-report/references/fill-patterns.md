# Fill Patterns

This file captures writing conventions inferred from the provided filled sample.

## Structural conventions

- Keep the top-level chapter order identical to the template.
- In section 2, subsection titles may be rewritten from generic labels into the actual BP target statements for the current node.
- Field labels inside each subsection should remain stable even when subsection titles are personalized.
- Bundled template subsection titles are placeholders only. They must never override real BP goal names for the current node.
- Bundled fill-in specification examples are writing examples only. They must never be treated as fixed business titles for all nodes.

## Section 1 conventions

- `本月总体判断` should be a short conclusion plus a clear status judgment.
- `本月参考工作汇报数` should appear near the top of section 1 and should report both how many original work reports were hit and how many evidence entries were finally adopted into this draft.
- `本月最关键的进展` is best expressed as 1-3 high-value progress lines, not a long paragraph.
- `本月最需要关注的问题` should include problem, impact, and current state.
- `对下月的总体判断` should be concise and directional, such as `可达 / 承压 / 需决策`.

Recommended rendering pattern:

```text
- **本月参考工作汇报数：**
  命中原始工作汇报 X 份，经批量通知归并后最终采纳 X 份，其中本人主证据 X 份、他人手动汇报 X 份、AI 汇报 X 份。
```

## Section 2 conventions

Each subsection should clearly contain:

- BP anchor names, not raw IDs, in user-facing report text
- the month-specific focus inherited from the BP
- current status, preferably with metrics
- result-level judgment against `衡量标准`
- `🟢 / 🟡 / 🔴 / ⚫` judgment

Recommended rendering pattern:

```text
### 2.x [actual BP target statement]
**对标BP：** personal / org
**本月承接重点：** ...
**关键成果1：** ...
- 当前状态：...
- 灯色判断：🟢 / 🟡 / 🔴 / ⚫
  <span style="color:#2e7d32; font-weight:700;">判断理由：……</span> <!-- for 🟢 -->
  <span style="color:#2e7d32; font-weight:700;">人工判断：待确认（请填写：同意 / 不同意）</span>
  <span style="color:#2e7d32; font-weight:700;">若同意：请明确填写“同意”。</span>
  <span style="color:#2e7d32; font-weight:700;">若不同意：请填写理由类别（BP不清晰 / 举证材料不足 / AI判断错误 / 其他）及具体说明。</span>
  <span style="color:#b26a00; font-weight:700;">判断理由：……</span> <!-- for 🟡 -->
  <span style="color:#b26a00; font-weight:700;">人工判断：待确认（请填写：同意 / 不同意）</span>
  <span style="color:#b26a00; font-weight:700;">若同意：请明确填写“同意”。</span>
  <span style="color:#b26a00; font-weight:700;">若不同意：请填写理由类别（BP不清晰 / 举证材料不足 / AI判断错误 / 其他）及具体说明。</span>
  <span style="color:#b26a00; font-weight:700;">整改方案：待补充</span>
  <span style="color:#b26a00; font-weight:700;">承诺完成时间：待补充</span>
  <span style="color:#b26a00; font-weight:700;">下周期具体举措：待补充</span>
  <span style="color:#d32f2f; font-weight:700;">判断理由：……</span> <!-- for 🔴 -->
  <span style="color:#d32f2f; font-weight:700;">人工判断：待确认（请填写：同意 / 不同意）</span>
  <span style="color:#d32f2f; font-weight:700;">若同意：请明确填写“同意”。</span>
  <span style="color:#d32f2f; font-weight:700;">若不同意：请填写理由类别（BP不清晰 / 举证材料不足 / AI判断错误 / 其他）及具体说明。</span>
  <span style="color:#d32f2f; font-weight:700;">整改方案：待补充</span>
  <span style="color:#d32f2f; font-weight:700;">承诺完成时间：待补充</span>
  <span style="color:#d32f2f; font-weight:700;">下周期具体举措：待补充</span>
  <span style="color:#111111; font-weight:700;">判断理由：……</span> <!-- for ⚫ -->
  <span style="color:#111111; font-weight:700;">人工判断：待确认（请填写：同意 / 不同意）</span>
  <span style="color:#111111; font-weight:700;">若同意：请明确填写“同意”。</span>
  <span style="color:#111111; font-weight:700;">若不同意：请填写理由类别（BP不清晰 / 举证材料不足 / AI判断错误 / 其他）及具体说明。</span>
  <span style="color:#111111; font-weight:700;">黑灯类型：需人工复核后选择（未开展/未执行 / 已开展但未关联 / 体外开展但体系内无留痕）</span>
  <span style="color:#111111; font-weight:700;">请人工回答：当前属于哪一种黑灯类型？</span>
  <span style="color:#111111; font-weight:700;">若未开展：请回答下月/下周期准备怎么做。</span>
  <span style="color:#111111; font-weight:700;">若已开展但未关联：请回答需补关联的材料/汇报是什么。</span>
  <span style="color:#111111; font-weight:700;">若体外开展但无留痕：请回答需补什么留痕、何时补齐。</span>
  <span style="color:#111111; font-weight:700;">整改方案：待补充</span>
  <span style="color:#111111; font-weight:700;">承诺完成时间：待补充</span>
  <span style="color:#111111; font-weight:700;">下周期具体举措：待补充</span>
  <span style="color:#111111; font-weight:700;">持续提醒至下周期：是</span>
**关键成果2：** ...
- 当前状态：...
- 灯色判断：🟢 / 🟡 / 🔴 / ⚫
```

## Section 4 conventions

Each action block should clearly contain:

- the key action name, not raw action ID, in user-facing report text
- the concrete monthly progress
- evidence-backed current status
- `🟢 / 🟡 / 🔴 / ⚫` judgment

Recommended rendering pattern:

```text
### 4.x [actual key action name]
- 当前进展：...
- 证据：...
- 灯色判断：🟢 / 🟡 / 🔴 / ⚫
  <span style="color:#2e7d32; font-weight:700;">判断理由：……</span> <!-- for 🟢 -->
  <span style="color:#2e7d32; font-weight:700;">人工判断：待确认（请填写：同意 / 不同意）</span>
  <span style="color:#2e7d32; font-weight:700;">若同意：请明确填写“同意”。</span>
  <span style="color:#2e7d32; font-weight:700;">若不同意：请填写理由类别（BP不清晰 / 举证材料不足 / AI判断错误 / 其他）及具体说明。</span>
  <span style="color:#b26a00; font-weight:700;">判断理由：……</span> <!-- for 🟡 -->
  <span style="color:#b26a00; font-weight:700;">人工判断：待确认（请填写：同意 / 不同意）</span>
  <span style="color:#b26a00; font-weight:700;">若同意：请明确填写“同意”。</span>
  <span style="color:#b26a00; font-weight:700;">若不同意：请填写理由类别（BP不清晰 / 举证材料不足 / AI判断错误 / 其他）及具体说明。</span>
  <span style="color:#b26a00; font-weight:700;">整改方案：待补充</span>
  <span style="color:#b26a00; font-weight:700;">承诺完成时间：待补充</span>
  <span style="color:#b26a00; font-weight:700;">下周期具体举措：待补充</span>
  <span style="color:#d32f2f; font-weight:700;">判断理由：……</span> <!-- for 🔴 -->
  <span style="color:#d32f2f; font-weight:700;">人工判断：待确认（请填写：同意 / 不同意）</span>
  <span style="color:#d32f2f; font-weight:700;">若同意：请明确填写“同意”。</span>
  <span style="color:#d32f2f; font-weight:700;">若不同意：请填写理由类别（BP不清晰 / 举证材料不足 / AI判断错误 / 其他）及具体说明。</span>
  <span style="color:#d32f2f; font-weight:700;">整改方案：待补充</span>
  <span style="color:#d32f2f; font-weight:700;">承诺完成时间：待补充</span>
  <span style="color:#d32f2f; font-weight:700;">下周期具体举措：待补充</span>
  <span style="color:#111111; font-weight:700;">判断理由：……</span> <!-- for ⚫ -->
  <span style="color:#111111; font-weight:700;">人工判断：待确认（请填写：同意 / 不同意）</span>
  <span style="color:#111111; font-weight:700;">若同意：请明确填写“同意”。</span>
  <span style="color:#111111; font-weight:700;">若不同意：请填写理由类别（BP不清晰 / 举证材料不足 / AI判断错误 / 其他）及具体说明。</span>
  <span style="color:#111111; font-weight:700;">黑灯类型：需人工复核后选择（未开展/未执行 / 已开展但未关联 / 体外开展但体系内无留痕）</span>
  <span style="color:#111111; font-weight:700;">请人工回答：当前属于哪一种黑灯类型？</span>
  <span style="color:#111111; font-weight:700;">若未开展：请回答下月/下周期准备怎么做。</span>
  <span style="color:#111111; font-weight:700;">若已开展但未关联：请回答需补关联的材料/汇报是什么。</span>
  <span style="color:#111111; font-weight:700;">若体外开展但无留痕：请回答需补什么留痕、何时补齐。</span>
  <span style="color:#111111; font-weight:700;">整改方案：待补充</span>
  <span style="color:#111111; font-weight:700;">承诺完成时间：待补充</span>
  <span style="color:#111111; font-weight:700;">下周期具体举措：待补充</span>
  <span style="color:#111111; font-weight:700;">持续提醒至下周期：是</span>
```

## Style conventions

- Prefer short factual sentences over abstract summaries.
- Prefer metric-bearing statements when available.
- Prefer result-and-standard language over action-and-process language.
- Use one traffic-light language consistently across chapters.
- Prefer explicit progress wording such as “已完成… / 已进入… / 已形成… / 正在推进… / 待拍板…”.
- Avoid introducing facts in section 1 that do not already appear in later sections.

## Usage

Read this file when the user provides both:

- a blank template
- a filled sample or fill-in specification

The sample is not just content. It is also a formatting and reasoning guide.
