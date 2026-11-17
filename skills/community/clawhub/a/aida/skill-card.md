## Description:

Conversational interface for AIDA, an AI-driven smart building automation platform.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[ak-khalis](https://clawhub.ai/user/ak-khalis)

### License/Terms of Use:


## Use Case:

Developers and demo teams use this skill to exercise AIDA smart-building status, device-control, optimization, and diagnostics intents against REST API endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send authenticated control or optimization commands to connected building systems.

Mitigation: Use a narrowly scoped AIDA token, lock the API URL to a trusted HTTPS host, and require explicit authorization before control or optimization actions.

Risk: Failures may be reported as successful fallback replies.

Mitigation: Fix response handling so failed API calls and non-success responses are surfaced clearly instead of returning success-like messages.

Risk: The security verdict is suspicious for environments connected to real building systems.

Mitigation: Review the skill carefully before installation and deploy only in authorized demo or development environments unless safeguards are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ak-khalis/skills/aida)
- [Artifact SKILL.md](artifact/SKILL.md)
- [Artifact README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, API calls]

**Output Format:** [Text replies based on AIDA REST API JSON responses or fallback strings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AIDA_API_URL and AIDA_API_KEY environment variables; calls use bearer token authentication.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
