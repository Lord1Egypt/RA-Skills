## Description:

Auto Continue helps an agent detect unfinished task records and incomplete skill directories, then report what work should continue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to check whether recorded work remains unfinished and to identify incomplete skill directories that may need follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill text may encourage an agent to continue work, update progress, test, or publish without waiting for explicit user approval.

Mitigation: Require explicit user approval before any edits, state-changing tests, publishing, or release actions triggered after this skill reports unfinished work.

Risk: The checker reads workspace task state and scans skill directories, so results depend on the workspace layout it is run against.

Mitigation: Run the checker only in the intended workspace and review reported paths before acting on its recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/auto-continue)
- [Publisher profile](https://clawhub.ai/user/freedompixels)
- [AISoBrand website](https://aisobrand.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with optional shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The checker may exit nonzero when unfinished tasks or incomplete skill directories are found.]

## Skill Version(s):

1.2.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
