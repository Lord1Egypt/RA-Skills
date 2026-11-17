## Description:

Retrieves and assesses a company's retirement plan details from planprovider.pro, including providers, participation, assets, plan type, compliance signals, and source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oil-can-man](https://clawhub.ai/user/oil-can-man)

### License/Terms of Use:

MIT-0

## Use Case:

External plan advisors, consultants, and sales teams use this skill to research a company's 401(k), 403(b), or retirement plan profile, benchmark plan health, identify current providers, and prepare for sponsor conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Form 5500-derived retirement-plan data can lag current plan status.

Mitigation: State the filing year shown by the source as the as-of date and verify important business conclusions against the cited source.

Risk: Unsupported company identifiers, balances, or provider relationships could mislead plan research.

Mitigation: Report only details present in the planprovider.pro markdown response and include the source company URL.

Risk: A company may not be present in the planprovider.pro directory under the searched name.

Mitigation: Report that the company is not currently listed and offer to search by EIN, state, or alternate legal name.

## Reference(s):

- [PlanProvider company directory](https://planprovider.pro/companies)
- [ClawHub skill page](https://clawhub.ai/oil-can-man/skills/401k-plan-health)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summary with linked provider references and a source company URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes company, plan name, EIN when shown, participants, total assets, plan type, current providers, notable health signals, filing year, and source URL.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
