## Description:

Generates secure random passwords with configurable length, character classes, similar-character exclusion, and batch generation using only the Python standard library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operators use this skill to generate one or more random passwords locally with configurable length and character-set options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated passwords are printed to the console and may remain visible in logs or terminal history.

Mitigation: Run the skill in a trusted local session and avoid copying generated passwords into shared logs or transcripts.

Risk: The documentation includes an external marketing link unrelated to password generation.

Mitigation: Treat external marketing links as informational only and review them separately before following them in managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-password-generator)
- [Publisher profile](https://clawhub.ai/user/freedompixels)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with optional JSON password output from the Python script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated passwords are printed to the console; default length is 16 characters and batch generation is supported.]

## Skill Version(s):

1.2.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
