## Description:

Automates personal diary drafting from configured SOUL, MEMORY, daily memory, recent diary, and optional news-summary sources, then exports the entry as a 1080px-wide image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1204tmax](https://clawhub.ai/user/1204tmax)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to generate daily, catch-up, or style-continuation diary entries and shareable diary images from their configured personal memory sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read broad private memory, SOUL, recent diary, and optional news-summary files while drafting a diary entry.

Mitigation: Review and customize config.yaml before first use, and ask the agent to show the exact files it will read for each run.

Risk: Generated diary Markdown and image files may contain private or sensitive personal content.

Mitigation: Review the generated Markdown and image before sharing or archiving them outside the private workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1204tmax/skills/auto-diary)
- [Publisher profile](https://clawhub.ai/user/1204tmax)
- [README](artifact/README.md)
- [Initialization workflow](artifact/INIT.md)
- [Configuration template](artifact/config.template.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, files, configuration, guidance]

**Output Format:** [Markdown diary text, PNG image file, and concise path/status details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image output is specified as 1080px wide with height adapting to content.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
