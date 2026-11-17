## Description: <br>
Evolve Loop Free guides an AI agent through a PDCA self-improvement loop that records corrections, preferences, and reflections in layered local Markdown memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical leads, creators, and other agent users use this skill to persist cross-session preferences, corrections, and lessons in local Markdown files so future agent work can apply them with source references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently records user corrections, preferences, and reflections across sessions in local files. <br>
Mitigation: Install only when local cross-session memory is intended, review ~/evolve-loop regularly, and use the forget/delete workflow when memory should not persist. <br>
Risk: Memory exports or git backups may disclose sensitive personal data or secrets stored in the memory directory. <br>
Mitigation: Avoid storing secrets or sensitive personal data, and review ZIP exports or backups before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/evolve-loop-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and local file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, read, update, export, and delete local Markdown memory files under ~/evolve-loop when the hosting agent follows the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
