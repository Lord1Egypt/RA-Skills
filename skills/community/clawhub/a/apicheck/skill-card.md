## Description: <br>
Apicheck helps agents prepare API requests, curl commands, mock data, API documentation, HTTP status-code explanations, and header guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and API practitioners use Apicheck to draft request payloads, generate curl examples, create mock data, write API documentation, and look up HTTP status-code or header guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated curl commands or API examples may include sensitive values if a user supplies tokens, keys, or credentials. <br>
Mitigation: Review generated commands before running them and avoid passing secrets as command arguments. <br>
Risk: The release includes an unrelated workflow-style shell script that records command arguments in a local Apicheck history file. <br>
Mitigation: Avoid invoking that script with sensitive arguments, and check or clear the local Apicheck history file when needed. <br>
Risk: The server security verdict is suspicious because the package combines a static API helper with the unrelated local-history behavior. <br>
Mitigation: Install only after reviewing the shipped shell scripts and confirming the behavior is acceptable for the target environment. <br>


## Reference(s): <br>
- [Apicheck on ClawHub](https://clawhub.ai/xueyetianya/apicheck) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [API Tester reference document](artifact/tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with code blocks, curl commands, API documentation tables, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include executable shell commands and sample credentials placeholders that users should review before use.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
