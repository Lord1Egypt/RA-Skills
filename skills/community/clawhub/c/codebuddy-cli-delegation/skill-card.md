## Description:

Guides developers in delegating large coding batches to a headless CodeBuddy CLI agent, with controlled execution and independent verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carloswonmore](https://clawhub.ai/user/carloswonmore)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to delegate lengthy refactoring, test-writing, and documentation batches to CodeBuddy CLI, then independently audit the resulting changes and tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended jobs with auto-approval may execute unreviewed changes or project hooks.

Mitigation: Run only in trusted repositories or sandboxed copies; inspect project settings and hooks before enabling auto-approval.

Risk: Prompts and session logs may expose sensitive information.

Mitigation: Keep secrets out of prompts and exclude .cli-runs/ and CodeBuddy session logs from commits and sensitive backups.

Risk: A delegated agent's completion report may not match its actual code changes or test results.

Mitigation: Review the diff and independently rerun validation before accepting the batch.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/carloswonmore/skills/codebuddy-cli-delegation)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes delegation checklists and independent audit steps.]

## Skill Version(s):

0.1.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
