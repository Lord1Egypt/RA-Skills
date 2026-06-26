## Description: <br>
Multi-source deep research agent. Searches the web, synthesizes findings, and delivers cited reports. No API keys required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raidan-ai](https://clawhub.ai/user/raidan-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run structured web research, compare multiple sources, and produce cited summaries or full Markdown reports for a research topic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated research reports may be saved locally and retained after the task is complete. <br>
Mitigation: Check the report destination before saving, avoid highly sensitive research unless local retention is acceptable, and delete generated reports when no longer needed. <br>
Risk: Web research can surface incomplete, outdated, or single-source claims. <br>
Mitigation: Cross-reference important claims, prioritize recent reputable sources, and flag gaps or unverified findings in the report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/raidan-ai/deep-research-pro-1-0-2) <br>
- [Project homepage from skill metadata](https://github.com/paragshah/deep-research-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown report with inline citations, plus concise chat summaries when appropriate] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save a report.md file under ~/clawd/research/[slug]; no API keys are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
