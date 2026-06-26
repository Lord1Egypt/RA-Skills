## Description: <br>
Train autonomous OpenClaw AI agents through LLM-guided curriculum design and multi-turn dialogue evaluation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myismyname](https://clawhub.ai/user/myismyname) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use ClawSergeant to design, approve, run, and evaluate structured OpenClaw training sessions for a target agent. It is suited for iterative curriculum-driven improvement where an LLM generates tasks, scores responses, and records training outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Training content and agent outputs are sent to external LLM or agent services. <br>
Mitigation: Use a controlled OpenClaw training setup, avoid confidential prompts or outputs, and configure a limited API key. <br>
Risk: The skill persists training memory and lesson logs with limited runtime control. <br>
Mitigation: Inspect or disable lesson logging and MEMORY.md writes before running if persistent memory is not intended. <br>
Risk: The release evidence reports that learning_logger.py is missing from the artifact while runtime code imports it. <br>
Mitigation: Obtain and review the missing learning_logger.py implementation before executing a full training session. <br>


## Reference(s): <br>
- [ClawSergeant ClawHub release](https://clawhub.ai/myismyname/clawsergeant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON examples, configuration instructions, and generated training result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write training_results.json, lesson logs under .claw_sergeant_accumulated_lessons/, and an OpenClaw MEMORY.md summary when the target workspace exists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
