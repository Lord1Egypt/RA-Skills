## Description: <br>
Daily Life Autopilot helps agents proactively manage daily logistics, including briefings, message triage, follow-ups, bills, files, meetings, and reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AGIstack](https://clawhub.ai/user/AGIstack) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users such as busy professionals, founders, parents, and people returning from time away use this skill to have an agent summarize schedules, triage messages, track follow-ups, monitor bills, prepare meetings, organize files, and review the day or week. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to read and summarize sensitive email, calendar, billing, task, and local file data. <br>
Mitigation: Restrict connected accounts, folders, and integrations where possible, and enable only the data sources needed for the intended workflow. <br>
Risk: Broad automatic briefings and triage can expose more personal information than a user expects. <br>
Mitigation: Disable automatic briefings or make them opt-in until the user has reviewed the connected data scope. <br>
Risk: Actions related to messages, archives, files, or billing can affect personal records or communications. <br>
Mitigation: Keep sending, archiving, file moves, subscription changes, and billing-related actions confirmation-only. <br>


## Reference(s): <br>
- [Daily Life Autopilot on ClawHub](https://clawhub.ai/AGIstack/daily-life-autopilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown briefings, summaries, draft responses, checklists, and action proposals] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended to stay confirmation-gated for message sending, archiving, file moves, and billing-related actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
