## Description: <br>
Baidu Scholar Search - Search Chinese and English academic literature (journals, conferences, papers, etc.) <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search Chinese and English academic literature on Baidu Scholar by keyword, with optional pagination and abstracts when detailed paper information is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search keywords, page number, and abstract preference are sent to Baidu's service using a required API key. <br>
Mitigation: Use the skill only when sending the query to Baidu is acceptable, and avoid submitting secrets, private research topics, personal data, or confidential internal project names. <br>
Risk: The skill depends on a local BAIDU_API_KEY environment variable for authenticated requests. <br>
Mitigation: Store the API key in the execution environment, do not include it in prompts or command arguments, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lean-zhouchao/baidu-scholar-search-skill-1-1-0) <br>
- [Baidu Scholar](https://xueshu.baidu.com/) <br>
- [Baidu Scholar search API endpoint](https://qianfan.baidubce.com/v2/tools/baidu_scholar/search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON search results from the Baidu Scholar API, with Markdown usage guidance and shell command examples in the skill documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and the BAIDU_API_KEY environment variable; abstracts are omitted by default unless explicitly requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence; artifact metadata reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
