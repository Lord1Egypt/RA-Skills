## Description: <br>
Automatically fetches Bilibili overall ranking video data with detailed video statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangjinghua0127](https://clawhub.ai/user/yangjinghua0127) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve the current Bilibili overall Top 50 ranking, inspect video statistics, and save the results as structured JSON and readable text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes live network requests to the Bilibili ranking API, so output can change over time or fail if the API is unavailable. <br>
Mitigation: Treat results as current API output, handle request failures, and rerun the skill when fresh ranking data is needed. <br>
Risk: The skill writes JSON and text files into the workspace scripts directory. <br>
Mitigation: Run it in an intended workspace and review generated files before using them downstream. <br>


## Reference(s): <br>
- [Bilibili Ranking API](https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all) <br>
- [ClawHub skill page](https://clawhub.ai/yangjinghua0127/bilibili-hot) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Files, Text, JSON] <br>
**Output Format:** [Console text plus saved JSON and plain-text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and writes bilibili-hot.json and bilibili-hot.txt under the workspace scripts directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
