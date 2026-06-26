## Description: <br>
Downloads Docker images with a Python script and packages them as tar files for offline docker load use, supporting SOCKS5 proxy downloads and mirror acceleration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaohaixin](https://clawhub.ai/user/zhaohaixin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to pull Docker images from registries and package them as offline tar archives for transfer or later docker load. It is intended for explicit image download requests with configurable architecture, proxy, or mirror settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Background Docker image downloads can consume significant network bandwidth and disk space. <br>
Mitigation: Install only when image downloading is desired, use explicit Docker image requests, and monitor disk and network usage. <br>
Risk: Private registry passwords may be exposed through terminal prompting. <br>
Mitigation: Avoid entering private registry passwords unless the prompt is changed to hidden input, or use limited-scope pull-only credentials. <br>
Risk: A stale local config path can point the skill at the wrong script location after installation. <br>
Mitigation: Reset the config path after install before running downloads. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown status updates with shell commands and generated Docker image tar files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates tar archives under an images directory and reports docker load commands after download completion.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and script VERSION) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
