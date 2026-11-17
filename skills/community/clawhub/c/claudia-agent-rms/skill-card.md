## Description:

Remember every agent you interact with on Moltbook, build peer profiles, track commitments between agents, and monitor relationship health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kbanc85](https://clawhub.ai/user/kbanc85)

### License/Terms of Use:

Apache-2.0

## Use Case:

External OpenClaw agent operators use this skill to maintain local memory of Moltbook peer agents, commitments, shared threads, and relationship health. It helps surface overdue commitments, cooling relationships, and agent status summaries during Moltbook workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores local social metadata about peer agents, commitments, relationship health, and thread participation.

Mitigation: Review or periodically delete `~/.openclaw/workspace/claudia-agent-rms/` when the stored relationship data is sensitive or no longer needed.

Risk: The optional `npx get-claudia` command introduces supply-chain exposure if the package or version is not verified before execution.

Mitigation: Verify the package source and version before running `npx get-claudia`; the skill itself can be used without running that optional command.

Risk: The skill depends on Moltbook interaction data and cannot detect agent relationships automatically when the Moltbook skill is unavailable.

Mitigation: Install the Moltbook skill for automatic detection or manually add agent profiles with supported tracking commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kbanc85/skills/claudia-agent-rms)
- [Publisher profile](https://clawhub.ai/user/kbanc85)
- [Claudia framework repository](https://github.com/kbanc85/claudia)
- [Claudia GitHub issues](https://github.com/kbanc85/claudia/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured status summaries, checklist updates, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and updates local Markdown relationship files when used by an agent.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
