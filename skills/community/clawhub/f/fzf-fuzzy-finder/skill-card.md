## Description: <br>
Command-line fuzzy finder for interactive filtering and selection - integrates with shell, vim, and other tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Arnarsson](https://clawhub.ai/user/Arnarsson) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and command-line users use this skill to get concise fzf usage patterns, shell integrations, aliases, and workflow examples for interactive filtering and selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some optional shell examples can delete files, kill processes, or change Docker and Kubernetes resources if copied and run carelessly. <br>
Mitigation: Review shell snippets before execution, add confirmation or dry-run steps to destructive commands, and verify the current working directory plus Docker or Kubernetes context before running admin commands. <br>
Risk: The history replay alias can immediately re-run prior commands. <br>
Mitigation: Avoid adding the history replay alias unless the operator understands the behavior and inspects the selected command before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Arnarsson/fzf-fuzzy-finder) <br>
- [fzf Project Homepage](https://github.com/junegunn/fzf) <br>
- [fzf Wiki](https://github.com/junegunn/fzf/wiki) <br>
- [fzf Examples](https://github.com/junegunn/fzf/wiki/examples) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command examples, aliases, and environment variable configuration guidance that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
