## Description: <br>
Fitbit fitness data integration for querying activity, heart rate, sleep, workout, and trend data and turning those metrics into conversational insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poisondminds](https://clawhub.ai/user/poisondminds) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users with Fitbit accounts use this skill to ask natural language questions about activity, sleep, heart rate, workouts, and fitness trends. The agent fetches relevant Fitbit data and summarizes patterns, goals, and recent metrics in conversational form. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests persistent access to sensitive Fitbit activity, sleep, heart-rate, workout, and profile data. <br>
Mitigation: Use read-only Fitbit scopes, install only when that access is acceptable, and revoke the Fitbit app tokens when the skill is no longer needed. <br>
Risk: OAuth tokens and client secrets are stored in a local configuration file. <br>
Mitigation: Protect the config file with restrictive permissions and avoid pasting tokens or secrets into chats, logs, or shared files. <br>
Risk: The release evidence flags incomplete credential/privacy safeguards and missing helper scripts that should be verified. <br>
Mitigation: Review the installed helper scripts from a trusted source before use and confirm the skill only performs the expected read-only Fitbit API calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/poisondminds/fitbit-insights) <br>
- [Fitbit developer apps](https://dev.fitbit.com/apps) <br>
- [Fitbit Web API reference](https://dev.fitbit.com/build/reference/web-api/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Conversational Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided Fitbit OAuth credentials and read-only Fitbit API scopes; results depend on available Fitbit account data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and CLAWHUB-SUBMISSION.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
