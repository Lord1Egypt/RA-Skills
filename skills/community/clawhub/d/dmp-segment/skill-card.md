## Description: <br>
基于明日DMP API，支持组合人群、广告行为规则人群、APP规则人群、LBS规则人群、拓展人群和打通人群等6种人群圈选方式，用于精准营销、用户画像、竞品分析和区域推广。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mingri26](https://clawhub.ai/user/mingri26) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators, analysts, and developers use this skill to configure Mingri DMP credentials, select or query audience segments, validate required parameters, and create or track DMP audience tasks through guided workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install or run helper skills while creating business audience data with API credentials. <br>
Mitigation: Install only when the publisher, the Mingri DMP auth helper, and the optional logger helper are trusted. <br>
Risk: A helper skill path could be resolved from a local workspace or user skill directory. <br>
Mitigation: Confirm exactly which helper skill path will execute and avoid running the skill in workspaces where untrusted skills can be placed. <br>
Risk: API credentials and audience or task parameters may be stored locally or by the logger. <br>
Mitigation: Review local credential and logging storage before use, restrict file access, and avoid submitting data without required user authorization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mingri26/dmp-segment) <br>
- [Mingri DMP auth helper skill](https://clawhub.ai/mingri26/mingdata-dmp-auth) <br>
- [DMP task logger helper skill](https://clawhub.ai/mingri26/dmp-skill-logger) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with JSON API payloads and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local credential setup, helper-skill installation, Mingri DMP API calls, and optional task logging.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
