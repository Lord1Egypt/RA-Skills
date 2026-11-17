## Description:

Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auroechan](https://clawhub.ai/user/auroechan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to automate browser workflows with deterministic accessibility-tree snapshots, ref-based element selection, session isolation, and browser state management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved login sessions, cookies, storage, and captured network data can expose sensitive account or site data.

Mitigation: Treat saved auth files and network captures as secrets, keep them out of source control, and avoid reusing them across unrelated accounts or sites.

Risk: Global CLI installation and browser dependency installation can broaden system exposure.

Mitigation: Review before installing, use isolated projects or test environments, and pin and verify the CLI where possible.

Risk: Browser automation can make unintended changes on live websites or accounts.

Mitigation: Limit use to authorized sites and accounts, isolate sessions by workflow, and verify browser state before executing actions that modify data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/auroechan/skills/agent-browser-clawdbot-0)
- [agent-browser project homepage](https://github.com/vercel-labs/agent-browser)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing command guidance for browser automation workflows.]

## Skill Version(s):

1.0.0 (source: target metadata and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
