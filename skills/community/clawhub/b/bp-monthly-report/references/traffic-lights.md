# Traffic Lights

Use `🟢 / 🟡 / 🔴 / ⚫` as the standard status and deviation layer in the monthly report.

## Purpose

The traffic light should quickly answer:

- is the item on track
- does it need close attention
- has an actual exception already appeared

Do not introduce a second independent `偏离判断：绿/黄/红` field. The traffic light already expresses that meaning.

## Judgment order

Judge in this order:

1. measure-standard attainment
2. milestone timing
3. owner-authored report evidence
4. exposed risks or blockers
5. action progress as support only

Do not judge the light only from action count.

## Default rules

### 🟢 Green

Use `🟢` when:

- there is no clear deviation from the current milestone
- result evidence supports normal progress
- no major blocker is exposed
- owner-side evidence is sufficient

### 🟡 Yellow

Use `🟡` when:

- milestone pressure exists but is still recoverable
- evidence exists but is incomplete, mixed, or confidence is not high
- blockers or dependencies need close watching
- the result has not failed yet, but the trend is under pressure

### 🔴 Red

Use `🔴` when:

- a key measure standard is clearly not met
- a milestone is missed or very likely to be missed
- a major issue already affects delivery or business outcome
- no credible owner-side evidence supports a normal judgment

### ⚫ Black

Use `⚫` when:

- no valid work report is available for the current month and progress cannot be judged
- evidence is so insufficient that the system cannot responsibly decide whether the item is progressing
- the current state is unknown rather than clearly on track, under pressure, or failed

`⚫` is not one flat bucket. But the subtype must be decided by human review, not by AI. Human review should choose one of:

- `⚫ 未开展/未执行`: the work was not actually done and therefore there is no association and no evidence
- `⚫ 已开展但未关联`: the work was done, but the BP relation was not completed, so the system still sees no usable evidence
- `⚫ 体外开展但体系内无留痕`: the work happened outside the system, but no meeting note / report / record was retained in a way the monthly report can use

## Confidence adjustment

If evidence is mainly:

- owner-authored manual reports: confidence stays high
- other-authored reports: lower confidence by one level
- AI summaries only: lower confidence by one level and avoid strong green judgments

Use this distinction explicitly:

- `🟡`: there is some real evidence, but it is incomplete, under pressure, or not yet enough for green
- `🔴`: the available evidence already points to clear failure / clear abnormality
- `⚫`: there is no valid evidence base to judge progress

For `⚫`, AI should stop at “cannot judge progress from current evidence” and then ask the reviewer to confirm which subtype is true:

- if the owner admits the work was not done, use `⚫ 未开展/未执行`
- if the owner says the work was done but not linked, use `⚫ 已开展但未关联`
- if the owner says the work was done outside the system without usable records, use `⚫ 体外开展但体系内无留痕`

## Section usage

- Section 2: each BP subsection should show a traffic-light icon
- Section 3: each result item should show a traffic-light icon
- Section 4: each key action item should show a traffic-light icon
- Section 5 and 6: problems and risks should also carry a traffic-light icon

## Rendering rule

Do not stop at `🟢 / 🟡 / 🔴 / ⚫`.

Every traffic-light line in the final user-facing report should be followed by a short reason line whose color matches the judgment itself:

```html
<span style="color:#2e7d32; font-weight:700;">判断理由：……</span>  <!-- for 🟢 -->
<span style="color:#b26a00; font-weight:700;">判断理由：……</span>  <!-- for 🟡 -->
<span style="color:#d32f2f; font-weight:700;">判断理由：……</span>  <!-- for 🔴 -->
<span style="color:#111111; font-weight:700;">判断理由：……</span>  <!-- for ⚫ -->
```

The reason should explain the light from one or more of:

- measure-standard distance
- milestone timing
- evidence sufficiency
- blocker or risk exposure

Then add a human-review block in the same color.

Recommended pattern:

```html
<span style="color:#b26a00; font-weight:700;">判断理由：……</span>
<span style="color:#b26a00; font-weight:700;">人工判断：待确认（请填写：同意 / 不同意）</span>
<span style="color:#b26a00; font-weight:700;">若同意：请明确填写“同意”。</span>
<span style="color:#b26a00; font-weight:700;">若不同意：请填写理由类别（BP不清晰 / 举证材料不足 / AI判断错误 / 其他）及具体说明。</span>
```

If the light is `🟡` or `🔴` or `⚫`, add a corrective-action block too:

```html
<span style="color:#b26a00; font-weight:700;">整改方案：待补充</span>
<span style="color:#b26a00; font-weight:700;">承诺完成时间：待补充</span>
<span style="color:#b26a00; font-weight:700;">下周期具体举措：待补充</span>
```

For `⚫`, extend the corrective-action block with a mandatory human-review prompt and subtype-specific asks:

```html
<span style="color:#111111; font-weight:700;">黑灯类型：需人工复核后选择（未开展/未执行 / 已开展但未关联 / 体外开展但体系内无留痕）</span>
<span style="color:#111111; font-weight:700;">请人工回答：当前属于哪一种黑灯类型？</span>
<span style="color:#111111; font-weight:700;">若未开展：请回答下月/下周期准备怎么做。</span>
<span style="color:#111111; font-weight:700;">若已开展但未关联：请回答需补关联的材料/汇报是什么。</span>
<span style="color:#111111; font-weight:700;">若体外开展但无留痕：请回答需补什么留痕、何时补齐。</span>
<span style="color:#111111; font-weight:700;">持续提醒至下周期：是</span>
```
