## Description: <br>
agentMemo provides a FastAPI-based semantic memory server for AI agents to store, search, retrieve, version, and share memory across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yxjsxy](https://clawhub.ai/user/yxjsxy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use agentMemo to give AI agents persistent, searchable shared memory with namespace scoping, version history, hybrid semantic and keyword search, batch operations, and event streams. It is intended for local or controlled deployments where memories and API keys can be treated as sensitive operational data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RBAC and network behavior do not fully match the skill's security claims. <br>
Mitigation: Review the deployment before use, set a strong admin key outside the project directory when possible, and avoid exposing the service until RBAC and network-binding gaps are fixed. <br>
Risk: Stored memories may contain sensitive project, user, or agent state, and scoped keys may affect more namespaces than intended. <br>
Mitigation: Treat stored memories as sensitive data, use isolated local or containerized environments, and limit API keys and namespaces to the minimum needed. <br>
Risk: Artifact behavior includes a server bind to 0.0.0.0 even though some documentation describes localhost-only operation. <br>
Mitigation: Do not expose the service directly; run it behind an authenticated, TLS-protected reverse proxy only after the binding behavior has been reviewed or changed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yxjsxy/agentmemo-karl) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>
- [Acceptance checklist](benchmark/ACCEPTANCE_CHECKLIST.md) <br>
- [Evaluation summary](benchmark/results/eval_summary.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, Python snippets, and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit HTTP API examples and local service configuration; no structured output contract.] <br>

## Skill Version(s): <br>
3.2.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
