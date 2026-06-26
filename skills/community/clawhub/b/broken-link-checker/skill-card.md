## Description: <br>
Verifies external HTTP and HTTPS URLs for availability using 200-399 status codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanng-ide](https://clawhub.ai/user/wanng-ide) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and documentation maintainers use this skill to check whether one or more external documentation or reference links are reachable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes network requests to every URL supplied by the user, which may expose or probe private, internal, or sensitive addresses. <br>
Mitigation: Use it only with URLs intended for checking, and avoid internal or sensitive addresses unless that access is explicitly desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wanng-ide/broken-link-checker) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON array printed to standard output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Each result reports the URL, whether it was valid, and either an HTTP status code or an error message.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
