## Description: <br>
Provides defensive Linux Bash scripting guidance for safe foundations, argument parsing, production patterns, and ShellCheck-compliant scripts, cron jobs, and CLI tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iliaal](https://clawhub.ai/user/iliaal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when writing or reviewing GNU Bash 4.4+ scripts, cron jobs, and CLI tools for Linux, with emphasis on safe defaults, robust parsing, production patterns, and ShellCheck/shfmt validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Bash scripts can delete files, write system paths, make network requests, or run through cron and other automation if applied without review. <br>
Mitigation: Review generated scripts before running them, with extra attention to destructive commands, system paths, network calls, and scheduled execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iliaal/compound-eng-linux-bash-scripting) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Skill specification](artifact/SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review generated scripts before execution, especially scripts that delete files, write system paths, make network requests, or are scheduled through automation.] <br>

## Skill Version(s): <br>
4.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
