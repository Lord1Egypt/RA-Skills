## Description:

Proactive Obsidian vault maintenance and review. Find stale tasks, orphan notes, projects that need attention, and connection opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gabebac](https://clawhub.ai/user/gabebac)

### License/Terms of Use:

MIT-0

## Use Case:

External users with an Obsidian-based personal knowledge vault use this skill to review stale tasks, pending staged files, open project items, therapy-note activity, orphan notes, and connection opportunities before approving any vault updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect broad areas of a personal Obsidian vault, including health and therapy metadata.

Mitigation: Install only where that vault access is acceptable, use explicit review commands, and avoid quoting therapy-note contents in generated reports.

Risk: The skill includes unsafe keyword search instructions that may mishandle untrusted note names or topics.

Mitigation: Sanitize and quote search terms before execution, and fix the search command pattern before relying on it with untrusted inputs.

Risk: Web enrichment may introduce inaccurate or unwanted changes into staged notes.

Mitigation: Review all staged enrichment output and require explicit approval before using vault-push or applying updates.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gabebac/skills/brain-proactive)
- [ClawHub Publisher Profile](https://clawhub.ai/user/gabebac)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown bullet-list reports with optional shell command snippets and staged-change guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Caps reports at 10 items, summarizes overflow, and requires approval before vault changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
