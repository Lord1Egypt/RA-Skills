## Description:

Create and edit Amazon catalog images, PDP galleries, A+ Content modules, Brand Store heroes, variant sets and advertising creative bases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and ecommerce teams use this skill to generate and edit listing, PDP gallery, A+ Content, Brand Store, localization, and advertising image bases from approved product and brand source assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores an AI Hive API key in a local configuration file.

Mitigation: Use a dedicated key with limited exposure, protect ~/.ai-hive/config.json, and remove or rotate the key when the skill is no longer needed.

Risk: A custom API endpoint can receive the configured API key with requests.

Mitigation: Use the default AI Hive endpoint unless the custom endpoint is fully trusted.

Risk: Reference images and generated outputs pass through AI Hive during generation and retrieval.

Mitigation: Avoid submitting product assets, brand marks, or commercial materials unless the user has appropriate rights and accepts the service handling those files.

Risk: Generated ecommerce images can accidentally include unsupported claims, ratings, badges, prices, certifications, or competitor references.

Mitigation: Review generated assets against the seller source sheet, approved claims, rights, and current marketplace requirements before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/amazon-ecommerce-image-generation-editing)
- [ClawHub publisher profile](https://clawhub.ai/user/wubin1836)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key portal](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, image files]

**Output Format:** [Markdown guidance with bash commands; generated image files are downloaded by the bundled script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses reference images, batch generation, routing options, an output directory, and submit-only mode.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
