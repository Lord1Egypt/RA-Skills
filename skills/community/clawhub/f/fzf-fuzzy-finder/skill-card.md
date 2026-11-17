## Description:

Command-line fuzzy finder for interactive filtering and selection - integrates with shell, vim, and other tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arnarsson](https://clawhub.ai/user/arnarsson)

### License/Terms of Use:


## Use Case:

Developers and command-line users use this skill to get concise fzf usage patterns, shell integration examples, and command snippets for interactive filtering, file selection, git workflows, process management, Docker, and Kubernetes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copyable shell snippets can delete files, kill processes, remove Docker or Kubernetes resources, or execute shell history without confirmation.

Mitigation: Review snippets before use and replace destructive pipelines with preview, dry-run, explicit confirmation, context checks, and safe argument handling.

Risk: Persistent aliases such as fh and fkill can execute shell history or force-kill processes unintentionally if installed verbatim.

Mitigation: Do not install persistent aliases verbatim; adapt them with confirmations and scope checks before adding them to shell configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arnarsson/skills/fzf-fuzzy-finder)
- [fzf project homepage](https://github.com/junegunn/fzf)
- [fzf wiki](https://github.com/junegunn/fzf/wiki)
- [fzf examples](https://github.com/junegunn/fzf/wiki/examples)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides copyable command examples and shell configuration snippets; commands should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
