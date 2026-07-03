# Example Candidate Flow

User asks:

> Help me join Cruit and publish a candidate profile.

Expected agent behavior:

1. Fetch the latest instructions from `https://cruit.dev/skills/candidate/INSTRUCTIONS.md`.
2. Explain the 7-step setup map.
3. Start Cruit browser device auth.
4. Ask which project folders the user approves for review.
5. Ask for an optional resume.
6. Ask brief fit/preference questions.
7. Draft a profile from approved metadata and resume facts.
8. Show the full draft in chat.
9. Publish only after approval.
10. Ask before setting up weekly refresh.

The agent should emphasize that Cruit publishes metadata and profile text, not source
code, secrets, private keys, or contact details.

