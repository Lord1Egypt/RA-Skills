## Description: <br>
AI agent self-portrait generator. Create avatars, profile pictures, and visual identity using SkillBoss API Hub image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to generate agent avatars, profile pictures, banners, and visual identity assets from personality, mood, theme, and format inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Avatar prompts and personality details are sent to the SkillBoss API. <br>
Mitigation: Use only personality details and visual prompts that are acceptable to share with that API service. <br>
Risk: The skill requires SKILLBOSS_API_KEY. <br>
Mitigation: Use a revocable key and keep it out of repositories, shared dotfiles, logs, and public examples. <br>
Risk: Heartbeat guidance can lead to public avatar changes on Discord, Twitter/X, AgentGram, or similar services. <br>
Mitigation: Require explicit user approval for each target account and each profile update before publishing changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abeltennyson/abel-agent-selfie) <br>
- [OpenClaw](https://openclaw.org) <br>
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions] <br>
**Output Format:** [PNG image files, prompts.json metadata, an HTML gallery, and markdown setup examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends image prompts and personality details to the SkillBoss API Hub.] <br>

## Skill Version(s): <br>
1.0.0 (source: target metadata and SKILL.md frontmatter; artifact package.json reports 1.2.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
