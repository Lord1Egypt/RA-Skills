## Description:

AI Poster Generator Skills Served By Craftsman Agent, Generate Editable AI Poster using sota Image models and design config, support various formats, ratio, design styles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate editable AI posters through the Craftsman Agent image generator, with configurable prompts, templates, asset sizes, ratios, styles, and design layers. It documents website, API, and CLI workflows for generating, editing, and exporting poster assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented CLI path runs an unpinned external npm package while an API key is present in the environment.

Mitigation: Prefer the documented curl/API workflow or use a pinned and reviewed onekey package version before exposing credentials.

Risk: Prompts and uploaded images are sent to DeepNLP/Craftsman third-party services.

Mitigation: Use only non-sensitive prompts and images unless the user has approved sending that content to the third-party service.

Risk: Broad or long-lived OneKey credentials could be exposed during CLI or API use.

Mitigation: Use narrowly scoped, short-lived keys where available and avoid storing long-lived access keys in shared shell environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-hub-admin/skills/ai-poster-generator)
- [Craftsman image generator console](https://craftsman-agent.aiagenta2z.com/app/image-generator)
- [Craftsman website](https://craftsman-agent.aiagenta2z.com)
- [DeepNLP workspace keys](https://deepnlp.org/workspace/keys)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with curl and npx commands plus JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated service outputs may include editable workspace URLs, image URLs, poster layer data, and exportable poster assets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
