## Description: <br>
Auto Continue helps an agent inspect unfinished task records and skill directories so it can identify remaining work and report the next step. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to check local task progress and skill completeness, then surface unfinished items that may need continued work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's usage guidance may encourage an agent to continue editing, testing, updating progress, or publishing work without fresh user confirmation. <br>
Mitigation: Require explicit approval before external, irreversible, publishing, credential-related, or destructive actions, and review proposed next steps before execution. <br>
Risk: The checker inspects local task and skill directories and may report incomplete work based on workspace file state. <br>
Mitigation: Run it only in the intended workspace and review its status output before using it to drive follow-up actions. <br>


## Reference(s): <br>
- [Auto Continue on ClawHub](https://clawhub.ai/freedompixels/auto-continue) <br>
- [Publisher profile: freedompixels](https://clawhub.ai/user/freedompixels) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown status guidance with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The checker may exit non-zero when unfinished tasks or incomplete skills are detected.] <br>

## Skill Version(s): <br>
1.2.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
