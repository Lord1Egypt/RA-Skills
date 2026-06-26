## Description: <br>
Use when Codex needs to operate an llm-wiki knowledge base: ingest source files into Markdown wiki pages, answer questions from wiki/index.md and linked pages, run agent-bridge status/lint/link/relink/merge/query/index tasks, preserve provenance and temporal metadata, or use Zotero as a literature-discovery layer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nemo4110](https://clawhub.ai/user/nemo4110) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to maintain a local Markdown knowledge base: ingesting source materials, preserving provenance and temporal metadata, linking wiki pages, querying distilled knowledge, and running status, lint, merge, index, and retrieval helper commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External embedding or MCP providers can receive wiki content and search queries when enabled. <br>
Mitigation: Review config.yaml before enabling embeddings and prefer local Ollama when wiki content should remain local. <br>
Risk: Broad ingest requests can expose or summarize sensitive repository folders. <br>
Mitigation: Avoid broad ingest requests for sensitive folders and ingest only user-provided files or verified fetched sources. <br>
Risk: Generated merges, lint fixes, or link updates can introduce incorrect wiki content. <br>
Mitigation: Use dry-run previews where available and review diffs before applying merge or lint fixes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nemo4110/041-llm-wiki) <br>
- [Karpathy llm-wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) <br>
- [llm-wiki GitHub repository](https://github.com/Nemo4110/llm-wiki.git) <br>
- [OpenAI Plugins Zotero skill](https://github.com/openai/plugins/tree/main/plugins/zotero/skills/zotero) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, file edits, and generated wiki pages or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local Markdown wiki content, link updates, logs, lint/status reports, and optional embedding index artifacts depending on the requested workflow.] <br>

## Skill Version(s): <br>
1.4.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
