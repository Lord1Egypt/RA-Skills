## Description:

Batch monthly-close self-check for bookkeeping agencies. Runs the seven industry monthly self-check packs for every client folder in one go, one result line per client, and every finding cites the source file and line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Bookkeeping agency accountants and supervisors use this before monthly-close delivery to batch-check every client folder, identify pass/problem/not-run status across seven industry self-check packs, and trace findings back to source files and line numbers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the client materials supplied through the selected input folder.

Mitigation: Run it only on intended local client folders and review what materials are included before execution.

Risk: Self-check output may be mistaken for a complete audit, tax opinion, accounting compliance judgment, or professional review.

Mitigation: Treat results as local month-close self-check findings and have qualified staff review unresolved issues before delivery.

Risk: Missing, partial, or malformed client materials can leave checks marked as not run rather than passed.

Mitigation: Review not-run statuses and source file/line citations for each client before relying on the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/agency-monthly-close-free)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Plain text stdout summaries, with JSON available when --json is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-only batch results with client names, package status, finding counts, and source file/line citations]

## Skill Version(s):

1.0.28 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
