## Description:

Book flights, hotels, and eSIMs on cryptotraveler.com with Bitcoin and other cryptocurrencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g33kme](https://clawhub.ai/user/g33kme)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to help agents search flights, hotel stays, and eSIM packages, prepare booking workflows, and redirect users to hosted checkout for cryptocurrency payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CryptoTraveler API credentials and optional USER_ACCESS tokens can expose booking or account data if placed in prompts, logs, repositories, or shared folders.

Mitigation: Store CLIENT_SECRET and USER_ACCESS outside prompts and source files, preferably in a secret manager or tightly permissioned local storage, and revoke exposed secrets immediately.

Risk: Travel booking workflows can require personal passenger or guest data and may present multiple valid offers or changed booking conditions.

Mitigation: Validate required fields, ask the user for missing or ambiguous details, and obtain confirmation before continuing when selections or conditions are unclear.

## Reference(s):

- [CryptoTraveler Skill Page](https://clawhub.ai/g33kme/skills/crypto-traveler)
- [CryptoTraveler Homepage](https://www.cryptotraveler.com)
- [CryptoTraveler Agent Registration](https://www.cryptotraveler.com/en/agent)
- [CryptoTraveler Flights](https://www.cryptotraveler.com/en/flight)
- [CryptoTraveler Hotels and Stays](https://www.cryptotraveler.com/en/stay)
- [CryptoTraveler eSIM](https://www.cryptotraveler.com/en/esim)
- [CryptoTraveler Agents API Base](https://agents.cryptotraveler.com/v1)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with JSON, HTTP, bash, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API endpoint workflows, HMAC signing guidance, credential handling rules, and hosted checkout handoff guidance.]

## Skill Version(s):

1.3.2 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
