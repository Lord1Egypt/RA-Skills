## Description:

Auto Model Router automatically selects the best model for OpenClaw agents based on task complexity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmchenggh](https://clawhub.ai/user/hmchenggh)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to classify tasks, choose a configured model plan, and route work across reasoning, coding, writing, reading, formatting, image, and video/audio categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts or files may be routed to model providers that the user has not approved.

Mitigation: Review Plan A, Plan B, and any custom provider mappings before setup, and avoid sensitive inputs until the selected providers are approved.

Risk: Routing setup, reset, or reload behavior may persist or replace existing model-routing configuration.

Mitigation: Back up current OpenClaw routing configuration before setup or reset and review the saved configuration after changes.

Risk: The README install example uses an unpinned npx command.

Mitigation: Prefer a pinned or otherwise verified ClawHub installer when installing the release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hmchenggh/skills/auto-model-router-hmchenggh)
- [Project homepage](https://github.com/HMCHENGGH/auto-model-router)
- [Artifact README](artifact/README.md)
- [Task routing rules](artifact/task-rules.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes work through configured model categories and may produce downstream outputs appropriate to the selected model.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, artifact/_meta.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
