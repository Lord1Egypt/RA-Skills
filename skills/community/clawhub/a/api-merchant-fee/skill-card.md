## Description:

API Merchant Fee helps agents query merchant fee and rate information by collecting merchant, terminal, agent, and API-key parameters and calling the bundled merchant-fee API script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sgfa005](https://clawhub.ai/user/sgfa005)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and payment operations users use this skill to look up merchant fee, debit card, credit card, scan payment, terminal, and merchant management fee details from merchant and terminal identifiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials may be passed on the command line, saved in a local plaintext file, and reused automatically.

Mitigation: Use only in environments where that credential handling is acceptable, or replace it with a managed secret store and explicit credential reuse.

Risk: The artifact ships a possible hardcoded API key and an HTTP endpoint.

Mitigation: Treat the bundled key as exposed, avoid production credentials, require HTTPS, and validate the official API host before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sgfa005/skills/api-merchant-fee)
- [Publisher profile](https://clawhub.ai/user/sgfa005)
- [Configured merchant fee API endpoint](http://47.111.144.23:8094/agent/getMerchantFeeInfo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance]

**Output Format:** [Markdown fee summaries, error messages, and parameter prompts with shell command usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should not expose API keys.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
