## Description:

Provides paid daily weather reports for a user-specified location after creating and verifying a Clawtip/JD payment order.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liulian822](https://clawhub.ai/user/liulian822)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to request a weather report for a location after completing a paid Clawtip/JD order flow. Agents use it to create the order, pass payment parameters to the bundled Clawtip payment helper, and return the resulting weather report or payment status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill drives real payment flows before producing the weather report.

Mitigation: Install only when this specific paid weather workflow is intended, require clear user confirmation for payment actions, and do not allow the workflow to skip payment inspection or confirmation.

Risk: Payment tokens and order credentials are stored in local plaintext JSON files.

Mitigation: Use a single-user trusted machine, restrict file and directory permissions, and apply disk encryption on shared or security-sensitive hosts.

Risk: The weather skill depends on the bundled Clawtip payment helper and its external JD payment endpoints.

Mitigation: Verify the Clawtip payment skill publisher and version before use, and review outbound network behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liulian822/skills/clawtip-weather-bak)
- [ClawHub publisher profile](https://clawhub.ai/user/liulian822)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with command snippets, order fields, payment status, and a weather report response.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow can initiate a paid order, stores order/payment state locally, and requires payment verification before report generation.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata; artifact metadata lists bundled source version 1.0.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
