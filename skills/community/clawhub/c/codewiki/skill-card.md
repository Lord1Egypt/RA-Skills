## Description: <br>
CodeWiki triggers a confirmed workflow that clones or updates a Git repository, generates a structured wiki with the codewiki CLI, and optionally renders a local MkDocs or VitePress preview. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiangsier-xyz](https://clawhub.ai/user/jiangsier-xyz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn a specified code repository into generated Markdown wiki documentation. When requested, it can also build MkDocs or VitePress static preview sites after the user confirms the repository, output path, render stack, and any preview ports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confirmed runs can clone public or SSH-accessible repositories and may use the user's normal git credentials for git@ URLs. <br>
Mitigation: Confirm the expanded repository URL before execution and use only repositories and accounts the user intended to process. <br>
Risk: Rendering can download MkDocs or VitePress packages and write generated files under the selected output directory. <br>
Mitigation: Use a deliberate output path and allow renderer installs only for the requested MkDocs or VitePress build. <br>
Risk: Optional preview serving opens localhost ports and keeps foreground server processes running until stopped. <br>
Mitigation: Show the preview port numbers before execution and stop the preview servers when review is complete. <br>


## Reference(s): <br>
- [CodeWiki upstream project](https://github.com/FSoft-AI4Code/CodeWiki) <br>
- [CodeWiki ClawHub skill page](https://clawhub.ai/jiangsier-xyz/skills/codewiki) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command invocations; generated wiki files and optional static site files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before cloning repositories, installing renderer packages, writing outputs, or opening localhost preview ports.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
