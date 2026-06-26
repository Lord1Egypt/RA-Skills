# Real User Scenario

## Recommended first production scenario

Use this skill first for:

`互联网公司社招场景下，HR 汇总多位面试官反馈并产出推进材料`

This is a realistic recruiting workflow in China because:

1. feedback is often fragmented across Feishu, WeCom, forms, and verbal notes
2. the hiring manager needs a quick go or no-go recommendation
3. HR still needs documentation that can be forwarded, archived, and pasted back into ATS

## Typical trigger

An HRBP or recruiter says something like:

1. "这是产品经理候选人的三轮面试反馈，帮我汇总成一版给老板看的纪要，再给候选人一条推进消息。"
2. "面试官反馈很散，你帮我判断要不要进终面，并给我一行 tracker 更新。"
3. "把这些反馈整理成结论，顺手给我生成一个 Word 版纪要。"

## Typical inputs

1. Candidate basic profile
2. Target JD or a short role summary
3. Interview feedback from 2 to 5 interviewers
4. Optional salary expectation or notice-period info

## Minimum useful outputs

1. normalized feedback summary
2. recommendation with confidence level
3. candidate-facing follow-up draft
4. tracker update row
5. internal interview debrief memo

## Recommended second production scenario

Use this skill next for:

`JD + 简历初筛，输出是否推进、面试重点、候选人消息和跟进记录`

This is another strong recruiting use case because:

1. almost every recruiting team does resume screening every day
2. the input is stable enough to structure
3. the output can directly move the process forward

Typical trigger:

1. "这是岗位 JD 和候选人简历，帮我判断要不要推进。"
2. "给我一版初筛结论，再补 3 个面试重点。"
3. "顺手生成候选人沟通话术和一行进展记录。"

Minimum useful outputs:

1. match score and match rationale
2. risk flags
3. interview focus
4. candidate-facing follow-up draft
5. progress-record update

## Internet-company flavor

This scenario is especially common in internet hiring because:

1. recruiting speed matters, so HR often cannot wait for perfectly formatted feedback
2. interviewers frequently leave short comments such as "还行", "项目深度一般", "推进但要补看 owner 意识"
3. HR has to translate vague feedback into a structured decision for the hiring manager

## Decision policy

When summarizing feedback for this scenario:

1. distinguish hard blockers from soft concerns
2. call out disagreement between interviewers explicitly
3. do not overstate certainty when feedback is thin
4. keep the candidate message aligned with the actual next action
5. keep the memo concise enough to circulate internally
