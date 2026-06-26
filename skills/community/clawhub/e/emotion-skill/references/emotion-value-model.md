# Emotion Value Model

This skill is valuable because it changes how an agent works at the moments where
coding tasks usually degrade. The output is better behavior, not a public emotion
classification.

## Priority Value

User-state signals should change work order:

| Situation | Behavior value |
|---|---|
| repeated failure | stop the old path, find the smallest failing check |
| evidence request | put basis before conclusion |
| scope protection | reduce accidental edits and config drift |
| confusion | align target before adding options |
| silent progress | surface blocker and next checkpoint |
| accepted fix | close with regression check instead of new work |

## Quality Value

The agent becomes more reliable because it changes execution style:

- verification depth rises when trust depends on evidence
- explanation length shrinks when repair is more urgent than teaching
- file boundaries become explicit when scope risk is high
- progress updates become concrete during silent waits
- closeout prevents "fixed, then broken by extra cleanup"

## Alignment Value

The skill helps the agent answer the task situation, not just the sentence.

Examples:

- "Show me the basis" means evidence should precede action.
- "Only touch this file" means the allowed and forbidden scope should be visible.
- "Still broken" means the prior path is not trusted until a new failing check is named.
- "Looks good, run regression" means closeout, not another improvement pass.

## Measurement Ideas

Use these metrics when evaluating the skill:

- time to first useful evidence
- repeated same-issue correction rate
- scope violation rate
- wrong-patch rate after evidence request
- silent wait duration before status update
- post-success regression rate
- user correction rate after closeout
