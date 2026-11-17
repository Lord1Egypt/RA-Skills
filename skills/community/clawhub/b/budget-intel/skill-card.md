## Description:

Budget Intel helps sales and customer success teams estimate enterprise digitalization and AI budgets, budget composition, procurement timing, and sales recommendations from public company research and local budget calculations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ken0122](https://clawhub.ai/user/ken0122)

### License/Terms of Use:


## Use Case:

Sales, customer success, and go-to-market teams use this skill to build concise budget intelligence for named companies. It combines public-source company research with a local estimator to produce budget ranges, confidence notes, procurement-cycle context, stakeholder-role guidance, supplier context, and sales advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Budget, procurement, supplier, and stakeholder-role outputs are inferred estimates and may be inaccurate or outdated.

Mitigation: Verify cited public sources and treat the report as sales planning input rather than a decision record.

Risk: Company research workflows can drift into private personal information collection when identifying decision makers.

Mitigation: Use public business information only and avoid collecting or inferring private personal information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ken0122/skills/budget-intel)
- [Skill instructions](artifact/SKILL.md)
- [Tool schema](artifact/tools_schema.json)
- [Budget engine](artifact/budget_engine.py)
- [Test cases](artifact/TEST_CASES.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with budget ranges, confidence notes, tables, and concise sales recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language one-page intelligence report; budget and stakeholder outputs are estimates that require source verification.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact MANIFEST.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
