## Description: <br>
Implement secure webhook receivers and senders with proper verification and reliability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carloscbrls](https://clawhub.ai/user/carloscbrls) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design and review secure webhook receivers and senders, including signature verification, replay prevention, idempotency, retry behavior, and delivery tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook logging can expose secrets or personal data if payloads, headers, or response bodies are stored verbatim. <br>
Mitigation: Redact secrets and personal data, restrict log access, and keep retention short. <br>
Risk: Server-resolved GitHub provenance is unavailable for this version. <br>
Mitigation: Verify the publisher profile before relying on provenance-sensitive deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/carloscbrls/cc3po-webhook) <br>
- [Skill homepage](https://clawhub.ai/carloscbrls/webhook) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with implementation checklists and inline code patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executable guidance; no API calls or shell commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
