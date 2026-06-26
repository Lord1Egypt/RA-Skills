## Description: <br>
Audits local skill packages or archives with a bundled Rust scanner engine and can optionally bridge to an external scanner. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyzlmh](https://clawhub.ai/user/cyzlmh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to inspect local skill bundles before installation and review scanner findings, summaries, and installation risk signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded scan reports may disclose sensitive project review details. <br>
Mitigation: Use local scan mode by default and configure --upload-url only for trusted internal HTTPS endpoints after reviewing report contents. <br>
Risk: The release includes a bundled executable scanner that requires trust in the publisher or binary provenance. <br>
Mitigation: Verify the documented SHA-256 checksum before execution, or build the scanner from source after reviewing it. <br>
Risk: External scanner bridging can execute user-configured local tooling. <br>
Mitigation: Enable the external engine only when the configured scanner is trusted and its behavior is understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyzlmh/cmic-skill-scanner-linux-amd64) <br>
- [Publisher profile](https://clawhub.ai/user/cyzlmh) <br>
- [Build source referenced by artifact](https://gitee.com/random_player/cmic-skill-scanner.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and command examples describing scan findings, risk level, and installation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local scan reports when an output directory is provided; report upload is optional and disabled unless explicitly configured.] <br>

## Skill Version(s): <br>
0.9.0 (source: server release metadata and bundled build metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
