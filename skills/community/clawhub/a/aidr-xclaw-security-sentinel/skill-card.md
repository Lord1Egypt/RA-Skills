## Description: <br>
AIDR-XClaw-Security-Sentinel audits OpenClaw agent messages and skills for prompt-injection, sensitive-data, and malicious-code risks using local masking, device fingerprinting, API-key authentication, and remote security analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhz292](https://clawhub.ai/user/zhz292) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators of OpenClaw-based agents use this skill to audit user messages, skill installation, and skill runtime behavior before execution. It is intended to help detect prompt injection, credential exposure, data leakage, and malicious skill behavior while producing staged security reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently changes agent instructions during initialization. <br>
Mitigation: Run it only in an isolated test environment first and review the exact AGENTS.md diff before applying it to a normal or production OpenClaw environment. <br>
Risk: The skill sends device, message, and skill data to a remote security service. <br>
Mitigation: Verify the remote service provenance, require explicit consent before raw skill uploads, and confirm organizational approval for sharing this data. <br>
Risk: The workflow depends on API keys, device fingerprints, and sensitive credential handling. <br>
Mitigation: Use administrator review, protect local state files, and validate that credentials are handled according to the documented masking and authentication flow. <br>
Risk: Security guidance flags the need for preserved TLS verification and a clear rollback path. <br>
Mitigation: Prefer a release that preserves TLS verification and document rollback steps before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhz292/aidr-xclaw-security-sentinel) <br>
- [Publisher profile](https://clawhub.ai/user/zhz292) <br>
- [API endpoint reference](artifact/references/api-reference.md) <br>
- [Desensitization rules reference](artifact/references/desensitization-rules.md) <br>
- [Fingerprint algorithm reference](artifact/references/fingerprint-algorithm.md) <br>
- [Security quick reference](artifact/SecurityQuickRef.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown security reports with staged status blocks and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local state and agent configuration files during initialization.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
