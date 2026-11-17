## Description:

Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate browser navigation, interaction, state inspection, and extraction through the agent-browser CLI. It is useful for multi-step web workflows that benefit from JSON accessibility snapshots and stable element references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved browser auth state can include cookies or storage values that behave like login credentials.

Mitigation: Keep saved state files private, avoid committing them, and use separate sessions for each account or role.

Risk: Browser automation commands can interact with real sites, stored sessions, cookies, storage, and network routes.

Mitigation: Use the skill only for sites and sessions the agent is intended to control, and review sensitive cookie, storage, network-mocking, and interaction commands before execution.

Risk: Global CLI installation and browser downloads can introduce supply-chain or environment risk.

Mitigation: Install from trusted sources and prefer pinned or reviewed agent-browser versions where possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/demo-resource-upload)
- [agent-browser Project Homepage](https://github.com/vercel-labs/agent-browser)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the agent-browser command and browser installation for execution.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
