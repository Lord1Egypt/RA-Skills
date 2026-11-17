## Description:

AI Auto Dev guides a coding agent workflow in which Claude Code acts as a project manager and a builder agent executes implementation tasks from requirements alignment through specification, execution, validation, and documentation staging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mwangxiang](https://clawhub.ai/user/mwangxiang)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to coordinate autonomous coding work: clarify requirements, generate task specifications, dispatch builder agents, run checks, and stage delivery documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill promotes a highly autonomous coding workflow with disabled approval prompts and full filesystem access.

Mitigation: Keep approval prompts enabled and avoid danger-full-access unless it is narrowly justified for a reviewed task.

Risk: The workflow includes automatic GitHub commit, tag, and push behavior without requiring user confirmation.

Mitigation: Remove automatic publishing steps or require explicit human review before commits, tags, or pushes are created.

Risk: Persistent logs under a user home directory may retain sensitive project details across sessions.

Mitigation: Redirect logs to a project-local location and minimize sensitive details in retained logs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mwangxiang/skills/ai-auto-dev)
- [Publisher Profile](https://clawhub.ai/user/mwangxiang)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline command and configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces plans, task specifications, validation reports, documentation staging content, and operational guidance for autonomous coding workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
