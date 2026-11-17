## Description:

BetterPrompt helps agents discover, install, run, and review reusable AI prompt skills from the BetterPrompt registry through the betterprompt/bp CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeqle](https://clawhub.ai/user/mikeqle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use BetterPrompt to find prompt skills, inspect inputs and model options, generate text, image, or video outputs, and manage installed skill libraries through the CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or run a mutable third-party BetterPrompt CLI.

Mitigation: Review before installing and prefer a pinned or sandboxed CLI install instead of a global @latest install.

Risk: Prompts or local files can be sent to an external BetterPrompt service during generation.

Mitigation: Avoid sending private prompts or local files unless the user is comfortable uploading them to that service.

## Reference(s):

- [ClawHub BetterPrompt Skill](https://clawhub.ai/mikeqle/skills/betterprompt)
- [BetterPrompt Skills](https://betterprompt.me/skills)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text, Markdown]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can request structured JSON from the BetterPrompt CLI for generation runs and output retrieval.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
