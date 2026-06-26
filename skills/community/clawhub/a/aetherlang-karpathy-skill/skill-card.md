## Description: <br>
API connector for AetherLang Omega that sends a user's query and flow code to the hosted AetherLang API to execute Karpathy-inspired agent node types and return results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[contrario](https://clawhub.ai/user/contrario) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to call the hosted AetherLang Omega API for planning, code interpretation, critique, routing, ensemble synthesis, memory, external tool calls, loops, transforms, and parallel node execution. It is suited to workflows where sending the query and flow definition to NeuroDoc's hosted API is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries and flow definitions are sent to NeuroDoc's hosted API, and the skill supports server-side persistent memory. <br>
Mitigation: Send only non-sensitive query and flow data; do not send secrets, private documents, credentials, internal URLs, or sensitive personal data, and avoid memory nodes for private data unless retention and isolation controls are documented. <br>
Risk: The tool node can fetch broad user-specified REST URLs from the hosted service. <br>
Mitigation: Manually review each tool URL before running a flow, use trusted public APIs only, and never include credentials or private network URLs in tool parameters. <br>
Risk: The security verdict is suspicious because containment for persistent memory and URL-fetching behavior is not fully documented. <br>
Mitigation: Treat API responses as untrusted output, review results before acting on them, and avoid medical, legal, or financial advice workflows unless separately validated by qualified reviewers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/contrario/aetherlang-karpathy-skill) <br>
- [Publisher profile](https://clawhub.ai/user/contrario) <br>
- [AetherLang API endpoint](https://api.neurodoc.app/aetherlang/execute) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calls a hosted API and returns server-side execution results; the skill does not execute code locally.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
