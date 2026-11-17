## Description:

Guides agents through AceDataCloud's Fish Audio API for text-to-speech, saved voices, and one-shot voice cloning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acedatacloud](https://clawhub.ai/user/acedatacloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to configure AceDataCloud access and generate narration with public, saved, or authorized reference voices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: One-shot voice cloning can impersonate someone without their consent.

Mitigation: Use only voices and reference audio you own or are authorized to use; obtain consent before cloning another person's voice.

Risk: Submitting sensitive text or reference audio sends it to AceDataCloud.

Mitigation: Avoid submitting sensitive material unless you are comfortable sharing it with AceDataCloud.

Risk: A broadly scoped or exposed API token can permit unintended requests.

Mitigation: Keep the token private and restrict it to the APIs needed for the workflow.

## Reference(s):

- [ClawHub release](https://clawhub.ai/acedatacloud/skills/fish-audio)
- [AceDataCloud first-run guide](https://github.com/AceDataCloud/Skills#first-run-with-clawhub-and-openclaw)
- [AceDataCloud authentication guide](https://github.com/AceDataCloud/Skills/blob/main/skills/_shared/authentication.md)
- [AceDataCloud asynchronous task guide](https://github.com/AceDataCloud/Skills/blob/main/skills/_shared/async-tasks.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with bash commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API responses provide an audio URL or an asynchronous task ID.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
