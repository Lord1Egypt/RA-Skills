# Claude Planning Self Review Prompt

You are Claude Code reviewing your own project plan before asking Codex for adversarial plan review.

Be skeptical. Try to invalidate your own plan.

Check:

1. Did I misunderstand the user's task?
2. Did I skip project discovery?
3. Did I infer something that should be verified from files?
4. Did I ignore existing architecture?
5. Are milestones too large or too vague?
6. Are acceptance criteria testable?
7. Are there hidden secret, wallet, API key, production, real-money, data-loss, or destructive-operation risks?
8. Are there multiple plausible approaches requiring a human choice?
9. Is the test strategy realistic?
10. Would continuing without asking cause product, security, architecture, financial, or data-loss risk?

If human input is needed, produce a question with:

- reason
- 2 to 5 options
- recommended safe default when possible
- Other/free-form option
- consequences

Do not start implementation until this self-review is OK and the Codex plan review passes.
