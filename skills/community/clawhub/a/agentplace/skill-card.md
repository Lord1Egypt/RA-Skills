## Description:

Agentplace lets OpenClaw users browse, search, inspect, and install community-contributed agent skills from the Agentplace marketplace when explicitly requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[himanshunextbase](https://clawhub.ai/user/himanshunextbase)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to discover marketplace agents, review their metadata and documentation, and install selected free or paid agents into a local OpenClaw workspace after explicit confirmations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install flow can persistently add third-party skills without strong package verification or safe extraction controls.

Mitigation: Install only trusted agents, preview archive contents and skill documentation before installation, and prefer releases with signed packages or published SHA-256 checksums.

Risk: Paid-agent downloads require an API key that could be exposed if pasted into prompts or shared transcripts.

Mitigation: Store API keys securely and do not paste real keys into prompts, transcripts, public repositories, or shared logs.

## Reference(s):

- [Agentplace ClawHub listing](https://clawhub.ai/himanshunextbase/skills/agentplace)
- [Agentplace dashboard](https://www.agentplace.sh/dashboard)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include marketplace API requests, install prompts, archive preview steps, and API-key handling guidance.]

## Skill Version(s):

2.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
