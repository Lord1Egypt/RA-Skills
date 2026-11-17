## Description:

Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mifashion](https://clawhub.ai/user/mifashion)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate browser workflows with agent-browser, using accessibility tree snapshots and ref-based actions for navigation, interaction, extraction, sessions, screenshots, and network or storage operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live browser sessions, saved authentication state, cookies, and storage values.

Mitigation: Use it in an isolated environment, avoid real admin sessions unless necessary, treat saved auth JSON and browser state as secrets, and delete them after use.

Risk: The documented global npm install can resolve mutable tooling over time.

Mitigation: Prefer a pinned local install before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mifashion/skills/agent-dyxc)
- [ClawHub metadata homepage](https://www.sztv.com.cn/ysz/zx/zw/80706997.shtml)
- [agent-browser CLI project](https://github.com/vercel-labs/agent-browser)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes browser automation command examples, session guidance, state persistence guidance, and safety-relevant installation notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
