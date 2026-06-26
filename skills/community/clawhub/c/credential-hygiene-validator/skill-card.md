## Description: <br>
Checks whether credentials and tokens are stored safely by validating file permissions, plaintext exposure, git contamination, log redaction coverage, and token rotation status for OpenClaw and dotfile directories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Techris93](https://clawhub.ai/user/Techris93) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to audit local credential storage before publishing dotfiles, onboarding a machine, rotating credentials, or performing routine security hygiene checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential scans can expose full local secrets in agent output while inspecting credential files and logs. <br>
Mitigation: Constrain the exact directories to inspect and require redacted output, such as file path, line number, token type, and a short hash or prefix only. <br>


## Reference(s): <br>
- [OpenClaw threat model](https://github.com/openclaw/trust) <br>
- [OpenClaw security policy](https://github.com/openclaw/openclaw/security/policy) <br>
- [RFC 6750 - Bearer Token Usage](https://www.rfc-editor.org/rfc/rfc6750) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only audit guidance; no files modified.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
