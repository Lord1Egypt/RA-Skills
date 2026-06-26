## Description: <br>
儿童成长跟踪与评估 is a child-growth recordkeeping and assessment skill that helps structure observations around an 8-dimensional development model covering relationship safety, exercise, academics, cognition, social-emotional behavior, habits, motivation, and interests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duzhilei951](https://clawhub.ai/user/duzhilei951) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parents and caregivers use this skill to turn child-development observations into structured monthly notes, quarterly assessments, trend summaries, and next-step guidance while emphasizing intrinsic motivation and relationship safety. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive child-development, school, emotional, and family-observation notes in local workspace files that may be synced or backed up. <br>
Mitigation: Use it only in trusted workspaces, review where files are stored, and avoid entering information that should not be retained or synchronized. <br>
Risk: Broad trigger phrases may cause the agent to create or update child-related records when the user intended only a casual discussion. <br>
Mitigation: Ask the agent to confirm before creating or updating records, especially when discussing sensitive observations. <br>
Risk: Growth assessments can be misleading if isolated observations or benchmark data are treated as definitive conclusions. <br>
Mitigation: Treat generated assessments as reference notes, review them before relying on them, and combine them with broader caregiver judgment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/duzhilei951/child-growth-tracker) <br>
- [External benchmark reference data](references/benchmarks.md) <br>
- [Monthly quick-note template](references/template-monthly.md) <br>
- [Quarterly assessment template](references/template-quarterly.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Analysis, Guidance] <br>
**Output Format:** [Markdown records and assessment summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local child-growth records in workspace files.] <br>

## Skill Version(s): <br>
2.1.0 (source: release evidence, manifest, and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
