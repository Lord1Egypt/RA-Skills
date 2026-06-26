## Description: <br>
Extract calendar events from Microsoft Exchange via EWS API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[basuev](https://clawhub.ai/user/basuev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and developers use this skill to retrieve Microsoft Exchange calendar events for a requested date and return subjects, times, locations, organizers, body text, and links as structured JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calendar bodies, locations, organizers, and extracted links can contain sensitive personal or business information. <br>
Mitigation: Run the skill only against trusted Exchange endpoints and keep JSON output or debug XML out of shared, synced, or source-controlled locations. <br>
Risk: Exchange credentials are required and standalone use can rely on environment variables or a .env file. <br>
Mitigation: Use the keyring wrapper for normal operation, avoid command-line passwords and plaintext .env files, and rotate or delete stored credentials when access changes. <br>
Risk: Debug XML may include raw Exchange response content. <br>
Mitigation: Enable debug XML only for troubleshooting and delete debug files after use. <br>


## Reference(s): <br>
- [ClawHub EWS Skill release](https://clawhub.ai/basuev/ews-skill) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON array of calendar event objects, with optional file output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EWS_URL and EWS_USER configuration, curl and xmllint, and macOS Keychain or Linux libsecret for password retrieval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
