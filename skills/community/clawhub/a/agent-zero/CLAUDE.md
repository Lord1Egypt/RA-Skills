# AgentZero

Property listing parser — Rust (Axum) backend + React/TypeScript (Vite) frontend.

## Running locally

### Backend
```bash
cd backend
cargo run --release
```
Starts at `http://127.0.0.1:8000`. Creates `backend/listings.db` on first run.

### Frontend (dev server)
```bash
npm --prefix frontend run dev
```
Starts at `http://localhost:5173/`. Proxies `/api/*` to the backend.

### One-command restart scripts
Use these scripts to kill currently running processes, rebuild latest code, and restart fresh instances.

```bash
./scripts/run_backend.sh
./scripts/run_frontend.sh
```

Defaults:
- Backend log: `/tmp/agent_zero_backend.log`
- Frontend log: `/tmp/agent_zero_frontend.log`

## Logs

**Backend log**: `/tmp/agent_zero_backend.log`

Key log patterns to look for when debugging:

| Pattern | Meaning |
|---|---|
| `add_listing: id=N registering 0 image URL(s)` | Parser found no images — likely a sold/off-market listing |
| `redfin::parse: no images in JSON-LD for …` | Redfin sold listing — photos stripped from JSON-LD |
| `Image URL returned error status …` | Image server returned 4xx/5xx — URL probably expired |
| `Failed to download image …` | Network error fetching an image |
| `cache_images: listing_id=N pending=0` | No new images to download (all already cached or none registered) |

## HTML Snapshots

Every time a listing is saved or refreshed, the raw fetched HTML is written to `backend/html_snapshots/` as:

```
{listing_id}_{source}.html   e.g.  42_redfin.html,  42_rew.html
```

Refreshing a listing overwrites the file with the latest fetch. Use these files to:
- Inspect exactly what the parser received
- Re-run or fix the parser locally without re-fetching the URL
- Copy to `backend/src/parsers/fixtures/` (and run the strip tool) to create a test fixture

Optional overrides:
```bash
BACKEND_PORT=8000 LOG_FILE=/tmp/backend.log ./scripts/run_backend.sh
FRONTEND_PORT=5173 LOG_FILE=/tmp/frontend.log ./scripts/run_frontend.sh
SKIP_SAFARI=1 ./scripts/run_backend.sh   # skip Safari, go straight to Chrome CDP
```

## API

Route definitions and handler signatures are the source of truth. See:
- `backend/src/main.rs` — all routes wired up
- `backend/src/api/` — one file per handler group (`add.rs`, `refresh.rs`, `listings.rs`, `details.rs`, `images.rs`, `parse.rs`)

## Tests

```bash
cd backend
cargo test
```

Snapshots live in `backend/src/parsers/snapshots/`. To update them after intentional changes:
```bash
cargo insta review
```

### Stripping HTML fixtures

Parser test fixtures live in `backend/src/parsers/fixtures/`. Raw saved pages can be large (700 KB–1.8 MB). Use the strip tool to remove styles, SVGs, tracking scripts, and other bloat while preserving the elements parsers rely on (JSON-LD, `__NEXT_DATA__`, meta tags, property data scripts, DOM elements used by CSS selectors):

```bash
cd backend
cargo run --bin strip                            # strip all fixtures in-place
cargo run --bin strip -- path/to/file.html       # strip a single file in-place
cargo run --bin strip -- input.html output.html  # strip to a separate file
```

Always run `cargo test` after stripping to verify no parser-relevant content was removed.

## TypeScript Type Bindings

