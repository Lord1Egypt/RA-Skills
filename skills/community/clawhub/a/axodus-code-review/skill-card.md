## Description:

Review code for correctness, security, performance, and maintainability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzfshark](https://clawhub.ai/user/mzfshark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review code or diffs before merging, investigate suspected bugs, and conduct hardening or security passes with prioritized findings and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Malformed trigger metadata may cause the skill to activate at unintended times or fail to activate for intended code-review requests.

Mitigation: Correct the trigger metadata so activation is limited to explicit code-review requests.

Risk: Review guidance can be incorrect or misleading if findings are not tied to concrete evidence.

Mitigation: Require line references, observed behavior, or reproducible scenarios, and review proposed changes before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mzfshark/skills/axodus-code-review)
- [Publisher profile](https://clawhub.ai/user/mzfshark)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review report with prioritized findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings may include severity, category, issue, impact, and recommendation fields when structured output is requested.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
