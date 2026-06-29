## Description: <br>
Automates MAO-to-CNF flight searches twice daily and sends a WhatsApp report with the cheapest matching one-way flights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andreataide86](https://clawhub.ai/user/andreataide86) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers or operators use this skill to monitor one-way flights from Manaus (MAO) to Belo Horizonte/Confins (CNF) for a fixed August 2026 travel window and receive WhatsApp summaries of the top matching fares. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring WhatsApp reports may send travel search data to the wrong recipient or continue after the trip search is no longer needed. <br>
Mitigation: Confirm the recipient, schedule, and data being sent before enabling the cron job, and disable the job when monitoring is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andreataide86/skills/flight-tracker-bak) <br>
- [Publisher profile](https://clawhub.ai/user/andreataide86) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with scheduled search configuration and WhatsApp reporting details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search criteria include route MAO to CNF, one-way travel from 2026-08-07 to 2026-08-14, maximum 7-hour duration, up to 1 connection, 08:00-16:00 arrival, R$1,000 maximum price, and top 5 cheapest results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
