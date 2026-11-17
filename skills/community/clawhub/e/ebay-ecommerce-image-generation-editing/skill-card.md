## Description:

Create and edit eBay listing images for new, used, refurbished, parts and collectible items, including condition disclosure, defects, identifiers, included accessories and scale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and listing operators use this skill to create and edit eBay product images that keep the exact sale item inspectable, including condition, defects, identifiers, included accessories and scale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API key misuse or exposure.

Mitigation: Use a dedicated AI Hive API key and store it only through the supported configuration path or environment variable.

Risk: Private or unrelated files may be uploaded when used as reference media.

Mitigation: Upload only seller-approved listing photos needed for the task and avoid private or unrelated files.

Risk: Generated images may misrepresent item condition or included accessories.

Mitigation: Review every output against the source photos and listing record; keep defects, wear, missing parts and accessory counts visible.

Risk: Generated files are saved locally after task completion.

Mitigation: Use a controlled output directory and review downloaded files before listing publication.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/wubin1836/skills/ebay-ecommerce-image-generation-editing)
- [AI Hive API base URL](https://ai-hive.iclip.cn/api)
- [AI Hive API access page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and generated image files from AI Hive tasks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload seller-selected reference media to AI Hive and save generated files to a local output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
