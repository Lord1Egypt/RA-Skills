## Description:

Autonomous skill optimizer inspired by Karpathy's autoresearch that evaluates SKILL.md files with an 8-dimension rubric, runs hill-climbing with git version control, and validates changes through test prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alchaincyf](https://clawhub.ai/user/alchaincyf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to evaluate and improve Claude Code skills by designing test prompts, scoring structure and behavior, proposing focused edits, and retaining only improvements after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can broadly inspect and modify installed skill files.

Mitigation: Run it first on a named skill or reviewed allowlist, and avoid full-scan optimization unless all local skill instructions are acceptable inputs.

Risk: Generated edits may introduce incorrect or lower-quality skill guidance.

Mitigation: Review generated test prompts, score changes, diffs, and sample outputs before accepting changes.

Risk: The workflow creates git branches and commits while optimizing skills.

Mitigation: Inspect the generated branch and commits before merging or deploying, and rely on revert behavior for changes that do not improve the score.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alchaincyf/skills/darwin-skill)
- [Publisher profile](https://clawhub.ai/user/alchaincyf)
- [Karpathy autoresearch](https://github.com/karpathy/autoresearch)
- [Claude Code](https://claude.ai/code)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks, tabular scoring summaries, JSON or TSV artifacts, and proposed file edits.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create git branches, commits, test-prompts.json, results.tsv, and SKILL.md changes when the user approves the optimization workflow.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
