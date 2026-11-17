## Description:

Car Log helps an assistant manage vehicle mileage, refueling, maintenance, and expense records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengkang](https://clawhub.ai/user/zengkang)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to let an assistant track multiple vehicles, record mileage, fuel, maintenance, and expenses, and summarize cost and consumption information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete vehicle and expense records, including bulk deletion.

Mitigation: Use explicit user requests for delete operations and review the target vehicle or record before deletion.

Risk: The skill stores persistent vehicle names, plates, notes, mileage, refueling, maintenance, and expense data locally.

Mitigation: Install only where local persistence of this data is acceptable, and treat stored names and notes as untrusted text.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text with inline shell commands and concise lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, update, query, and soft-delete local persistent vehicle, mileage, refueling, maintenance, and expense records.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
