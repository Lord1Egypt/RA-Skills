## Description:

面向解说/讲解场景的 Sparki skill 变体，沿用最新版官方 Sparki 安装、API key、上传和命令说明，同时保留 commentary 场景定位。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fischerlam](https://clawhub.ai/user/fischerlam)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to guide Sparki video editing for commentary, explainer, reaction, and narration-heavy videos. Agents can use it to configure upload, prompt-driven editing, and result retrieval workflows for local video files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected videos and prompts may be uploaded to Sparki for remote processing.

Mitigation: Install and use the skill only when that upload behavior is acceptable for the content being processed.

Risk: Credential handling may store API keys on disk under ~/.openclaw/config.

Mitigation: Prefer SPARKI_API_KEY for credentials and protect the local configuration directory.

Risk: A custom --base-url can send requests to an unexpected endpoint.

Mitigation: Use --base-url only with endpoints the user fully trusts.

Risk: Remote workflow output may be selected when local video tools would be more appropriate.

Mitigation: Review generated outputs and task fit before relying on the remote workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fischerlam/skills/ai-commentary-zh)
- [Sparki homepage](https://sparki.io)
- [Sparki Telegram upload](https://t.me/Sparki_AI_bot/upload)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown with inline shell commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Sparki task IDs, status JSON, download URLs, and local output paths for edited videos.]

## Skill Version(s):

1.0.12 (source: SKILL.md frontmatter, _meta.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
