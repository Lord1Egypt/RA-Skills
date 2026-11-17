## Description:

58区块同城 helps agents retrieve digital city information, city popularity rankings, NFT avatar information, and block activity details for users of a blockchain-based digital city platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgta23](https://clawhub.ai/user/hgta23)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to ask an agent for digital city rankings, city details, NFT avatar marketplace information, and block activity summaries. It is most relevant when the user wants blockchain city data or NFT-related guidance surfaced through the documented 58区块同城 workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags requested local file read/write access as potentially unnecessary for the documented workflows.

Mitigation: Grant only the network access needed for documented city and NFT lookup workflows unless local file access is separately justified.

Risk: The skill describes NFT, wallet, purchase, trading, and governance activity that can have financial consequences.

Mitigation: Require the user to verify sites and wallet prompts directly, never request seed phrases or private keys, and obtain explicit confirmation before any transaction-like action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hgta23/skills/5)
- [58区块同城 official site](https://www.58.tl)
- [BlockCity city ranking endpoint](https://www.blockcity.vip/pages/block/area)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown text with optional inline shell commands and API-derived summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access; wallet, NFT purchase, trading, and governance actions should require explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
