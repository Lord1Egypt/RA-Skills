## Description:

Helps agents remove unwanted text or watermarks from selected images, remove hardcoded subtitles or watermarks from videos, and resolve supported video share links through the 550W service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshinehu](https://clawhub.ai/user/sunshinehu)

### License/Terms of Use:

MIT

## Use Case:

People and agents working with media they own or are authorized to edit can request image cleanup, video subtitle or watermark removal, and supported share-link resolution through 550W.

### Deployment Geography for Use:

China (domestic service release)

## Known Risks and Mitigations:

Risk: Selected media, share links, and account requests are sent to the 550W service.

Mitigation: Use only media you own or are authorized to edit; confirm the selected material and transfer before processing.

Risk: API keys can be stored locally as plaintext JSON with restricted file permissions.

Mitigation: Prefer OAuth or securely managed environment credentials; explicitly approve any local credential storage.

Risk: Repeated processing submissions can consume credits, and task deletion does not refund credits.

Mitigation: Confirm charges and each deletion; check existing tasks after timeouts before submitting again.

## Reference(s):

- [550W skill release](https://clawhub.ai/sunshinehu/skills/550w-ai-media-cn)
- [OAuth access guide](references/oauth-access.md)
- [API key access guide](references/openapi-access.md)
- [Open API contract](references/api-contract.md)
- [550W OAuth authorization](https://qzm.550wai.cn/mcp-connect/)
- [550W API key management](https://qzm.550wai.cn/api-keys)

## Skill Output:

**Output Type(s):** [Guidance, Text, Configuration instructions]

**Output Format:** [Markdown with task status and result links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a processed-media link or task ID; media processing occurs through the 550W service.]

## Skill Version(s):

3.1.4 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
