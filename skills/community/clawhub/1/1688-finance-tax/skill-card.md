## Description:

A finance and tax burden calculation skill that helps agents calculate tax-inclusive product pricing, VAT, combined VAT/surtax/stamp/income-tax impacts, and overall annual tax burden.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External business users and agents use this skill to collect finance and tax inputs, run 1688 tax-calculation commands, and present concise Chinese Markdown results with an advisory disclaimer. It supports VAT-only pricing, four-tax pricing, and annual overall tax burden scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access keys may be handled through environment variables, OpenClaw configuration, or the configure command.

Mitigation: Use a platform-managed secret store where available and avoid giving the agent raw AK values in chat or command-line history.

Risk: A configurable OpenClaw gateway URL can affect where credential configuration is written.

Mitigation: Verify OPENCLAW_GATEWAY_URL is trusted and either local or HTTPS before running configuration commands.

Risk: Business and tax inputs are sent to the 1688 skill gateway for calculations.

Mitigation: Review data-handling requirements before using real business or tax data and submit only the inputs needed for the calculation.

Risk: Usage events may be reported after CLI commands run.

Mitigation: Assume invocation metadata can be reported to the 1688 gateway and review this behavior before installation.

Risk: Tax calculations may be incomplete or unsuitable for a specific filing situation.

Mitigation: Keep the user-facing disclaimer and have qualified tax staff review results before business or compliance decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/1688-finance-tax)
- [1688aiinfra publisher profile](https://clawhub.ai/user/1688aiinfra)
- [Distribution notes](artifact/DISTRIBUTION.md)
- [Tax calculation workflow](artifact/references/tax-calculation.md)
- [Field mapping reference](artifact/references/reference.md)
- [Common user-facing rules](artifact/references/common/common-rules.md)
- [1688 tax calculator pages](https://work.1688.com/?_path_=sellerPro/zijinguanli/taxrouter&_hex_tracelog=openSkills)
- [ClawHub AK portal](https://clawhub.1688.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON command results containing a Markdown field for user-facing Chinese output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command outputs include success, markdown, and data fields; results should be treated as advisory tax calculations.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact constants report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
