# Existing Agentic Checks: temporary compatibility path

Agentic Checks stop running on **2026-12-01**. If a project must continue managing
existing Agentic Checks as code before that date, keep its Checkly CLI dependency
and lockfile on **9.x**. The current CLI does not export `AgenticCheck`; upgrading
that project without migration makes it fail to load. Do not silently upgrade,
remove definitions, or substitute check types on the user's behalf.

Choose the path explicitly:

- **Continue temporarily:** retain the compatible dependency and use the legacy
  documentation matching that installation. The current skill's deployment
  flags, confirmation statuses, and ownership semantics must not be assumed to
  apply to that legacy CLI. Pin the project toolchain; do not rely on an unpinned
  `npx` download or assume a separately installed newer CLI overrides it.
- **Migrate:** obtain approval to replace the checks with `BrowserCheck` or
  `MultiStepCheck` and `aiAutoRepairEnabled: true`. Review the deployment plan and
  resource identities. Removing an old definition can delete its check and run
  history; use the approved preservation/adoption workflow where required.

Remaining on the legacy toolchain does not extend the service's retirement date.

Source: [official Checkly CLI release: AgenticCheck removal](https://github.com/checkly/checkly-cli/releases/tag/10.0.0#agenticcheck-is-removed).
