## Description: <br>
Manage Exa AI via CLI - search, contents, answer, context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Melvynx](https://clawhub.ai/user/Melvynx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to install and authenticate exa-cli, then run Exa web search, content retrieval, answer, and context commands from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow runs third-party CLI installer and build commands. <br>
Mitigation: Review the disclosed commands before execution and install only in environments where running the third-party Exa CLI is acceptable. <br>
Risk: The skill uses an Exa API token and sends searches, URLs, and content requests to Exa. <br>
Mitigation: Use a revocable Exa API token, keep tokens out of shared logs, and avoid submitting sensitive proprietary data unless it is appropriate to share with Exa. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Melvynx/exa-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands generally use the --json flag for programmatic use.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
