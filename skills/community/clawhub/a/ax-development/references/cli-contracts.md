# CLI Contracts for Agent Consumption

## Output Format

### Machine-First Default

CLIs consumed by agents must default to machine-readable output.
Human-readable mode is opt-in.

```bash
# Default: JSONL (one JSON object per line)
mytool run vault.md --target "Deploy"
# → {"event":"step_start","target":"Deploy","timestamp":"..."}
# → {"event":"step_done","target":"Deploy","success":true,"durationMs":1234}

# Opt-in human mode
mytool run vault.md --target "Deploy" --human
# → ✅ Deploy completed in 1.2s
```

### JSONL Event Schema

Every line is a self-contained JSON object with at minimum:

```json
{
  "event": "string (required — event type discriminant)",
  "timestamp": "string (ISO-8601, required)"
}
```

Additional fields are event-specific. Use consistent key names across event types.

### Stable Keys

Once a key is emitted, it's part of the contract. Renaming or removing keys is a breaking change.

Document all event types and their keys:

```typescript
// Event types (exhaustive)
type CliEvent =
  | { event: "step_start"; target: string; timestamp: string }
  | { event: "step_done"; target: string; success: boolean; durationMs: number; timestamp: string }
  | { event: "error"; code: string; message: string; timestamp: string }
  | { event: "candidate"; candidateId: string; target: string; confidence: number; validation: ValidationStatus; timestamp: string };
```

## Exit Codes

| Code | Meaning | Agent Action |
|------|---------|-------------|
| 0 | Success | Parse stdout for results |
| 1 | User error (bad input, validation) | Fix input and retry |
| 2 | System error (network, disk, crash) | Report to human or retry with backoff |
| 3 | Approval required (HIL pause) | Present approval to user, continue with flag |

## Interactive vs Non-Interactive

Detect TTY and adjust behavior:

```typescript
const interactive = Deno.stdin.isTerminal();

if (interactive) {
  // Show progress bars, ask confirmations
} else {
  // JSONL only, no prompts, fail on required confirmation
}
```

**Rule:** Never block on stdin in non-interactive mode. If confirmation is required, exit with code 3 and structured output describing what needs approval.

## Flag Conventions

```bash
# Prefer explicit flags over positional args
mytool run --vault vault.md --target "Deploy"  # ✅ Agent can discover flags
mytool run vault.md Deploy                      # ❌ Positional = ambiguous

# Boolean flags: --flag enables, --no-flag disables
mytool run --dry        # Dry run
mytool run --no-cache   # Disable cache

# Key-value: --key value or --key=value
mytool run --inputs '{"days": 7}'
mytool run --inputs @inputs.json    # File reference with @
```

## Versioning

Include version in machine output when format changes:

```json
{"event": "meta", "version": "1.2.0", "outputFormat": "jsonl/v2"}
```

Breaking changes to output format require either:
- A `--output-version` flag
- A major version bump in the tool itself
- A migration period where both formats are emitted

## Error Output

Errors go to stderr in human mode, but in machine mode they're JSONL events on stdout:

```json
{"event": "error", "code": "INVALID_VAULT", "message": "Missing frontmatter in vault.md", "details": {"line": 1, "expected": "---"}, "timestamp": "..."}
```

Never mix free-text errors on stderr with JSONL on stdout in machine mode — agents can't reliably parse both streams.
