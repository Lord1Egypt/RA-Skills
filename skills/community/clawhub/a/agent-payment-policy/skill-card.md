## Description:

Bind a buyer-owned response contract to an agent payment decision and validate the settled output before accepting delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[epistemedeus](https://clawhub.ai/user/epistemedeus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent builders use this skill to decide, bind, and classify paid JSON responses so payment settlement and output validity remain separate acceptance decisions. It is intended for x402, MPP, HTTP 402, paid API, paid MCP, and other machine-commerce workflows that need a buyer-owned output contract.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The npm CLI dependency is third-party code and may run in contexts that also contain wallet secrets, signing keys, or unrelated credentials.

Mitigation: Use locked installs with integrity metadata, run the local installed binary or npx with no-install behavior, and keep wallet secrets, signing keys, and unrelated credentials out of the execution environment.

Risk: A paid response can settle successfully while the delivered body fails the buyer-owned schema or freshness requirements.

Mitigation: Preserve payment settlement and output validation as independent receipt fields, and release paid output to downstream reasoning only after validation passes.

## Reference(s):

- [JSON Schema 2020-12](https://json-schema.org/draft/2020-12/schema)
- [ClawHub Skill Page](https://clawhub.ai/epistemedeus/skills/agent-payment-policy)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON, JavaScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on buyer-owned JSON Schema contracts, authorization binding, delivery validation, and receipt completeness checks.]

## Skill Version(s):

0.15.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
