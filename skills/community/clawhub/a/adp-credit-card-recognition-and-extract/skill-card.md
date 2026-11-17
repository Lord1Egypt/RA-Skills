## Description:

Recognizes bank-card images with Laiye ADP and extracts card number, issuing institution, validity period, and card type as structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laiye-adp](https://clawhub.ai/user/laiye-adp)

### License/Terms of Use:

Commercial License Agreement

## Use Case:

Developers and operations teams use this skill to configure the ADP CLI and extract structured bank-card fields for account opening, payment binding, and financial data-entry workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup documentation includes unverified installer patterns such as curl-to-bash, PowerShell iex, and unpinned global npm installation.

Mitigation: Prefer a pinned, verifiable release or inspected binary before installing the ADP CLI.

Risk: Bank-card images may contain sensitive financial data and are sent to Laiye ADP for processing.

Mitigation: Process only card images the user is authorized to send, and review Laiye ADP data-handling terms before use.

Risk: The ADP CLI exposes broader document-processing and application-management commands than the narrow bank-card extraction task requires.

Mitigation: Grant agents only the ADP commands and credentials needed for the intended card-recognition workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laiye-adp/skills/adp-credit-card-recognition-and-extract)
- [ADP China portal](https://adp.laiye.com/?utm_source=clawhub)
- [ADP global portal](https://adp-global.laiye.com/?utm_source=clawhub)
- [ADP CLI user guide](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc)
- [ADP Open API guide](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc)
- [ADP CLI releases](https://github.com/laiye-ai/adp-cli/releases)
- [ADP CLI issues](https://github.com/laiye-ai/adp-cli/issues)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured field values for card number, issuing institution, validity period, and card type; supports URL, local file, Base64, batch, and async workflows.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
