## Description:

Helps an agent list, import, price, limit, inspect, and remove a Codex or ChatGPT subscription offered for sale on the asale market.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage selling a Codex or ChatGPT subscription through the asale daemon, including account discovery, marketplace enablement, price floors, concurrency limits, lane status checks, and delisting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release uses a remote installer for the asale daemon.

Mitigation: Verify the installer from a trusted release and prefer a pinned version with a checksum or signature before running it.

Risk: The daemon can import and retain Codex or ChatGPT subscription credentials for marketplace selling.

Mitigation: Review exactly which accounts are imported before enabling selling and only proceed if credential retention for this purpose is acceptable.

Risk: The sample flow can import every discovered account.

Mitigation: Run discovery and account listing first, then enable selling only for the intended account with reviewed price and concurrency settings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dlazyai/skills/asale-sell-codex)
- [Publisher profile](https://clawhub.ai/user/dlazyai)
- [asale homepage](https://asale.ai)
- [asale source repository](https://github.com/asale-ai/asale)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local daemon RPC examples and operational cautions for account selling settings.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 0.2.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
