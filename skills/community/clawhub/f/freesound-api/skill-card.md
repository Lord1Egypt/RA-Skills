## Description: <br>
Set up and use Freesound API access from a local Windows OpenClaw workspace with OAuth login, local credential storage, and sound search helpers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanestane](https://clawhub.ai/user/stanestane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure Freesound credentials locally, complete localhost OAuth login, search sounds, inspect sound metadata, and download originals or previews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Freesound client credentials and OAuth tokens are stored in a local JSON file. <br>
Mitigation: Treat %APPDATA%\OpenClaw\freesound-api\credentials.json as sensitive, avoid committing or syncing it, and rotate the Freesound secret if it is exposed. <br>
Risk: The API key fallback can place the saved Freesound secret in request parameters. <br>
Mitigation: Prefer OAuth login for user-level access and use the query-token fallback only when that behavior is acceptable for the environment. <br>


## Reference(s): <br>
- [Freesound API v2](https://freesound.org/apiv2) <br>
- [ClawHub skill page](https://clawhub.ai/stanestane/freesound-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and PowerShell command examples; helper scripts print JSON, file paths, or status messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper scripts read and write local credential state and may download audio files to a user-selected output directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
