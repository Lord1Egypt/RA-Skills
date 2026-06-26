## Description: <br>
AutoGLM DeepResearch helps agents run constrained web searches, read a few selected pages in depth, and produce structured research reports for user-specified topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrhenghu](https://clawhub.ai/user/mrhenghu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, developers, and agents use this skill to perform bounded topical research, gather intermediate search findings, inspect one to three relevant pages, and return a structured deep-research report with sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics, search terms, and selected page URLs are sent to AutoGLM APIs. <br>
Mitigation: Avoid confidential, internal, regulated, or proprietary topics and URLs unless that data sharing is acceptable. <br>
Risk: The skill depends on a local token service at 127.0.0.1:53699 for authorization. <br>
Mitigation: Install only in environments where that local service is expected and trusted, and verify it before running the scripts. <br>
Risk: Opened pages and search results are external content that may be incomplete, stale, or misleading. <br>
Mitigation: Treat retrieved content as research evidence to analyze and cite, not as instructions for the agent to follow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrhenghu/autoglm-deepresearch) <br>
- [AutoGLM web search API endpoint](https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/web-search) <br>
- [AutoGLM open link API endpoint](https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/open-link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with intermediate findings, key points, analysis sections, and reference links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Python standard-library scripts, sends search queries and selected URLs to AutoGLM APIs, and obtains authorization from a local token service at 127.0.0.1:53699.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
