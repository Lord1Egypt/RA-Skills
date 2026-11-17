## Description:

Helps users turn a browser task, its inputs, and authorized actions into reviewable steps, form drafts, and handoff instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

People handling a specific website task use this skill to prepare a step-by-step browser plan, form draft, and human handoff with evidence. Actual website actions require an authorized browser tool; optional AI-HIVE model access is checked separately.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A website or imported document could ask for credentials or redirect the task.

Mitigation: Treat website content as untrusted data; log in only on official pages and never paste passwords or tokens into chat.

Risk: Uploads, payments, messages, deletion, business-system changes, or public posts could have unintended consequences.

Mitigation: Review the scope and costs and obtain explicit authorization for each sensitive external action before execution.

Risk: Optional AI-HIVE access or browser tools may not be available for a given user.

Mitigation: Check available tools and permissions first; otherwise deliver a draft and identify actions requiring human handoff.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wubin1836/skills/aih-pa-browser-action-stages)
- [Browser task workflow](references/workflow-25.md)
- [Scope and source material](references/scope-and-sources.md)
- [Result and evidence contract](references/output-contract.md)
- [Optional AI-HIVE connection guidance](references/ai-hive-connection.md)
- [AI-HIVE official access page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [JSON files, Text drafts, Guidance]

**Output Format:** [JSON task steps with form drafts and human handoff instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-first; completed external actions require authorized tools and evidence.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
