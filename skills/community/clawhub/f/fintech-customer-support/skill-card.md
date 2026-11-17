## Description:

AI-powered customer support agent for fintech and remittance products that handles transfer status lookups, refund requests, account suspensions, KYC document guidance, and complaint escalation across messaging channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gameotivity](https://clawhub.ai/user/gameotivity)

### License/Terms of Use:

MIT-0

## Use Case:

Customer support and operations teams use this agent to triage fintech and remittance support messages, look up transfer, account, and KYC status, attempt permitted refund workflows, escalate complaints, and produce weekly operations digests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive customer, transaction, account, and KYC-related support data.

Mitigation: Define retention, access permissions, redaction rules, and approved storage and transmission destinations before production use.

Risk: Customer messages may be sent to a third-party LLM classifier.

Mitigation: Disable the LLM classifier or explicitly approve it with documented data handling, minimization, and provider controls.

Risk: The workflow examples use shell command patterns with customer-controlled identifiers and references.

Mitigation: Replace shell-string examples with structured tool calls and validate customer IDs, transaction references, and summaries before invoking handlers.

Risk: The release depends on installable package and API/webhook destinations configured outside the skill.

Mitigation: Install only from a trusted, pinned package source and restrict API and webhook endpoints to approved production destinations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gameotivity/skills/fintech-customer-support)
- [Project homepage](https://github.com/nabeel/fintech-support-agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with shell command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Handlers print structured plain text for the agent; weekly digest output is Markdown.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
