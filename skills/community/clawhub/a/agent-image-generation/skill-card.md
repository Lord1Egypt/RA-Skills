## Description:

Guides autonomous agents to generate AI images through a hosted workflow with named models, per-image cost limits, and durable media links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielgwilson](https://clawhub.ai/user/danielgwilson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to generate AI images from agent workflows, set per-image spending limits, and keep resulting media available for later retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic feedback may include private prompts, URLs, credentials, or other tools' results.

Mitigation: Keep feedback optional and review and redact its contents before submission.

Risk: CLI or skill updates and global installation can affect behavior or the environment where the skill runs.

Mitigation: Review and pin CLI and skill versions, and approve global installation deliberately.

Risk: Image generation can use paid credits after preview credits run out.

Mitigation: Retain spending limits and run generation commands only when media spend is allowed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/danielgwilson/skills/agent-image-generation)
- [Luxin skill guide](https://luxin.sh/skill.md)
- [Luxin full guidance](https://luxin.sh/skill-core.md)
- [Luxin LLM contract](https://luxin.sh/llms.txt)
- [Luxin CLI documentation](https://luxin.sh/cli.md)
- [Luxin hosted API](https://api.luxin.sh)

## Skill Output:

**Output Type(s):** [Images, Shell commands, Guidance, API Calls]

**Output Format:** [Markdown guidance and shell commands; generated images are available as hosted media links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media can be retained for later retrieval; per-image spending limits can be specified.]

## Skill Version(s):

1.0.0 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
