## Description:

Organizes audit evidence into catalogs, checklists, control mappings, missing-item lists, naming suggestions, priorities, and delivery recommendations for later review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Compliance, audit, governance, and evidence-management users use this skill to turn provided evidence folders, control lists, or narrative inputs into reviewable evidence summaries, control mappings, missing-evidence lists, and next-step recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can summarize local evidence folders, which may include personal, credential, or private material if the user selects a broad directory.

Mitigation: Run it only on intended evidence folders, avoid broad home or private directories, and review outputs before sharing.

Risk: The generated report may contain incomplete or misleading compliance evidence if source materials are missing or ambiguous.

Mitigation: Treat outputs as review drafts, keep missing items visible, and do not use the skill as a substitute for a formal audit conclusion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/compliance-evidence-assembler)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and optional JSON report payloads with reviewable checklists and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with python3 and the standard library; default behavior is read-only analysis of provided inputs.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
