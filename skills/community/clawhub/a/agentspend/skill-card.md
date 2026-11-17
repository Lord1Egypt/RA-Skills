## Description:

AgentSpend helps agents discover priced services and call paid x402 endpoints through AgentSpend Cloud with budget, allowlist, and per-request cost controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpbonch](https://clawhub.ai/user/jpbonch)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to search for paid external services, check endpoint pricing, configure spending controls, and make paid API requests when built-in tools are insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger paid external API requests through AgentSpend Cloud.

Mitigation: Set a low weekly budget and domain allowlist, check prices before paid requests, and require --max-cost on every pay command.

Risk: The documented workflow uses npx agentspend without pinning a reviewed CLI version.

Mitigation: Use a pinned reviewed version of the CLI in controlled environments.

Risk: Credentials are stored locally and paid requests may include request bodies or headers.

Mitigation: Avoid sending secrets, private headers, or regulated data through paid endpoints unless AgentSpend Cloud and the target provider are trusted for that data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jpbonch/skills/agentspend)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include paid API response bodies, charge amounts, remaining weekly budget, endpoint prices, service search results, and configuration URLs.]

## Skill Version(s):

0.1.3 (source: server release metadata; package.json reports 0.2.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
