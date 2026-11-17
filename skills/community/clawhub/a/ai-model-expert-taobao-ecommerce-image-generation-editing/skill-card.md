## Description:

Helps e-commerce teams generate and edit Taobao product images through AI-HIVE, with optional reference images, task submission, progress polling, and result downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce operators, brand teams, product photography teams, livestream commerce teams, and developers use this skill to create product main images, detail-page visuals, ad creatives, posters, retouching, background replacement, and reference-guided image outputs through AI-HIVE.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send an AI-HIVE API key to a configurable API endpoint.

Mitigation: Use the default AI-HIVE endpoint or another trusted endpoint only, and do not set --base-url or AI_HIVE_BASE_URL to an untrusted host.

Risk: Reference-image uploads and generation jobs may transfer product images to AI-HIVE and consume account quota.

Mitigation: Review file uploads, batch size, routing mode, and task requests before execution, especially for proprietary product images or high-cost runs.

Risk: Local API key storage can expose credentials if the configuration file is mishandled.

Mitigation: Store real API keys only in local environment variables or the local AI-HIVE config file, keep file permissions restricted, and avoid placing keys in skills, screenshots, chats, or public repositories.

## Reference(s):

- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-taobao-ecommerce-image-generation-editing)
- [ClawHub publisher profile](https://clawhub.ai/user/wubin1836)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and downloaded image files from AI-HIVE tasks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit paid networked AI-HIVE generation jobs, save task IDs, poll task status, upload reference media, and download generated images to a local output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
