## Description:

aispace helps agents use the aispace CLI for temporary artifact storage, expiring shares, encrypted transfers, trusted agent handoffs, identity workflows, quota checks, and recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aispace-sh](https://clawhub.ai/user/aispace-sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a task needs remote artifact storage or encrypted delivery through aispace, including public shares, sealed transfers, pinned agent inbox delivery, handoff, recovery, and quota-aware uploads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create public links, transfer tokens, or recipient deliveries that expose artifact access when used broadly.

Mitigation: Confirm before creating public links, deleting files, or sending to recipients; prefer short expiries, download caps, pinned recipients, and private storage unless public access is requested.

Risk: AISPACE_KEY, bearer URLs, sealed tokens, owner tickets, age identities, and private identity records are credentials with different scopes.

Mitigation: Keep secrets out of chat, logs, screenshots, shell history, and normal JSON output; use protected files, prompts, or secret environment variables.

Risk: Revocation, expiry, or deletion cannot recall bytes already downloaded.

Mitigation: Use distinct links per recipient, verify intended access before sharing, and communicate effective expiry and download caps from the service response.

Risk: Client-side encryption does not by itself prove sender identity.

Mitigation: Use verified recipient pins and out-of-band fingerprint checks for trusted delivery, and do not equate unknown valid signatures or processed receipts with trusted sender identity or downstream correctness.

Risk: The aispace CLI dependency performs remote storage and transfer actions.

Mitigation: Install this skill only for aispace workflows and consider pinning or reviewing the @aispace-sh/cli package before using it in sensitive environments.

## Reference(s):

- [Secure workflow reference](references/secure-workflows.md)
- [aispace homepage](https://aispace.sh)
- [ClawHub skill page](https://clawhub.ai/aispace-sh/skills/aispace)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline shell commands and structured command-output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include artifact IDs, transfer IDs, selected workflow, encryption status, expiry, download caps, and public URLs only when deliberately created.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
