## Description:

Generates concise English or Chinese AI and technology briefing text and saved Markdown files, with demo-style story content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[greatworks](https://clawhub.ai/user/greatworks)

### License/Terms of Use:

MIT-0

## Use Case:

Readers, teams, and community managers use this skill to create quick AI and technology update briefings in English or Chinese and save or share the result as Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package needs review before installation in shared or sensitive workspaces.

Mitigation: Review the artifact contents and security notes before deployment, especially in workspaces with sensitive files.

Risk: Generated briefings may be demo-style content and may include an embedded donation footer.

Mitigation: Confirm the output meets the intended use case and remove or modify the donation/footer text before organizational use.

Risk: The fetch command may read unexpected Markdown files if given untrusted date values.

Mitigation: Use trusted date values only until date validation and path containment are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/greatworks/skills/ai-tech-intelligence-briefing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown briefing text and local .md files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports English or Chinese output, configurable region, configurable story count, and a local briefing output directory.]

## Skill Version(s):

1.1.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
