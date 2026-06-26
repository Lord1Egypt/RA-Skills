## Description: <br>
Track football accumulator (acca) betting slips by parsing slip photo or text, checking live scores every 15 minutes, and reporting each leg's status with overall acca health and cash-out context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[svenmedina07-ship-it](https://clawhub.ai/user/svenmedina07-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to monitor football accumulator betting slips from images, screenshots, or typed text. It helps confirm parsed bet legs, schedule recurring score checks, and summarize whether the accumulator is winning, pending, lost, or complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Betting slip details may contain private wagering information. <br>
Mitigation: Only share slips with agents and environments trusted to process that information, and review or delete local report files on shared machines. <br>
Risk: Recurring score checks may continue after the user no longer needs tracking. <br>
Mitigation: Confirm the parsed slip before tracking starts and use the documented stop-tracking flow when monitoring should end. <br>
Risk: Live score data can be delayed, unavailable, or incomplete for some matches. <br>
Mitigation: Treat reports as tracking assistance, require unavailable scores to be stated explicitly, and avoid guessing outcomes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/svenmedina07-ship-it/acca-tracker) <br>
- [Bet Type Reference](references/bet-types.md) <br>
- [Data Source Strategy](references/data-sources.md) <br>
- [TheSportsDB events day API](https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={today}&s=Soccer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports and confirmation prompts with optional cron scheduling instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recurring score checks may produce local report files until tracking completes or is stopped.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
