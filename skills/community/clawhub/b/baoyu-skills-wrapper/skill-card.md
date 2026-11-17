## Description:

Baoyu Skills Wrapper provides a wrapper for Baoyu's shared productivity skill set, including content generation, AI backend, and daily utility tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongjie-oss](https://clawhub.ai/user/dongjie-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to discover and run Baoyu's content creation, AI generation, social publishing, translation, transcript, and Markdown utility workflows from an agent environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper directs users to run separate Baoyu skill code that is not bundled for review in this artifact.

Mitigation: Review the exact external code or revision before running it, and install only when the source is trusted.

Risk: Some workflows can use API keys, browser sessions, or live social publishing accounts.

Mitigation: Use restricted API keys and dedicated social accounts, protect ~/.baoyu-skills/.env with owner-only permissions, and manually confirm posting or account-modifying actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dongjie-oss/skills/baoyu-skills-wrapper)
- [Original baoyu-skills repository](https://github.com/JimLiu/baoyu-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide use of external Baoyu skill code, browser sessions, API keys, and social publishing accounts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
