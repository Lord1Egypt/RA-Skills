## Description: <br>
Bimiyun Search lets an agent query the Bimiyun web-search API and return LLM-friendly results in Markdown or JSON, with safe search enabled by default. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bimiyun888](https://clawhub.ai/user/bimiyun888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run web searches through Bimiyun from an agent workflow and receive concise search results for research, news lookup, or general information retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and the configured API key are sent to Bimiyun. <br>
Mitigation: Use the skill only when sending those queries to Bimiyun is acceptable, and avoid searching secrets, private internal data, or sensitive personal information. <br>
Risk: A local .env file may contain BIMIYUN_API_KEY. <br>
Mitigation: Keep .env files out of version control and rotate the key if it is exposed. <br>
Risk: BIMIYUN_ENDPOINT can change the destination that receives search requests. <br>
Mitigation: Set BIMIYUN_ENDPOINT only when the destination is trusted. <br>


## Reference(s): <br>
- [Bimiyun website](https://bimiyun.com) <br>
- [ClawHub skill page](https://clawhub.ai/bimiyun888/bimiyun-search) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/bimiyun888) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown search-result list or raw JSON object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BIMIYUN_API_KEY; supports language, result-count, safe-search, fulltext/snippet mode, and output-format options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
