## Description:

Switch Gemini CLI between buying from the asale market and using its own subscription, and identify running Gemini CLI sessions that are still using the old configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Gemini CLI users use this skill to route future Gemini CLI sessions through the local asale daemon for market buying, restore the original Gemini configuration, and check which existing sessions still need to be restarted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or updating asale uses an unverified remote installer script.

Mitigation: Review the installer source or use a verifiable release path before running install or update commands.

Risk: The skill reads the local asale daemon token and sends it to the loopback daemon for RPC calls.

Mitigation: Keep the daemon token local, use the loopback endpoint, and avoid exposing the token in logs, shared terminals, or remote shells.

Risk: The skill changes Gemini CLI configuration so future sessions may route through asale.

Mitigation: Run the status check before changing settings, confirm the target tool is Gemini CLI, and verify the configuration after switching.

Risk: Already-running Gemini CLI sessions may continue using the previous configuration.

Mitigation: Report affected sessions for user review and let the user decide which sessions to restart.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dlazyai/skills/asale-buy-gemini-cli)
- [asale homepage](https://asale.ai)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON RPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is intended for local daemon interaction and Gemini CLI configuration changes.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter is 0.2.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
