## Description:

Checks a specified directory for console.log statements, excludes common build and dependency folders, and reports file locations with line previews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sy724](https://clawhub.ai/user/sy724)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill before commit, review, or deployment to find leftover console.log debugging statements and decide whether to remove them or replace them with proper logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad scan can include private or irrelevant project files in the agent's working context.

Mitigation: Run the skill with a specific path and exclude patterns when the workspace contains sensitive or unrelated code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sy724/skills/console-log-checker)
- [ClawHub publisher profile](https://clawhub.ai/user/sy724)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with a findings table, total occurrence count, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes file path, line number, and content preview for each reported console.log occurrence.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
