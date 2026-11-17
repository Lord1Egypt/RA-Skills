## Description:

Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexbingquanxu-cpu](https://clawhub.ai/user/alexbingquanxu-cpu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to automate browser workflows through the agent-browser CLI, including navigation, ref-based interaction, information retrieval, session isolation, state persistence, screenshots, PDFs, and network control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on installing and running the third-party agent-browser npm package as a global CLI.

Mitigation: Install only after trusting the package source and reviewing it under the adopting team's dependency policy.

Risk: Saved browser state, cookies, and localStorage can contain credentials or session secrets.

Mitigation: Treat state and storage outputs like passwords: keep them out of source control and logs, restrict file permissions, and use isolated sessions for sensitive accounts.

## Reference(s):

- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser)
- [ClawHub skill page](https://clawhub.ai/alexbingquanxu-cpu/skills/agent-browser-custom)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command-oriented guidance for browser automation, isolated sessions, saved state, cookies, localStorage, screenshots, PDFs, and network controls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
