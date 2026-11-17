## Description:

AI大模型专家｜电商主图 helps e-commerce teams create main product images through AI-HIVE from prompts and optional reference images, with task submission, polling, and result downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce operators, product photographers, brand teams, and live-commerce teams use this skill to produce product main images, detail-page visuals, ad creatives, posters, retouching, background replacement, and consistent-character marketing imagery through AI-HIVE.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can use stored AI-HIVE API keys.

Mitigation: Keep the API key private, avoid committing configuration files, and use a dedicated key that can be rotated or revoked.

Risk: Prompts and selected media may be uploaded to AI-HIVE.

Mitigation: Use the skill only when AI-HIVE is an intended processor and confirm rights to any referenced product, brand, or media assets.

Risk: Custom base URLs can redirect requests to an endpoint other than the default AI-HIVE service.

Mitigation: Avoid custom base URLs unless the endpoint is fully trusted and controlled by the deployer.

Risk: Downloaded generation results should not be treated as inherently trusted files.

Mitigation: Use a dedicated output directory and review or scan downloaded files before publishing or moving them into production workflows.

Risk: The agent integration allows broad implicit invocation.

Mitigation: Disable or constrain implicit invocation where possible so media upload and paid generation only occur after user intent is clear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-ecommerce-main-image)
- [AI-HIVE entry point](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with bash commands, JSON task responses, and downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated image results are downloaded to a local output directory when AI-HIVE tasks succeed; --no-download returns task JSON for later polling.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
