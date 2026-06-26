## Description: <br>
Cloudbase helps agents develop, design, deploy, debug, migrate, and troubleshoot CloudBase projects across web apps, WeChat Mini Programs, authentication, databases, cloud functions, CloudRun, storage, AI integrations, operations, and spec workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binggg](https://clawhub.ai/user/binggg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and implement CloudBase and Tencent CloudBase applications, choose the right reference workflow, configure backend resources, generate application code, and produce deployment or troubleshooting commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports agent-directed hidden comments and unsafe copy-paste deployment or security examples. <br>
Mitigation: Review deployment, public access, CORS, and authentication examples before production use, and require explicit user approval before executing shell commands or changing cloud resources. <br>
Risk: The skill can auto-activate for broad UI, AI, operations, and planning requests outside CloudBase work. <br>
Mitigation: Install and use it only for CloudBase or Tencent CloudBase development tasks, and route unrelated requests to more specific skills. <br>


## Reference(s): <br>
- [ClawHub Cloudbase skill page](https://clawhub.ai/binggg/skills/cloudbase) <br>
- [CloudBase main skill](artifact/SKILL.md) <br>
- [MCP setup guidance](artifact/references/mcp-setup.md) <br>
- [CloudBase CLI workflows](artifact/references/cloudbase-cli/SKILL.md) <br>
- [Cloud functions guidance](artifact/references/cloud-functions/SKILL.md) <br>
- [Web development guidance](artifact/references/web-development/SKILL.md) <br>
- [CloudBase agent guidance](artifact/references/cloudbase-agent/SKILL.md) <br>
- [CloudBase pricing](https://cloud.tencent.com/document/product/876/75213) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to inspect CloudBase MCP tools, read scenario-specific references, and review generated deployment or security examples before use.] <br>

## Skill Version(s): <br>
1.92.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
