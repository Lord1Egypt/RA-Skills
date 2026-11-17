## Description:

Generates a preliminary duplicate-contact report from a US sales contact CSV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US sales operations and RevOps staff can use this skill to produce an initial duplicate-contact report from a CSV before manually reviewing records. The report is preliminary and should not be treated as validated or ready to import.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The preliminary report may be mistaken for validated, safely merged, import-ready contact data, although the skill's documented human-review outputs are not established by the report.

Mitigation: Use copies of data, correct the template header, manually check blank emails and shared inboxes, and independently review records before import.

Risk: The optional Windows application is separate from the skill bundle and requires its own security assessment.

Mitigation: Do not treat the bundle's report as an assessment of that application; assess it separately before deciding whether to obtain or run it.

## Reference(s):

- [US contact data rules for a clean CRM](references/crm-hygiene-rules.md)
- [CRM Hygiene Cleanup on ClawHub](https://clawhub.ai/rapidworker1/skills/crm-hygiene-cleanup)

## Skill Output:

**Output Type(s):** [Files, Markdown]

**Output Format:** [A duplicates.md preliminary report with row counts and up to 100 repeated-email entries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Written to the selected output directory; does not establish that contacts are validated or ready to import.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
