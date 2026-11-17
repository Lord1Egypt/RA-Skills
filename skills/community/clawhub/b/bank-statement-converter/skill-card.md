## Description:

Convert PDF bank statements to CSV or JSON using API calls with support for password-protected files and processing status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ballerindustries](https://clawhub.ai/user/ballerindustries)

### License/Terms of Use:


## Use Case:

Developers and finance operations users can use this skill to prepare API calls that upload bank statement PDFs, check processing status, and retrieve converted transaction data as CSV or JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles highly sensitive bank statements through a third-party API.

Mitigation: Review the provider's privacy, retention, and security terms before using real bank statements.

Risk: The skill includes a shell command pattern that places a PDF password directly in a command payload.

Mitigation: Avoid pasting real PDF passwords directly into shell commands; prefer local decryption or a safer client flow that keeps secrets out of shell history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ballerindustries/skills/bank-statement-converter)
- [Bank Statement Converter registration](https://bankstatementconverter.com/legacy-register)
- [Bank Statement Converter account settings](https://bankstatementconverter.com/settings)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BANKSTATEMENT_API_KEY and access to the Bank Statement Converter API.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
