## Description:

Use CCAPI's unified AI API gateway to access text, image, video, and audio models through an OpenAI-compatible API endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[littleblackone](https://clawhub.ai/user/littleblackone)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to configure agents or applications to call CCAPI for chat, image, video, audio, model discovery, streaming, and related OpenAI-compatible API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CCAPI API keys could be exposed if pasted into prompts, logs, shared code, or committed files.

Mitigation: Keep CCAPI API keys private, use scoped credentials where available, and store keys in local secret managers or environment variables.

Risk: Prompts, files, media URLs, or generated content may be sent to a third-party AI API gateway.

Mitigation: Use the skill only when CCAPI's data handling terms are acceptable for the intended workload, and avoid sending sensitive data unless approved.

## Reference(s):

- [CCAPI Documentation](https://docs.ccapi.ai)
- [CCAPI Model Showcase](https://ccapi.ai/models)
- [CCAPI Pricing](https://ccapi.ai/pricing)
- [CCAPI Dashboard and API Keys](https://ccapi.ai/dashboard)
- [ClawHub Skill Page](https://clawhub.ai/littleblackone/skills/ccapi)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with Python, TypeScript, cURL, endpoint, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include external API endpoint guidance, model identifiers, request examples, and API-key handling notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
