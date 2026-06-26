## Description: <br>
Deep Research guides an agent through iterative web search, page reading, gap analysis, and synthesis to produce well-sourced Markdown research reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangsjt](https://clawhub.ai/user/yangsjt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users can use this skill to turn complex research questions into structured, citation-rich Markdown briefings using available web search and page-fetch tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The standalone script grants broad automatic Gemini CLI permissions. <br>
Mitigation: Prefer the SKILL.md workflow with normal platform search and fetch tools, or review and constrain the script before running it. <br>
Risk: Background execution behavior needs review before unattended use. <br>
Mitigation: Avoid the background mode until the shell construction is fixed, and run the script in the foreground where output can be inspected. <br>
Risk: Sensitive research questions may be sent through the Gemini-based script or an intentionally started local search fallback. <br>
Mitigation: Do not paste sensitive internal research questions into the script, and only run the Docker fallback when a local SearXNG service is intended. <br>


## Reference(s): <br>
- [Research Methodology Reference](references/research-methodology.md) <br>
- [Deep Research repository](https://github.com/yangsjt/deep-research.git) <br>
- [OpenClaw](https://github.com/anthropics/openclaw) <br>
- [Gemini CLI](https://github.com/google-gemini/gemini-cli) <br>
- [SearXNG](https://github.com/searxng/searxng) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown research report with inline citations and a source list] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Matches the user's prompt language when generating the report.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
