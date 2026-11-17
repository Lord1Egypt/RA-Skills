## Description:

Cloud workflow cache for OpenClaw. Reduces token usage by reusing verified automation patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ainclaw](https://clawhub.ai/user/ainclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to query and replay cached browser automation workflows, reducing repeated exploration for common tasks. It can also compile successful session traces into reusable workflows for later matching.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends automation intents, URLs, DOM skeleton hashes, node/session identifiers, and compiled workflow patterns to a cloud service.

Mitigation: Use only with a trusted endpoint, restrict use on sensitive sites, and disable the skill where workflow data should not leave the local environment.

Risk: The skill can execute cloud-returned workflows with browser and session access.

Mitigation: Review before installation, pin the installed version, and monitor workflow execution on accounts or sites where unintended browser actions could cause harm.

Risk: Successful sessions may be automatically contributed to the cloud service.

Mitigation: Set auto_contribute to false unless sharing successful workflow patterns is explicitly acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ainclaw/skills/aintoken)
- [Publisher profile](https://clawhub.ai/user/ainclaw)
- [Artifact README](artifact/README.md)
- [Skill manifest](artifact/skill.json)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown and runtime OpenClaw hook responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute or contribute cached Lobster workflows through configured OpenClaw hooks.]

## Skill Version(s):

1.0.4 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
