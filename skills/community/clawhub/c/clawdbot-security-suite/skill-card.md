## Description: <br>
Advanced security validation for Clawdbot - pattern detection, command sanitization, and threat monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gtrusler](https://clawhub.ai/user/gtrusler) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to validate commands, URLs, file paths, and external content before execution or processing in Clawdbot workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional automatic hook has review-worthy behavior: it shells out with user-controlled arguments and fails open. <br>
Mitigation: Prefer manual validation first, and enable the hook only after reviewing its shell invocation and fail-open behavior. <br>
Risk: Local logs may retain sensitive commands, URLs, paths, and tool arguments. <br>
Mitigation: Treat security logs as sensitive, restrict access to them, and avoid passing secrets through logged inputs. <br>
Risk: An ALLOWED result can be over-trusted for destructive or privileged operations. <br>
Mitigation: Continue to require normal user approval and review before running destructive or privileged commands. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/gtrusler/clawdbot-security-suite) <br>
- [README](README.md) <br>
- [Security Skill Reference](skills/security/SKILL.md) <br>
- [Installation Guide](skills/security/INSTALL.md) <br>
- [Agent Integration Guide](skills/security/CLAWDBOT-INSTRUCTIONS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration snippets, and command-line validation output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash and jq; optional hooks can produce local security event logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
