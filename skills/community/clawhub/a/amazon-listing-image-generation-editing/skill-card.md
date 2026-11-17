## Description:

This skill helps Amazon sellers plan and generate a Nano Banana Pro image stack for listings and A+ content, including main images, feature evidence, dimensions, lifestyle scenes, usage steps, and packing-list visuals while keeping claims consistent with ASIN/SKU evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and ecommerce creative teams use this skill to generate and edit listing image assets for product detail pages, A+ content, white-background main images, infographics, lifestyle images, dimension images, and packing-list visuals. Users should review generated assets against ASIN/SKU source facts and current Amazon Seller Central policy before upload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an AI Hive API key.

Mitigation: Provide the key through the documented environment variable or local config file, keep the config file private, and do not commit credentials.

Risk: Reference product images may be uploaded to AI Hive.

Mitigation: Upload only product or reference images that the user is authorized to share with AI Hive.

Risk: Generated files are downloaded from service-provided URLs to a local output directory.

Mitigation: Use a controlled output directory and review downloaded assets before reuse or publication.

Risk: Generated Amazon listing assets may contain unsupported claims or drift from ASIN/SKU facts.

Mitigation: Validate product appearance, included items, dimensions, performance claims, and marketplace policy compliance before submitting assets to Amazon.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/amazon-listing-image-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON task responses, and downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the fixed public_model_nano_banana_pro image model through AI Hive; generated image results are saved to the configured local output directory unless no-download mode is used.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
