## Description: <br>
A Chinese communication-guidance skill that prompts an agent to structure replies into thinking, execution, and review steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[markma84](https://clawhub.ai/user/markma84) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to make agent responses more explicit by separating goal and option analysis, command or action results, and post-action review. It is especially suited to communication workflows where both the user and assistant need to inspect assumptions and execution quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to run a bundled local license-verification script before revealing the skill content. <br>
Mitigation: Review the script before running it and avoid installing or using the skill if local code execution for licensing is not acceptable. <br>
Risk: The license check can withhold the communication guidance when a local license file is missing, expired, revoked, or malformed. <br>
Mitigation: Confirm the expected subscription or license state with the publisher before relying on the skill in a workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/markma84/3steps-to-wisdom) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional shell command output from local license verification] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill content is license-gated by a local verify.py script that reads a local license file and prints the skill instructions or renewal guidance.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
