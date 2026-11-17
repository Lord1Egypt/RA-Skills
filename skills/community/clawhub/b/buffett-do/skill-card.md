## Description:

Buffett-style research prioritization assistant that helps decide whether a company deserves deeper research, what to check first, and provides a copy-paste prompt for another agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[choosenobody](https://clawhub.ai/user/choosenobody)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to triage company or ticker research ideas, identify three checks to perform first, and generate a short prompt for deeper business analysis. It is not intended to provide financial advice, buy/sell/hold calls, price targets, or portfolio allocation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat research-prioritization labels as financial advice.

Mitigation: Present outputs as research triage only and avoid buy, sell, hold, price-target, or portfolio-allocation guidance.

Risk: Sensitive financial credentials or private portfolio data could be exposed if supplied unnecessarily.

Mitigation: Do not provide brokerage credentials, wallet keys, private portfolio files, or other sensitive financial data.

Risk: A lightweight prompt can miss current facts or valuation context.

Mitigation: Verify business quality, moat or thesis risk, and valuation sanity with current sources before relying on the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/choosenobody/skills/buffett-do)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with a short decision label, three verification checks, and a copy-paste research prompt.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code; no API keys or credentials requested.]

## Skill Version(s):

1.1.10 (source: server release metadata; artifact frontmatter reports 1.1.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
