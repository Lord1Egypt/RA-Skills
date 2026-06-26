## Description: <br>
Extract structured learnings (lessons, decisions, patterns, dead ends) from AI conversation exports using a local Ollama model or any OpenAI-compatible API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djc00p](https://clawhub.ai/user/djc00p) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to analyze exported AI conversation histories and extract reusable lessons, decisions, patterns, and dead ends into semantic memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive conversation content may be sent to a configured OpenAI-compatible API when OPENAI_API_KEY or OPENAI_BASE_URL is set. <br>
Mitigation: Use the default local Ollama mode for sensitive exports, or only configure a remote endpoint after confirming the provider is acceptable for the data. <br>
Risk: The skill writes extracted learnings to workspace memory files and tracks processed chat IDs. <br>
Mitigation: Run with --dry-run or --limit first to inspect behavior before allowing writes to the workspace. <br>


## Reference(s): <br>
- [Chat Learnings Extractor on ClawHub](https://clawhub.ai/djc00p/chat-learnings-extractor) <br>
- [Publisher Profile](https://clawhub.ai/user/djc00p) <br>
- [Prompt Template](references/prompt-template.md) <br>
- [chat-history-importer](https://clawhub.ai/djc00p/chat-history-importer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown appended to memory/semantic/learnings-from-exports.md, with optional command-line output during dry runs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can process OpenAI or Anthropic JSON conversation exports, deduplicate processed chats, and use either local Ollama or an OpenAI-compatible chat completions endpoint.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
