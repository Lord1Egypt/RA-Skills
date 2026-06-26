## Description: <br>
Use Zhipu / BigModel web search as a non-invasive fallback when the built-in web_search route is unavailable, failing, or the user explicitly wants Zhipu / BigModel / GLM search, with direct structured search results and chat-completions search-with-summary across search_std, search_pro, search_pro_sogou, and search_pro_quark. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gxhdky2345](https://clawhub.ai/user/gxhdky2345) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when OpenClaw's built-in web search is unavailable or when a task specifically needs BigModel/Zhipu search. It supports structured search results for agent-written summaries and chat-based search answers for quick synthesis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and chat prompts are sent to BigModel/Zhipu using the configured API key. <br>
Mitigation: Use this skill only where that provider is approved, and do not send secrets, regulated data, or confidential internal content unless approved for the environment. <br>
Risk: Chat mode returns a synthesized answer that may need verification before use. <br>
Mitigation: Review the returned answer and sources before presenting or acting on the result; use raw mode when structured source data is needed for independent summarization. <br>


## Reference(s): <br>
- [Zhipu Web Search Notes](references/api-notes.md) <br>
- [BigModel Web Search API endpoint](https://open.bigmodel.cn/api/paas/v4/web_search) <br>
- [BigModel Chat Completions API endpoint](https://open.bigmodel.cn/api/paas/v4/chat/completions) <br>
- [ClawHub release page](https://clawhub.ai/gxhdky2345/bigmodel-web-search-fallback) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses from the wrapper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The wrapper supports raw structured results and chat-generated answers; users should sanity-check chat output before relying on it.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
