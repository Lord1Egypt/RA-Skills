## Description: <br>
Security scanner for OpenClaw skills that detects suspicious patterns before execution, assigns risk scores, and supports file integrity checks through static analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ParthGhumatkar](https://clawhub.ai/user/ParthGhumatkar) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security reviewers use this skill to audit installed OpenClaw skills before execution, identify risky patterns, and generate risk scores or SHA256 inventories for local review and CI checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reads installed skill files and may report local paths, hashes, and risk flags that are sensitive in some environments. <br>
Mitigation: Keep scan roots limited to directories intended for audit and avoid sharing full scan output unless paths and hashes are safe to disclose. <br>
Risk: Static, pattern-based scanning can miss runtime behavior or flag legitimate code as suspicious. <br>
Mitigation: Use results as one review signal alongside manual code review, trusted-source checks, and runtime controls for high-risk skills. <br>


## Reference(s): <br>
- [Claw-lint ClawHub page](https://clawhub.ai/ParthGhumatkar/claw-lint) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Terminal table output or JSON scan results with optional SHA256 file inventory.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports filtering by skill name, minimum risk score, strict mode, and scan byte limits; JSON output requires Python 3.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
