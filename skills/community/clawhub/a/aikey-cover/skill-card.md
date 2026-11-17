## Description:

Creates video cover images from supplied person and background images, with layouts tailored to each target platform's aspect ratio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamzifei](https://clawhub.ai/user/iamzifei)

### License/Terms of Use:

MIT-0

## Use Case:

Creators use this skill to make and organize video cover image sets from supplied person and background images, with layouts for the requested platform ratios and optional language variants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured hosted image provider may receive the original person and background photos.

Mitigation: Use an image provider you trust with the supplied photos.

Risk: Prompts and design feedback may be saved, and related configuration, family rules, or skills are outside this package's inspection.

Mitigation: Review the separately supplied configuration, family rules, and related skills before use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/iamzifei/skills/aikey-cover)
- [Platform dimensions reference](artifact/references/平台尺寸表.md)
- [Cover design rules](artifact/references/规则卡.md)

## Skill Output:

**Output Type(s):** [Images, Markdown]

**Output Format:** [Cover image files and a Markdown production note]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One image per requested language and aspect ratio; layouts are adjusted per ratio, pixel dimensions are checked, and files are organized by date.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
