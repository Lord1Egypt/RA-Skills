# Security Positioning

## CompleteTech LLC Tone

Use practical, direct, implementation-focused language. The review should help a client understand what the agent can access, what it can do, what can go wrong, who approves risky actions, what evidence exists, and what still needs a decision.

## Guardrails

- Do not claim formal compliance, certification, legal approval, penetration-test completion, production readiness, or guaranteed security without verified evidence.
- Do not invent facts about systems, permissions, incidents, test outcomes, credentials, logs, or approvals.
- Use `TBD` for missing owners, contacts, email addresses, dates, systems, evidence, or decisions.
- Treat secret exposure, missing approval gates, broad production access, sensitive data export, payment actions, and irreversible file/system changes as escalation triggers.
- Keep findings specific: name the workflow, tool, permission, data class, action, evidence, risk, owner, mitigation, and decision needed.

## Human Review Triggers

Recommend human or client approval when the workflow:

- Sends external email, calendar invitations, chat messages, invoices, proposals, contracts, or other client-facing content.
- Reads, writes, deletes, exports, or transforms client data or sensitive business records.
- Can purchase services, issue refunds, change billing, accept terms, or trigger payments.
- Can modify production systems, repositories, deployments, files, permissions, DNS, infrastructure, or user accounts.
- Uses credentials, service accounts, admin scopes, persistent memory, retrieval indexes, or third-party integrations.
- Has unresolved launch blockers, incomplete rollback, missing logs, weak sandboxing, or unclear incident ownership.

## Email And Contact Routing

Security artifacts may name contact roles, but should not invent addresses. Use verified routing from the project record. If unknown, write:

- Security contact: `TBD`
- Client approver: `TBD`
- Technical escalation: `TBD`
- Incident notification: `TBD`
- Billing/legal/support contact: `TBD`

When an artifact concerns email/calendar/file actions, require an approved sender/account, allowed recipient domains, review gate, and escalation contact before enabling automation.
