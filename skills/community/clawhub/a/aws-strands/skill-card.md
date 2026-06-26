## Description: <br>
Build and run Python-based AI agents using the AWS Strands SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TrippingKelsea](https://clawhub.ai/user/TrippingKelsea) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold, configure, and run Strands-based agents with local, commercial API, or AWS Bedrock model providers. It also provides guidance for custom tools, MCP integration, multi-agent workflows, sessions, and observability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated agent scaffolds include file read, file write, and shell command tools with broad local access. <br>
Mitigation: Review or remove those tools before running generated agents, and test in an isolated Python environment or disposable workspace. <br>
Risk: Provider credentials, AWS credentials, local files, and secrets may be exposed if an agent or connected MCP server is given excessive access. <br>
Mitigation: Use least-privilege credentials, keep secrets out of the working directory, and connect only trusted MCP servers. <br>
Risk: The server security verdict is suspicious because the scaffold lacks strong user-facing guardrails around powerful tools. <br>
Mitigation: Review the generated code and planned tool access before deployment, especially for production repositories or important local files. <br>


## Reference(s): <br>
- [Strands SDK](https://github.com/strands-agents/sdk-python) <br>
- [Strands SDK Cheatsheet](references/cheatsheet.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/TrippingKelsea/aws-strands) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Python agent scaffolds and configuration files when its bundled scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter states 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
