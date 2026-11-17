## Description:

FB Ads Copywriter Pro helps agents draft marketing prompt templates for ads, social posts, email campaigns, product descriptions, landing pages, blogs, and video scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chungvic](https://clawhub.ai/user/chungvic)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, operators, and developers use this skill to prepare structured copywriting prompts and draft payloads for campaigns across Facebook, Google Ads, XiaoHongShu, email, ecommerce, landing pages, blogs, and video scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes an OpenAI-compatible dependency although the current script behaves as a prompt/template generator.

Mitigation: Install dependencies in an isolated environment and pin or remove the OpenAI dependency until live API generation is intentionally enabled.

Risk: Future API integration could expose confidential marketing inputs if privacy behavior is not documented.

Mitigation: Avoid submitting confidential campaign material unless the deployed integration has clear data handling and privacy controls.

Risk: Generated advertising prompts or draft copy may produce unsupported marketing claims.

Mitigation: Review generated copy for factual accuracy, regulatory compliance, and brand policy before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chungvic/skills/fb-ads-copywriter-pro-vic)
- [Publisher profile](https://clawhub.ai/user/chungvic)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON or plain text prompt templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return multiple variations; current behavior emits ready-for-API prompt payloads rather than live model-generated copy.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
