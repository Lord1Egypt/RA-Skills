## Description: <br>
Given a task an AI agent needs to perform, find the right agent-native service from the awesome-agent-native-services catalog and explain how the agent can start using it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haoruilee](https://clawhub.ai/user/haoruilee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to choose an agent-native service for tasks such as communication, browsing, payments, memory, approvals, code execution, search, observability, scheduling, meetings, voice, routing, or agent social workflows. The skill returns a recommendation plus the most direct onboarding pattern, including URL onboarding, SDK, MCP, REST, daemon, or skill-install entry points when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may recommend third-party onboarding instructions that lead an agent to register with a service, install packages, configure MCP, or call external endpoints. <br>
Mitigation: Review the target service, data access, permissions, costs, and revocation options before allowing an agent to follow onboarding instructions or use the service. <br>


## Reference(s): <br>
- [awesome-agent-native-services catalog](https://github.com/haoruilee/awesome-agent-native-services) <br>
- [Moltbook skill onboarding](https://www.moltbook.com/skill.md) <br>
- [Ensue documentation](https://ensue.dev/docs) <br>
- [autoresearch@home collaboration instructions](https://raw.githubusercontent.com/mutable-state-inc/autoresearch-at-home/master/collab.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown recommendation with rationale, onboarding instructions, and relevant catalog use-case excerpts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include third-party URLs, install commands, MCP configuration snippets, SDK examples, or REST guidance drawn from the catalog.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
