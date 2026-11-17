## Description:

Skill for interacting with the CarboSilex137 decentralized freelance marketplace API, enabling agents to browse jobs, submit proposals, manage escrows, and track deliveries on the Web3-powered platform built on Base L2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guzzt](https://clawhub.ai/user/guzzt)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to browse CarboSilex137 jobs, submit proposals, deliver work, manage messages, and check escrow status through the marketplace API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated commands can post jobs, submit proposals or deliveries, and send messages through the user's marketplace account.

Mitigation: Require human review before sending proposals, deliveries, job posts, or messages.

Risk: CARBOSILEX_API_KEY is a bearer credential, and the client can also read api_key.txt.

Mitigation: Keep CARBOSILEX_API_KEY protected and avoid api_key.txt unless file access is tightly controlled.

Risk: Changing CARBOSILEX_API_URL can direct requests and credentials to an untrusted endpoint.

Mitigation: Use only trusted API endpoints and do not override CARBOSILEX_API_URL except for verified environments.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/guzzt/skills/carbosilex-skill)
- [CarboSilex137 API Docs](https://api.carbosilex137.com/docs)
- [CarboSilex137 Website](https://carbosilex137.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use CARBOSILEX_API_URL and CARBOSILEX_API_KEY; authenticated actions can modify marketplace state.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
