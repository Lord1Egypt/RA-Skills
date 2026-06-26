## Description: <br>
Synchronizes Garmin Connect activity data from an international account to a China account using the open-source garminconnect library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucetangc](https://clawhub.ai/user/brucetangc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Garmin users use this skill to authenticate international and China Garmin Connect accounts, list recent activities, test account access, and sync selected FIT activity files from the international account to the China account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Garmin account credentials or tokens and can access personal fitness history. <br>
Mitigation: Use dedicated environment variables, review account scope before first use, and avoid running the skill where other agents or users can read the process environment or token cache. <br>
Risk: Cross-account sync downloads FIT files locally and uploads them to another Garmin account. <br>
Mitigation: Require explicit confirmation before sync operations, check the configured source and destination accounts, and review where cached FIT files and token files are stored. <br>
Risk: Cached FIT files, sync state, and OAuth tokens may remain on disk after use. <br>
Mitigation: Set a controlled sync directory, periodically delete cached data that is no longer needed, and document how to remove stored tokens and FIT files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucetangc/garmin-connect-sync) <br>
- [Publisher profile](https://clawhub.ai/user/brucetangc) <br>
- [python-garminconnect project](https://github.com/cyberjunky/python-garminconnect) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status messages with fenced command output and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands include sync, status, list, and auth-test; sync supports day range and activity count parameters.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
