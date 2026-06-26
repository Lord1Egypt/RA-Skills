## Description: <br>
Expert AI agent for designing email intelligence pipelines that turn raw email into structured, reasoning-ready context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouqkt](https://clawhub.ai/user/zhouqkt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan email ingestion, thread reconstruction, deduplication, participant extraction, retrieval, and context assembly pipelines for AI agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email processing can expose sensitive mailbox content, personal data, attachments, or cross-tenant information. <br>
Mitigation: Confirm mailbox authorization, use least-privilege scopes, isolate tenants, redact sensitive data where appropriate, and avoid logging raw message bodies or attachments. <br>
Risk: Incorrect thread reconstruction or quoted-text handling can misattribute action items, decisions, or participant intent. <br>
Mitigation: Preserve message headers and participant identity through the pipeline, cite source messages, and review ambiguous or malformed threads before relying on extracted decisions. <br>
Risk: Unclear retention and deletion behavior can create compliance and privacy exposure for processed email data. <br>
Mitigation: Define retention windows, deletion workflows, and monitoring practices before connecting real mailboxes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhouqkt/agency-email-intelligence-engineer) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration, markdown] <br>
**Output Format:** [Markdown guidance with code examples and structured output patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only guidance; no runtime dependencies or required binaries are disclosed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
