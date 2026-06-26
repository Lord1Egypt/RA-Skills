## Description: <br>
Audits local skill packages or archives with a bundled Rust scanner engine and can optionally bridge to an external scanner. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyzlmh](https://clawhub.ai/user/cyzlmh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill before installing local skills, archives, or release bundles to inspect scanner findings, risk levels, and installation readiness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A bundled or downloaded scanner binary requires trust in the release host. <br>
Mitigation: Verify the scanner binary SHA-256 against the documented checksum before execution, or build the scanner from source. <br>
Risk: Optional upload of scan reports can expose findings about private skills or internal packages. <br>
Mitigation: Use --upload-url only with a trusted endpoint and confirm the upload destination before sending reports. <br>
Risk: The optional external scanner bridge delegates analysis to a user-configured local tool. <br>
Mitigation: Enable the external engine only for trusted local scanner tools and review their behavior separately. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyzlmh/cmic-skill-scanner-darwin-arm64) <br>
- [Publisher profile](https://clawhub.ai/user/cyzlmh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and scanner findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local scan summaries, risk levels, engine status, and optional report output paths.] <br>

## Skill Version(s): <br>
0.9.0 (source: server release metadata and build-info.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
