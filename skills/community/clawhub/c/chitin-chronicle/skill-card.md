## Description:

Coordinates multi-agent content publishing with a shared content registry, cross-agent claim system, publication ledger, timeline tracking, and boot-time editorial state checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adroidian](https://clawhub.ai/user/adroidian)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to coordinate publishing across multiple agents and channels, avoid duplicate work, reserve content tasks with short-lived claims, and record publication history in local JSON files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local helper script can run unintended shell commands or write outside its state folder when given crafted identifiers, channels, titles, URLs, or OPENCLAW_AGENT values.

Mitigation: Review the skill before installing and do not use claim, release, or publish commands with untrusted or free-form values until identifiers are validated, shell command construction is removed, paths are constrained, and only intended files are staged.

Risk: The boot hook or shell alias can expose the workspace to unsafe behavior if added in a sensitive environment before the helper is fixed.

Mitigation: Avoid adding the boot hook or shell alias in sensitive workspaces until the security guidance is addressed and local behavior is reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adroidian/skills/chitin-chronicle)
- [Publisher profile](https://clawhub.ai/user/adroidian)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include CLI status messages, conflict checks, claim and release actions, publication ledger entries, registry updates, and boot-time summaries.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
