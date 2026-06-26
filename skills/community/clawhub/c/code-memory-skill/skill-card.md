## Description: <br>
Use when doing coding work in a Git repository and semantic code search, AST-aware symbol lookup, documentation search, Git-history search, or dead-code discovery would help. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimdawdy-hub](https://clawhub.ai/user/jimdawdy-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to decide when and how to run the code-memory MCP server for local repository indexing, semantic code search, documentation search, Git-history lookup, and dead-code candidate discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local indexes can contain source excerpts, embeddings, file paths, and Git-derived data from repositories. <br>
Mitigation: Index only repositories appropriate for local storage, keep sensitive files ignored before indexing, and avoid committing or sharing code_memory.db files. <br>
Risk: Package and model artifacts are fetched during install or first run, and the default embedding model may execute model code. <br>
Mitigation: For sensitive environments, vet or pin package and model artifacts, or use a trusted local model through EMBEDDING_MODEL. <br>
Risk: The SSE transport is unauthenticated if exposed beyond the local machine. <br>
Mitigation: Keep SSE bound to 127.0.0.1 unless it is protected by an authenticated reverse proxy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jimdawdy-hub/code-memory-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with shell and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides local MCP server installation, configuration, indexing workflow, and security precautions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
