## Description: <br>
Track fishing spots, gear, catches, and conditions with personalized recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to maintain a local fishing journal, track gear, catches, and fishing spots, and receive recommendations based on their saved history and conditions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores fishing notes in local files that may include exact private fishing spots or license details. <br>
Mitigation: Avoid saving sensitive location or license details unless the user is comfortable keeping them under ~/fishing, and review saved files periodically. <br>
Risk: Automatic catch or spot logging could record details the user did not intend to preserve. <br>
Mitigation: Ask the agent to confirm before logging entries when the user wants manual control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/fishing) <br>
- [Fishing homepage](https://clawic.com/skills/fishing) <br>
- [Memory Setup - Fishing](memory-template.md) <br>
- [Species Guide - Fishing](species.md) <br>
- [Tackle Reference - Fishing](tackle.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with optional shell commands and local markdown file entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local files under ~/fishing for memory, catches, spots, and archived seasons.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
