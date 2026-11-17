## Description:

AI PR analysis companion that collects GitHub pull request metadata, diffs, and comments, analyzes change scope, technical debt, test coverage, and review risk, then produces a structured review report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering leads use this skill to review GitHub pull requests more consistently by summarizing changed files, diffs, comments, risk areas, code quality findings, test coverage gaps, and technical debt. The skill can publish the resulting review report to Feishu for team collaboration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read full GitHub pull request diffs and comments, including private or sensitive repository content when the agent has access.

Mitigation: Use least-privilege GitHub access, run it only on authorized repositories, and redact secrets or sensitive diffs before sharing generated reports.

Risk: The skill can publish generated review content to Feishu without clear approval or containment controls in the artifact.

Mitigation: Require a preview and explicit approval before publication, and confirm Feishu document permissions and audience before posting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/skills/ai-pr-analysis-companion)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Structured Markdown review report with risk ratings, findings, recommendations, and Feishu publication output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses GitHub PR metadata and diff content as input and may publish generated review content to Feishu.]

## Skill Version(s):

1.0.0 (source: workflow.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
