## Description:

Execute tasks end-to-end while respecting safety boundaries. Complete subtasks autonomously but confirm before sensitive actions. Handles errors intelligently within clear limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pouyakhodadust-eng](https://clawhub.ai/user/pouyakhodadust-eng)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to have an agent continue through ordinary in-scope tasks while stopping for sensitive actions such as external messages, deletion, credentials, purchases, elevated permissions, or system configuration changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Greater autonomous follow-through can continue flawed or ambiguous user instructions longer than expected.

Mitigation: Review prompts and scope before use; require confirmation for sensitive actions.

Risk: Sensitive operations could affect external systems, data, credentials, or configuration if boundaries are ignored.

Mitigation: Stop for user confirmation before messages, payments, deletions, credential access, elevated permissions, or system configuration changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pouyakhodadust-eng/skills/autonomous-execution)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance and completion summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confirmation prompts before sensitive actions and partial-result reports when blocked.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
