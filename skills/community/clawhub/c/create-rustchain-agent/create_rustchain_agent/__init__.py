"""create-rustchain-agent — 60-second onboarding for a RustChain-participating agent.

Scaffolds a working agent project: an Ed25519 RTC wallet, a ready agent.py that
claims the live First-Light newcomer bounty, an MCP config wiring rustchain-mcp,
and printed claude/Cursor/Cline snippets.

Safe by default: scaffolding is LOCAL only (generates files + a wallet). Network
writes (Beacon registration) happen only with --register.
"""

__version__ = "0.1.0"
