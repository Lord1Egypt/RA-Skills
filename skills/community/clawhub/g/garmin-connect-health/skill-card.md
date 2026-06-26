## Description: <br>
Fetch health and fitness data from Garmin Connect -- 40+ metrics including sleep, HRV, stress, body battery, SpO2, VO2 Max, training status, and activities. Stores data locally as JSON and SQLite. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dw1161](https://clawhub.ai/user/dw1161) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an AI agent retrieve, cache, and query their own Garmin Connect health and fitness data for personal health, recovery, and training analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Garmin credentials or OAuth tokens can expose sensitive account access if stored or passed insecurely. <br>
Mitigation: Use macOS Keychain or a credentials file with mode 600 instead of command-line passwords, and keep the token cache in a private directory. <br>
Risk: Local JSON snapshots and SQLite databases can retain sensitive health history on disk. <br>
Mitigation: Store GARMIN_DATA_DIR in a private directory and periodically delete cached health and token files when retention is no longer needed. <br>
Risk: Using the wrong Garmin regional endpoint can cause unreliable access or rate-limit errors. <br>
Mitigation: Set GARMIN_IS_CN=true or use the --cn flag for China-registered accounts or mainland China network locations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dw1161/garmin-connect-health) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [python-garminconnect](https://github.com/cyberjunky/python-garminconnect) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Markdown guidance, shell commands, JSON snapshots, and SQLite data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local daily JSON snapshots, latest.json, a SQLite database, and an OAuth token cache unless paths are overridden.] <br>

## Skill Version(s): <br>
1.0.11 (source: frontmatter, skill.json, changelog, released 2026-05-31) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
