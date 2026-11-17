## Description:

Anti-Infinite-Loop Guard helps agents detect repeated actions, enforce iteration and time limits, track basic progress, and reduce resource waste from repetitive execution cycles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add a simple local guard that detects repeated actions, iteration limits, timeouts, and missing progress during agent execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation may overstate how complete or dependable the loop protection is.

Mitigation: Review and test the actual guard behavior before relying on it to stop runaway agent work.

Risk: Broad or automatic invocation could interrupt normal agent tasks that legitimately repeat actions.

Mitigation: Use clear trigger conditions and tune iteration, timeout, and repetition thresholds for the target workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kofna3369/skills/anti-infinite-loop)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands]

**Output Format:** [Markdown with Python examples and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local loop-guard guidance and Python helper usage; no external service calls are required by the provided artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
