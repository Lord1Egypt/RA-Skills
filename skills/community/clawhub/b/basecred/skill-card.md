## Description:

BaseCred fetches unified onchain reputation profiles for 0x wallet addresses from Ethos, Talent Protocol, and optional Farcaster/Neynar sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[callmedas69](https://clawhub.ai/user/callmedas69)

### License/Terms of Use:


## Use Case:

Developers and agents use BaseCred to query a wallet address, interpret Ethos, Talent Protocol, and Farcaster reputation signals, and present credibility, score levels, and freshness caveats to end users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The query script loads values from a discovered .env file, which can expose unrelated workspace secrets to the runtime.

Mitigation: Run the skill only in a workspace whose .env contains no unrelated secrets, or provide only the required API keys through a tightly controlled environment.

Risk: The documented install command resolves the latest basecred-sdk package at install time.

Mitigation: Pin and review the basecred-sdk version before use.

## Reference(s):

- [BaseCred Output Schema and Level Tables](references/output-schema.md)
- [BaseCred ClawHub Skill Page](https://clawhub.ai/callmedas69/skills/basecred)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Guidance]

**Output Format:** [JSON from the query script, followed by concise Markdown or text summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a 0x wallet address and TALENT_PROTOCOL_API_KEY; NEYNAR_API_KEY is optional for Farcaster scoring.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
