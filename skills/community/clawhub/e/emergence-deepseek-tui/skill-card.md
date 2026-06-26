## Description: <br>
Use DeepSeek TUI CLI as an autonomous code assistant with `deepseek exec` for headless text-in/text-out delegation and `deepseek run` for interactive coding with filesystem tool access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emergencescience](https://clawhub.ai/user/emergencescience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to delegate code generation to DeepSeek TUI in headless mode or to run an interactive autonomous coding session in a trusted workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Interactive `deepseek run` sessions can edit files and run shell commands in the active workspace. <br>
Mitigation: Use interactive mode only in a trusted or disposable, version-controlled workspace and review file changes and commands before relying on them. <br>
Risk: DeepSeek TUI usage may require sensitive credentials for its provider. <br>
Mitigation: Install and configure the CLI only when the provider is trusted, and prefer headless `deepseek exec` mode for controlled delegation. <br>
Risk: Headless `deepseek exec` output may include simulated tool-call text or incorrect code snippets. <br>
Mitigation: Treat headless responses as text only, apply targeted edits yourself, and build or test after applying changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/emergencescience/emergence-deepseek-tui) <br>
- [DeepSeek TUI repository](https://github.com/Hmbown/DeepSeek-TUI.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Headless mode requires the caller to provide file context; interactive mode may read, edit, and execute commands in the current workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
