## Description: <br>
Audits local OpenClaw security configuration and runtime exposure across proxy settings, sandbox configuration, Docker port mappings, gateway status, file permissions, workspace symlinks, and listening ports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ASantsSec](https://clawhub.ai/user/ASantsSec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to inspect local OpenClaw deployments and sandboxed development environments for common configuration, exposure, and permission risks. It helps choose focused checks or a full audit and summarizes findings with risk levels and remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit output can expose local paths, file permissions, command output, and sensitive proxy or configuration lines. <br>
Mitigation: Review and redact audit results before sharing them outside the trusted environment. <br>
Risk: The skill runs local read-only commands and file inspections that depend on installed tools, file access, and current user permissions. <br>
Mitigation: Treat missing files, command failures, and permission errors as coverage limits rather than proof that the environment is secure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ASantsSec/ants-openclaw-security-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown audit summaries with structured findings and JSON output from local helper checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local checks can include paths, permissions, command output, and proxy or configuration lines; review results before sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
