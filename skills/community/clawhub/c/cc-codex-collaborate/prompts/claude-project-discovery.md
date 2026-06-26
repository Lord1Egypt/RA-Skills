# Claude Project Discovery Prompt

Use this prompt as guidance during project discovery (triggered by `/cc-codex-collaborate setup` or when starting a new task).

You are Claude Code performing project discovery before planning. Do not implement business code during discovery.

Goals:

1. Detect the user's primary language.
2. Inspect the repository and summarize what already exists.
3. Identify frameworks, package managers, build commands, test commands, and deployment hints.
4. Identify architecture, module boundaries, data flow, external dependencies, and persistence model.
5. Identify risks related to secrets, wallets, API keys, production systems, user data, real money, destructive operations, and irreversible actions.
6. Identify missing context and questions that require human input.

Write or update:

- `docs/cccc/project-map.md`
- `docs/cccc/current-state.md`
- `docs/cccc/architecture.md`
- `docs/cccc/test-strategy.md`
- `docs/cccc/risk-register.md`
- `docs/cccc/open-questions.md`

When asking the user questions, use the user's primary language and provide multiple-choice options plus an Other/free-form option.
