# Communication topology and reliability

Choose the smallest topology that preserves accountability:

- One agent, one inbox: a single durable identity serves one agent role.
- Specialist identities: separate inboxes make ownership, policy, and audit trails explicit.
- Shared human review: agents create drafts; a human-approved application sends them.
- A2A directory: publish capabilities and contact policy, then discover identities before direct exchange.

For reliable delivery, assign a stable idempotency key before the first write, store the returned resource ID, and reconcile by that ID after a timeout. Webhook consumers should verify the unmodified request, deduplicate by event ID, durably enqueue, then acknowledge. Realtime consumers should advance cursors only after durable processing.

Human approval establishes who may use an identity. It does not authorize every future recipient, attachment, or action. Apply current-turn intent and application policy at each consequential boundary.
