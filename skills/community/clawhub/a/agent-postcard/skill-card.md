## Description:

Generates and sends AI-created postcards featuring an agent selfie at real locations in 12 artistic styles through the Turai Postcard API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpaulgrayson](https://clawhub.ai/user/jpaulgrayson)

### License/Terms of Use:


## Use Case:

Agents and their operators use this skill to create postcard images from a chosen location, style, optional message, and either a supplied selfie prompt or a persona-derived prompt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persona-derived local file content may be sent to the Turai API when the skill auto-detects SOUL.md or IDENTITY.md.

Mitigation: Use --selfie with a sanitized prompt, or use --persona only with a file created specifically for postcard appearance data.

Risk: The third-party API receives the generated selfie prompt plus the requested location, style, and message.

Mitigation: Avoid including private instructions, identity details, secrets, or sensitive workspace context in persona files or postcard messages.

## Reference(s):

- [Agent Postcard ClawHub page](https://clawhub.ai/jpaulgrayson/skills/agent-postcard)
- [Turai](https://turai.org)

## Skill Output:

**Output Type(s):** [API Calls, Files, Shell commands]

**Output Format:** [PNG image file or JSON image response with console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TURAI_API_KEY and user-provided location and style; can save the generated postcard to a specified output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
