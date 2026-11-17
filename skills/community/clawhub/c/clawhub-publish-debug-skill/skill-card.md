## Description:

A minimal but concrete diagnostic skill used to verify whether ClawHub publish and install return the same SKILL.md content.

This skill is for research and development only.

## Publisher:

[miniade](https://clawhub.ai/user/miniade)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release maintainers use this skill as a controlled diagnostic fixture to manually verify that an installed SKILL.md matches the freshly published ClawHub content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake this diagnostic fixture for a production workflow.

Mitigation: Use it only to verify installed SKILL.md marker text against the published content, and do not rely on it for broader registry or install validation.

Risk: Manual marker checks can miss stale or mismatched content if the expected phrases are not reviewed exactly.

Mitigation: Compare the installed SKILL.md against the expected marker and phrases before treating the publish/install consistency check as successful.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown instructions with marker text to verify manually]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces manual verification guidance only; it does not execute commands or automate validation.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
