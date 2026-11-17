## Description:

Synchronizes post-release documentation by aligning README, ARCHITECTURE, CONTRIBUTING, CLAUDE.md, CHANGELOG, TODOS, and VERSION-related content with actual repository changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill after code changes and before PR merge to audit Markdown documentation against the branch diff, apply low-risk factual updates, improve changelog wording, and surface risky documentation decisions for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can update repository documentation and create a documentation commit, which could introduce incorrect or misleading project guidance.

Mitigation: Review the generated diff and commit before pushing, especially for reviewers who do not read Chinese comfortably.

Risk: The workflow inspects branch diffs and documentation state, so running it from the wrong branch can produce irrelevant documentation changes.

Mitigation: Run it from the intended feature branch and honor its base-branch precheck before applying edits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/x-rayluan/skills/clawlite-doc-sync)
- [Publisher profile](https://clawhub.ai/user/x-rayluan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown documentation changes with concise text summaries and optional shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce repository file edits and a documentation commit when changes are needed; asks before risky narrative changes or version bumps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
