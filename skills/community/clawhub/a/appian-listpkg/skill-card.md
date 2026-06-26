## Description: <br>
List all packages for an Appian application by UUID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solarspiker](https://clawhub.ai/user/solarspiker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Appian release engineers use this skill to list packages for a specific Appian application and find package UUIDs before inspection, export, or deployment work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Appian credentials and sends API requests to the configured Appian base URL. <br>
Mitigation: Set APPIAN_BASE_URL and APPIAN_API_KEY explicitly, verify the base URL points to the intended Appian environment, and prefer a least-privileged read-only API key. <br>
Risk: The script can read appian.json from the current working directory or parent directories, which may unintentionally load credentials from an untrusted workspace. <br>
Mitigation: Run the skill from a controlled directory and avoid untrusted workspaces containing appian.json files. <br>


## Reference(s): <br>
- [Appian Package Management API](https://docs.appian.com/suite/help/25.4/Package_Management_API.html) <br>
- [ClawHub skill page](https://clawhub.ai/solarspiker/appian-listpkg) <br>
- [solarspiker ClawHub profile](https://clawhub.ai/user/solarspiker) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance, API calls] <br>
**Output Format:** [Plain text CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Appian application UUID and Appian API credentials.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence and script metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
