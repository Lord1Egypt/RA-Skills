## Description:

Build, check, deploy, and verify static landing pages for ChatGPT and OpenAI ad campaigns, including country routing, consent-aware pixel events, and campaign parameter forwarding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xt-felix](https://clawhub.ai/user/xt-felix)

### License/Terms of Use:

MIT

## Use Case:

Developers and advertising teams use this skill to create and maintain static landing pages for ChatGPT and OpenAI ad campaigns, configure campaign destinations and measurement, and check or deploy the resulting pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags a possible consent bypass.

Mitigation: Review the consent flow and confirm nonessential tracking remains gated before using or publishing a page.

Risk: The security review notes public-access guidance and a preview-server weakness.

Mitigation: Inspect the relevant files and keep preview servers accessible only to trusted local users.

Risk: The scan was partial, so its findings do not cover all files or behavior.

Mitigation: Treat the security review as incomplete and manually review the skill before deployment.

## Reference(s):

- [Page configuration guide](references/page-config.md)
- [Pixel events guide](references/pixel-events.md)
- [OpenAI requirements guide](references/openai-requirements.md)
- [Privacy and consent guide](references/privacy-consent.md)
- [Platform deployment guide](references/platform-deploy.md)
- [OpenAI Ads Measurement Pixel documentation](https://developers.openai.com/ads/measurement-pixel)
- [OpenAI Ads image tag documentation](https://developers.openai.com/ads/image-tag)
- [OpenAI crawler guidance for advertisers](https://help.openai.com/en/articles/20001243-advertiser-guidance-for-allowing-openai-web-crawlers)

## Skill Output:

**Output Type(s):** [Code, Files, Configuration instructions, Shell commands, Guidance]

**Output Format:** [Static HTML, CSS, JavaScript, JSON configuration, shell commands, and verification findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces static landing-page files and deployment or verification guidance tailored to the supplied campaign details.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
