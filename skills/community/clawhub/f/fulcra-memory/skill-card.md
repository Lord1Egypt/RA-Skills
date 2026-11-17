## Description:

Manages agent progress reporting and OKF-compliant memory syncing to Fulcra.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fulcra](https://clawhub.ai/user/fulcra)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to maintain OKF-compliant progress, role, session, task, knowledge, and inbox memory files and sync selected summaries to Fulcra.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads persistent agent and user context, including work summaries, decisions, links, preferences, and task context, to Fulcra.

Mitigation: Review memory content before upload, minimize sensitive disclosures, and require explicit user approval before syncing sensitive context.

Risk: The skill relies on an external Fulcra CLI for authentication, uploads, and deletion, and the security evidence notes that the CLI is unpinned.

Mitigation: Use a pinned and trusted fulcra-api installation and limit Fulcra credentials to the intended agent namespace.

Risk: Inbox processing can delete source files after archiving.

Mitigation: Verify archive upload success before deleting inbox files.

## Reference(s):

- [Fulcra Memory CLI Reference](references/fulcra-memory-cli.md)
- [Fulcra CLI Documentation](https://raw.githubusercontent.com/fulcradynamics/agent-skills/main/skills/fulcra-get-started/references/fulcra-cli.md)
- [Open Knowledge Format Specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
- [ClawHub Skill Page](https://clawhub.ai/fulcra/skills/fulcra-memory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and OKF-formatted memory file examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in persistent Fulcra memory files when the agent follows the CLI workflow.]

## Skill Version(s):

0.1.9 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
