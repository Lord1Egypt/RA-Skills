## Description:

Calculate loan payments for mortgages, car loans, and personal loans using equal principal plus interest or equal principal repayment methods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to calculate loan repayment totals, interest, and monthly payment values for common loan scenarios. It is a lightweight local calculator and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calculator results may be unsuitable for financial decisions if users rely on them without review.

Mitigation: Treat outputs as lightweight estimates and review them carefully before making financial decisions.

Risk: Unbounded or untrusted loan terms can create reliability issues because additional validation and timeouts are not present.

Mitigation: Add input bounds, validation, and execution time limits before forwarding untrusted loan terms.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python CLI usage and JSON calculator output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Python standard library only; no API key or network service is required.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
