## Description: <br>
Analyzes Garmin Ultimate Frisbee activity and health data so an agent can help review sprints, fatigue, heart-rate zones, recovery, tournament load, and season trends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EvelynDevelops](https://clawhub.ai/user/EvelynDevelops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Garmin users, Ultimate Frisbee players, coaches, and their agents use this skill to fetch activity and health metrics, run analysis scripts, and generate post-game, tournament, training, and season review outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Garmin account credentials and can access sensitive health metrics and activity location history. <br>
Mitigation: Use a short-lived environment value for login, avoid passing or storing GARMIN_PASSWORD in shell profiles or command history, and install only when the publisher is trusted with this account data. <br>
Risk: Session tokens and generated activity files or dashboards may expose private health, route, and performance details if shared or stored insecurely. <br>
Mitigation: Protect ~/.clawdbot/garmin and generated HTML, FIT, GPX, or TCX files with local file permissions, remove stale tokens when access is no longer needed, and avoid uploading dashboards to public locations. <br>
Risk: Generated dashboards load Chart.js assets from cdn.jsdelivr.net when viewed. <br>
Mitigation: Review the generated HTML before opening in sensitive environments, use network controls where required, or adapt the dashboard to use locally hosted chart assets. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/EvelynDevelops/garmin-ultimate-frisbee-analysis) <br>
- [Garmin Connect API Reference](references/api.md) <br>
- [Health Analysis Reference](references/health_analysis.md) <br>
- [Extended Capabilities](references/extended_capabilities.md) <br>
- [MCP Setup Guide](references/mcp_setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON, HTML files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON command output, and generated HTML dashboards] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Garmin health metrics, activity summaries, FIT/GPX/TCX-derived analysis, and local dashboard files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
