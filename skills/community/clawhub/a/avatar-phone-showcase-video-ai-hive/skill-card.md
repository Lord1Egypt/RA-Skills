## Description:

Turns avatar phone showcase requests into a Chinese production workflow with briefs, scripts, prompts, AI-HIVE commands, task records, and video readability checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing teams, creators, and developers use this skill to plan and execute avatar-led phone screen showcase videos for app, ecommerce, education, and internet-product promotion using authorized references and real interface screenshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags API key handling and network media transfers with weak destination controls.

Mitigation: Install only if the publisher and AI-HIVE workflow are trusted, use a limited API key, and monitor ~/.ai-hive/config.json because it controls authenticated request destinations.

Risk: Custom base URLs can redirect authenticated requests or uploaded media to unintended endpoints.

Mitigation: Avoid custom base URLs unless the endpoint is controlled and reviewed.

Risk: Generated commands may run paid AI-HIVE operations or upload private media.

Mitigation: Review every generated command before execution, confirm final parameters and routing before paid generation, and upload only media the user is allowed to share.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/avatar-phone-showcase-video-ai-hive)
- [AI-HIVE Chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE OpenAPI Endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown with inline shell commands, JSON task records, generated blueprint files, and local media file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-HIVE task IDs, pricing snapshots, model routing choices, status results, and downloaded media locations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
