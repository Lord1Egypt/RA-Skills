## Description: <br>
Generate PPT with SkillBoss API Hub. Smart template selection based on content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to generate PowerPoint presentations from a topic, either by choosing a template style or by allowing the skill to select an appropriate template automatically. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a SkillBoss API key, which could be exposed or misused if handled carelessly. <br>
Mitigation: Use a dedicated, revocable key stored in the environment, avoid pasting it into prompts or files, and rotate it if exposure is suspected. <br>
Risk: Presentation topics and content may be sent to SkillBoss during generation. <br>
Mitigation: Do not submit confidential, regulated, personal, or secret business content unless SkillBoss is approved for that data. <br>
Risk: The artifact references Python scripts that are not included in the reviewed artifact. <br>
Mitigation: Install only from a source that provides the scripts, then review them before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alvisdunlop/alvis-ppt-generator) <br>
- [Publisher profile](https://clawhub.ai/user/alvisdunlop) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands, streaming JSON status, and a final PowerPoint URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and SkillBoss_API_KEY; generation may take 2-5 minutes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
