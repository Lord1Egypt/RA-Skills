## Description: <br>
Sync activities from Garmin China to Garmin Global using local timestamps and distance to avoid duplicates in a one-way sync process. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IamTonyZHOU](https://clawhub.ai/user/IamTonyZHOU) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Garmin users and automation operators use this skill to configure and run a one-way sync of activity files from Garmin China to Garmin Global while avoiding duplicate uploads. <br>

### Deployment Geography for Use: <br>
Global, with functionality specific to Garmin China and Garmin Global account synchronization. <br>

## Known Risks and Mitigations: <br>
Risk: The sync tool stores Garmin credentials locally in plaintext and accepts passwords on the command line. <br>
Mitigation: Use a dedicated or low-risk account when possible, avoid shared shells, keep the credentials file permission-restricted, and delete ~/.config/garmin-sync when no longer using the skill. <br>
Risk: The skill copies Garmin activity data between Garmin accounts and depends on the local garth package used for Garmin API access. <br>
Mitigation: Verify the garth package source and version before use, review the account pairing before syncing, and run an initial sync with a small or low-risk account when practical. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/IamTonyZHOU/garmin-sync-cn-to-global) <br>
- [Publisher profile](https://clawhub.ai/user/IamTonyZHOU) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command-line setup and sync instructions; the bundled script may print progress, retry, status, and failure summaries during execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
