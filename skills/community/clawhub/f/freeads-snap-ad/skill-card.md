## Description:

FreeAds 随手拍广告 helps agents turn product photos into 8-second advertising videos with product recognition, storyboard and slogan planning, audio guidance, and an Atlas Cloud video URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lipeng0820](https://clawhub.ai/user/lipeng0820)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketers use this skill to generate short product-ad video workflows and final video URLs from product photos. The skill guides product recognition, scene design, storyboard creation, slogan generation, prompt review, and video generation through Atlas Cloud.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API-key setup script can modify shell startup files.

Mitigation: Avoid running scripts/setup-api-key.sh as-is; configure ATLASCLOUD_API_KEY manually for the current session or through a trusted secret manager.

Risk: Product images, logos, unreleased marketing assets, and prompts may be sent to Atlas Cloud and model providers.

Mitigation: Use only assets approved for those providers and avoid submitting confidential or unreleased material unless that data sharing is acceptable.

Risk: Setup guidance includes a referral promotion.

Mitigation: Review external service links and commercial terms before installing or funding provider accounts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lipeng0820/skills/freeads-snap-ad)
- [Atlas Cloud API Reference](references/atlas-cloud-api.md)
- [Brand Protection Guide](references/brand-protection-guide.md)
- [Ad Copy Templates and Examples](examples/ad-copy-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown report with JSON blocks, English generation prompts, shell snippets, and a final video URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ATLASCLOUD_API_KEY; may send product images and prompts to Atlas Cloud and model providers; server metadata estimates $0.80-1.60 per video.]

## Skill Version(s):

3.7.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
