## Description:

Perform instant crypto swaps via ChangeNOW and earn affiliate commissions when routing token swaps with a partner fee.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yakelb0815](https://clawhub.ai/user/yakelb0815)

### License/Terms of Use:


## Use Case:

External users and developers can use this skill to estimate ChangeNOW exchange amounts or create crypto swap transactions that include the configured affiliate partner ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create third-party crypto swap transactions with affiliate attribution.

Mitigation: Use estimate-only mode first, disclose the partner fee routing, and proceed only after the user confirms the asset, network, amount, and destination address.

Risk: Crypto transfers can be irreversible and the artifact does not provide a built-in confirmation step or financial safety warning.

Mitigation: Independently verify transaction details before sending funds and avoid using a broadly privileged ChangeNOW API key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yakelb0815/skills/changenow)
- [ChangeNOW API base](https://api.changenow.io/v1)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Text]

**Output Format:** [Markdown guidance with shell commands; script output is JSON plus transaction instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CHANGENOW_API_KEY for estimates and transaction creation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
