## Description: <br>
Executes OpenClaw/Moltbot/ClawDBot skill creation using the official 5-step research flow for compliant, secure, and well-structured skill development. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to create or modify OpenClaw, Moltbot, and ClawDBot skills through a structured research, comparison, and output process. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can auto-trigger broadly and send skill-creation prompts to a third-party SkillBoss/HeyBossAI API using a sensitive API key. <br>
Mitigation: Use a dedicated API key, avoid including secrets or proprietary code in requests, and review generated skills before installation or deployment. <br>
Risk: The included processor simulates parts of the advertised research flow. <br>
Mitigation: Manually verify generated recommendations against current official documentation and inspect generated SKILL.md files before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alvisdunlop/alvis-advanced-skill-creator) <br>
- [ClawdBot skills documentation](https://docs.clawd.bot/tools/skills) <br>
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills) <br>
- [SkillBoss API endpoint](https://api.heybossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code blocks and structured recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call a third-party SkillBoss API when SKILLBOSS_API_KEY is configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
