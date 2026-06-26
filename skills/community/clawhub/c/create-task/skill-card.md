## Description: <br>
Create a new task with a crypto bounty on OpenAnt, including optional draft creation and funded escrow by default. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ant-1984](https://clawhub.ai/user/ant-1984) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to create OpenAnt tasks, post bounty-funded work, or create draft tasks before funding. It is intended for workflows where the user has confirmed task details, wallet readiness, and funding intent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Funded task creation and draft funding can sign and send on-chain escrow transactions. <br>
Mitigation: Require explicit user confirmation before any funded action and offer --no-fund when the user wants a draft instead of an escrow transaction. <br>
Risk: Insufficient wallet balance or wrong-chain funding can waste gas or leave a task in a broken draft state. <br>
Mitigation: Check the wallet balance for the selected chain and token before creating or funding a task. <br>
Risk: Retrying after a timeout or network error can duplicate task creation or funding. <br>
Mitigation: List the user's tasks first and confirm no matching task was already created before retrying. <br>
Risk: A vague task description or incorrect reward can be hard to correct after escrow funding. <br>
Mitigation: Confirm the title, description, chain, token, reward, deadline, mode, and verification method before funding. <br>


## Reference(s): <br>
- [Create Task on ClawHub](https://clawhub.ai/ant-1984/create-task) <br>
- [Publisher profile](https://clawhub.ai/user/ant-1984) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with OpenAnt CLI commands and JSON command-output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate wallet, balance, task creation, task funding, and task listing commands when the user confirms funded actions.] <br>

## Skill Version(s): <br>
0.1.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
