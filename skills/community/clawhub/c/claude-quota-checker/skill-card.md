## Description:

Checks remaining Claude Max/Pro subscription quota by automating Claude Code CLI's /usage command through tmux and reporting plan, usage percentages, and reset times.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mfang0126](https://clawhub.ai/user/mfang0126)

### License/Terms of Use:


## Use Case:

Developers and Claude Code users use this skill to check remaining Claude Pro or Max subscription quota, diagnose rate-limit concerns, and see when usage windows reset.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches tmux and Claude Code CLI locally and relies on the user's existing Claude login.

Mitigation: Install and run it only in an environment where local Claude CLI automation is acceptable, and review the shell script before execution.

Risk: The script automatically responds to the Claude Code trust prompt for a temporary scratch folder.

Mitigation: Use the skill only when automatic trust-prompt handling is acceptable; the script scopes the prompt to a temporary scratch directory and removes it during cleanup.

Risk: Usage parsing depends on the current Claude Code CLI /usage output layout.

Mitigation: Verify results if Claude CLI changes its usage screen, and update the parser if expected plan, usage, or reset lines are no longer captured.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mfang0126/skills/claude-quota-checker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown instructions with shell command examples and terminal text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports subscription plan, session usage, weekly usage, and reset times parsed from Claude Code CLI output.]

## Skill Version(s):

1.1.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
