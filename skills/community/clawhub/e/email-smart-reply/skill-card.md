## Description:

Email Smart Reply (AI-Powered) helps agents classify B2B sales emails, retrieve relevant knowledge-base context, generate draft replies, and route drafts to Discord for human review before sending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjboy007](https://clawhub.ai/user/cjboy007)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and support teams use this skill to draft first responses for B2B electronics manufacturing inquiries, delivery follow-ups, technical questions, partnership messages, and spam triage. It is intended to keep a human reviewer in the loop before outbound email is sent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox and knowledge-base data may be sent through third-party services during classification, reply generation, and review.

Mitigation: Use a contained service account and non-production mailbox first, restrict mailbox and KB scope, and confirm OpenRouter and Discord are approved for the relevant customer data.

Risk: Knowledge-base retrieval includes an unsafe shell-command path reachable from email-derived search text.

Mitigation: Replace string-based shell execution with argument-based process execution, validate query inputs, and test with hostile email content before live use.

Risk: Secrets and mailbox credentials can be exposed through local environment files or logs.

Mitigation: Store secrets in an approved secret manager or protected environment variables, avoid printing .env contents, and redact credentials from test output and logs.

Risk: Drafts, review records, and test reports may retain customer content after processing.

Mitigation: Define retention limits, cleanup jobs, and access controls for drafts, review queues, and integration-test reports.

Risk: Generated replies may contain incorrect product, pricing, delivery, or support statements.

Mitigation: Keep human approval enabled for outbound sends, escalate complaints, and use dry-run testing before processing real customer email.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cjboy007/skills/email-smart-reply)
- [OpenRouter chat completions endpoint](https://openrouter.ai/api/v1/chat/completions)
- [Discord API v10 endpoint](https://discord.com/api/v10/)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command snippets; generated pipeline artifacts are JSON draft, review, and test-result files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces draft email content, intent labels, confidence scores, Discord review payloads, and local review records.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
