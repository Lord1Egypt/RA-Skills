## Description: <br>
Real-time supervisor and control interface for the DRADIS Polymarket high-frequency trading engine. Full support for DRADIS_API_KEY authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mbordash](https://clawhub.ai/user/mbordash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to monitor a DRADIS Polymarket trading engine, inspect portfolio and position state, and request approved changes to live strategy parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can view trading data and change live DRADIS strategy settings. <br>
Mitigation: Install only for DRADIS trading engines you control and review every proposed PATCH before approving it. <br>
Risk: A reused or overprivileged DRADIS_API_KEY could expand the impact of an agent or configuration mistake. <br>
Mitigation: Use a dedicated least-privilege API key and point DRADIS_API_URL only at a trusted instance. <br>


## Reference(s): <br>
- [DRADIS project repository](https://github.com/mbordash/DRADIS) <br>
- [ClawHub skill page](https://clawhub.ai/mbordash/dradis-tactical-command) <br>
- [Publisher profile](https://clawhub.ai/user/mbordash) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration, shell commands, text] <br>
**Output Format:** [Markdown and structured API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live trading status, portfolio summaries, position data, and human-confirmed configuration updates.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata and artifact SKILL.md heading) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
