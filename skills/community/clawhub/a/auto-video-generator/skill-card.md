## Description: <br>
Helps agents plan and attempt demo video generation from web pages or local UI files using Playwright-oriented recording, scenario decomposition, and narration workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rosscui-chy](https://clawhub.ai/user/rosscui-chy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and product teams use this skill to automate product-demo and tutorial video workflows from web UI targets, local UI files, templates, or project code. It can guide CLI, Python API, Web UI, and VS Code extension usage for generating or validating video outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may overstate working video generation or report success before a real, usable video has been produced. <br>
Mitigation: Manually verify the generated media file and playback quality before relying on any success message or publishing the result. <br>
Risk: The skill can interact with local files, workspace code, environment secrets, and web content, including sensitive pages if pointed at them. <br>
Mitigation: Run it only in a reviewed, isolated workspace against non-sensitive pages or files; avoid authenticated, internal, financial, customer, or secret-bearing targets. <br>
Risk: Untrusted templates or helper integrations may expose local data or credentials. <br>
Mitigation: Review template archives before installation and scrub sensitive environment variables before using the VS Code helper or related automation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rosscui-chy/auto-video-generator) <br>
- [Project Homepage](https://github.com/avg-team/auto-video-generator) <br>
- [README](artifact/README.md) <br>
- [CI/CD Documentation](artifact/CI_CD_DOCUMENTATION.md) <br>
- [VS Code Extension README](artifact/vscode-extension/README.md) <br>
- [Web UI README](artifact/web-ui/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or reference generated video files and project files when the underlying tooling is executed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact files contain conflicting 2.0.0, 3.0.0, and 3.2.0 version signals) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
