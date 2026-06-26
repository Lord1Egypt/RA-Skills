## Description: <br>
Agent Matchmaking helps agents discover, compare, rank, and publish capability profiles using capability, reputation, compatibility, pricing, availability, and federation signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexfleetcommander](https://clawhub.ai/user/alexfleetcommander) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create capability profiles, search for suitable agents for a task, compare delegation candidates, and rank agents using reputation and compatibility signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to install and use an external PyPI package. <br>
Mitigation: Install only if you trust the package, and check or pin the package version before use. <br>
Risk: Publishing capability profiles or federating discovery data may expose agent capability, availability, pricing, or reputation details. <br>
Mitigation: Treat published or federated profile data as public or semi-public, and verify where it goes and how it can be updated or removed. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/alexfleetcommander/agent-matchmaking) <br>
- [PyPI package](https://pypi.org/project/agent-matchmaking/) <br>
- [Agent Matchmaking whitepaper](https://vibeagentmaking.com/whitepaper/matchmaking/) <br>
- [Vibe Agent Making](https://vibeagentmaking.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local capability profile files when the referenced Python package is used.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
