## Description:

Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reknottycat](https://clawhub.ai/user/reknottycat)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to drive headless browser workflows from agent sessions, including navigation, interaction, extraction, state checks, multi-session testing, state persistence, and network control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved auth state, cookies, and local storage can expose credentials.

Mitigation: Use test or least-privilege accounts, keep state files out of source control, restrict access to saved state files, and delete them when no longer needed.

Risk: The global npm install and browser dependency installation can introduce operational risk, especially when elevated privileges or system dependencies are used.

Mitigation: Install only from the expected npm package and publisher, prefer pinning a reviewed version, and use caution with --with-deps or elevated privileges.

## Reference(s):

- [Agent Browser project homepage](https://github.com/vercel-labs/agent-browser)
- [ClawHub skill page](https://clawhub.ai/reknottycat/skills/agent-browser-clawdbot-local)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI command examples and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes ref-based browser command patterns, session guidance, state persistence guidance, and JSON snapshot conventions.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
