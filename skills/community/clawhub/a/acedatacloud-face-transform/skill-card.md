## Description:

Guides agents through face analysis, portrait transformations, face swaps, and liveness checks using AceDataCloud's Face APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acedatacloud](https://clawhub.ai/user/acedatacloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare authenticated requests for face analysis, portrait editing, face swaps, and liveness checks through AceDataCloud.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Face image URLs and analysis results are sensitive and are sent to AceDataCloud.

Mitigation: Use only images you are authorized to process and confirm you are comfortable sharing them with AceDataCloud.

Risk: Face swaps or altered likenesses can be used deceptively or without consent.

Mitigation: Avoid non-consensual likeness changes and deceptive face swaps.

Risk: Exposing the API key can allow unauthorized use of face-processing endpoints.

Mitigation: Restrict the key to needed endpoints where possible, and do not put it in prompts or commit the .env token.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/acedatacloud/skills/face-transform)
- [AceDataCloud application setup](https://platform.acedata.cloud/console/applications)
- [First-run and key setup guide](https://github.com/AceDataCloud/Skills#first-run-with-clawhub-and-openclaw)
- [AceDataCloud token instructions](https://github.com/AceDataCloud/Skills/blob/main/skills/_shared/authentication.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AceDataCloud API key and face image URLs.]

## Skill Version(s):

1.0.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
