## Description:

Switches opencode between asale market buying and its own subscription, and identifies running sessions that still use the old configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and opencode users use this skill to switch opencode traffic between an asale market buying flow and their own subscription, inspect available market models, and understand which running sessions still use the previous configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer is fetched and executed from a mutable remote URL.

Mitigation: Review the installer before running it, and prefer a signed or checksum-verified release when available.

Risk: The skill can alter opencode configuration and route future opencode usage through asale buying.

Mitigation: Run buy_tools before set_buy_tool, confirm the selected models and account implications, and tell users the switch affects opencode on its next start.

Risk: Running opencode sessions may continue using the old configuration.

Mitigation: Report affected sessions as informational only and let users decide which sessions to restart.

Risk: The skill reads the local asale daemon token to call the loopback daemon.

Mitigation: Keep daemon calls on the loopback endpoint, use the token only for local RPC calls, and do not expose or copy the token into outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dlazyai/skills/asale-buy-opencode)
- [asale homepage](https://asale.ai)
- [asale source repository](https://github.com/asale-ai/asale)
- [asale Unix installer](https://asale.ai/dl/install.sh)
- [asale Windows installer](https://asale.ai/dl/install.ps1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command snippets and JSON RPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local daemon status, opencode config paths, selected models, and running process information.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter is 0.2.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
