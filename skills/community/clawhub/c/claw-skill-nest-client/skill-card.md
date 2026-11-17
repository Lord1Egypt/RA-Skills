## Description:

Local/private Claw Skill Nest client for listing, uploading, installing, and updating skills in a configured local repository; it is not intended for clawhub.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kklldog](https://clawhub.ai/user/kklldog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to manage skills in a local/private Claw Skill Nest, including list, upload, install, and update workflows through the bundled TypeScript client.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A malicious or compromised configured Claw Skill Nest server could cause install or update workflows to make persistent filesystem changes outside the intended trust boundary.

Mitigation: Install or update only from a Claw Skill Nest server that the user controls and trusts, and review skills before deployment.

Risk: Remote plaintext HTTP endpoints and the default API key can expose or weaken access to the private skill repository.

Mitigation: Avoid remote plaintext HTTP endpoints, configure a trusted endpoint, and replace the default API key before use.

Risk: Skill names, filenames, archive entries, or extracted paths can create unsafe archive-handling or path-write behavior.

Mitigation: Validate skill names, filenames, archive entries, and extracted paths before broad use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kklldog/skills/claw-skill-nest-client)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown or terminal text with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke a TypeScript client that calls the configured Claw Skill Nest API and persists installed skills under the local OpenClaw skills directory.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
