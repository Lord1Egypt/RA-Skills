## Description: <br>
ClawGuard audits ClawHub skill folders locally and reports PASS, WARN, or FAIL findings for prompt-injection, exfiltration, shell-injection, permission, endpoint, and structure risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Taha2053](https://clawhub.ai/user/Taha2053) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use ClawGuard before installing or publishing ClawHub skills to inspect local skill files and review security findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A PASS verdict can be mistaken for proof that another skill is safe. <br>
Mitigation: Treat ClawGuard as a lightweight screening tool and manually review high-impact skills and any findings before installation. <br>
Risk: The documentation describes broader checks than the implementation may fully cover. <br>
Mitigation: Use the report as decision support, not as a complete security audit, and validate important claims against the scanned files. <br>
Risk: Running an unexpected scan.py path could audit the wrong files. <br>
Mitigation: Verify the installed ClawGuard path and target skill directory before running scans. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Taha2053/claw-guard) <br>
- [Publisher profile](https://clawhub.ai/user/Taha2053) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown-style terminal report or JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes PASS, WARN, or FAIL verdicts with finding severity, location, and recommendation details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
