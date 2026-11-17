## Description:

Complete Facticity.AI integration for fact-checking claims, extracting claims from content, transcribing links, checking link reliability, checking credits, and monitoring task status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shahruj](https://clawhub.ai/user/shahruj)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to connect an OpenClaw agent to Facticity.AI for claim fact-checking, claim extraction, multimedia transcription, source reliability checks, credit checks, and async task-status monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted claims, text, multimedia links, and source URLs are sent to Facticity.AI using the user's API key.

Mitigation: Avoid confidential documents, secrets, private or signed URLs, and sensitive personal data; review Facticity.AI privacy and retention terms before use with sensitive material.

Risk: Fact-checking and reliability responses can be incomplete or context-dependent.

Mitigation: Review returned evidence, sources, bias metrics, and quality labels before relying on results in high-stakes workflows.

## Reference(s):

- [Facticity.AI App](https://app.facticity.ai)
- [Facticity.AI API Documentation](https://api.facticity.ai/docs)
- [Facticity.AI API Key Page](https://app.facticity.ai/api)
- [ClawHub Skill Page](https://clawhub.ai/shahruj/skills/facticity-ai)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Shell commands, Configuration guidance]

**Output Format:** [JSON API responses and Markdown guidance with shell and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FACTICITY_API_KEY and may return verbatim external API responses.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
