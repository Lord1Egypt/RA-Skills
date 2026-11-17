## Description:

Helps agents research web sources and market data, keep sourced notes, create checked Markdown reports, and edit text files using the agentbox CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex-ht](https://clawhub.ai/user/alex-ht)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users use this skill to find cited web information and market quotes, extract and compare data, prepare sourced reports, and make requested text-file edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested file edits can change local files when applied.

Mitigation: Review the preview and approve the target and changes before using --apply.

Risk: Saved pages, notes, tables, and configuration persist in local task state.

Mitigation: Review stored task data and use AGENTBOX_HOME to select an appropriate state directory.

Risk: Optional external-service API keys are sensitive.

Mitigation: Have the human set keys privately; do not paste them into chat.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/alex-ht/skills/agentbox)
- [Project homepage (skill metadata)](https://github.com/alex-ht/agentbox)
- [Research reference](artifact/references/research.md)
- [Reports reference](artifact/references/reports.md)
- [File editing reference](artifact/references/files.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files]

**Output Format:** [Sourced text and Markdown reports; CLI command results as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can be checked against templates; file edits show a preview before application.]

## Skill Version(s):

0.2.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
