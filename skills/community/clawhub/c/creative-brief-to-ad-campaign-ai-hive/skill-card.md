## Description:

Transforms a creative brief for ecommerce or campaign marketing into a reviewable campaign plan, runnable AI-HIVE image and video generation commands, content assets, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Brand marketers, advertising agencies, creative directors, and ecommerce campaign teams use this skill to turn a Creative Brief into campaign strategy, channel plans, scripts, image and video tasks, AI-HIVE generation commands, and review criteria before any billable generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper scripts handle AI-HIVE API credentials and can store an API key in a local configuration file.

Mitigation: Use environment variables or a locked-down local config, never commit real keys, rotate keys if exposed, and prefer a separate test key for non-production runs.

Risk: Generation and download helpers depend on a remote API endpoint and local output paths.

Mitigation: Use the default HTTPS AI-HIVE base URL unless intentionally testing, choose a contained output directory, and review downloaded files and overwrite behavior.

Risk: Image or video generation requests may be billable and can trigger large downloads.

Mitigation: Review prompts, model parameters, routing mode, and pricing snapshot before submission; start with a small sample before batch generation.

Risk: Marketing outputs can overstate product claims, imply unauthorized endorsements, or reuse protected references too closely.

Mitigation: Require factual support, confirm rights for reference assets, label uncertain claims for review, and rewrite creative structure instead of copying protected expression.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/wubin1836/skills/creative-brief-to-ad-campaign-ai-hive)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON artifacts and command-line snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local JSON plans and edited media files; authenticated AI-HIVE calls can submit billable image or video generation jobs and download resulting assets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
