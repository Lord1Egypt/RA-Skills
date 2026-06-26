## Description: <br>
Guide users to configure local Chanjing credentials safely via local commands only, and validate local token status when needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binkes](https://clawhub.ai/user/binkes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up and check local Chanjing AK/SK credentials and access tokens before running Chanjing API workflows. It keeps secret handling in local commands and credential files instead of asking users to paste secrets into chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live Chanjing AK/SK values and access tokens stored on disk. <br>
Mitigation: Keep credentials in the local credentials file only, do not paste keys or tokens into chat, and rotate credentials if they appear in shell history, logs, or shared backups. <br>
Risk: Overriding the Chanjing API base URL can redirect token requests away from the default service. <br>
Mitigation: Leave CHANJING_OPENAPI_BASE_URL and CHANJING_API_BASE unset unless intentionally using a verified Chanjing HTTPS endpoint. <br>
Risk: The scanner verdict is suspicious because the helper handles secrets and has under-scoped token and environment controls. <br>
Mitigation: Review before installation, restrict file permissions on the credentials directory, and install only when the publisher and intended Chanjing workflow are trusted. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/binkes/chanjing-credentials-guard) <br>
- [Credentials Guard Reference](reference.md) <br>
- [Chanjing documentation](https://doc.chanjing.cc) <br>
- [Chanjing OpenAPI login](https://www.chanjing.cc/openapi/login) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands and local configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May open a browser for Chanjing login and may print local token status or a valid access token when the user runs the bundled scripts.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
