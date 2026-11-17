## Description:

Code Sandbox guides an agent through reviewing and running untrusted AI-generated code with sandbox-style checks, resource limits, network restrictions, filesystem controls, and execution reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to assess AI-generated code, identify risky patterns, and produce sandbox execution reports before code is run in an independently enforced isolation environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill promises safe execution of untrusted code without providing an enforceable sandbox implementation.

Mitigation: Use it only with a real, independently enforced sandbox such as a fresh container or microVM with no network access, restricted mounts, low privileges, and hard resource limits.

Risk: Markdown blacklists and sample pattern checks can miss dangerous behavior and should not be treated as a security boundary.

Mitigation: Require explicit user confirmation before running untrusted code and rely on external isolation controls rather than the documented blacklist.

## Reference(s):

- [ClawHub Code Sandbox Skill Page](https://clawhub.ai/534422530/skills/code-sandbox)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with code snippets, structured pass/reject/timeout examples, configuration guidance, and safety recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include execution status, timing, memory usage, warnings, rejection reasons, matched risk patterns, and suggested fixes.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
