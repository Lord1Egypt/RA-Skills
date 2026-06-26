## Description: <br>
Prompt injection and malware detection filter for external content. Scans text, files, or URLs for 20+ attack patterns including instruction overrides, credential exfiltration, persona hijacking, encoded payloads, fake system messages, and invisible character injection. Returns JSON with risk level and sanitized text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BryanTegomoh](https://clawhub.ai/user/BryanTegomoh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill as a defensive pre-check before processing external text, files, stdin, or selected URLs, so potentially malicious prompt-injection and malware-like patterns can be identified and handled before downstream use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A SAFE result does not prove that content is fully harmless. <br>
Mitigation: Use the skill as a defensive pre-check and continue applying normal review before trusting or executing external content. <br>
Risk: Scan output can include private or sensitive source text. <br>
Mitigation: Avoid sharing JSON reports when they contain private text, credentials, or confidential content. <br>
Risk: URL scanning fetches remote content selected by the operator. <br>
Mitigation: Only scan URLs that were intentionally chosen for review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BryanTegomoh/content-security-filter) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [JSON report with risk level, findings, sanitized text, and character count] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit code 0 indicates no detected threat; exit code 1 indicates a detected threat.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
