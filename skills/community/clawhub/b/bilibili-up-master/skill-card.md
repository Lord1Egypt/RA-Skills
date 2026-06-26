## Description: <br>
Bilibili Up Master helps agents monitor Bilibili trending videos, analyze creator and video metrics, compare creators, plan content, and generate operations reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, social media operators, and content strategists use this skill to gather Bilibili trend signals, analyze UP creator performance, review individual videos, and turn those observations into publishing guidance and daily or weekly reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the skill weakens HTTPS security. <br>
Mitigation: Review or remove the global HTTPS certificate-verification override before deployment, and use a dedicated browser profile when collecting Bilibili data. <br>
Risk: The security evidence says generated data is stored in a predictable temporary folder. <br>
Mitigation: Treat /tmp/bilibili-data as temporary local storage, avoid placing sensitive account information there, and delete generated reports and cached data when analysis is complete. <br>
Risk: The security guidance notes that the skill may use browser or agent-reach access for Bilibili pages. <br>
Mitigation: Run with the minimum needed browser access, confirm target pages before collection, and respect Bilibili community rules and rate limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onlyloveher/bilibili-up-master) <br>
- [Bilibili ranking](https://www.bilibili.com/ranking) <br>
- [Bilibili ranking API](https://api.bilibili.com/x/web-interface/ranking/v2) <br>
- [Bilibili creator card API](https://api.bilibili.com/x/web-interface/card) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON data structures, Python command output, and concise guidance text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated JSON data and Markdown reports under /tmp/bilibili-data and /tmp/bilibili-data/reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.yaml; _meta.json lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
