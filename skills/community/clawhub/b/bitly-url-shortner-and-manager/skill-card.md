## Description: <br>
Bitly URL Shortner and Manager helps a local Windows OpenClaw workspace use Bitly credentials to validate auth, inspect account and group details, list, search, filter, export, shorten, expand, and review metrics for Bitly links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanestane](https://clawhub.ai/user/stanestane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Bitly links from a local CLI, including account validation, link creation, bulk shortening, link export, custom aliases, and click metric inspection. It is intended for workflows where sending target URLs to Bitly and storing a local access token are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a local Bitly access token and can read credentials from environment variables or a local env file. <br>
Mitigation: Use a dedicated or least-privileged Bitly token, keep env files outside shared folders with restrictive permissions, and avoid embedding secrets in the skill folder. <br>
Risk: Bulk shortening and export workflows can send confidential, internal, or unintended URLs to Bitly. <br>
Mitigation: Review input URL lists, filters, and export destinations before running commands, and only shorten URLs that are acceptable for the configured Bitly account. <br>


## Reference(s): <br>
- [Bitly API notes](references/api-notes.md) <br>
- [Local env example](references/env-example.md) <br>
- [ClawHub skill page](https://clawhub.ai/stanestane/bitly-url-shortner-and-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, plus CLI output as JSON, CSV, TXT, or local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Bitly access token supplied through environment variables or a local env file outside the skill folder.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
