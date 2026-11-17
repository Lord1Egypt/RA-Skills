# Contributing

Thanks for helping improve the DomainHelp DNS skill docs.

This repository is a public mirror generated from the deployed DomainHelp DNS skill documentation. Maintainers should update DomainHelp first, deploy those docs, then regenerate this mirror with the private local sync utility.

Community contributions are welcome as issues or pull requests. If a pull request edits generated files directly, maintainers may translate the suggested change back into DomainHelp before regenerating the mirror.

## Style

- Keep skill documents concise and agent-actionable.
- Prefer stable `/api/v1/...` execution endpoints over browser form routes.
- Include input contracts, output contracts, error behavior, auth and rate-limit notes, examples, and related skills.
- Avoid examples that depend on private credentials or private infrastructure.
