## Description:

A meta-skill that continuously improves other skills through trace and feedback driven evolution, with conversational workflows for training, status checks, proposals, and approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyingzhuangk](https://clawhub.ai/user/zhangyingzhuangk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent maintainers use this skill to propose, review, and apply improvements to other skill files based on execution traces and feedback. It is intended for isolated development or trusted CI workflows where local command execution and file changes are expected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run local commands and modify persistent skill instructions.

Mitigation: Use it only in an isolated development workspace or trusted CI environment, point it only at skills you are willing to modify, and review every proposed diff before applying it.

Risk: Untrusted traces, feedback, token files, or command inputs may influence proposed changes or execute with the local account's authority.

Mitigation: Do not provide untrusted inputs unless that authority is acceptable; prefer hash-based or interactive approval and keep approval tokens out of command history when possible.

Risk: Generated proposals may introduce unsafe or unwanted behavior into another skill.

Mitigation: Rely on the proposal-first workflow, security scans, section whitelist, write-scope guard, and self-target guard, then manually inspect the full diff before approval.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python snippets, JSON status payloads, and generated skill-file proposals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create proposal, metadata, report, backup, and secure workspace files while operating on local skill artifacts.]

## Skill Version(s):

1.5.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
