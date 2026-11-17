## Description:

Helps users manage real austerity after a drastic income drop by prioritizing which bills to pay first, what to negotiate, what to stop completely, and how to maintain dignity while doing it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to build a prioritized financial survival plan after severe income loss, including which bills to pay first, which expenses to reduce or stop, and which creditors or assistance programs to contact.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill may track sensitive financial state.

Mitigation: Only store financial details in trusted workspaces and remove stored state when it is no longer needed.

Risk: Recurring calendar reminders may continue after bill negotiation tasks are complete.

Mitigation: Enable reminders only when wanted and disable them after the calls or assistance applications are complete.

Risk: Installer provenance is not available in the server evidence.

Mitigation: Verify that `npx clawhub` resolves from a trusted registry or use a pinned installer if available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/howtousehumans/skills/austerity-living)
- [Publisher Profile](https://clawhub.ai/user/howtousehumans)
- [HHS Poverty Guidelines](https://aspe.hhs.gov/topics/poverty-economic-mobility/poverty-guidelines)
- [USDA SNAP](https://www.fns.usda.gov/snap/supplemental-nutrition-assistance-program)
- [HealthCare.gov](https://www.healthcare.gov/)
- [KFF Medicaid](https://www.kff.org/medicaid/)
- [LIHEAP](https://www.acf.hhs.gov/ocs/programs/liheap)
- [Feeding America Food Bank Locator](https://www.feedingamerica.org/find-your-local-foodbank)
- [Federal Student Aid Income-Driven Repayment](https://studentaid.gov/manage-loans/repayment/plans/income-driven)
- [CFPB Mortgage Relief Options](https://www.consumerfinance.gov/housing/)
- [NeedyMeds](https://www.needymeds.org/)
- [Benefits.gov](https://www.benefits.gov/)
- [211](https://www.211.org/)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with checklists, scripts, and YAML agent state examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use calendar reminders and filesystem-backed financial state when the host agent provides those tools.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
