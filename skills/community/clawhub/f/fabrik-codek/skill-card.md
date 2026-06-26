## Description: <br>
Fabrik Codek helps an agent use a local personal knowledge base built from work sessions, knowledge graphs, vector search, full-text search, and outcome feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ikchain](https://clawhub.ai/user/ikchain) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to configure and query Fabrik Codek as a local MCP-backed memory and retrieval system for coding context, session knowledge, graph search, and personalized model routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create a persistent local knowledge base from work history and session transcripts, which may include sensitive code, credentials, or conversation history. <br>
Mitigation: Review local transcript and datalake contents before indexing, and avoid indexing secrets or sensitive projects. <br>
Risk: Optional SSE transport can expose indexed data if bound to a public interface. <br>
Mitigation: Keep the default local transport unless SSE is required, bind SSE to localhost, and use firewall or access controls before any broader network exposure. <br>
Risk: The skill relies on upstream Fabrik Codek source and local services outside the skill artifact. <br>
Mitigation: Audit the upstream source before installing and keep Ollama, Meilisearch, and the fabrik command restricted to trusted local environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ikchain/fabrik-codek) <br>
- [Fabrik Codek homepage](https://github.com/ikchain/Fabrik-Codek) <br>
- [Ollama](https://ollama.ai/) <br>
- [Meilisearch](https://meilisearch.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; produces guidance for configuring and using a local MCP server and knowledge base.] <br>

## Skill Version(s): <br>
1.10.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
