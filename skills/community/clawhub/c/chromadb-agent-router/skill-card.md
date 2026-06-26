## Description: <br>
Local semantic message routing for multi-agent systems using embeddings, keyword scoring, and context scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mars375](https://clawhub.ai/user/mars375) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route messages to specialized local agents in multi-agent systems. It is especially suited to local French/English intent routing where external API calls are not desired. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Python dependencies are unpinned in the release metadata. <br>
Mitigation: Install in an isolated environment and review resolved package versions before use. <br>
Risk: The ChromaDB embedding stack may download a model during first use. <br>
Mitigation: Run the first initialization in a network environment and cache location that match local policy. <br>
Risk: Route descriptions and routed messages can expose sensitive operational intent. <br>
Mitigation: Keep route descriptions free of secrets and ensure downstream agents enforce their own approval gates for deploy, install, and security-sensitive actions. <br>


## Reference(s): <br>
- [Routing Research Notes](artifact/references/ROUTING-RESEARCH.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/mars375/chromadb-agent-router) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python, JSON, and shell command examples; the router API returns JSON route decisions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run locally with ChromaDB and numpy; optional REST API usage requires Starlette and Uvicorn.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
