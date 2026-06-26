## Description: <br>
Manage and query DevOps platform data, including applications, iterations, releases, and statistics via configured API access with user token authorization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanqiuqian](https://clawhub.ai/user/yuanqiuqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to configure access to a DevOps efficiency platform and query or manage applications, iterations, release windows, release tasks, release records, favorites, and platform statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and uses a DevOps platform access token and can expose operational data from the configured endpoint. <br>
Mitigation: Use a least-privilege, revocable or short-lived token, avoid sharing it in chat or command history, and install only when the publisher and endpoint are trusted. <br>
Risk: Local configuration may contain sensitive base URL and token material. <br>
Mitigation: Check local config file permissions after setup and clear or rotate credentials when access is no longer needed. <br>
Risk: Debug output and API error details may include sensitive platform metadata. <br>
Mitigation: Treat debug logs and copied command output as sensitive and avoid pasting them into untrusted channels. <br>
Risk: Using an HTTP base URL could expose credentials or operational data in transit. <br>
Mitigation: Configure an HTTPS endpoint unless a trusted local development environment explicitly requires otherwise. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yuanqiuqian/devops-platform-skill) <br>
- [README.md](artifact/README.md) <br>
- [INSTALL.md](artifact/INSTALL.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [SUMMARY.md](artifact/SUMMARY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown and CLI text with inline shell commands and tabular data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured DevOps platform base URL and user Open Token; API calls use bearer-token authorization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
