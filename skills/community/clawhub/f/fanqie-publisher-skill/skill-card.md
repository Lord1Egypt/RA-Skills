## Description: <br>
番茄小说章节自动发布工具，支持单章发布、批量发布、存入草稿箱、登录番茄小说作家后台和查看作品列表与状态. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[followaf](https://clawhub.ai/user/followaf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authors or operators with a Fanqie Novel writer account use this skill to automate chapter upload workflows, including direct publication, draft saving, login status checks, and work-list review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a logged-in Fanqie writer account and directly publish chapters. <br>
Mitigation: Use draft mode first, confirm the target work and chapter files, and require a human review before direct publication. <br>
Risk: Saved cookies can preserve access to the writer account if the cookie file is exposed. <br>
Mitigation: Protect fanqie_cookies.json with local file permissions and delete it after publishing or when the session is no longer needed. <br>
Risk: Automation-evasion flags and --no-sandbox browser settings can increase operational and policy risk. <br>
Mitigation: Review the browser configuration before use and remove stealth flags and --no-sandbox on normal machines when they are not required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/followaf/fanqie-publisher-skill) <br>
- [Fanqie Novel writer zone](https://fanqienovel.com/writer/zone/) <br>
- [Fanqie Novel writer login](https://fanqienovel.com/main/writer/login?enter_from=skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with Python examples, shell commands, and dictionary-style status results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces browser automation actions against a logged-in Fanqie Novel writer account and may create screenshots on failure.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
