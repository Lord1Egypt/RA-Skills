## Description:

Draft SOAP clinical notes, generate Medicare MBS item number reference tables, write patient recall SMS and email templates, and produce GP report letters for Australian allied health practitioners including physiotherapy, OT, psychology, speech pathology, and podiatry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arbazex](https://clawhub.ai/user/arbazex)

### License/Terms of Use:

MIT-0

## Use Case:

External Australian allied health practitioners and practice staff use this skill to draft clinical documentation, Medicare item-number reference tables, patient recall messages, and GP/referrer letters. Clinicians must verify all patient facts, clinical details, and billing details before use in practice.

### Deployment Geography for Use:

Australia

## Known Risks and Mitigations:

Risk: The security review found unsafe clinical-record examples that may invent patient details.

Mitigation: Require clinician review of every patient statement, objective finding, assessment, intervention, exercise, dosage, and billing detail before filing or sending outputs.

Risk: Medicare item descriptors, session limits, and rebate amounts can change.

Mitigation: Check current MBS Online and relevant Services Australia guidance before billing or advising on item numbers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arbazex/skills/au-allied-health-notes-recall)
- [MBS Online](https://www.mbsonline.gov.au)
- [Services Australia Medicare Benefits Schedule](https://www.servicesaustralia.gov.au/medicare-benefits-schedule-mbs)
- [AHPRA Managing Health Records](https://www.ahpra.gov.au/Resources/Managing-health-records.aspx)
- [Services Australia GP Chronic Condition Management Plan referrals](https://www.servicesaustralia.gov.au/allied-health-and-other-primary-health-care-referrals-for-gp-chronic-condition-management-plans)
- [Australian Government Better Access initiative](https://www.health.gov.au/topics/mental-health-and-suicide-prevention/what-were-doing/better-access-initiative)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown and structured text templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external API calls or real-time eligibility checks; outputs require clinician verification before practice, billing, or patient communication use.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
