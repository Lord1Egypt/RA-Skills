## Description:

Git archaeology engine that reconstructs the why behind code changes by analyzing commit history patterns, reverts, hotspots, refactors, and ownership signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcools1977](https://clawhub.ai/user/jcools1977)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to inspect a repository's git history and explain why code evolved into its current shape. It supports onboarding, incident follow-up, architecture review, and work on old or volatile code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to inspect local git history for the repository under discussion.

Mitigation: Use it only in repositories where local commit history review is acceptable for the task.

Risk: Broad activation wording such as casual questions about why something changed could trigger history analysis outside explicit code-archaeology requests.

Mitigation: Narrow activation wording or invoke the skill explicitly for repository archaeology, onboarding, incident follow-up, or architecture review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jcools1977/skills/fossil-record)
- [Publisher profile](https://clawhub.ai/user/jcools1977)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown analysis with timelines, maps, summaries, and inline examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local git-history analysis guidance and narrative repository archaeology reports.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
