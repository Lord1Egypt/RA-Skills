## Description:

Generate professional Amazon market research reports using a complete 18-step product development framework.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lenger666](https://clawhub.ai/user/lenger666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate structured Amazon product-market research for a specified product, country, and ecommerce platform. The report supports product development and market-entry decisions with an 18-step analysis framework.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill loads a local .env file as shell code.

Mitigation: Review the .env file before use, keep it owner-writable only, and avoid placing shell commands or untrusted content in it.

Risk: The skill uses API credentials and sends market-research queries to the configured external model provider.

Mitigation: Protect MARKET_API_KEY and avoid submitting confidential product plans unless third-party processing is acceptable.

Risk: The skill stores generated reports on disk.

Mitigation: Review local report files for sensitive business information and manage retention according to the user's data-handling requirements.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON containing a full report answer and metadata; also writes a local Markdown report file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured model API key and sends market-research queries to the configured OpenAI-compatible chat completions endpoint.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
