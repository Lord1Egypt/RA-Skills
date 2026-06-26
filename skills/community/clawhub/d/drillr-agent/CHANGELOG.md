# Changelog

All notable changes to this skill are tracked here. The skill version
tracks the Drillr External API version it was written against.

## [1.0.0] — 2026-04-23

Initial release. Complete rewrite of the earlier repository contents.

### What's covered

- **Three channels**: MCP (Streamable HTTP), REST, CLI — all accept
  the same `drl_*` API key
- **Dual onboarding paths**:
  - Path A (indirect): IM / web-chat / remote-host agents; user
    pastes key into chat, agent persists to
    `~/.config/drillr/config.json` (mode `0600`)
  - Path B (direct): co-located terminal; three equivalent sub-paths
    (MCP via Claude Code, `drillr-cli`, REST + env var)
- **Nine capabilities**: `search`, `signals`, `article_list`,
  `article_get`, `watchlist_list`, `watchlist_create`, `watchlist_add`,
  `watchlist_remove`, `watchlist_delete`
- **Frontmatter compatible with both** Anthropic Agent Skills and the
  clawhub / openclaw skill format (same `SKILL.md`, different consumers)
- **Example MCP configs** for Claude Code, OpenClaw, Hermes
- **Copy-paste user-onboarding prompts** in
  `examples/user-onboarding-script.md`

### Deliberately not covered

- OAuth 2.1 flow for MCP (browser callback is incompatible with
  remote-host deployments; token TTL is a moving target in the
  client ecosystem)
- Helper scripts wrapping the API — the earlier revision shipped a
  Python wrapper, but that coupling is what rots first when the API
  evolves. Agents should call MCP / REST / CLI directly.

### API version

Tracks Drillr External API **v1** (2026-04). Breaking changes will
ship under `/api/v2/*` alongside `/api/v1/*`; this skill will bump
its minor version when v1 gains non-breaking additions, and bump
major when switching to v2.
