## Description:

C++ Code Review Master helps developers review C and C++ changes by combining C++-specific checks, static prechecks, multi-reviewer analysis, scoring, and optional user-approved fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigmasteryy](https://clawhub.ai/user/bigmasteryy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review C and C++ files, diffs, pull requests, or full projects for memory safety, undefined behavior, security, performance, maintainability, and Modern C++ practice. It produces prioritized findings, scores, and optional user-approved fix guidance before code is merged.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read repository code and use configured AI providers during review.

Mitigation: Use local analysis mode or approved AI provider settings for sensitive repositories, and confirm provider configuration before running deep review.

Risk: Optional repair behavior can modify files when fixes are requested.

Mitigation: Keep repair user-gated, review generated diffs, and run the project's tests before merging changes.

Risk: The workflow depends on related review and repair skills for deeper analysis and fixing.

Mitigation: Review dependent skills, especially code-review-fix, before enabling repair or auto-fix behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bigmasteryy/skills/cpp-code-review-master)
- [README](artifact/README.md)
- [C++ Code Review Workflow](artifact/references/workflow.md)
- [C++ Review Checklist](artifact/references/cpp-checklist.md)
- [Severity Definitions](artifact/references/severity.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown review reports with severity tables, scoring, prioritized findings, shell command examples, and optional code fix guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read repository code and may propose or perform file changes only when repair behavior is explicitly requested by the user.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
