## Description: <br>
Enterprise-grade 5-layer agent memory system with routing, scoring, and multi-backend storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laojun509](https://clawhub.ai/user/laojun509) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add persistent memory to production AI agents, including conversation context, task state, user profiles, document retrieval, and experience-based pattern recall. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent agent memory can store private, regulated, or multi-tenant user data. <br>
Mitigation: Use isolated databases, least-privilege credentials, access controls, retention and deletion policies, and sensitive-data redaction before storing production data. <br>
Risk: Stored memory content may preserve prompt-injection text or misleading instructions for later retrieval. <br>
Mitigation: Scan and filter retrieved memory content before prompt injection, and review memory sources before using them in sensitive workflows. <br>
Risk: Incorrect memory routing or importance scoring can surface irrelevant or stale context to an agent. <br>
Mitigation: Tune retrieval thresholds, apply token budgets, monitor memory quality, and allow users or operators to clear or correct stored memory. <br>


## Reference(s): <br>
- [Agent Memory Pro - API Reference](references/api_reference.md) <br>
- [Agent Memory Pro - Usage Examples](references/examples.md) <br>
- [ClawHub release page](https://clawhub.ai/laojun509/agent-memory-enterprise) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration instructions, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-memory integration guidance, API usage examples, configuration patterns, and supporting Python package files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
