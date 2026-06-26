## Description: <br>
Render BestYou health data as visual Dark Glass dashboards via OpenClaw canvas for daily briefings, action plans, progress snapshots, weekly summaries, meal analysis, and workout plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kentsteffen](https://clawhub.ai/user/kentsteffen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External BestYou and OpenClaw users use this skill to fetch BestYou MCP responses and render health coaching data as visual dashboards with brief actionable summaries. It supports daily planning, progress review, meal analysis, workout generation, and setup troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive health insights and a persistent BestYou API key. <br>
Mitigation: Treat the API key like a password: keep configuration private, avoid committing or syncing it, restrict file access where possible, and rotate the key if exposed. <br>
Risk: Write-capable nutrition or workout actions could affect a user's BestYou account. <br>
Mitigation: Ask for confirmation before using write-capable nutrition or workout actions. <br>
Risk: Installation depends on trusting both BestYou and mcporter. <br>
Mitigation: Install only when the user trusts BestYou and mcporter, and verify the configured MCP endpoint before use. <br>


## Reference(s): <br>
- [BestYou OpenClaw Setup](https://bestyou.ai/openclaw-setup) <br>
- [BestYou MCP Endpoint](https://mcp.bestyou.ai/mcp) <br>
- [BestYou MCP Setup Reference](references/setup.md) <br>
- [Security & Privacy](references/security.md) <br>
- [ClawHub Skill Listing](https://clawhub.ai/kentsteffen/bestyou-coach) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, HTML] <br>
**Output Format:** [Self-contained HTML dashboard widgets with concise text summaries, plus markdown setup guidance and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live BestYou MCP responses and static HTML/CSS templates; no local health-data persistence is described.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
