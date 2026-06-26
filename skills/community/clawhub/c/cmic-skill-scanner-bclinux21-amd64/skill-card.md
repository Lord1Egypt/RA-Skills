## Description: <br>
使用内置 Rust 引擎审计待安装的 skill 包或归档，并可选桥接外部 scanner。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyzlmh](https://clawhub.ai/user/cyzlmh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run a local Rust-based scan of skill packages, archives, or release bundles before installation. It helps review engine findings, risk level, and installation readiness before trusting a package. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's main risk is the expected need to download and run a scanner binary. <br>
Mitigation: Install only from a trusted release source, verify the documented SHA-256 checksum before running the binary, or build the scanner from source. <br>
Risk: Optional upload and external-scanner modes add behavior beyond the default local scan. <br>
Mitigation: Keep upload and external-scanner modes disabled unless deliberately configured, and scan only intended skill directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyzlmh/cmic-skill-scanner-bclinux21-amd64) <br>
- [Cisco Skill Scanner](https://github.com/cisco-ai-defense/skill-scanner.git) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and local scan findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write local scan reports when an output directory is configured.] <br>

## Skill Version(s): <br>
0.9.0 (source: server release metadata; binary build v0.9.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
