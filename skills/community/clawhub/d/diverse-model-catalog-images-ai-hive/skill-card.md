## Description:

Helps ecommerce and marketing teams create production briefs, prompts, reference-image strategies, batch variants, and AI-HIVE generation commands for diverse fashion model catalog images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External brand, ecommerce, and marketing users use this Chinese-language skill to plan model catalog image sets for the same garment across different skin tones, body types, ages, scenarios, and platform formats. It can also provide executable AI-HIVE commands after human review of inputs, routing, and potential cost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom AI-HIVE API host can receive the user's AI-HIVE API key.

Mitigation: Use only the default AI-HIVE endpoint unless the custom endpoint is fully trusted, and use a limited or disposable API key where possible.

Risk: Image generation, media upload, and batch jobs may spend credits or expose private commercial media.

Mitigation: Confirm final parameters, route, batch size, pricing snapshot, input-media authorization, and expected cost before submitting generation tasks.

Risk: Generated model imagery can misrepresent products, body appearance, endorsement, or platform compliance if facts and disclosures are not checked.

Mitigation: Require human review for product accuracy, authorization, synthetic-person disclosure, prohibited claims, and platform-specific rules before publication.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wubin1836/skills/diverse-model-catalog-images-ai-hive)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash command examples and optional JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local blueprint JSON files and download generated media after explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
