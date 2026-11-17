## Description:

爱图表 AIPPT generates complete, editable PPT presentation projects from a topic, pasted content, or supported local file, with configurable page count and visual style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aitubiao](https://clawhub.ai/user/aitubiao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create editable presentation projects through Aitubiao from a topic, source text, or supported file, then view, edit, or export the result from the Aitubiao workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The saved API-key file can be abused to run commands later.

Mitigation: Review before installation and replace shell-sourced credential storage with a non-executable data format.

Risk: Secrets may be exposed if API keys are passed through command-line arguments or chat text.

Mitigation: Validate API keys strictly, avoid command-line secret passing where possible, and document key deletion and rotation steps.

Risk: The bundled CLI exposes actions beyond PPT generation.

Mitigation: Narrow the CLI surface to PPT-related actions unless chart, Sankey, and 3D API tools are intentionally supported and documented.

Risk: PPT creation and some exports can consume paid Aitubiao credits or require membership privileges.

Mitigation: Check quotas and obtain explicit user confirmation before generation or paid export actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aitubiao/skills/aitubiao-ppt)
- [Aitubiao App](https://app.aitubiao.com)
- [Aitubiao API Key Management](https://app.aitubiao.com/setting/api-keys?utm_source=skill_skill-clawhub&channel=skill-clawhub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown responses with shell command invocations and JSON API request bodies; successful runs return project links and may download PPT, PDF, PNG, JPG, or ZIP export files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to api.aitubiao.com plus Bash, curl, and jq; PPT creation is asynchronous and may consume Aitubiao AI-bei credits per page.]

## Skill Version(s):

1.2.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
