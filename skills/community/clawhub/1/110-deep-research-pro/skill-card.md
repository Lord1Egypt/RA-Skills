## Description: <br>
Multi-source deep research agent. Searches the web, synthesizes findings, and delivers cited reports. No API keys required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallkeyboy](https://clawhub.ai/user/smallkeyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to plan and run multi-source web research, deep-read selected pages, and produce cited reports for learning, decisions, or writing tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries, fetched URLs, and visited pages may disclose sensitive topics to external search or website services. <br>
Mitigation: Avoid confidential topics unless external web access is acceptable, and review or narrow queries and URLs before running research. <br>
Risk: Generated research reports may persist on local disk after the session. <br>
Mitigation: Use non-sensitive output locations, review saved report contents, and remove local reports when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/smallkeyboy/110-deep-research-pro) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [uv package manager](https://github.com/astral-sh/uv) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports with citations; optional JSON output for CLI-style research results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save reports under ~/clawd/research/[slug]/report.md and fetch external web pages during research.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
