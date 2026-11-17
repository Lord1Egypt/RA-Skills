## Description:

Switches OpenClaw between buying from the asale market and using its own subscription, and reports running sessions that are still using the previous configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to route OpenClaw through asale's local buying flow, select market models, restore the prior configuration, and identify sessions that need a restart before the new configuration takes effect.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install and update path executes a live remote script.

Mitigation: Download and inspect the installer before execution, and prefer a versioned release with checksum or signature verification.

Risk: The skill can route OpenClaw traffic through asale using a signed-in asale account.

Mitigation: Confirm the account, model selection, and buying mode before enabling the switch, and verify the resulting state with buy_tools.

Risk: The skill rewrites OpenClaw configuration for future sessions.

Mitigation: Review the target config path before changing it, keep the generated snapshot available for restore, and tell users that already-running sessions keep their old configuration until restarted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dlazyai/skills/asale-buy-openclaw-cli)
- [asale homepage](https://asale.ai)
- [asale project source](https://github.com/asale-ai/asale)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and JSON RPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides local OpenClaw configuration changes through the asale daemon; the skill itself does not produce standalone files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and target metadata; artifact frontmatter reports 0.2.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
