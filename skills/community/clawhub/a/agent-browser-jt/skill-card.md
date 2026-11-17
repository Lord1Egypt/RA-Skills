## Description:

Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeytbuilds](https://clawhub.ai/user/joeytbuilds)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to automate browser workflows through a CLI, including navigation, interaction, waiting, session isolation, state handling, screenshots, network control, cookies, storage, tabs, and frames.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad unpinned installation steps can install an unexpected or changed CLI package version.

Mitigation: Use a pinned reviewed agent-browser package version where possible and review the package before installation.

Risk: Saved auth state, cookies, and storage data can expose credentials or authorized sessions.

Mitigation: Use only authorized test accounts, keep saved state files out of source control and logs, restrict file access, and delete them when no longer needed.

Risk: Installing browser system dependencies with elevated privileges can increase host-level risk.

Mitigation: Avoid elevated dependency installation unless necessary and review the environment before running system-level install commands.

## Reference(s):

- [Agent Browser homepage](https://github.com/vercel-labs/agent-browser)
- [ClawHub skill page](https://clawhub.ai/joeytbuilds/skills/agent-browser-jt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance commonly references the agent-browser CLI and may include JSON snapshot parsing patterns.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
