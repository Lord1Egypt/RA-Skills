## Description: <br>
Real-time web search and page reading using Aliyun IQS APIs for current information, fact verification, URL content extraction, and web research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve current search results and read web pages through Alibaba Cloud IQS when a task needs recent information, source links, fact verification, or URL content extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and page URLs are sent to Alibaba Cloud IQS. <br>
Mitigation: Do not submit secrets, private documents, authenticated links, internal URLs, or regulated data unless approved. <br>
Risk: The skill requires an Alibaba Cloud IQS API key. <br>
Mitigation: Use approved credential storage and avoid exposing the API key in prompts, logs, or shared outputs. <br>
Risk: Stealth page-reading mode may have policy or site-compliance implications. <br>
Mitigation: Use stealth mode only when it is appropriate for the target site and local policy. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-iqs-search) <br>
- [Alibaba Cloud IQS Search Endpoint](https://cloud-iqs.aliyuncs.com/search/unified) <br>
- [Alibaba Cloud IQS ReadPage Endpoint](https://cloud-iqs.aliyuncs.com/readpage/scrape) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; scripts return JSON search results or JSON page content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ALIYUN_IQS_API_KEY; search queries and page URLs are sent to Alibaba Cloud IQS.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
