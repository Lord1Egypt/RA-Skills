## Description:

AI 蛋糕烘焙培训老师 helps users create cake recipes, learn cake categories and steps, diagnose baking failures, substitute ingredients, improve decoration techniques, choose equipment, plan bakery operations, and generate interactive HTML teaching reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External learners, baking instructors, and bakery operators use this skill for Chinese-language cake recipes, step-by-step baking instruction, failure diagnosis, ingredient substitution, decoration guidance, equipment selection, and shop-opening checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The report generator can write to arbitrary output paths.

Mitigation: Write reports only to a controlled safe directory and do not run the script with elevated privileges.

Risk: Generated HTML may embed report content without escaping, which can create active browser content if untrusted text is included.

Mitigation: Use trusted report inputs, avoid untrusted text in report fields, and treat generated HTML as active content until escaping is added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/cake-teacher)
- [Publisher profile](https://clawhub.ai/user/bettermen)
- [Homepage from ClawHub metadata](https://github.com/bettermen/cake-teacher)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands and generated HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate interactive HTML teaching reports through the bundled report generator.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
