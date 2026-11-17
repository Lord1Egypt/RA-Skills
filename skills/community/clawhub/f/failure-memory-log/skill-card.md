## Description:

Automatic failure pattern recording and recall system that helps agents avoid repeating mistakes by logging errors with context, root cause, and resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voidlight00](https://clawhub.ai/user/voidlight00)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to record resolved failures, search previous failure patterns before new work, and summarize repeated issues for process improvement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A durable local troubleshooting log can retain sensitive error details, credentials, personal data, proprietary incident details, or signed URLs if entries are recorded automatically.

Mitigation: Keep the memory directory outside source control, review and delete stale entries, avoid recording secrets or personal data, and prefer explicit approval before automatic logging in sensitive projects.

Risk: Broad pre-task recall can surface stale or irrelevant failure patterns that may steer an agent toward outdated fixes.

Mitigation: Review recalled entries for relevance before applying them and periodically prune or update failure records.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates a local markdown failure log when initialized and used by an agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
