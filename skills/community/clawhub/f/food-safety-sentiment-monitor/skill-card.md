## Description:

Monitors food safety sentiment on Chinese social platforms, detects negative events, grades risks, and generates PR response plans and reports.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[stylemonster](https://clawhub.ai/user/stylemonster)

### License/Terms of Use:

MIT-0

## Use Case:

Food safety, restaurant operations, and communications teams can use this skill to monitor Chinese social-platform sentiment, triage potential negative events, and draft response materials. The current release should be treated as a demo/test monitor because server security evidence says it can present simulated allegations and fixed crisis statements as analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Simulated allegations and fixed crisis statements may be mistaken for verified food safety analysis.

Mitigation: Do not publish or act on generated allegations or PR statements without independent verification and human communications review.

Risk: Browser automation and optional API configuration can affect where data is collected from and how analysis is generated.

Mitigation: Review the Playwright install path and any Minimax/OpenClaw API configuration before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stylemonster/skills/food-safety-sentiment-monitor)
- [Publisher profile](https://clawhub.ai/user/stylemonster)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Console text and markdown-style response plans, with JavaScript code and configuration files in the artifact]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use Playwright browser automation and optional Minimax/OpenClaw API configuration; defaults can fall back to simulated monitoring results.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
