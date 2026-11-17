## Description:

Generate a daily AI ecosystem pulse on Claude Code skills and agent-skill trends; scan ClawHub trending skills, Hacker News, and X/Twitter chatter; and output a 5-bullet Markdown brief with sentiment tags and draft replies for opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rabgpt](https://clawhub.ai/user/rabgpt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, founders, and skill builders use this agent skill to collect a daily public-source briefing on Claude Code, ClawHub, Hacker News, and X/Twitter activity related to agent skills. It helps them identify ecosystem trends, engagement opportunities, and noteworthy safety or adoption signals without manually checking each channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes an optional remote installer command that pipes downloaded code into bash.

Mitigation: Do not run the installer command unless the installer source has been reviewed, the publisher is trusted, and the local machine changes are understood.

Risk: The daily pulse depends on live public search results from ClawHub, Hacker News, and X/Twitter, so items may be incomplete, stale, or noisy.

Mitigation: Review cited source URLs and fallback notes before acting on the brief or posting draft replies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rabgpt/skills/daily-ai-skills-pulse)
- [Implexa homepage](https://implexa.ai)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a dated 5-bullet brief with sentiment tags, source URLs, optional draft replies for opportunity items, and a short coverage or fallback note.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
