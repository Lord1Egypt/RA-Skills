## Description:

Generates draft privacy policy documents for GDPR/CCPA-oriented workflows, including data-practice scans, consent-flow audits, compliance checks, and policy drafting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate draft privacy policy text for websites and apps, including GDPR- and CCPA-oriented variants. Users should treat the output as a starting point for legal review rather than compliance verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated privacy policies may be incomplete, jurisdiction-specific, or legally inaccurate.

Mitigation: Use generated text only as a draft and have qualified legal counsel verify the final policy before publication.

Risk: The artifact includes a separate security CLI that can persist raw command inputs locally.

Mitigation: Inspect commands before execution and do not pass secrets, passwords, tokens, or confidential policy details to the CLI.

Risk: The package purpose is inconsistent because it combines privacy-policy generation with unrelated security-tool commands.

Mitigation: Review the full artifact before installation and expose only the commands required for the intended privacy-policy workflow.

## Reference(s):

- [BytesAgain homepage](https://bytesagain.com)
- [ClawHub skill page](https://clawhub.ai/loutai0307-prog/skills/bytesagain-privacy-policy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text and Markdown-style policy templates with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes legal disclaimers; generated policy text requires qualified legal review before use.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and script declare 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
