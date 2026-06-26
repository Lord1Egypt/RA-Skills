## Description: <br>
Cross-device sync for OpenClaw workspace skills, memory, and settings via GitHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imink](https://clawhub.ai/user/imink) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this plugin to synchronize workspace skills, memory, and settings across devices through a configured GitHub repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically upload and download OpenClaw skills, memory, and settings without per-session approval. <br>
Mitigation: Use a dedicated private sync repository, review synced paths, and set autoSync to false until the workflow is trusted. <br>
Risk: Sensitive workspace content or secrets could be synced to GitHub if included in configured paths. <br>
Mitigation: Avoid syncing secrets or sensitive memory, and review the mapping configuration before pushing. <br>
Risk: The skill depends on GitHub authentication and may use GITHUB_TOKEN or GitHub CLI credentials. <br>
Mitigation: Use credentials scoped for the intended private repository and rotate them if sync access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/imink/any-sync) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger GitHub-backed workspace synchronization through configured commands and session hooks.] <br>

## Skill Version(s): <br>
0.2.10 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
