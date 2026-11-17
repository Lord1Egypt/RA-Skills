## Description:

Security audit and validation tools for the Agent Skills ecosystem that scan skill packages for common vulnerabilities like credential leaks, unauthorized file access, and Git history secrets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rongself](https://clawhub.ai/user/rongself)

### License/Terms of Use:

MIT

## Use Case:

Developers and skill maintainers use this skill to run a lightweight local audit of Agent Skills packages before installation or release. It helps identify common security hygiene issues and validation concerns that should be reviewed before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A clean audit result may be mistaken for proof that a skill is safe.

Mitigation: Treat findings as lightweight heuristic guidance and use a maintained secret scanner plus code review for security decisions.

Risk: Running the audit against broad or unintended directories can produce noisy results or inspect files outside the intended skill package.

Mitigation: Run the tool only on the specific skill directory you intend to inspect.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rongself/skills/agent-skills-tools)
- [ClawHub publisher profile](https://clawhub.ai/user/rongself)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style text with inline shell commands and audit findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are heuristic local audit findings and recommendations, not a complete security certification.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
