## Description: <br>
DeerFlow 2.0 installation and configuration guidance for OpenClaw, covering repository setup, Docker or local Python installation, configuration, service startup, validation, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangbb-coder](https://clawhub.ai/user/fangbb-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install DeerFlow 2.0 in OpenClaw, choose Docker or local Python setup, write required model and tool configuration, start services, and troubleshoot common deployment issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may be written into environment files or reused during setup. <br>
Mitigation: Use throwaway or least-privilege API keys, keep .env files out of source control, restrict file permissions, and rotate keys after testing. <br>
Risk: The setup guidance enables file-write and shell-style tools that can modify local files or run commands. <br>
Mitigation: Enable write_file or bash-style tools only in a sandboxed project or disposable environment where file changes and command execution are acceptable. <br>
Risk: Installation commands modify dependencies and start local services. <br>
Mitigation: Review commands and configuration before execution, limit exposed ports to the intended host, and monitor service logs during validation. <br>


## Reference(s): <br>
- [DeerFlow project homepage](https://github.com/bytedance/deer-flow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown with shell commands, configuration snippets, and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation reports, validation steps, troubleshooting checklists, and example client-script guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
