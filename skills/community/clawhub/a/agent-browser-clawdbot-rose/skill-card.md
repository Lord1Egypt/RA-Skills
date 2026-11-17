## Description:

Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roseknife520](https://clawhub.ai/user/roseknife520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to drive headless browser workflows, inspect accessibility snapshots, interact with elements by stable refs, and manage isolated browser sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved browser sessions, cookies, storage values, and auth-state files can expose account access if mishandled.

Mitigation: Treat saved state as secrets, keep it out of source control, use test or least-privilege accounts where possible, and delete stale session files.

Risk: Global CLI installation and browser dependency installation can change the host environment.

Mitigation: Install only from a trusted registry or source, pin the package version where practical, and avoid elevated privileges unless required.

## Reference(s):

- [Agent Browser GitHub Repository](https://github.com/vercel-labs/agent-browser)
- [Skill Page](https://clawhub.ai/roseknife520/skills/agent-browser-clawdbot-rose)
- [Publisher Profile](https://clawhub.ai/user/roseknife520)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference browser session state, cookies, storage values, screenshots, PDFs, and saved auth-state files produced by the underlying CLI.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
