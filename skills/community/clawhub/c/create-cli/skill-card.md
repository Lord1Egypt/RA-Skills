## Description: <br>
Design command-line interface parameters and UX, including arguments, flags, subcommands, help text, output formats, error messages, exit codes, prompts, config and environment precedence, and safe dry-run behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to design or refactor CLI surfaces before implementation, with attention to human usability, scriptability, safe destructive behavior, and consistent configuration conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated CLI specifications may include destructive-operation flags, confirmation behavior, or configuration conventions that affect downstream implementations. <br>
Mitigation: Review generated destructive-operation controls, non-interactive behavior, and config precedence before implementing or shipping the CLI. <br>


## Reference(s): <br>
- [Command Line Interface Guidelines (condensed)](references/cli-guidelines.md) <br>
- [Command Line Interface Guidelines](https://clig.dev/) <br>
- [CLI Guidelines GitHub Repository](https://github.com/cli-guidelines/cli-guidelines) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown CLI specification with command synopsis, option tables, behavior rules, and example invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include arguments and flags, subcommand semantics, stdout and stderr rules, exit-code maps, safety controls, configuration precedence, and shell completion guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
