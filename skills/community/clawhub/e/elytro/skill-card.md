## Description: <br>
This ClawHub skill is presented as an Ethereum EIP-4337 smart contract wallet assistant for AI agents, but the packaged artifact only redirects agents to a mutable remote skill definition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jayden-sudo](https://clawhub.ai/user/jayden-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and wallet operators would use this skill to guide an agent through Ethereum wallet tasks such as account management, balance checks, and transfers. Reviewers should inspect the exact remote content before use because the packaged release does not contain the wallet workflow locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaged file contains no usable wallet instructions and tells the agent to load mutable instructions from a remote GitHub URL. <br>
Mitigation: Review the exact remote repository content and install only if the skill vendors its instructions locally or pins them to an immutable, reviewed commit. <br>
Risk: Wallet workflows can expose real keys, production accounts, or valuable funds to unsafe agent behavior. <br>
Mitigation: Do not use this skill with real wallet keys, production accounts, or valuable funds unless credential handling and transaction safeguards have been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jayden-sudo/elytro) <br>
- [Publisher profile](https://clawhub.ai/user/jayden-sudo) <br>
- [Remote skill definition referenced by packaged artifact](https://raw.githubusercontent.com/Elytro-eth/skills/main/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with possible inline commands and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The packaged artifact delegates behavior to remote content, so concrete output depends on the reviewed remote definition.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
