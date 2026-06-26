# Ghostclaw Agent Guidelines

## Project Structure

This project follows a modular architecture. Please respect the separation of concerns:

- `src/ghostclaw/core/`: Core analysis orchestration, metrics, and rule validation.
  - `adapters/`: Scoring and analysis plugins (e.g., Lizard).
- `src/ghostclaw_mcp/`: Model Context Protocol (MCP) server implementation.
- `src/ghostclaw/lib/`: Shared utilities (Caching, GitHub integration, Notifications).
- `src/ghostclaw/stacks/`: Tech-stack specific analysis strategies (Python, Node.js, Go).
- `src/ghostclaw/cli/`: Command-line interface logic.
- `src/ghostclaw/core/bridge.py`: JSON-RPC 2.0 bridge server for IDE/UI integration.

## Extensibility & Hooks

Ghostclaw uses **pluggy** for a decoupled adapter system.

- **Scoring Adapters**: Implement `ghost_analyze` to return architectural metrics.
- **Vibe Computation**: Use `ghost_compute_vibe` to provide custom scoring logic based on gathered metrics.

## Scoring & Metrics

The default `LizardScoringAdapter` uses a weighted formula:

- **Nesting Depth (ND)**: 50% weight. Focuses on cognitive debt.
- **Cyclomatic Complexity (CCN)**: 30% weight. Focuses on logic branching.
- **Lines of Code (LoC)**: 20% weight.
- **Hotspot Penalties**: Extreme nesting (>8) or high CCN (>25) trigger a -10 point penalty.

## Bridge Protocol

The bridge provides a JSON-RPC 2.0 interface (via `GhostBridge`).

- **Methods**: `status`, `plugins`, `analyze`, `ping`.
- **Compliance**: Supports batch requests and standard error codes.

## Configuration Precedence

Ghostclaw resolves settings in this order (highest to lowest):

1. **CLI Flags** (e.g., `--use-ai`, `--no-ai`).
2. **Environment Variables** (prefixed with `GHOSTCLAW_`).
3. **Local Config** (`<repo>/.ghostclaw/ghostclaw.json`).
4. **Global Config** (`~/.ghostclaw/ghostclaw.json`).

## Coding Conventions

- **Encoding**: Always use `utf-8` when opening files.
- **Timestamps**: Use UTC ISO format with a 'Z' suffix.
- **Error Handling**: Use structured reporting via `ArchitectureReport` model.
- **Hashing**: Use SHA256 for fingerprints, not MD5.

## Testing

- Run tests from the root using `python3 -m pytest`.
- Integration tests are located in `tests/integration/`.
- Unit tests are located in `tests/unit/`.
