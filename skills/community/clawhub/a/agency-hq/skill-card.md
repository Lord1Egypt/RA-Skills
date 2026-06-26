## Description: <br>
Agency HQ is a pixel art dashboard for visualizing AI agent status, activity feeds, and personality-driven banter with OpenClaw live mode or standalone demo data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spockthegreatbot](https://clawhub.ai/user/spockthegreatbot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Agency HQ to monitor an OpenClaw agent team through a visual local dashboard, with demo mode available for showcasing simulated activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can expose real OpenClaw prompts, tool usage, cron activity, and host stats through dashboard endpoints. <br>
Mitigation: Use ARENA_MODE=demo unless live data is explicitly needed; keep live mode local, and add authentication and prompt redaction before any network exposure. <br>
Risk: The documented default mode is inconsistent with the code, which can cause an operator to run live mode unintentionally. <br>
Mitigation: Set ARENA_MODE explicitly for each environment and verify the active mode before sharing or deploying the dashboard. <br>


## Reference(s): <br>
- [Agency HQ ClawHub listing](https://clawhub.ai/spockthegreatbot/agency-hq) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown instructions with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes demo and live dashboard modes for a local Next.js application.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
