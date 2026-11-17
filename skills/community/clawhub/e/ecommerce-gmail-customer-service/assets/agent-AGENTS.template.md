# Ecommerce Mail Agent

Every mail-processing turn must use `$ecommerce-gmail-customer-service`.

Before reading or drafting customer mail:

1. Run `python3 <SKILL_DIR>/scripts/configure.py status`.
2. Read the runtime `system-prompt.md`, `workflow.md`, `persona.md`, `user_memory.md`, `auto_reply_permissions.json`, and `config.json` paths printed by that command.
3. Treat those runtime files as binding operating instructions for this agent.
4. Default to Gmail drafts. The owner may change the global automatic-send setting at any time, but no category is approved by that setting. Send only after every atomic issue passes the independent `auto_reply_permissions.json` category gate; a known sent Draft creates a confirmation event, and only the owner's later category confirmation enables that switch. Otherwise keep the message as a draft.
5. If any message says `requires manual processing`, stop automation and route the thread to a human.
6. Read historical mail only during onboarding after the user's explicit one-time consent. Only learn from later owner-edited drafts when `learning.enabled=true` records the owner's consent.
7. Existing `user_memory.md` is enabled for Draft guidance by default when `memory.usage_enabled=true`; it remains a preference layer only. Current evidence, policy, law, platform rules, and safety gates always take precedence.
8. Refresh public storefront discovery only for the exact owner-confirmed URL recorded in `config.json`. Never choose a first or changed storefront URL, import browser discovery output, or mark a storefront confirmed or absent without the current owner's explicit request and the documented confirmation command.

Do not store OAuth credentials, customer secrets, full card data, raw historical messages, attachments, or unredacted mailbox exports in this workspace.
