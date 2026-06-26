## Description: <br>
Discover agent-native CLIs for professional software and use the live catalog to find tools for creative workflows, productivity, AI, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuh-yang](https://clawhub.ai/user/yuh-yang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to discover, search, and install CLI-Anything tools for creative, productivity, AI, communication, development, and content-generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the catalog as blanket approval could lead an agent to install downstream CLI packages without sufficient review. <br>
Mitigation: Treat the skill as a discovery aid; review each downstream package or source before installing it. <br>
Risk: Installed downstream CLIs may access local files, accounts, browsers, infrastructure, or external services. <br>
Mitigation: Prefer isolated environments, pin versions where practical, and explicitly approve tools that request sensitive access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuh-yang/cli-anything-hub) <br>
- [CLI-Anything live catalog](https://clianything.cc/SKILL.txt) <br>
- [CLI-Anything web hub](https://clianything.cc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downstream CLI tools may provide JSON output when invoked with their own --json flag.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
