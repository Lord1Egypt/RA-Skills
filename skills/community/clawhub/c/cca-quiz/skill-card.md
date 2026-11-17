## Description:

Provides a Chinese-language CCA mock quiz with 12 scenario-based multiple-choice questions across five domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sawzhang](https://clawhub.ai/user/sawzhang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run an interactive CCA practice quiz, receive per-question feedback, and review domain-level performance after completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests shell access even though the release security summary says a static quiz does not need shell commands.

Mitigation: Review before installation and prefer a version that removes Bash permission or otherwise limits tool access to the minimum needed for presenting the quiz.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style conversational quiz prompts, answer explanations, scoring summary, and study guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Presents one question at a time and summarizes score by CCA domain after all 12 questions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
