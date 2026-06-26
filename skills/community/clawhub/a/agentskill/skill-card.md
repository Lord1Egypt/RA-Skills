## Description: <br>
Let any agent produce code indistinguishable from the existing codebase. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[airscripts](https://clawhub.ai/user/airscripts) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Agentskill to inspect code repositories, extract project conventions, and produce AGENTS.md guidance that helps coding agents follow the existing codebase. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated AGENTS.md guidance may be incorrect, incomplete, or too broad for a repository. <br>
Mitigation: Review generated files before relying on them or sharing them with other agents. <br>
Risk: Remote references can influence the generated guidance. <br>
Mitigation: Use remote references only from repositories and publishers you trust. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/airscripts/agentskill) <br>
- [README](README.md) <br>
- [System Specification](SYSTEM.md) <br>
- [API Reference Index](docs/reference/README.md) <br>
- [CLI Reference](docs/reference/cli.md) <br>
- [Command Modules](docs/reference/commands.md) <br>
- [Gotchas](references/GOTCHAS.md) <br>
- [PyPI Package](https://pypi.org/project/agsk) <br>
- [Turning Repository Knowledge Into Usable Agent Context](https://dev.to/airscript/turning-repository-knowledge-into-usable-agent-context-4pe4) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON, with optional shell commands and configuration excerpts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or update AGENTS.md and companion markdown files when the user requests file output.] <br>

## Skill Version(s): <br>
1.4.0 (source: release evidence, pyproject.toml, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
