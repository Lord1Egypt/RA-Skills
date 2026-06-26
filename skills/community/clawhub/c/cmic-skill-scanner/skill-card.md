## Description: <br>
Audits local skill packages or archives with a built-in Rust scanner, with optional delegation to a user-configured external scanner. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyzlmh](https://clawhub.ai/user/cyzlmh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill before installing local skills, archives, or release bundles to run a quick local scan and review findings, completeness, and risk level. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on a local scanner binary that must be trusted before execution. <br>
Mitigation: Build from source when possible, or verify the release checksum before running the binary. <br>
Risk: Optional report upload can send a structured findings report and supplied instance identifier to a configured endpoint. <br>
Mitigation: Leave upload disabled unless the endpoint is intentional and trusted; review the configured upload URL before use. <br>
Risk: Optional external-engine mode delegates scanning to another local tool. <br>
Mitigation: Enable external-engine mode only for a trusted local scanner and review its configuration before use. <br>


## Reference(s): <br>
- [Gitee Releases](https://gitee.com/random_player/cmic-skill-scanner/releases) <br>
- [v0.9.0 SHA256SUMS](https://gitee.com/random_player/cmic-skill-scanner/raw/main/releases/v0.9.0/SHA256SUMS) <br>
- [Source Repository](https://gitee.com/random_player/cmic-skill-scanner.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional local report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional report upload and external-engine behavior are disabled unless explicitly configured.] <br>

## Skill Version(s): <br>
0.9.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
