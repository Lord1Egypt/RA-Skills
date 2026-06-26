## Description: <br>
Autonomous deep research agent with multi-step web search, sub-agent delegation, and structured report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lingchenheiye](https://clawhub.ai/user/lingchenheiye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, researchers, and other external users use this skill to perform comprehensive multi-source research, literature reviews, market research, competitive analysis, and comparison reports with citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics, URLs, and fetched page content may be sent to Tavily and the selected LLM provider. <br>
Mitigation: Use the skill only for data that can be shared with those providers, and review provider settings and policies before use. <br>
Risk: Generated /research_request.md and /final_report.md files may contain sensitive research content. <br>
Mitigation: Review generated files before sharing, committing, or storing them in shared locations. <br>
Risk: External API calls may consume paid quota or create unexpected usage costs. <br>
Mitigation: Monitor Tavily and LLM provider usage, set appropriate quotas, and configure search depth before long research sessions. <br>
Risk: The backend installs Python dependencies and fetches external web content. <br>
Mitigation: Run the backend in a dedicated virtual environment or sandbox and keep dependencies reviewed before deployment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/lingchenheiye/deep-research-engine) <br>
- [Tavily](https://tavily.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown research reports with inline citations, source lists, and optional shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The Python backend writes /research_request.md and /final_report.md; output depends on Tavily and the selected LLM provider.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
