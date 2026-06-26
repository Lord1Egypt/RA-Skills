## Description: <br>
Search and browse local Beeper chat history (threads, messages, full-text search). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KrauseFx](https://clawhub.ai/user/KrauseFx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and other Beeper users use this skill to let an agent search and browse local Beeper chat history, including threads, messages, and full-text results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searching local Beeper history can expose private conversations or sensitive workplace and personal information. <br>
Mitigation: Use narrow queries, review outputs before reusing or sharing them, and avoid exposing confidential, legal, medical, financial, or sensitive workplace chats unless intentional. <br>
Risk: Installing the external beeper-cli dependency without review can introduce supply-chain risk. <br>
Mitigation: Pin or review the beeper-cli version before installation when using this skill in managed or sensitive environments. <br>


## Reference(s): <br>
- [ClawHub Beeper Skill](https://clawhub.ai/KrauseFx/beeper) <br>
- [Beeper](https://www.beeper.com/) <br>
- [beeper-cli Project](https://github.com/krausefx/beeper-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON] <br>
**Output Format:** [Markdown guidance with shell commands; beeper-cli returns JSON when --json is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Beeper database and the beeper-cli binary on PATH.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
