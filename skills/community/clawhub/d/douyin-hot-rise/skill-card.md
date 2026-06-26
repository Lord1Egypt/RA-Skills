## Description: <br>
Fetches real-time Douyin rising hot-topic data through the disclosed Douyin billboard API using an AZT_API_KEY credential. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyriswu](https://clawhub.ai/user/kyriswu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve and summarize current Douyin rising hot-topic rankings, optionally filtering by page, size, sort order, topic tag, or keyword. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an AZT_API_KEY and sends it to the devtool.uk/coze-js-api service. <br>
Mitigation: Use a scoped or low-privilege key, keep it in the AZT_API_KEY environment variable rather than chat logs, and rotate it if exposed. <br>
Risk: Results and availability depend on a third-party API and current Douyin trend data. <br>
Mitigation: Treat returned rankings as live external data, check API errors before relying on output, and retry later for network or service failures. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kyriswu/douyin-hot-rise) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/kyriswu) <br>
- [Douyin hot rise API endpoint](https://coze-js-api.devtool.uk/douyin/billboard/fetch_hot_rise_list) <br>
- [Devtool plugin and API key information](https://devtool.uk/plugin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown summary of API request status and returned trend items; optional raw JSON from the helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AZT_API_KEY credential and sends request parameters to a third-party API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
