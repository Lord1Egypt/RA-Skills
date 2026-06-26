## Description: <br>
Generate PPT with SkillBoss API Hub. Smart template selection based on content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate presentation decks from a topic through SkillBoss API Hub, either with a user-selected template or an automatically selected template. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to run helper Python scripts that are not included in the package. <br>
Mitigation: Confirm the referenced scripts come from a trusted, reviewed source and that the agent runs those specific files from the skill package rather than arbitrary relative paths. <br>
Risk: The workflow requires a SkillBoss API key and submits presentation topics to SkillBoss API Hub. <br>
Mitigation: Use a limited or revocable API key and avoid confidential presentation topics unless SkillBoss API Hub handling is trusted for that content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alvisdunlop/alvis2-ai-ppt-generator) <br>
- [Publisher profile](https://clawhub.ai/user/alvisdunlop) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and SkillBoss_API_KEY; the invoked workflow streams JSON status and returns a PPT URL when generation completes.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
