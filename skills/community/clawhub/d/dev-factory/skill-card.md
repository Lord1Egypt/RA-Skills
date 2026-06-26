## Description: <br>
Automates software development by discovering project ideas from GitHub trends, CVE databases, and security news, then generating, testing, correcting, and optionally publishing code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rebugui](https://clawhub.ai/user/rebugui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to automate discovery, implementation, testing, correction, and publishing workflows for security tools and DevOps utilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run commands and modify project files during build, test, and correction workflows. <br>
Mitigation: Run it in a sandboxed workspace with a scrubbed environment and review generated changes before using them in important repositories. <br>
Risk: The skill can use GLM, Claude, Notion, and GitHub credentials and may publish generated code. <br>
Mitigation: Use least-privilege credentials, prefer private repositories, and disable auto-publish unless publishing is explicitly intended. <br>
Risk: Daemon or health endpoints and broad automation can expose operational state or expand access if left enabled unnecessarily. <br>
Mitigation: Disable daemon health exposure unless needed and restrict runtime access to trusted local or protected environments. <br>


## Reference(s): <br>
- [Dev Factory ClawHub Listing](https://clawhub.ai/rebugui/dev-factory) <br>
- [Workflow](artifact/WORKFLOW.md) <br>
- [Quick Start](artifact/QUICK_START.md) <br>
- [Production Deployment](artifact/PRODUCTION_DEPLOYMENT.md) <br>
- [ChatDev 2.0](https://github.com/OpenBMB/ChatDev) <br>
- [NVD CVE API](https://services.nvd.nist.gov/rest/json/cves/2.0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated project files, code, configuration snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run build, test, correction, external API, Notion, and GitHub publishing workflows when configured.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
