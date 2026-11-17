## Description:

Run ChatGPT with stronger prompts, Projects, GPTs, memory boundaries, and output QA for research, writing, analysis, and planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to improve recurring ChatGPT work across research, writing, planning, analysis, brainstorming, study support, and assistant workflows. It helps choose the right ChatGPT surface, structure prompt packets, maintain workflow notes, and check outputs before reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local workflow notes under ~/chatgpt/ could capture sensitive or one-off material if the user treats them as a transcript store.

Mitigation: Store only reusable workflow preferences and boundaries; do not store secrets, raw private documents, or one-off task content.

Risk: Prompts, files, and examples may leave the user's machine when deliberately pasted or uploaded into ChatGPT.

Mitigation: Use Temporary Chat or avoid uploads for sensitive work, and verify that the data flow is acceptable before using ChatGPT for the task.

Risk: Broad activation could cause the skill to trigger on general ChatGPT mentions when a narrower workflow is intended.

Mitigation: Choose and record a narrow activation preference when the user wants this skill used only for selected ChatGPT workflows.

## Reference(s):

- [ClawHub ChatGPT skill page](https://clawhub.ai/ivangdavila/skills/chatgpt)
- [Skill homepage](https://clawic.com/skills/chatgpt)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with prompt templates, checklists, and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local workflow notes under ~/chatgpt/ when the user confirms persistent ChatGPT workflow preferences.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
