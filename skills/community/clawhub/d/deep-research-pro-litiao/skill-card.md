## Description: <br>
Multi-source deep research agent that searches the web, synthesizes findings, and delivers cited reports using Tavily API when available or DuckDuckGo as a fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and research-focused agents use this skill to plan multi-query web research, read selected sources, synthesize cited findings, and save or deliver structured reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries and fetched pages may be sent to external search providers or websites. <br>
Mitigation: Avoid confidential, internal, or regulated topics unless those data flows are approved. <br>
Risk: The skill can save generated research reports to local files. <br>
Mitigation: Review output paths and local persistence expectations before use. <br>
Risk: Documentation is inconsistent about whether Tavily API access is required or optional. <br>
Mitigation: Decide whether to provide TAVILY_API_KEY; otherwise expect the DuckDuckGo fallback path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/litiao1224/deep-research-pro-litiao) <br>
- [Publisher profile](https://clawhub.ai/user/litiao1224) <br>
- [Tavily](https://tavily.com) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [uv](https://github.com/astral-sh/uv) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with citations, source lists, methodology notes, and optional saved files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use external search providers and fetch web pages; reports may be saved locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
