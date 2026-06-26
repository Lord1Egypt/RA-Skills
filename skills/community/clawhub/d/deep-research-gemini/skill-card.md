## Description: <br>
Execute autonomous multi-step research using Google Gemini Deep Research Agent for market analysis, competitive landscaping, literature reviews, technical research, and due diligence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhengxinjipai](https://clawhub.ai/user/zhengxinjipai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and research teams use this skill to launch Gemini-powered research jobs for market analysis, competitive landscaping, literature reviews, technical research, and due diligence, then return reports or structured results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research prompts and outputs are sent to Google Gemini, which can expose sensitive or regulated information. <br>
Mitigation: Use a dedicated API key with limits and avoid sending secrets, regulated data, or confidential information unless approved. <br>
Risk: Gemini API calls can incur usage costs during long-running research tasks. <br>
Mitigation: Set billing or quota limits and confirm that the requested research scope justifies the expected API cost. <br>
Risk: The artifact references an upstream script and requirements that are not included in this release. <br>
Mitigation: Inspect any upstream script and dependency requirements before executing commands from the skill. <br>


## Reference(s): <br>
- [Google AI Studio](https://aistudio.google.com/) <br>
- [ClawHub skill page](https://clawhub.ai/zhengxinjipai/deep-research-gemini) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown reports, JSON, raw API responses, and progress/status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports streaming progress, job status checks, continuation from interaction IDs, and long-running research tasks that require a Gemini API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
