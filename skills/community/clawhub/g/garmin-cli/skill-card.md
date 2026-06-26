## Description: <br>
Access Garmin Connect health, fitness, and activity data via a non-interactive CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[voydz](https://clawhub.ai/user/voydz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users can use this skill to query Garmin Connect health, fitness, activity, device, workout, and training data through the gc CLI. It also documents commands for Garmin account actions such as activity upload, workout changes, file output, and raw API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to access Garmin account data and perform account-changing operations, including uploads, workout create/update/delete commands, file output, and raw API POST calls. <br>
Mitigation: Require explicit user approval before any upload, workout mutation, file output, or raw API POST command. <br>
Risk: Authentication examples include Garmin password and MFA arguments that could be exposed in commands, logs, or shared agent transcripts. <br>
Mitigation: Avoid placing Garmin passwords or MFA codes directly in commands, logs, or shared transcripts; use safer interactive or secret-handling flows where available. <br>
Risk: The skill depends on the external garmin-cli Homebrew package and Garmin account access. <br>
Mitigation: Install only after trusting the external package source and confirming the user is comfortable granting Garmin account access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/voydz/garmin-cli) <br>
- [Publisher profile](https://clawhub.ai/user/voydz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands commonly request JSON output from the gc CLI and may write Garmin data or downloaded activity files to disk.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
