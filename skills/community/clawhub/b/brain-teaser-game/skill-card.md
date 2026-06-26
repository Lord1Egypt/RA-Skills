## Description: <br>
Multi-language brain teaser interactive game supporting Chinese, English, and Japanese with automatic language detection, random questions, answer matching, hints, and no-repeat history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KickEGG](https://clawhub.ai/user/KickEGG) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run an interactive multilingual brain-teaser game, including starting sessions, answering questions, requesting hints, revealing answers, moving to the next question, and resetting history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may reuse existing Claude or OpenClaw configuration and send AI question-generation requests to model APIs when the local question pool runs low. <br>
Mitigation: Use a dedicated BRAIN_TEASER_API_KEY or keep AI generation unavailable, and review any configured API endpoint before deployment. <br>
Risk: Server security guidance identifies an offensive Chinese riddle in the bundled content. <br>
Mitigation: Remove the offensive Chinese riddle before broad use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/KickEGG/brain-teaser-game) <br>
- [Publisher Profile](https://clawhub.ai/user/KickEGG) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Python](https://www.python.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with command-line interaction output and optional JSON-based AI question generation responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes the current question, hints when requested, answer feedback, game statistics, and a session ID.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
