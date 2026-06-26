## Description: <br>
Autogen Multi Agent provides guidance for maintaining, migrating, and troubleshooting legacy AutoGen v0.4 multi-agent projects, while its bundled seed also includes finance/ZVT strategy workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to maintain legacy AutoGen v0.4 systems, migrate toward Microsoft Agent Framework, and troubleshoot multi-agent patterns such as Swarm handoffs, MCP tool use, code-executor pairs, and hosted agent teams. Reviewers should note that server security evidence reports finance/ZVT setup, credential, and execution workflows in the bundled artifact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The advertised AutoGen maintenance focus does not fully match the bundled finance/ZVT strategy, setup, data, credential, and execution workflows. <br>
Mitigation: Review references/seed.yaml before installation or use, and treat finance/ZVT workflows as in scope only after explicit user intent and review. <br>
Risk: The artifact may request broker or paid-data credentials for providers such as JoinQuant or QMT. <br>
Mitigation: Do not provide broker or paid-data credentials in chat; configure credentials locally through provider-approved mechanisms and avoid hardcoding them in generated scripts. <br>
Risk: Generated commands or code may install packages, access local workspaces, or run execution workflows. <br>
Mitigation: Inspect generated commands before running them, execute only in a controlled workspace, and use isolated execution for untrusted or LLM-generated code. <br>


## Reference(s): <br>
- [Seed reference](references/seed.yaml) <br>
- [ClawHub skill page](https://clawhub.ai/tangweigang-jpg/autogen-multi-agent) <br>
- [Doramagic crystal page](https://doramagic.ai/zh/crystal/autogen-multi-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with code and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for market, data source, strategy type, time range, entity IDs, and execution confirmation before generating runnable workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter v0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
