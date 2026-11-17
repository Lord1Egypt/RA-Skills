## Description:

ClawVision turns an OpenClaw chat session into a local visual summary with HTML, PNG, Markdown, and PowerPoint exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[monaxamo](https://clawhub.ai/user/monaxamo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use ClawVision to create exportable visual summaries of explicitly selected chat sessions for review, sharing, or presentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exported summaries can contain the contents of the selected chat session, including any secrets or private identifiers present in that session.

Mitigation: Confirm the selected session is safe to export before running the skill, and review generated files before sharing them.

Risk: The skill writes persistent HTML, PNG, Markdown, and PowerPoint files to local disk.

Mitigation: Choose an output location you control and handle generated files as copies of the original conversation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/monaxamo/skills/clawvision-publish)
- [Project homepage](https://github.com/monaxamo/clawvision)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, Files]

**Output Format:** [Markdown guidance plus generated HTML, PNG, Markdown, and PowerPoint files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated exports are written to a user-controlled local output directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata reports 1.0.13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
