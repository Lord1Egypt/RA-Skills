## Description:

CinePrompt helps agents build structured AI video prompts and share links from natural-language shot descriptions or CinePrompt state JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[belafontelabs](https://clawhub.ai/user/belafontelabs)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, cinematographers, and developers use CinePrompt to turn shot ideas into detailed AI video prompt state, prompt text, and share links for editing or generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags an unpinned global CLI install path.

Mitigation: Prefer a pinned local CLI install when available and do not run npm install with elevated privileges.

Risk: Prompt text, state JSON, reference images, saved subjects, and BYOK provider keys may be sent to CinePrompt/Supabase or listed generation providers.

Mitigation: Use only credentials and content appropriate for those services, and keep provider keys scoped to the intended workflow.

Risk: The artifact includes an internal service-key path for direct share-link creation.

Mitigation: Do not place CINEPROMPT_SERVICE_KEY in general agent environments; prefer the normal API-key path for routine use.

## Reference(s):

- [CinePrompt ClawHub skill](https://clawhub.ai/belafontelabs/skills/cineprompt)
- [CinePrompt](https://cineprompt.io)
- [CinePrompt guides](https://cineprompt.io/guides)
- [CinePrompt models](https://cineprompt.io/models)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON state examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce CinePrompt state JSON, generated prompt text, and share-link command guidance.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
