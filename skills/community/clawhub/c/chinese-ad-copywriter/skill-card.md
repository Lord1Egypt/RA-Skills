## Description:

Chinese ad copywriter with API-powered compliance checking for generating platform-specific Chinese marketing copy and checking ad text for banned words and advertising-law risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lm203688](https://clawhub.ai/user/lm203688)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing writers, ecommerce operators, and developers use this skill to draft Chinese advertising copy for platforms such as Xiaohongshu, Douyin, WeChat, Baidu, Taobao, and JD, then review the copy for banned terms and safer replacements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ad text, titles, keywords, and platform choices may be sent to an external Tencent Cloud API.

Mitigation: Avoid confidential or client-sensitive material unless the endpoint and data-handling expectations have been reviewed.

Risk: The bundled scripts build request payloads from command-line input.

Mitigation: Review and improve JSON and URL encoding before relying on the scripts in production workflows.

Risk: Generated marketing guidance and compliance scores may not fully reflect current advertising-law obligations.

Mitigation: Have qualified reviewers check final copy, especially for medical, health, education, finance, and other regulated categories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lm203688/skills/chinese-ad-copywriter)
- [Compliance API endpoint](https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text with Chinese copy variants, compliance findings, replacement suggestions, scores, and optional bash command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform-specific templates, risk labels, and compliance scores.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
