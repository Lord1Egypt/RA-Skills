---
name: bili-rs
metadata:
  openclaw:
    intent: personal-cli-tool
    domain: bilibili-api-client
description: >
  Development skill for bili-rs, a Rust CLI tool for Bilibili (B站). Use when implementing
  features, fixing bugs, or extending the bilibili-cli-rust codebase. Provides architecture
  conventions, API endpoints, coding patterns, and project-specific constraints. Triggers on
  tasks involving adding CLI commands, calling Bilibili APIs, handling authentication,
  implementing output formatting, or working with the layered cli/commands/client/payloads
  architecture.
---

# bili-rs Development Skill

Rust rewrite of [bilibili-cli](https://github.com/jackwener/bilibili-cli). Single binary, no runtime deps. Full feature parity with the Python original.

## Architecture (strict layering)

```
cli/ (clap structs only)  →  commands/ (business logic)  →  client/ (HTTP async fn)
                                      ↓
                               payloads/ (normalize raw JSON → structs)
                                      ↓
                               formatter.rs (JSON/YAML/Rich output)
```

**Rules:**
- `cli/` — clap derive structs only, zero business logic
- `commands/` — calls `client/`, never builds HTTP requests directly
- `client/` — never imports clap or formatter

## Adding a New Command

1. Add clap struct in `src/cli/<domain>.rs`
2. Add handler in `src/commands/<domain>.rs`
3. Add API call(s) in `src/client/<domain>.rs`
4. Add payload normalizer in `src/payloads/<domain>.rs` if needed
5. Wire into `src/main.rs` `run()` match arm

## Key Patterns

### Error handling
```rust
// client/ layer: always map API errors
let code = body["code"].as_i64().unwrap_or(-1);
if code != 0 {
    return Err(map_api_error(code, body["message"].as_str().unwrap_or("unknown")));
}

// commands/ layer
match result {
    Ok(data) => formatter::output(data, format),
    Err(e) => { emit_error(&e, format); std::process::exit(1); }
}
```

### Output envelope (never change the field names)
```rust
SuccessEnvelope { ok: true, schema_version: "1", data: T }
ErrorEnvelope   { ok: false, schema_version: "1", error: ErrorBody }
```

### Output format resolution
```rust
--json > --yaml > $OUTPUT env var > TTY→Rich / non-TTY→YAML
```

### Authentication levels
- `Optional` — load saved creds if available, don't fail if missing
- `Read` — requires SESSDATA
- `Write` — requires SESSDATA + bili_jct

Credential file: `~/.bilibili-cli/credential.json` (0o600, 7-day TTL)

## WBI Signature

Some Bilibili endpoints require a WBI request signature (a per-request HMAC-like parameter). Use `src/client/wbi.rs`:
```rust
let (img_key, sub_key) = fetch_wbi_keys(cred).await?;
let params = sign_params(vec![("bvid".to_string(), bvid)], &img_key, &sub_key);
req = req.query(&params);
```

Known endpoints needing WBI: `/x/web-interface/view/conclusion/get`

## Output & Terminal

- Status/errors → **stderr** with `console::style`
- Data → **stdout** as table (`comfy-table`) or JSON/YAML
- Counts ≥ 10000 → `"X.X万"` format

## Quality Gate (run before every commit)

```bash
cargo build && cargo clippy -- -D warnings && cargo fmt --check && cargo test
```

## References

- **All CLI commands & options**: See [references/commands.md](references/commands.md)
- **API endpoints & payloads**: See [references/api.md](references/api.md)
- **Full project spec**: `PRD.md` in project root
- **Implementation conventions**: `CLAUDE.md` in project root
