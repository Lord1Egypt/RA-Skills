## Description: <br>
The directory for AI agent services. Discover tools, platforms, and infrastructure built for agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover agent services, inspect service metadata, and fetch public skill.md files for integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested URLs and fetched public content are sent through the SkillBoss API Hub. <br>
Mitigation: Use the skill only with public service listings and public skill.md files; avoid private or authenticated URLs. <br>
Risk: The skill requires SKILLBOSS_API_KEY. <br>
Mitigation: Keep the key in environment configuration, protect it from logs and prompts, and rotate it if exposure is suspected. <br>
Risk: Fetched third-party skill.md content may contain instructions for an agent. <br>
Mitigation: Review fetched third-party skill instructions before allowing an agent to follow them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abeltennyson/agent-directory1) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/abeltennyson) <br>
- [ctxly.com](https://ctxly.com) <br>
- [ctxly.com services.json](https://ctxly.com/services.json) <br>
- [SkillBoss API Hub](https://api.heybossai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends requested public URLs to the SkillBoss API Hub.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
