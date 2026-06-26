## Description: <br>
Provides gated browser automation utilities for web research/search and local browser relay workflows. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[Biogod2020](https://clawhub.ai/user/Biogod2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to run gated browser automation for web research/search and local relay support in isolated environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package exposes a local browser-control relay. <br>
Mitigation: Run only in an isolated sandbox and avoid connecting it to a personal or logged-in browser profile. <br>
Risk: The package claims human-only lockout controls but the claimed wrapper is not included in the artifact. <br>
Mitigation: Do not rely on the lockout claim unless the missing wrapper and related controls are supplied and independently reviewed. <br>
Risk: Browser automation can access external web content and produce local output files. <br>
Mitigation: Review the target query and generated JSON output before using results in downstream workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Biogod2020/drission-agent) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Biogod2020) <br>
- [arXiv search endpoint](https://arxiv.org/search/) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Console text and JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local browser dependencies and the SOTA_NUCLEAR_CONFIRMED=true environment gate; search output is written to SOTA_SEARCH_REPORT.json.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
