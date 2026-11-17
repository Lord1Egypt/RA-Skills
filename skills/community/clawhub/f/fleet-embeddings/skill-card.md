## Description:

Fleet Embeddings helps agents generate and batch embeddings across an Ollama device fleet for RAG, semantic search, knowledge-base creation, and vector similarity workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up fleet-routed text embedding workflows for RAG indexes, semantic search, duplicate detection, recommendations, and vector similarity tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unpinned Python package may introduce unexpected dependency or package changes.

Mitigation: Install in a virtual environment and pin or review the `ollama-herd` package before use.

Risk: Embedding requests may route documents or prompts to any device fleet node.

Mitigation: Only send content to the fleet when every node that may process it is trusted.

Risk: Model pull or delete commands can change local model availability and storage usage.

Mitigation: Require user confirmation before allowing an agent to pull or delete models.

Risk: Skill guidance references files under `~/.fleet-manager/` that may contain operational state or logs.

Mitigation: Do not delete or modify files in `~/.fleet-manager/`.

## Reference(s):

- [Fleet Embeddings ClawHub page](https://clawhub.ai/twinsgeeks/skills/fleet-embeddings)
- [ollama-herd Python package](https://pypi.org/project/ollama-herd/)
- [ollama-herd project homepage](https://github.com/geeks-accelerator/ollama-herd)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)
- [Request Tagging Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/request-tagging-analytics.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash, Python, and HTTP API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local API endpoints, model suggestions, setup commands, monitoring commands, and guardrails for file and model operations.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