The backend models are annotated with `#[cfg_attr(test, derive(TS))]` (from the [`ts-rs`](https://github.com/Aleph-Alpha/ts-rs) crate). Running `cargo test` regenerates TypeScript reference types into `frontend/src/bindings/`.

These files are committed to git and serve as a **drift-detection signal**: when a Rust model changes, the corresponding file in `bindings/` changes in the git diff, which is your reminder to also update `frontend/src/types.ts`.

The generated files use `bigint` for `i64` (technically correct for Rust), while `types.ts` uses `number` (correct for JSON values). Do **not** import from `bindings/` directly in frontend code — it is reference material only.

**Workflow when changing a backend model:**
1. Update the Rust struct in `backend/src/models/`
2. Run `cargo test` — the file in `frontend/src/bindings/` updates automatically
3. Reflect the change in `frontend/src/types.ts`

## Publishing the Skill to ClawHub

```bash
# Check current published version
clawhub inspect agent-zero

# Publish a new version (bump version as needed)
clawhub publish /Users/yuchen/Projects/AgentZero --slug agent-zero --version 1.1.0
```

Login check: `clawhub whoami`. If not logged in: `clawhub login`.

## Frontend Design

When making layout or styling changes to the frontend, ask if the user would like to load the `frontend-design` skill first (invoke via `/frontend-design`). It provides design thinking guidelines and aesthetic direction to avoid generic UI patterns.

## Coding Conventions

### No code duplication — use shared utilities

Before writing a helper function, check if it already exists elsewhere in the codebase. Shared frontend utilities live in `frontend/src/utils.ts`. Do not copy-paste the same logic into multiple files; extract it to a shared location and import it.

### No hardcoded strings — use named constants

Magic strings that appear in multiple places must be extracted to a named constant and imported from there. This applies to status values, route paths, API keys, and any other string literal that carries semantic meaning.

**Don't:**
```ts
listings.filter(p => p.status === 'Pending')
STATUS_OPTIONS.filter(s => s !== 'Pending')
```

**Do:**
```ts
// constants.ts
export const PENDING_STATUS: StatusOption = 'Pending'

// elsewhere
listings.filter(p => p.status === PENDING_STATUS)
STATUS_OPTIONS.filter(s => s !== PENDING_STATUS)
```

Frontend string constants live in `frontend/src/constants.ts`.

### Rust: prefer named structs over tuples

When a function returns or stores more than one related value, define a small named struct instead of using a tuple. This improves call-site readability and makes fields self-documenting.

**Don't:**
```rust
fn parse_amenity_features(features: &[JsonValue]) -> (Option<i64>, Option<bool>, Option<bool>, Option<bool>) { … }
let (parking, ac, radiant, laundry) = parse_amenity_features(amenities);
```

**Do:**
```rust
struct AmenityFeatures {
    parking_garage: Option<i64>,
    ac: Option<bool>,
    radiant_floor_heating: Option<bool>,
    laundry_in_unit: Option<bool>,
}
fn parse_amenity_features(features: &[JsonValue]) -> AmenityFeatures { … }
let af = parse_amenity_features(amenities);
```

Existing examples in this codebase: `AmenityFeatures`, `AddressInfo`, `SchoolEntry`, `ParsedSource`, `SourceInput` (all in `backend/src/parsers/`).

### Rust: prefer functional, immutable data flow

Avoid mutable state and in-place mutation. Prefer constructing new values over modifying existing ones. Mutation makes it easy to forget to update a field (e.g. setting `images` or `open_houses` after mutating a struct), and those bugs are silent — the compiler can't catch them.

**Design for correctness at the type level.** If a type can be constructed in an invalid or incomplete state, make that state unrepresentable. For example, `StoredProperty` (DB row only) vs `Property` (API type with joined `images` + `open_houses`) forces all callers to explicitly provide joined data via `Property::from_stored(stored, images, open_houses)`. Before this split existed, internal helpers would return `Property { images: vec![], open_houses: vec![] }` as placeholders and callers would sometimes forget to repopulate them — causing a bug where `open_houses` always appeared empty in list responses, making every open house look like a new addition in the refresh diff view. The type split made the bug impossible: `StoredProperty` has no `images` or `open_houses` fields, so the compiler rejects any attempt to "construct" a `Property` without explicitly providing both.
