## Description:

Finds human-made visual, motion, and music references for AI-generated or coded video projects and organizes them into a review board.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, filmmakers, and creative teams use the skill to find and assess references for a video’s look, motion, casting, locations, or music before production. It prepares a short list and a board for a person to review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags privacy concerns when the workflow handles images or briefs alongside external services.

Mitigation: Do not share confidential images or briefs with external services unless authorized.

Risk: The security review flags credential-handling concerns.

Mitigation: Review any authentication prompts and avoid exposing credentials while using connected sources.

Risk: The security review reports unpinned installation examples.

Mitigation: Review package or container installation examples and pin versions before running them.

Risk: The security scan has partial coverage because some referenced paths could not be resolved.

Mitigation: Review unresolved referenced content before installation; the scan does not establish that all relevant content was examined.

## Reference(s):

- [Find references for an AI video](https://varg.ai/how-to/find-references-for-an-ai-video)
- [How to make a video with an AI agent in ten steps](https://varg.ai/how-to/make-a-video-in-ten-steps)
- [Skill source repository](https://github.com/vargHQ/skills/tree/main/find-references)

## Skill Output:

**Output Type(s):** [Markdown, HTML, JSON, Shell commands, Reference guidance]

**Output Format:** [Project files such as brief and query notes, reference records, an HTML review board, and production guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The files vary by selected reference jobs and by whether the project is generated, coded, or hybrid.]

## Skill Version(s):

1.0.8 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
