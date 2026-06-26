## Description: <br>
Find hotels where breakfast is included in the room rate, using flyai CLI results for current hotel availability, prices, and booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search for hotels that include breakfast, compare live results, and return booking-ready Markdown with verified detail links. It is activated for breakfast-specific hotel queries in English or Chinese. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install the flyai CLI globally before answering hotel queries. <br>
Mitigation: Review and approve the CLI installation path before use; if installation fails, require the user to install it manually rather than continuing with unsourced travel data. <br>
Risk: Travel search details may be sent to the flyai CLI and recorded locally in .flyai-execution-log.json. <br>
Mitigation: Use the skill only when sharing travel search details with the CLI is acceptable, and manage or delete the local execution log if query retention is not desired. <br>
Risk: Hotel prices, availability, or booking links can become stale or misleading if not taken from live CLI results. <br>
Mitigation: Require each user-facing hotel result to come from current flyai CLI output and include a booking detail link; do not answer from model memory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/breakfast-hotel) <br>
- [Parameter and output templates](references/templates.md) <br>
- [Hotel search playbooks](references/playbooks.md) <br>
- [Failure fallbacks](references/fallbacks.md) <br>
- [Execution log runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with hotel comparison tables, booking links, and inline shell commands when setup or retry guidance is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for hotel data; user-facing results should include booking detail links and avoid raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
