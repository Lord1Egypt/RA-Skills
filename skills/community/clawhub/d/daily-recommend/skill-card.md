## Description: <br>
Daily Recommend helps an agent send one concise literature, quote, book, film, or documentary recommendation at scheduled or user-requested moments, using feedback to adapt future picks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billxfan](https://clawhub.ai/user/billxfan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and teams use this skill to receive lightweight daily cultural recommendations in Markdown, either from scheduled agent turns or direct prompts such as asking for a poem, book, or film. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retain likes, dislikes, ignored items, and preference weights in a local workspace preference history file. <br>
Mitigation: Review or delete [WORKSPACE]/memory/recommend-preferences.md if that history should not be reused. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/billxfan/daily-recommend) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/billxfan) <br>
- [Submitted skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Feishu-compatible Markdown recommendation messages with title, quoted excerpt, rationale, and tags] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update a workspace preference history file to tune later recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
