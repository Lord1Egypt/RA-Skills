## Description: <br>
Audits local skill packages or archives with a bundled Rust scanner engine and can optionally bridge to an external scanner. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyzlmh](https://clawhub.ai/user/cyzlmh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill before installing local skill packages, archives, or release bundles to inspect scanner findings, review risk level, and make a concise installation decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A bundled or downloaded scanner binary requires trust in the release host and checksum integrity. <br>
Mitigation: Verify the SHA-256 checksum before execution or build the scanner from source when higher assurance is required. <br>
Risk: Optional report upload can disclose sensitive project or security review details if sent to an untrusted endpoint. <br>
Mitigation: Use local review mode by default and configure --upload-url only for approved HTTPS endpoints. <br>
Risk: External scanner mode delegates work to user-configured local tooling. <br>
Mitigation: Enable --engine external only for trusted scanner commands whose behavior has been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyzlmh/cmic-skill-scanner-linux-arm64) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports and command-line review output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write local scan reports when an output directory is configured; optional upload is available only when the user provides an upload URL.] <br>

## Skill Version(s): <br>
0.9.0 (source: server release metadata; bundled binary build-info.json reports v0.9.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
