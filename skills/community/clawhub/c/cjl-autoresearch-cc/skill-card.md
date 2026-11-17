## Description:

Optimize skills, prompts, articles, workflows, or systems via single-step iterative edits with testing and scoring to keep improvements and discard regressions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcjl](https://clawhub.ai/user/0xcjl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content authors use this skill to iteratively improve selected skills, plugins, prompts, articles, workflows, or system descriptions through small edits, realistic tests, scoring, and batch review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can edit selected prompts, documents, skills, or plugin files, including paths under ~/.claude.

Mitigation: Install only if you want an agent to help edit selected prompts, documents, skills, or plugins. Confirm the target carefully, especially for ~/.claude skill or plugin paths, and review the batch summary before allowing additional rounds.

Risk: Iterative edits may introduce inaccurate or lower-quality guidance if checklist scores miss an issue.

Mitigation: Review each batch summary and keep the one-mutation-per-round process so regressions can be identified and reverted.

## Reference(s):

- [Mutation Strategies Reference](references/mutation_strategies.md)
- [ClawHub Skill Page](https://clawhub.ai/0xcjl/skills/cjl-autoresearch-cc)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with proposed edits, checklist questions, test scenarios, scores, summaries, and inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May edit user-selected text files or skill/plugin files after confirmation; pauses every 30 rounds for human review.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
