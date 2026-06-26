## Description: <br>
Self-writing meta-extension that forges new capabilities - researches docs, writes extensions, tools, hooks, and skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use abe-foundry to install and configure Foundry for OpenClaw, research documentation, and generate extensions, tools, hooks, skills, and configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a high-privilege, self-modifying OpenClaw development extension. <br>
Mitigation: Review generated tools, hooks, skills, and self-updates before enabling them, and run the skill in a sandbox or separate OpenClaw profile. <br>
Risk: The skill requires sensitive credentials for SkillBoss API Hub access. <br>
Mitigation: Provide only scoped credentials, avoid sharing secrets in prompts or generated artifacts, and rotate credentials if exposure is suspected. <br>
Risk: Auto-learning or marketplace publishing can persist or share generated capabilities beyond the immediate task. <br>
Mitigation: Keep auto-learning and marketplace publishing disabled unless intentionally needed and manually approved. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/abeltennyson/abe-foundry) <br>
- [Publisher profile](https://clawhub.ai/user/abeltennyson) <br>
- [Foundry homepage](https://getfoundry.app) <br>
- [OpenClaw Foundry repository](https://github.com/lekt9/openclaw-foundry) <br>
- [SkillBoss API Hub](https://api.heybossai.com/v1/pilot) <br>
- [Foundry Marketplace](https://api.claw.getfoundry.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and code/configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or generate self-modifying OpenClaw artifacts; review before enabling or running them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
