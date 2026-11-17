# Threat model

What `apple-photos-cleaner` trusts, what it doesn't, and what stops each failure. Read this
before adding a command that takes new input or performs a new kind of mutation.

## What we protect

In priority order:

1. **The Photos library.** `Photos.sqlite` must never be written. A corrupted library can
   cost a user every photo they own.
2. **The user's photos.** No asset leaves the library or moves to Recently Deleted unless the
   user saw that exact set and approved it.
3. **The user's files.** Exports land only inside the directory the user named.
4. **The user's privacy.** Faces, places and names stay on the machine. Nothing goes over the
   network.

## Actors

| Actor | Trust | Notes |
| --- | --- | --- |
| The user | Trusted | Runs the CLI, approves mutations |
| An AI agent driving the skill | **Partially trusted** | Acts for the user, but it can misread intent, hallucinate flags, or be prompt-injected by content it read elsewhere. It must not be able to approve a mutation by itself |
| `Photos.sqlite` contents | **Untrusted data** | Filenames, album titles, person names and captions come from imports, shared libraries and other people's devices. Treat them as attacker-controlled strings |
| Photos.app / AppleScript | Trusted executor | Does what the generated script says. The danger is in what we generate |
| The local filesystem | Trusted, but racy | Symlinks inside `--output-dir` can point anywhere |

## Trust boundaries and mitigations

### 1. Database access

| Threat | Mitigation | Where |
| --- | --- | --- |
| A bug writes to `Photos.sqlite` | Connections open with `?mode=ro` | `connect_db` in [`scripts/_common.py`](../scripts/_common.py) |
| A misopened connection (wrong URI, future refactor) still allows writes | A SQLite authorizer (`_deny_writes`) allows only reads and the `table_info` pragmas. Every other statement fails to prepare (T1.20) | `connect_db`; `TestReadOnlyGuard` |
| A lock collides with Photos.app | `timeout=5` busy wait; read-only means we never take a write lock | `connect_db` |
| A second Photos database (the search index `database/search/psi.sqlite`, read for scene labels on macOS 26) is written or its private FTS5 tokenizer invoked | Opened with the same `connect_db` (`mode=ro` + authorizer); the schema registry never connects to its virtual tables | `_scenes.SearchIndex`; `test_scene_search_index.py` |

### 2. SQL built from user input

| Threat | Mitigation | Where |
| --- | --- | --- |
| `--person`, `--album`, search terms injected into SQL | Bound parameters (`?`), never string formatting | `scene_search`, `smart_export`, `face_quality` |
| `--year` injected into a `strftime` comparison | `validate_year` accepts only `\d{4}` | `_common.py` |
| `LIMIT` injection | `build_asset_query` casts with `int()` | `_common.py` |

Covered by `TestSqlInjection` in [`tests/test_security.py`](../tests/test_security.py).

### 3. AppleScript generation (mutating commands)

`cleanup_executor` and `smart_export` build AppleScript from database strings and run it with
`osascript`. This is the highest-risk boundary.

| Threat | Mitigation | Where |
| --- | --- | --- |
| A filename containing `"` or `\` closes the string literal and injects AppleScript | `escape_applescript` escapes backslashes first, then quotes | `_common.py` |
| A filename collision trashes or exports the wrong photo | Assets are addressed by `ZUUID` (`<UUID>/L0/001`), never by filename. The resolved item's filename is cross-checked against `ZASSET.ZFILENAME`, and on a mismatch the item is skipped. The `original_filename` shown to people is display-only and never feeds the cross-check | `build_identifier_lists`, `generate_trash_applescript`; `test_applescript_identity_still_uses_the_storage_name` |
| A schema without `ZUUID` falls back to filename matching | `require_uuid_support` refuses to run | `_common.py` |
| One bad item shifts the id/name pairing | The id and name lists are positional and built together; an item with no UUID aborts the build | `build_identifier_lists` |

Covered by `TestAppleScriptEscaping`, including a real `osascript` round trip on macOS.

### 4. Approval of mutations

| Threat | Mitigation | Where |
| --- | --- | --- |
| A mutation runs without the user seeing what it does | Both commands only preview unless given the preview's token: `cleanup_executor --execute --confirm <token>`, `smart_export --confirm <token>`. The JSON preview lists every asset; the human plan for `smart_export` shows folder totals | `cleanup_executor`, `smart_export` |
| An agent approves for the user (piping `yes`, passing `--yes`) | The preview emits a token (`plan_token`) hashed from the exact asset UUIDs and selection options, and executing requires `--confirm <token>`. A changed set invalidates it (exit 11). There is no interactive prompt to satisfy (T1.19) | `cleanup_executor`, `smart_export`; `TestCleanupConfirmation`, `TestExportConfirmation` |
| A runaway deletion | **Partial.** `--limit` defaults to 500 and must be a positive integer; a negative value used to reach SQLite as "no limit". It is still caller-controlled, so an agent can raise it, but the token then covers that larger set and the user sees its size. Deleted items go to Recently Deleted, recoverable for 30 days. *Planned:* a hard per-run cap and a cool-down (T1.21) | `cleanup_executor`; `TestCleanupConfirmation` |

A token proves the agent ran the preview, not that the user read it. SKILL.md tells agents to
pass `--confirm` only after the user says yes. The token makes sure that what runs is what was shown.

### 5. Filesystem writes (`smart_export`)

| Threat | Mitigation | Where |
| --- | --- | --- |
| A person or album name such as `../../etc` escapes `--output-dir` | `sanitize_folder_name` strips separators, dots and reserved characters | `_common.py` |
| A symlinked subfolder points outside, or at a sibling sharing a prefix (`/out-evil`) | `realpath` + `commonpath` containment check before every export | `export_with_applescript` |

Covered by `TestPathSafety`.

**Known gap (TOCTOU):** the containment check runs before the folder is created and handed to
Photos.app. Something that swaps the folder for a symlink in that window can still redirect the
export. Exploiting it needs a local process racing the export inside a directory the user chose,
which is outside the actor model above (see *Out of scope*), so it is documented rather than
fixed. Exporting into a directory only the user can write is the mitigation.

### 6. Output and privacy

| Threat | Mitigation |
| --- | --- |
| A library string (album title, filename, name) such as `=HYPERLINK(...)` runs as a formula when a `--format csv` report is opened in a spreadsheet | CSV text cells starting with `= + - @`, tab or CR are prefixed with `'`; real numbers are untouched, and JSON/Markdown aren't affected (`_csv_cell`; `TestCsvInjection`) |
| Data leaves the machine | No network code anywhere in the core. Any network feature must be opt-in and listed in SKILL.md's Privacy section |
| Sensitive results (home location, faces) end up in agent transcripts | Aggregate by default; see the roadmap's privacy-proportional principle and T2.10 |
| Personal names in shipped docs | `tests/test_no_personal_refs.py` |

## Out of scope

- A malicious local process with write access to `~/Pictures` (it can edit the library directly) or to the export directory (it can race the containment check).
- A compromised Photos.app or `osascript`.
- Supply-chain attacks on the dev toolchain. The core is stdlib-only with no runtime
  dependencies; CI actions are SHA-pinned (T0.6); release provenance is T0.7.

## When you change something

- **New input reaching SQL:** bind it, and add a case to `TestSqlInjection`.
- **New string reaching AppleScript:** pass it through `escape_applescript`, and add a case to
  `TestAppleScriptEscaping`.
- **New filesystem write:** sanitize the name, check containment, and add a case to `TestPathSafety`.
- **New mutation:** preview first, address by UUID, bound the count, and update this file.
