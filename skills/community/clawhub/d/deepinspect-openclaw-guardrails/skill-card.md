## Description:

Provides deterministic preflight risk classification for command-like actions, returning allow, require approval, or block decisions with detailed reason codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parmindersk](https://clawhub.ai/user/parmindersk)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to evaluate command-like actions before execution and decide whether they should be allowed, require approval, or be blocked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found that staged remote-code execution patterns may be incorrectly allowed despite the skill presenting itself as a preflight decision tool.

Mitigation: Review the default policy, shell parsing behavior, and staged download-to-execution detection before using this skill as an enforcement gate.

Risk: A command-risk classifier can produce incomplete or misleading decisions when policy coverage is too narrow.

Mitigation: Treat decisions as review support, tune policy.baseline.json for the deployment environment, and keep human approval for high-risk actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/parmindersk/skills/deepinspect-openclaw-guardrails)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON decisions with reason codes, plus concise Markdown guidance and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Decision values are allow, require_approval, or block.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
