## Description: <br>
Cognitive-state audit skill that prompts an agent to check uncertainty, contradictions, assumptions, blockers, and recovery steps when challenged, when tool results look anomalous, when requirements are ambiguous, or when post-fix verification is needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maochen1980](https://clawhub.ai/user/maochen1980) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to make an assistant pause and audit its reasoning state when the user questions an answer, tool output is unexpected, a requirement is ambiguous, or a recent fix needs verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to write its current thinking state to a temporary local file, which may expose sensitive task context if the file contains secrets or private user data. <br>
Mitigation: Keep audit notes sanitized, avoid writing credentials or private data, and delete the temporary audit file after the review is complete. <br>
Risk: The skill includes self-optimization language that asks the agent to load a skill manager to repair or optimize the skill. <br>
Mitigation: Require explicit human approval before modifying installed skill files and review any proposed changes before use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style inline assessment summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill also asks the agent to write and read back a temporary local audit file during execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
