## Description: <br>
Generate AI-powered notes from videos in document, outline, or graphic-text formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate structured notes from public video URLs through SkillBoss API Hub. It supports document notes, outline notes, and graphic-text notes for video summarization workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public video URLs are sent to SkillBoss/HeyBossAI for processing. <br>
Mitigation: Use the skill only for video links that users intend to share with that service, and avoid sensitive or private media links. <br>
Risk: The skill requires SKILLBOSS_API_KEY for authenticated API access. <br>
Mitigation: Configure a dedicated API key as a secret and avoid exposing it in prompts, logs, or shared command output. <br>
Risk: The artifact references Python scripts that were not included in the reviewed files. <br>
Mitigation: Verify the referenced scripts before running them and scan any downloaded or generated script files before deployment. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/marjoriebroad/ainotes-of-video) <br>
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Formatted notes with type labels, JSON API examples, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a public video URL and SKILLBOSS_API_KEY; optional polling parameters include max_attempts and interval_seconds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
