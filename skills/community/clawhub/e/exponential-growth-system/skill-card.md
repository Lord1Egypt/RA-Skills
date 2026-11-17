## Description:

A Chinese-language agent growth methodology and Node.js helper package for recording problem-solving patterns, tool decisions, evolution logs, and reusable skill creation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[126shitou](https://clawhub.ai/user/126shitou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to establish a structured self-improvement workflow for capturing errors, best practices, tool-selection decisions, and evolution notes as reusable knowledge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated growth logs and knowledge files may include task history or sensitive user context.

Mitigation: Review generated files before sharing, exporting, publishing, or connecting scheduled automation.

Risk: The package creates and appends local workspace files when its Node.js scripts are run.

Mitigation: Run the scripts in the intended workspace and inspect the created .learnings, EVOLUTION.md, and configuration files.

Risk: The instructions and generated materials are primarily Chinese-language.

Mitigation: Install and operate the skill only when the user or reviewer can understand the Chinese-language workflow and outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/126shitou/skills/exponential-growth-system)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, code]

**Output Format:** [Markdown guidance with inline shell commands and Node.js scripts that create or append local workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local knowledge files such as .learnings entries, EVOLUTION.md, and growth-config.json when its bundled scripts are run.]

## Skill Version(s):

1.0.0 (source: skill frontmatter, package.json, and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
