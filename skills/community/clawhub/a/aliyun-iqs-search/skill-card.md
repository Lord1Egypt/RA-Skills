## Description: <br>
Uses Aliyun Intelligent Query Service (IQS) UnifiedSearch API to perform web searches and return structured ranked results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lilisidu1210-ui](https://clawhub.ai/user/lilisidu1210-ui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Aliyun IQS web searches from Node.js and receive ranked JSON web results for current information lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are transmitted to Alibaba Cloud IQS under the user's Aliyun account. <br>
Mitigation: Use only when Alibaba Cloud processing is acceptable for the query content, and avoid submitting secrets, personal data, or confidential business terms. <br>
Risk: The skill requires an Aliyun IQS API key and may consume account quota or incur billing. <br>
Mitigation: Use a dedicated API key where possible, keep any .env file private, and monitor quota or billing. <br>


## Reference(s): <br>
- [Aliyun IQS product documentation](https://help.aliyun.com/product/42958.html) <br>
- [Aliyun IQS UnifiedSearch endpoint](https://cloud-iqs.aliyuncs.com/search/unified) <br>
- [ClawHub skill page](https://clawhub.ai/lilisidu1210-ui/aliyun-iqs-search) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text, shell commands, configuration] <br>
**Output Format:** [JSON object containing success status and data.web search results with title, URL, description, score, and position.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and ALI_IQS_API_KEY; filters to linked results with rerankScore above 0.5.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
