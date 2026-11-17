## Description:

Provides Baidu Cloud text and image moderation APIs that detect content safety issues and return detailed JSON review results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heke-uestc](https://clawhub.ai/user/heke-uestc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to submit text, image URLs, or local image files to Baidu Cloud content moderation and present the returned compliance result to users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewed content, including local image files, can be sent to Baidu Cloud.

Mitigation: Install only when this data transfer is intended, use restricted Baidu credentials, and confirm local file uploads before sending.

Risk: Token caching is weakly safeguarded.

Mitigation: Verify token-cache file permissions and rotate credentials if cached tokens may have been exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/heke-uestc/skills/baidu-content-censor)
- [Baidu Text Moderation API Endpoint](https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined)
- [Baidu Image Moderation API Endpoint](https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/v2/user_defined)

## Skill Output:

**Output Type(s):** [text, JSON, API calls, guidance]

**Output Format:** [JSON responses summarized in human-facing text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Baidu API credentials in BCE_SINAN_AK and BCE_SINAN_SK.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
