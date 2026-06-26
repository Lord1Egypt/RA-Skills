## Description: <br>
Deep web research across 11 Chinese and international sources (Baidu, Bing, Sogou, Quark, ChinaSo, WeChat, Yandex, Zhihu, Bilibili, V2EX, GitHub). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nb-clh](https://clawhub.ai/user/nb-clh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to run multi-source web research, especially for Chinese platforms such as Zhihu, Bilibili, and WeChat, and receive synthesized answers with evidence tables, sources, confidence, and contradiction notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research questions are sent to a local Agentic RAG-CN service on localhost:18888, whose logging, storage, and forwarding behavior is outside the skill artifact. <br>
Mitigation: Install and use the skill only with a local service you run or trust, and avoid secrets, credentials, proprietary material, or regulated personal data unless that service's handling is understood. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/nb-clh/agentic-rag-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with evidence tables, source lists, contradiction notes, and optional shell/API commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted local Agentic RAG-CN API on localhost:18888; falls back to built-in web search when unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
