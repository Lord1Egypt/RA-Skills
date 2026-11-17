## Description:

Query and filter 383,000+ court-released Jeffrey Epstein emails with structured JSON data through a pay-per-request API using USDC on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blockboy32](https://clawhub.ai/user/blockboy32)

### License/Terms of Use:


## Use Case:

Developers, researchers, and agents use this skill to search, filter, preview, and retrieve structured records from court-released Epstein email documents while estimating and confirming paid API requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API requests can spend wallet funds during searches or pagination.

Mitigation: Confirm cost before paid or paginated queries, use the free preview endpoint for estimates, and set a spending limit where supported.

Risk: A reused or high-value private key could expose funds if mishandled.

Mitigation: Use a fresh low-balance hot wallet funded only with the USDC needed for approved requests, and avoid logging, displaying, or echoing the private key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blockboy32/skills/epstein-emails)
- [Epstein Emails API](https://epsteinemails.xyz)
- [U.S. Department of Justice Epstein source documents](https://www.justice.gov/epstein)
- [x402 Protocol](https://x402.org)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON examples, tables, and Python/bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include paid API request guidance, pagination cost estimates, and x402 payment setup instructions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
