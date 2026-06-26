## Description: <br>
The directory for AI agent services. Discover tools, platforms, and infrastructure built for agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to discover agent-oriented services, fetch service directory data, and inspect linked skill.md files before integrating with third-party tools or platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill sends requested public directory or skill-file URLs to the third-party SkillBoss scraping API. <br>
Mitigation: Use it only with URLs that are appropriate to share with SkillBoss, and avoid submitting private, internal, or sensitive resources. <br>
Risk: Fetched third-party skill.md content can contain untrusted instructions. <br>
Mitigation: Review fetched skill files before allowing an agent to follow them or take downstream actions. <br>
Risk: The skill requires a SkillBoss API key. <br>
Mitigation: Provide the key through environment-based secret management, avoid exposing it in prompts or logs, and rotate it if disclosure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abeltennyson/abel-agent-directory) <br>
- [Ctxly homepage](https://ctxly.com) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>
- [SkillBoss API base](https://api.heybossai.com/v1) <br>
- [Ctxly services directory](https://ctxly.com/services.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, API calls, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, JSON response examples, and API request patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends requested public directory or skill-file URLs to the SkillBoss scraping API.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; artifact frontmatter declares 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
