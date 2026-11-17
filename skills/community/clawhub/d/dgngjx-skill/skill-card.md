## Description:

A Chinese-language toolbox that helps agents with calculations, text and file processing, media, system utilities, and meeting notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fyniujin](https://clawhub.ai/user/fyniujin)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers can ask an agent to calculate values, transform text or media, inspect system health, and work with local files through a modular utility toolbox.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File and system operations may read, alter, or overwrite user-selected data.

Mitigation: Review requested operations and file paths before execution; back up important files before bulk changes.

Risk: Online or API features may send sensitive content to third-party services.

Mitigation: Avoid online or API modes for confidential audio, internal URLs, secrets, and sensitive documents.

Risk: Automatic local history can retain summaries of user inputs and outputs.

Mitigation: Disable or regularly clear history stored under ~/.workbuddy/dgngjx_history.json.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/fyniujin/skills/dgngjx-skill)
- [Data calculation module](references/modules/calc.md)
- [System tools and local history module](references/modules/sys.md)
- [AI meeting notes module](references/modules/ai.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files]

**Output Format:** [Task-dependent text, Markdown, CLI output or JSON, and processed files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some features use optional packages or online services; local history may retain input and output summaries.]

## Skill Version(s):

4.1.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
