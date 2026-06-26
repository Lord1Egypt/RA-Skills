## Description: <br>
Answer Arknights questions about operator roles, skill mechanics, investment planning, story context, terminology, and stage strategy; read and maintain a local structured Doctor profile so advice can adapt to the user's roster and progress; clearly separate fresh version checks from non-current judgment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[morandot](https://clawhub.ai/user/morandot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External players and agent users use this skill to get structured Arknights operator, investment, lore, terminology, comparison, and stage-strategy guidance. The skill can personalize advice from explicitly provided account facts stored in a local Doctor profile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may save explicitly stated game account facts, including server, level, UID, goals, resources, and operators, in a local Doctor profile. <br>
Mitigation: Tell users where the profile is stored and avoid asking them to provide sensitive information beyond what is needed for Arknights guidance. <br>
Risk: The optional manual install path uses a remote shell script. <br>
Mitigation: Prefer installation through a skill manager, or inspect and pin the install script before running it. <br>
Risk: Version-sensitive Arknights guidance can become stale. <br>
Mitigation: For current events, banners, and strength assessments, perform a fresh lookup when available or clearly state that conclusions are not current. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/morandot/arknights-skill) <br>
- [Project Homepage](https://github.com/morandot/arknights-skill) <br>
- [Quick Start](references/quickstart.md) <br>
- [Answer Templates](references/answer-templates.md) <br>
- [Style Examples](references/examples.md) <br>
- [Doctor Profile Schema](references/doctor-profile-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with occasional inline shell commands or JSON snippets for local profile operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update a local Doctor profile when the client permits local file access.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
