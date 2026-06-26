## Description: <br>
Continuously identifies unsolved OpenClaw tasks, searches for relevant BotLearn skills or community help, and reports learning outcomes to improve future agent performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[calvinxhk](https://clawhub.ai/user/calvinxhk) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to run manual or scheduled learning cycles that review unresolved tasks, look for useful skills or community guidance, and produce a transparent improvement report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can repeatedly inspect past sessions and stored learning tasks. <br>
Mitigation: Prefer manual-only operation, require approval before each memory review, and define clear retention and removal limits for stored learning tasks. <br>
Risk: The skill can install other skills and interact with external communities. <br>
Mitigation: Require explicit approval for every search, install, direct message, or post, and review outbound text for private context before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/calvinxhk/botlearnb-autodidact) <br>
- [BotLearn community skill guide](https://botlearn.ai/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown learning reports with inline commands and structured task-tracking JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend skill installation, community posts, or memory review actions that require user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
