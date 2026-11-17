## Description:

Turns a validated customer problem-discovery package into a POC engagement charter covering the business outcome, proof criteria, scope, mutual commitments, timeline, and governance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xukun0821](https://clawhub.ai/user/xukun0821)

### License/Terms of Use:

MIT-0

## Use Case:

FDEs, delivery leads, and customer-facing technical teams use this skill to convert a validated discovery package into a time-boxed POC charter with explicit proof criteria, scope, customer commitments, decision gates, and stop conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: POC charters may mention customer data, system access, owners, and risks.

Mitigation: Review charter outputs before sharing and avoid treating generated text as approved customer, legal, security, or operational commitments.

Risk: The local validator can confirm that required sections are present but cannot verify the accuracy of commitments or approvals.

Mitigation: Require accountable business, technical, and risk owners to confirm success criteria, scope, data access, timelines, and continue-adjust-stop decisions.

Risk: A POC charter can be misread as production approval or permission to bypass compliance gates.

Mitigation: Keep production approval, sensitive data handling, system write access, privacy, legal, procurement, and compliance decisions as explicit preconditions with owners.

## Reference(s):

- [POC Contract Entry Guide](references/charter-input-guide.md)
- [POC Contract Rules](references/charter-rules.md)
- [FDE POC Project Contract Template](references/engagement-charter-template.md)
- [POC Contract Field Manual](references/charter-field-handbook.md)
- [POC Contract Quality Score](references/charter-quality-rubric.md)
- [Complete Example of POC Contract](references/charter-worked-example.md)
- [Atlassian Project Poster](https://www.atlassian.com/team-playbook/plays/project-poster)
- [Atlassian Goals, Signals, Measures](https://www.atlassian.com/team-playbook/plays/goals-signals-measures)
- [AWS Designing Generative AI for Success POC](https://docs.aws.amazon.com/prescriptive-guidance/latest/gen-ai-lifecycle-operational-excellence/dev-architecting.html)
- [GOV.UK How the Discovery Phase Works](https://www.gov.uk/service-manual/agile-delivery/how-the-discovery-phase-works)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown charter content with an optional shell command for structural validation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces draft or frozen POC charter guidance; the bundled validator checks document structure but does not prove business, technical, legal, or security approval.]

## Skill Version(s):

1.0.0 (source: server release evidence and TRUST-CARD.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
