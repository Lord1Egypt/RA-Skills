## Description: <br>
Fleet Embeddings helps agents generate text embeddings for RAG, semantic search, vector similarity, duplicate detection, and recommendation workflows through a local Ollama fleet router. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up and call local fleet-routed embedding endpoints for knowledge bases, RAG indexes, semantic search, duplicate detection, and recommendation systems. It provides setup guidance, curl requests, Python examples, and operational guardrails for Ollama Herd embeddings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Embedding text, prompts, tags, audio, image, or transcription requests may move through trusted fleet nodes and appear in local logs or dashboards. <br>
Mitigation: Use trusted fleet nodes, avoid sensitive request content and tags, and review local logging and dashboard exposure before use. <br>
Risk: The skill guides use of a local fleet service on port 11435 and optional model pulls or feature endpoints. <br>
Mitigation: Install and run Ollama Herd only in environments where a local fleet router is acceptable, and confirm before pulling models or enabling optional image or transcription features. <br>
Risk: Fleet manager configuration and log files under ~/.fleet-manager/ affect local routing state and operational history. <br>
Mitigation: Do not delete or modify ~/.fleet-manager/ files unless the user explicitly asks and understands the local service impact. <br>


## Reference(s): <br>
- [Fleet Embeddings on ClawHub](https://clawhub.ai/twinsgeeks/fleet-embeddings) <br>
- [ollama-herd package](https://pypi.org/project/ollama-herd/) <br>
- [ollama-herd repository](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>
- [Request Tagging Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/request-tagging-analytics.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash, Python, JSON, and local HTTP API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local Ollama Herd API calls, package installation, router startup commands, and model-pull commands; model pulls should be confirmed by the user.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata; artifact frontmatter states 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
