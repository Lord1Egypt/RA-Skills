## Description: <br>
Clawdbot documentation expert with decision tree navigation, search scripts, doc fetching, version tracking, and config snippets for all Clawdbot features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to navigate Clawdbot documentation, find setup and troubleshooting pages, and produce configuration guidance or snippets for Clawdbot providers, gateway operations, automation, platforms, tools, and installs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires the sensitive SKILLBOSS_API_KEY credential. <br>
Mitigation: Install only after verifying what the key can access, and provide the least-privileged key suitable for the intended use. <br>
Risk: The skill references ./scripts/*.sh helper commands that are not included in the package. <br>
Mitigation: Before allowing those commands to run, confirm the publisher supplies the missing scripts or inspect the local execution path to avoid running unrelated project scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abeltennyson/abe-clawddocs) <br>
- [Clawdbot Discord provider documentation](https://docs.clawd.bot/providers/discord) <br>
- [SkillBoss API Hub pilot endpoint](https://api.skillboss.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cite Clawdbot documentation URLs and may propose helper script commands when those scripts are present.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
