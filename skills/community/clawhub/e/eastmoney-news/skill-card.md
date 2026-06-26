## Description: <br>
Searches Eastmoney for real-time A-share market and financial news and returns readable article summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[njbilly007-lab](https://clawhub.ai/user/njbilly007-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to answer user requests about today's A-share market movement, finance news, sector rotation, and stock-specific news by querying Eastmoney and summarizing returned articles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A shared API key is published in the artifact. <br>
Mitigation: Rotate the exposed key and move authentication to a managed or user-provided credential before broad use. <br>
Risk: Finance search terms are sent to a hardcoded external Eastmoney service. <br>
Mitigation: Disclose this data flow to users, avoid sensitive queries, and require user approval or configuration before sending requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/njbilly007-lab/eastmoney-news) <br>
- [Eastmoney news search API endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Readable article summaries with title, content, date, and source; the helper script can emit JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries are sent to a hardcoded Eastmoney API endpoint; the helper script truncates article content to 200 characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
