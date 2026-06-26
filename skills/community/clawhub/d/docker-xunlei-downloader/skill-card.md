## Description: <br>
Interact with Docker-deployed Xunlei to submit magnet links, monitor tasks, and prioritize main content downloads with intelligent filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saaak](https://clawhub.ai/user/saaak) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to control a Docker-deployed Xunlei service from an agent workflow, including configuring the service endpoint, submitting magnet downloads, and checking task status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A misconfigured host can send requests, magnet links, and file lists to an unintended Xunlei service. <br>
Mitigation: Before running commands, edit or replace config.json and confirm the configured Xunlei host and port belong to the user. <br>
Risk: Submitting magnet links can consume network bandwidth and storage and may reveal the link and selected file list to the configured Xunlei service. <br>
Mitigation: Use submit commands only for content the user is allowed to download and monitor task status after submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/saaak/docker-xunlei-downloader) <br>
- [README](artifact/README.md) <br>
- [Configuration guide](artifact/CONFIG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Plain text and Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns status, progress, configuration, version, help, and error messages for the configured Xunlei service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
