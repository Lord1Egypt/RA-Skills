# Example Recruiter Flow

User asks:

> Find me full-stack TypeScript developers who have shipped AI tooling recently.

Expected agent behavior:

1. Fetch the latest instructions from `https://cruit.dev/skills/recruiter/INSTRUCTIONS.md`.
2. Explain the 7-step recruiter flow.
3. Start Cruit browser device auth.
4. Check recruiter access and available contact credits.
5. Ask for optional company or role context.
6. Translate the hiring need into explicit search filters.
7. Show the filters before searching.
8. Present low-PII candidate cards.
9. Ask before revealing contact info or sending a message.
10. Show exact message text before sending.

The agent should not reveal contact details, spend credits, or send messages without
explicit approval.

