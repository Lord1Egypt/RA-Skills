## Description: <br>
Ensures an agent checks the current session date before answering time-sensitive questions involving today, now, relative dates, current events, prices, rankings, or schedules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dbottrader](https://clawhub.ai/user/dbottrader) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers configuring agents use this skill to make date-sensitive answers and searches reflect the current session date instead of stale training-time assumptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can add an extra status/date tool call before time-sensitive answers. <br>
Mitigation: Apply it to queries involving relative time, current events, prices, rankings, schedules, or similar current-date dependencies. <br>
Risk: If current-date or real-time data cannot be retrieved, answers may be inaccurate. <br>
Mitigation: Tell the user that current-date or real-time data could not be obtained and avoid filling gaps with training-time assumptions. <br>


## Reference(s): <br>
- [Time Awareness on ClawHub](https://clawhub.ai/dbottrader/cp8-time-awareness) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instructional guidance for current-date checks, search query construction, and fallback messaging.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
