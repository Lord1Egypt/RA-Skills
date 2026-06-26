## Description: <br>
Behavior Persona analyzes local OpenClaw conversation history to generate user behavior profiles and personalized response guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chefroger](https://clawhub.ai/user/chefroger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users can use this skill to profile their own local conversation patterns, communication style, work preferences, and recurring needs. It is intended for users who explicitly want conversation-derived data reused to personalize future agent behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill profiles local OpenClaw conversation history and stores conversation-derived data, which can include sensitive information. <br>
Mitigation: Run the scripts manually first, inspect generated files under the skill data directory, and delete stored data if the collected content is not acceptable. <br>
Risk: The skill can persistently change future agent behavior by injecting a generated profile block into SOUL.md. <br>
Mitigation: Back up SOUL.md before use, keep the daily cron job disabled until reviewed, and manually remove the profile block to revert behavior. <br>
Risk: Memory writes can further persist profile-derived guidance if explicitly enabled. <br>
Mitigation: Keep WRITE_MEMORY disabled unless persistent MEMORY.md updates are intentionally desired and reviewed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chefroger/behavior-persona) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python scripts, JSON profile files, and generated prompt text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local data files such as collected_data.json, analysis reports, user-profile.json, and optional SOUL.md profile blocks.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
