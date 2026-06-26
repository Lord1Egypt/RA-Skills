## Description: <br>
Finds the cheapest day to fly within a date range by comparing flight prices day by day through flyai CLI results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-support agents use this skill to compare flexible-date flight options, identify cheaper travel days, and present real-time booking links from flyai CLI output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may direct an agent to install a global third-party npm CLI. <br>
Mitigation: Review the CLI dependency and installation scope before use; prefer a controlled environment where package installation is explicit and approved. <br>
Risk: Travel queries may be stored in local execution logs. <br>
Mitigation: Avoid entering passport numbers, payment details, loyalty account data, or private itinerary details unless logging is clearly user-controlled. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/xiejinsong/flexible-flights) <br>
- [Publisher Profile](https://clawhub.ai/user/xiejinsong) <br>
- [README](README.md) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands when setup or recovery is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results must come from flyai CLI output and include booking links when flight results are shown.] <br>

## Skill Version(s): <br>
v3.2.2 (source: server release metadata; artifact frontmatter remains 3.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
