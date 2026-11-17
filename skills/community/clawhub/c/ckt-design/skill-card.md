## Description:

根据用户的海报平面设计需求，调用创客贴智能设计 API 生成设计缩略图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hitlmt](https://clawhub.ai/user/hitlmt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and design-focused agents use this skill to turn poster, invitation, daily-card, social-image, product-poster, and banner requests into a generated Chuangkit design thumbnail for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Design prompts are sent to Chuangkit's external service.

Mitigation: Do not include confidential business plans, unreleased product details, personal data, or secrets unless sharing them with that service is acceptable.

Risk: The skill opens a returned thumbnail URL in the user's default browser.

Mitigation: Review the generated response and URL before opening when operating in restricted or sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hitlmt/skills/ckt-design)
- [Chuangkit intelligent design API endpoint](https://gw.chuangkit.com/openplatform/intelligentDesign/api/generate)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and generated thumbnail URL handling guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calls Chuangkit's external service with the user's prompt, parses JSON response fields, and opens the first returned thumbnail URL in the default browser.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
