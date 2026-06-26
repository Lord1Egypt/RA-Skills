## Description: <br>
Dep Radar scans dependency manifests, release notes, code usage, and community reports to flag breaking-change risk before upgrades. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tarun-khatri](https://clawhub.ai/user/tarun-khatri) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DevOps engineers, and CI maintainers use Dep Radar to evaluate dependency upgrades, identify breaking changes, locate impacted code, and prioritize migrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The SessionStart hook sources project and user configuration files as shell. <br>
Mitigation: Install the hook only in trusted repositories, or disable or remove it when project configuration files are not trusted. <br>
Risk: Reports, cache entries, or saved Markdown may contain private dependency names, local paths, or code snippets. <br>
Mitigation: Avoid sharing reports from sensitive repositories, clear ~/.cache/depradar when needed, and remove saved reports that may expose private project details. <br>
Risk: API keys used for GitHub, Stack Overflow, Reddit, Slack, or X/Twitter could be exposed if stored in project files. <br>
Mitigation: Keep secrets in environment variables or user-level config with restrictive permissions, and do not commit project-level files containing API keys. <br>
Risk: Slack notifications may send dependency and project details outside the local environment. <br>
Mitigation: Use Slack notifications only for repositories whose report contents are approved for that destination. <br>


## Reference(s): <br>
- [ClawHub Dep Radar release page](https://clawhub.ai/tarun-khatri/depradar) <br>
- [Dep Radar README](artifact/README.md) <br>
- [Dep Radar changelog](artifact/CHANGELOG.md) <br>
- [Semantic Versioning](https://semver.org/) <br>
- [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Terminal text, JSON, Markdown, or compact context depending on invocation flags] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include package versions, ranked breaking-change findings, impacted file paths, community signals, exit codes, and optional saved report files.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
