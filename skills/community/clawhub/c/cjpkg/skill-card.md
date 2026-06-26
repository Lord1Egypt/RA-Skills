## Description: <br>
cjpkg helps agents search, download, configure, and develop Cangjie packages from the Cangjie Central Repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[l3gi0nxxxx](https://clawhub.ai/user/l3gi0nxxxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to find Cangjie packages, download package artifacts, update Cangjie project configuration, and follow cjpm-based build or package-development workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead agents to modify Cangjie project files such as cjpm.toml. <br>
Mitigation: Require the agent to show exact commands and diffs, and back up project configuration before applying changes. <br>
Risk: The skill includes setup guidance that can change persistent shell or PATH configuration. <br>
Mitigation: Avoid persistent shell-profile changes unless explicitly approved, and review any environment changes before execution. <br>
Risk: The skill can download package artifacts from the Cangjie package registry. <br>
Mitigation: Use it when package management is intended, and confirm package name, organization, version, and destination before download. <br>


## Reference(s): <br>
- [cjpkg on ClawHub](https://clawhub.ai/l3gi0nxxxx/cjpkg) <br>
- [Cangjie Central Repository](https://pkg.cangjie-lang.cn/index) <br>
- [Cangjie SDK Download](https://cangjie-lang.cn/download) <br>
- [Cangjie Developer Guide](https://gitcode.com/Cangjie/cangjie_docs/blob/main/docs/dev-guide/summary_cjnative_EN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose package-search, download, cjpm, and TOML-editing commands for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
