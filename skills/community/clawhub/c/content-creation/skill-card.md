## Description: <br>
部署内容创作Agent团队（墨白主编+探风选题+锦书文案），平台无关的内容生产核心。使用 /content-creation 触发，交互式引导配置品牌信息并自动部署。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Little-ke](https://clawhub.ai/user/Little-ke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and operators use this skill to deploy a three-agent OpenClaw content team for topic planning, editorial review, and article drafting. The setup collects brand, audience, style, publishing cadence, and topic constraints before creating local agent workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup answers and agent memory files may retain brand plans, audience details, content preferences, and other sensitive operating context locally across sessions. <br>
Mitigation: Do not enter passwords, API keys, unpublished confidential plans, private customer data, or other sensitive information unless local retention is acceptable. <br>
Risk: The setup registers three OpenClaw agents and writes files under the user's OpenClaw workspace. <br>
Mitigation: Review the expected workspace path and agent registrations before installation, especially on shared machines or managed environments. <br>
Risk: Generated content may contain factual errors or unsupported claims if agents rely on incomplete source material. <br>
Mitigation: Review drafts before publication and verify facts, data, and citations as part of the editorial workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Little-ke/content-creation) <br>
- [Publisher profile](https://clawhub.ai/user/Little-ke) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and local workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local OpenClaw agent workspaces and persistent memory files under the user's OpenClaw home directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
