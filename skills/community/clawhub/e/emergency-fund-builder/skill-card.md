## Description:

Step-by-step protocol for building an emergency fund from zero for users who have no savings buffer, live paycheck to paycheck, or want a concrete system to build financial resilience.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to calculate emergency fund targets, identify realistic monthly savings, choose safe account criteria, automate transfers, and define when the fund should be used. Agents can use it to guide structured financial resilience conversations without recommending specific banks or investment products.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may retain sensitive financial profile details between sessions.

Mitigation: Do not provide account numbers, passwords, banking login information, or other credentials; prefer session-only use or clear deletion controls for stored budget details.

Risk: The installer command is unpinned.

Mitigation: Verify the ClawHub publisher, package name, and source before running the npx install command.

Risk: Filesystem access is requested without a clear user-facing need in the release evidence.

Mitigation: Grant filesystem access only when needed for an explicit task and review what files the agent can read or write.

## Reference(s):

- [Emergency Fund Builder on ClawHub](https://clawhub.ai/howtousehumans/skills/emergency-fund-builder)
- [FDIC](https://www.fdic.gov/)
- [Consumer Financial Protection Bureau](https://www.consumerfinance.gov/)
- [National Foundation for Credit Counseling](https://www.nfcc.org/)
- [National Credit Union Administration](https://mycreditunion.gov/)
- [Bankrate High-Yield Savings Account Comparisons](https://www.bankrate.com/banking/savings/best-high-yield-interests-savings-accounts/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration instructions]

**Output Format:** [Markdown guidance with interactive prompts, checklists, calculations, and YAML-style state and reminder definitions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request and retain sensitive financial profile details such as monthly expenses, savings targets, transfer settings, and emergency definitions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
