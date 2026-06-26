## Description: <br>
Fusion Workflow Hub guides agents through codebase analysis, TDD development, code review, and continuous-learning workflows that combine Graphify knowledge-graph commands with ECC and OpenClaw practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuang-he](https://clawhub.ai/user/zhuang-he) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to understand repository structure, plan and review feature work, run TDD-oriented workflows, and generate knowledge-graph artifacts for deeper code analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to install and run a third-party Python package for repository analysis. <br>
Mitigation: Verify the package source before installation and run it in a virtual environment. <br>
Risk: Repository graph artifacts may expose sensitive project structure or code relationships. <br>
Mitigation: Run analysis only on intended project folders and exclude or delete graphify-out artifacts when they should not be shared. <br>
Risk: Workflow guidance can lead to incorrect code plans or review conclusions if accepted without inspection. <br>
Mitigation: Review proposed commands, plans, generated reports, and code changes before execution or deployment. <br>


## Reference(s): <br>
- [Fusion Workflow Hub on ClawHub](https://clawhub.ai/zhuang-he/fusion-workflow-hub) <br>
- [Graphify command reference](references/graphify-commands.md) <br>
- [ECC best practices](references/ecc-best-practices.md) <br>
- [Everything Claude Code](https://github.com/probinger/00-everything-claude-code) <br>
- [Graphify](https://github.com/safishamsi/graphify) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to generate local graphify-out artifacts such as graph.html, GRAPH_REPORT.md, graph.json, and cache files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
