## Description:

Control Emacs. Search, edit, navigate, and pair programming with user

This skill is ready for commercial/non-commercial use.

## Publisher:

[calsys456](https://clawhub.ai/user/calsys456)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to let an agent interact with a running Emacs session for navigation, buffer inspection, text insertion, replacement, saving, and pair-programming support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can read Emacs buffers and kill-ring contents that may contain sensitive information.

Mitigation: Use the skill only for intended Emacs interaction and require explicit user intent before full-buffer reads or kill-ring inspection.

Risk: The agent can evaluate Emacs Lisp, edit buffers, save files, and modify non-current buffers.

Mitigation: Require explicit user intent before ELisp evaluation, saves, or edits outside the current working context, and review proposed changes before execution.

Risk: Interactive or blocking Emacs functions can hang an agent workflow.

Mitigation: Avoid interactive prompts and blocking functions during evaluation unless the user is actively supervising the Emacs session.

## Reference(s):

- [emacsctl setup and usage](https://github.com/calsys456/emacsctl)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and Emacs Lisp examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read, edit, replace, save, or inspect Emacs buffers when the user has configured emacsctl and intends Emacs interaction.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
