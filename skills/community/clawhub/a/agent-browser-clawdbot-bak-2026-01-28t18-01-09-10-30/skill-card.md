## Description:

Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicoataiza](https://clawhub.ai/user/nicoataiza)

### License/Terms of Use:


## Use Case:

Developers and AI agents use this skill to drive the agent-browser CLI for deterministic headless browser navigation, element interaction, multi-session testing, and extraction from web pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persisted browser authentication state can expose cookies or storage if it is committed, logged, or stored in a shared location.

Mitigation: Use least-privilege test accounts where possible, keep saved auth state out of source control and logs, store it only in access-controlled locations, and delete it after use.

Risk: Installing an unpinned global CLI and downloaded browser/runtime components can introduce supply-chain drift.

Mitigation: Pin or verify the agent-browser package and downloaded browser/runtime components before running global installs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nicoataiza/skills/agent-browser-clawdbot-bak-2026-01-28t18-01-09-10-30)
- [Agent Browser homepage](https://github.com/vercel-labs/agent-browser)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing instructions for using the agent-browser CLI; command results may include JSON snapshots, page text, screenshots, PDFs, and saved browser state files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
