## Description: <br>
Performs web searches with Alibaba Cloud Unified Search API and returns relevant results with snippets, relevance scores, and metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neotize](https://clawhub.ai/user/neotize) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search the web through an Aliyun account, especially for Chinese-language content or searches that need time-range or category filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Alibaba Cloud through the user's Aliyun account. <br>
Mitigation: Use a scoped, revocable API key and unset ALIYUN_IQS_API_KEY when agents should not use this provider. <br>
Risk: Agents may expose or overuse the configured Aliyun API key if it is left broadly available in the environment. <br>
Mitigation: Provide the key only to trusted agent sessions and rotate it if exposure is suspected. <br>
Risk: Search results can be incomplete, stale, or affected by restrictive category filters. <br>
Mitigation: Review important results before relying on them and avoid category filters for general searches unless they are needed. <br>


## Reference(s): <br>
- [Alibaba Cloud Unified Search API Documentation](https://help.aliyun.com/zh/document_detail/2883041.html?spm=a2c4g.11186623.help-menu-2837261.d_4_0_2_3_0.153cda16tmvRJQ) <br>
- [Alibaba Cloud API Key Credential Documentation](https://help.aliyun.com/zh/document_detail/2872258.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/neotize/aliyun-unified-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown-formatted search result list or raw JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ALIYUN_IQS_API_KEY; supports time-range and category filters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
