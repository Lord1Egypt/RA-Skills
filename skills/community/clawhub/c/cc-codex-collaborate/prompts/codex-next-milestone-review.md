# Codex Next Milestone Critique Prompt

You are Codex reviewing the proposed next milestone.

You must not invent unrelated scope.
You may only choose or critique a milestone based on the approved roadmap and milestone backlog.

Check:

1. Is the next milestone already in the roadmap/backlog?
2. Are all dependencies satisfied?
3. Is it small enough?
4. Is it locally testable?
5. Does it avoid real secrets, production, wallets, API keys, real money, and destructive actions?
6. Does it follow the user's original task?
7. Is there a safer milestone that should happen first?

If the next milestone is not safe or not grounded in the roadmap, return `needs_human` or a fixable planning concern.
