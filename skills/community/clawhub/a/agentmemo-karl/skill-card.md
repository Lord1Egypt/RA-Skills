## Description:

agentMemo is a Semantic Memory Mesh server for AI agents that stores, searches, retrieves, versions, and streams memory across sessions using FastAPI, SQLite, HNSW embeddings, and hybrid semantic plus keyword search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yxjsxy](https://clawhub.ai/user/yxjsxy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use agentMemo to give AI agents persistent, searchable memory across sessions, including preferences, decisions, project state, event streams, and versioned rollback. It is suited to local or controlled deployments where memory storage, namespace access, and API-key handling can be reviewed before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advertised isolation and localhost-only protections are not reliably enforced.

Mitigation: Install only in an isolated local environment, change the default bind address to 127.0.0.1, and avoid exposing the service to shared networks until reviewed.

Risk: Namespace authorization bugs may affect isolation in shared or multi-agent memory stores.

Mitigation: Fix and test namespace authorization before using the skill for shared, multi-agent, or sensitive memories.

Risk: Secret handling, privacy controls, and retention controls need review before sensitive use.

Mitigation: Use a strong AGENTMEMO_ADMIN_KEY, keep secrets out of logs and shell history, and add explicit privacy and retention controls before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yxjsxy/skills/agentmemo-karl)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Evaluation summary](artifact/benchmark/results/eval_summary.md)
- [FastAPI documentation](https://fastapi.tiangolo.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, curl, and Python examples; API responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a running local service and an X-API-Key for protected endpoints.]

## Skill Version(s):

3.2.2 (source: ClawHub release metadata; artifact files also mention 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
