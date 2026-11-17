## Description:

AI虚拟网红孵化器｜AI-HIVE helps brands, MCNs, virtual IP studios, and content entrepreneurs turn virtual influencer ideas into character positioning, character bibles, visual anchors, content matrices, image and video tasks, and consistency checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, brands, MCNs, and virtual IP teams use this skill to design Chinese-language virtual influencer workflows and produce reviewable plans, scripts, prompts, runnable AI-HIVE commands, generated media task records, and delivery checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AI-HIVE API keys locally.

Mitigation: Use a dedicated low-privilege API key, keep it in an environment variable or protected local config, and avoid sharing logs or screenshots that might expose credentials.

Risk: Selected images, video, audio, or brand assets may be uploaded to third-party services.

Mitigation: Use only authorized media and avoid sensitive customer, likeness, proprietary, or regulated content unless the upload and downstream use are approved.

Risk: Image and video generation can incur charges.

Mitigation: Confirm prompts, model, routing mode, pricing snapshot, and batch size before submission; start with small samples before batch generation.

Risk: Custom base URLs or untrusted execution environments can change where credentials and media are sent.

Mitigation: Use the default AI-HIVE endpoint unless a trusted operator has reviewed the alternate endpoint and runtime environment.

Risk: Virtual influencer outputs can create likeness, copyright, endorsement, product-claim, or platform-disclosure issues.

Mitigation: Confirm rights and platform rules, disclose AI or commercial identity where required, and mark unverifiable product or market claims for human review.

## Reference(s):

- [AI-HIVE chat entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE OpenAPI endpoint](https://ai-hive.iclip.cn/api)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-virtual-influencer-incubator-ai-hive)
- [Publisher profile](https://clawhub.ai/user/wubin1836)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and optional JSON files, task records, downloaded media paths, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call AI-HIVE APIs for model lookup, media upload, image/video generation, asynchronous task polling, and result downloads when the user provides a valid API key and confirms potentially billable work.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
