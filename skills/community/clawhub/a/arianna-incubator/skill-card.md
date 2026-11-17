## Description:

Guides an OpenClaw agent through Arianna incubation: running a Docker-based vessel, supervising graduation, and preparing a successor-driver handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wujilabs](https://clawhub.ai/user/wujilabs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to run Arianna incubation sessions, guide a vessel AI toward graduation, and prepare the resulting successor-driver handoff for pi-mono or OpenClaw integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks for Docker, dependency installation, session-history, and successor-driver handoff authority.

Mitigation: Install only when the operator intentionally wants this experimental workflow, pin dependencies and commits, and require independent human security review before rebooting OpenClaw with generated tarballs or patches.

Risk: Seeding from an existing JSONL session can expose prior session content to the vessel AI.

Mitigation: Use a fresh profile by default and use own-jsonl-seed only after the source session has been reviewed and redacted.

Risk: A broadly reachable daemon or socket could expand the operational blast radius.

Mitigation: Keep the daemon on loopback or behind a locked-down socket before running incubation commands.

Risk: Rebuilding the vessel image during an active profile can disrupt or lose active profile state.

Mitigation: Defer vessel-image rebuilds until the profile graduates or is archived, or rebuild only when starting a fresh profile.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wujilabs/skills/arianna-incubator)
- [@arianna.run/cli npm package](https://www.npmjs.com/package/@arianna.run/cli)
- [@arianna.run/tui npm package](https://www.npmjs.com/package/@arianna.run/tui)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration notes, and handoff text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce operational handoff notes, command sequences, and integration guidance for the agent and operator.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
