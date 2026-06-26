## Description: <br>
Use when managing Alibaba Cloud ApsaraVideo VOD resources and media workflows via OpenAPI/SDK, including upload and media asset operations, transcoding templates, playback authorization, AI processing jobs, and VOD troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud media operators use this skill to manage Alibaba Cloud ApsaraVideo VOD assets and workflows through OpenAPI or SDK calls. It supports upload, playback authorization, media management, transcoding, AI jobs, API discovery, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward deleting media, changing production VOD configuration, or starting billable processing jobs. <br>
Mitigation: Use read-only or tightly scoped credentials by default, prefer short-lived STS credentials, and require explicit confirmation of exact VideoIds, account, region, and environment before delete, update, callback, template, or billable processing actions. <br>
Risk: Incorrect region, media IDs, template IDs, or request parameters could affect the wrong Alibaba Cloud VOD resources. <br>
Mitigation: Run metadata discovery and read-only Describe/List validation first, then save request payloads and responses under output/aliyun-vod-manage/ for review. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cinience/aliyun-vod-manage) <br>
- [OpenAPI product page for VOD](https://api.aliyun.com/product/vod) <br>
- [ApsaraVideo VOD API metadata](https://api.aliyun.com/meta/v1/products/vod/versions/2017-03-21/api-docs.json) <br>
- [ApsaraVideo VOD product documentation](https://www.alibabacloud.com/help/en/vod) <br>
- [Source list](references/sources.md) <br>
- [VOD task templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, API names, request templates, and generated evidence files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated API inventories, request payloads, responses, and evidence are directed to output/aliyun-vod-manage/.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
