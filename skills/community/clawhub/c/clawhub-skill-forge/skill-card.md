## Description:

Create ClawhHub-ready OpenClaw skills with correct structure, scanner criteria, security rules and a publish checklist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seph1709](https://clawhub.ai/user/seph1709)

### License/Terms of Use:


## Use Case:

Developers and skill authors use this skill to scaffold ClawHub-ready OpenClaw skills and check that generated skill files address registry structure, scanner, security and publishing requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The publishing guidance contains a hardcoded third-party GitHub and ClawHub namespace.

Mitigation: Before running any post-publish repository command, replace the owner, repository, homepage URL and exact changes with values the user has confirmed.

Risk: The skill generates new skill files whose instructions could introduce incorrect or misleading guidance.

Mitigation: Review generated SKILL.md and _meta.json files and run the relevant ClawHub scan before publishing or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seph1709/skills/clawhub-skill-forge)
- [Publisher profile](https://clawhub.ai/user/seph1709)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown skill instructions with file templates, JSON configuration examples and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces SKILL.md and _meta.json guidance for agent-authored OpenClaw skills.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
