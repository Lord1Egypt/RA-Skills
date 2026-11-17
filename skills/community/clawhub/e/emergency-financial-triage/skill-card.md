## Description:

Emergency Financial Triage provides a priority-based action plan for immediate financial emergencies such as missed rent, eviction risk, food insecurity, utility shutoff, or sudden income loss.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users and support agents use this skill to prioritize urgent needs, contact creditors, avoid predatory loans, and locate assistance resources during a financial crisis.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill declares calendar and filesystem access without explaining why those permissions are needed.

Mitigation: Install only if those permissions are acceptable for the deployment, or ask the publisher to remove them and provide a pinned, reproducible install command.

Risk: The financial assistance programs, phone numbers, and agency links are US-focused.

Mitigation: Confirm local equivalents before using the guidance outside the United States.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howtousehumans/skills/emergency-financial-triage)
- [USDA Supplemental Nutrition Assistance Program](https://www.fns.usda.gov/snap/supplemental-nutrition-assistance-program)
- [LIHEAP program](https://www.acf.hhs.gov/ocs/programs/liheap)
- [US Treasury Emergency Rental Assistance Program](https://home.treasury.gov/policy-issues/coronavirus/assistance-for-state-local-and-tribal-governments/emergency-rental-assistance-program)
- [211 helpline](https://www.211.org/)
- [NeedyMeds prescription assistance](https://www.needymeds.org/)
- [FindHelp local assistance search](https://www.findhelp.org)
- [LawHelp legal aid directory](https://www.lawhelp.org)
- [Feeding America food bank locator](https://www.feedingamerica.org/find-your-local-foodbank)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown guidance with prioritized checklists and call scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [US-focused resources; requires local adaptation outside the United States.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
