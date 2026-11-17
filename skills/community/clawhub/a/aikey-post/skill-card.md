## Description:

Turns validated content or fragments into a WeChat Official Account short post with a title of up to 20 Chinese characters, a body of up to 1,000 Chinese characters, and one banner image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamzifei](https://clawhub.ai/user/iamzifei)

### License/Terms of Use:

MIT-0

## Use Case:

External, independent knowledge creators use the skill to turn a validated post, topic, or fragment into a concise WeChat Official Account draft and banner concept that follows the documented platform constraints.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Banner concepts may be sent to the configured image provider, which could expose confidential material.

Mitigation: Confirm the image provider before use and keep confidential details out of prompts unless that provider is approved for them.

Risk: The workflow saves drafts and preference notes and updates topic-tracking files.

Mitigation: Review the configured vault locations and saved content, and avoid storing sensitive material there.

Risk: Copying the draft replaces the current clipboard contents.

Mitigation: Check the draft before copying and preserve any clipboard content that must be kept.

## Reference(s):

- [AI KEY README — rename and upgrade notes](https://github.com/iamzifei/aikey#老用户升级zmm-已改名为-ai-key)

## Skill Output:

**Output Type(s):** [Text, Markdown, Image prompts, Guidance]

**Output Format:** [Chinese WeChat short-post draft with title, body, and an English banner prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Title up to 20 Chinese characters; body up to 1,000 Chinese characters; one banner concept.]

## Skill Version(s):

0.1.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
