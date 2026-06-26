## Description: <br>
Find Skills Combo helps agents decompose complex user requests, search for relevant skills, evaluate candidate coverage, and recommend either a maximum-quality or minimum-dependency skill combination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[helloml0326](https://clawhub.ai/user/helloml0326) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to identify skill portfolios for multi-step tasks, compare quality versus dependency trade-offs, and decide which skills to install or inspect. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recommendations may route users toward external skill searches and third-party skill installs. <br>
Mitigation: Review candidate skills, publishers, and source links before installing or relying on them. <br>
Risk: Global no-confirm install commands can make persistent changes to the agent environment. <br>
Mitigation: Prefer explicit approval for each install or update, and avoid `-g -y` unless the user has authorized a global install. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/helloml0326/find-skills-combo) <br>
- [Publisher profile](https://clawhub.ai/user/helloml0326) <br>
- [Skills CLI directory](https://skills.sh/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include candidate skill lists, coverage ratings, install commands, coverage gaps, and risk notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
