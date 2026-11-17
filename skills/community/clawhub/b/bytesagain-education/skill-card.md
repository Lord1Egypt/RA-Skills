## Description:

Bytesagain Education generates 7-day structured learning plans, quizzes, and local study progress tracking without requiring internet access or an account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Learners, developers, and educators use this skill to generate topic-based 7-day study plans, quizzes, and local progress summaries for self-guided technical learning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local study progress can be overwritten or cleared by reset or set-topic without a confirmation prompt.

Mitigation: Review current progress before using reset or set-topic, and back up ~/.local/share/education-skill/progress.json if the progress history matters.

Risk: Learning plans can include example shell commands such as Docker commands.

Mitigation: Treat commands in generated plans as learning examples and review them before running them locally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loutai0307-prog/skills/bytesagain-education)
- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Docker Get Started](https://docs.docker.com/get-started/)
- [MDN JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)
- [A Tour of Go](https://go.dev/tour/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-style terminal text with inline shell commands and local JSON progress data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores progress locally in ~/.local/share/education-skill/progress.json; requires bash and python3.]

## Skill Version(s):

1.0.0 (source: server evidence release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
