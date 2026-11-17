## Description:

Register yourself with APort to get a verifiable passport, a DID credential that proves your identity, defines your capabilities, and enforces what you must deliver.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uchibeke](https://clawhub.ai/user/uchibeke)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to register an AI agent with APort, issue a DID-compliant passport, select capabilities, and optionally define deliverable completion requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a user email address and agent identity metadata to APort during registration.

Mitigation: Install and run it only when the user intends to share that information with APort.

Risk: The default registration payload includes showInGallery set to true, which can make the passport publicly listed.

Mitigation: Confirm or change showInGallery before submitting a registration request.

Risk: The skill asks the agent to perform follow-up announcements, README edits, task verification, and future passport attribution after registration.

Mitigation: Treat each follow-up action as opt-in and require explicit user approval before performing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uchibeke/skills/aport-id)
- [APort capability schema](https://aport.io/api/schema/capabilities-limits)
- [APort API documentation](https://aport.io/api/documentation)
- [APort ID](https://aport.id)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payloads, HTTP endpoint examples, and optional file or badge content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create aport-passport.json or README badge content only after user agreement.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter metadata.version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
