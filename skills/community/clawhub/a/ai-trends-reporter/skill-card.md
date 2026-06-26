## Description: <br>
Ai Trends Reporter generates structured AI trend reports and ClawHub skill recommendations using Brave Search and ClawHub search signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LiXingxun](https://clawhub.ai/user/LiXingxun) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and ClawHub users use this skill to produce daily, weekly, or topic-focused AI news reports and discover relevant uninstalled ClawHub skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may reveal the user's installed OpenClaw skills or tooling when shared. <br>
Mitigation: Review generated reports before sharing and remove local tooling details that should remain private. <br>
Risk: The skill depends on external search and ClawHub data, so report contents can be incomplete or time-sensitive. <br>
Mitigation: Treat generated reports as a starting point and verify important news, rankings, and installation recommendations before relying on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/LiXingxun/ai-trends-reporter) <br>
- [Brave Search API](https://brave.com/search/api/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with optional shell command and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports daily, weekly, and topic-focused reports with adjustable recommendation counts; Brave Search requires BRAVE_API_KEY, and CLAWHUB_TOKEN is optional.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
