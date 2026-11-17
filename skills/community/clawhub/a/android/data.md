# Data — Room, DataStore, Files, and Scoped Storage

Three storage decisions cover almost everything: structured data goes in Room, small key-values go in DataStore, and bytes go in a file whose location decides who can read it and when it disappears.

**Contents:** [Choosing a Store](#choosing-a-store) · [Room](#room) · [Migrations](#migrations) · [Query Performance](#query-performance) · [DataStore](#datastore) · [Files and Scoped Storage](#files-and-scoped-storage) · [Encryption at Rest](#encryption-at-rest) · [Backup and Data Extraction](#backup-and-data-extraction) · [Data Traps](#data-traps)

**Before designing storage**, read `## App Context` in `~/Clawic/data/android/memory.md` and open any `artifacts/` file its `## Boxes` index names for schema or migration decisions. A migration strategy that was already chosen and half-implemented is the worst thing to re-decide.

## Choosing a Store

| Need | Store | Switch when |
|---|---|---|
| Structured, queried, related data | Room | Never for this shape — a JSON blob in preferences is a database with no query engine |
| A handful of settings and flags | DataStore (Preferences) | The values become related enough to query (→ Room) |
| One typed settings object | DataStore (Typed, with a serializer) | — |
| Files the app owns: caches, downloads, generated media | App-specific internal or external directories | The user must see the file in a gallery or a file manager (→ MediaStore or SAF) |
| Media the user should keep after uninstall | MediaStore | The file type is not media (→ Storage Access Framework) |
| A file the user picks or the app writes anywhere | Storage Access Framework | — |
| Credentials | Nowhere in app storage — the OS keystore or a server-issued short-lived token | Never (`security.md`) |

`SharedPreferences` is the legacy of the second row: it loads the whole file into memory on first access, `commit()` blocks the calling thread on disk, and `apply()` still blocks the main thread at certain lifecycle points. DataStore exists because of that; new code has no reason to use it, and a migration path from it is built in.

## Room

- Entities, DAOs, and a database class. Suspend DAO functions run off the main thread automatically; DAO functions returning `Flow` emit again whenever the queried tables change — that reactivity is the reason to read from the database rather than from the network (`architecture.md`).
- Room throws when queried on the main thread. `allowMainThreadQueries()` exists for tests; enabling it in an app converts the crash into an ANR (SKILL.md Rule 5).
- A `Flow` DAO query re-emits on *any* write to the tables it touches, not only to matching rows. A screen observing a broad query in a write-heavy app re-renders constantly; narrow the query or add `distinctUntilChanged`.
- `@Transaction` on a DAO method with relations, or on any read-then-write sequence — without it, a concurrent write lands between the two halves.
- Relations (`@Relation`) issue additional queries under the hood, which is fine for a detail screen and a disaster inside a list; for lists, project exactly the columns the row shows into a small POJO.
- Type converters keep the schema simple, but a converter that serializes a list into a string creates a column you can never query. If you need to filter by it, it is a table.

## Migrations

- Every schema change needs a migration, and the schema JSON must be exported (the schema directory is a build setting) — automated migrations and migration tests both read it.
- Automated migrations handle additive and renaming changes declaratively; anything that transforms data still needs a hand-written migration with SQL.
- **`fallbackToDestructiveMigration()` in a shipped build deletes the user's data on any unmatched version change.** It belongs in debug builds only. The failure is silent: the app works perfectly, the user's content is simply gone.
- Test every migration: the migration test helper opens the old schema, inserts representative rows, runs the migration, and asserts the data survived. A migration that compiles is not a migration that works.
- Migrations are cumulative and must chain from any shipped version. A user who skipped four releases runs four migrations in order — never assume they came from the previous one.
- A destructive change that cannot be migrated (splitting a column into a new table with derived values) is still a migration: create, backfill with SQL, drop. Doing it in Kotlin after opening the database means running it on partially-migrated data.

## Query Performance

- Index the columns used in `WHERE`, `JOIN` and `ORDER BY`. An unindexed lookup on a table of a few hundred rows is invisible; on a few hundred thousand it is a frame drop and then an ANR.
- Room emits a warning for a query that will full-scan; treat it as an error. `EXPLAIN QUERY PLAN` on the raw SQL confirms whether the index is used — an index on `(a, b)` serves a query filtering `a`, and does nothing for one filtering only `b`.
- Indexes cost write time and space. Index what you query, not every column.
- Batch inserts inside one transaction: inserting a thousand rows one at a time means a thousand transactions, and it is roughly two orders of magnitude slower.
- Paging for lists that can grow without bound — loading ten thousand rows to show twelve is both a memory and a startup problem.

## DataStore

- Preferences DataStore is key-value with no schema; Typed DataStore takes a serializer and gives compile-time safety. Both are flow-based and asynchronous end to end, which is why neither can block the main thread.
- Reads are a `Flow`; the first emission requires a disk read, so a screen that gates its first frame on a DataStore read has added disk I/O to startup. Read it before you need it, or render with a default and update.
- Writes are atomic and serialized through an updater lambda: read-modify-write inside the lambda, never read outside and write inside.
- Handle `IOException` in the read flow — a corrupted file otherwise crashes on every launch, with no way out except clearing app data.
- One DataStore instance per file, created once at application scope. Two instances on one file corrupt each other, and the framework says so at runtime.

## Files and Scoped Storage

| Location | Permission | Visible to user | Deleted on uninstall |
|---|---|---|---|
| Internal files dir | None | No | Yes |
| Internal cache dir | None | No | Yes — and the system may delete it under storage pressure |
| App-specific external dir | None (since API 19) | Via a file manager, mostly | Yes |
| MediaStore collections | None to write your own media; per-type read permission or the photo picker to read others' | Yes, in the gallery | No |
| Anywhere via SAF | None — the user grants per-URI | Yes | No |

- Scoped storage means broad filesystem access is gone. The three legitimate routes are the app's own directories, MediaStore for media, and SAF for user-chosen locations. `MANAGE_EXTERNAL_STORAGE` is a policy-restricted permission granted to file managers and backup apps, and requesting it without qualifying is a rejection (`play-console.md`).
- The **photo picker** requires no permission at all and returns exactly the items the user chose. For "let the user attach a photo", it is strictly better than requesting media permissions (`permissions.md`).
- Sharing a file with another app: a `FileProvider` content URI plus a granted read permission on the intent. A raw `file://` URI throws since targetSdk 24.
- SAF URIs are revocable; persist them with a persistable permission grant if the app must reuse one later, and handle the revocation case rather than crashing.
- Cache directory content can vanish at any time. Anything that must survive is not a cache, whatever the directory is called.

## Encryption at Rest

- Full-disk / file-based encryption is on by default on modern devices when the user has a screen lock — that covers the "stolen phone" threat for most apps, and it is the reason blanket app-level encryption is often ceremony.
- What genuinely needs more: data that must be unreadable to another process with root, or that has a regulatory requirement. Then the key lives in the Android keystore (hardware-backed where available, optionally requiring user authentication) and encrypts the payload; the key never leaves the keystore and never enters a file under `~/Clawic/data/`.
- Encrypted databases (a SQLCipher-style layer) cost query performance and complicate migrations and debugging. Take the cost deliberately, and write the reason down in an artifact.
- Whatever the scheme: the passphrase is not in the APK, not in `BuildConfig`, not derived from a constant (SKILL.md Rule 7).

## Backup and Data Extraction

- `android:allowBackup` defaults to true, so app data leaves the device through cloud backup and device-to-device transfer unless restricted. Anything sensitive — tokens, cached personal data, an offline database of someone else's information — should be excluded.
- Modern targets use `dataExtractionRules` with separate rule sets for cloud backup and device transfer; older ones use the full-backup content rules. Ship both while `min_sdk` spans the boundary.
- A restore delivers old data into a new install with a new signing state and possibly a new server-side session. Handle "restored data references a session that no longer exists" explicitly, or the first launch after a device transfer crashes.
- Test restore at least once before relying on it, and note the result — an untested backup configuration is a claim, not a feature.

## Data Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| `fallbackToDestructiveMigration()` in release | Silently deletes user data on any schema change | Real migrations, tested; destructive fallback in debug only |
| `allowMainThreadQueries()` | Converts a loud crash into an ANR | Suspend DAOs and flows |
| JSON blob in preferences instead of a table | Unqueryable, unmigratable, and rewritten whole on every change | Room |
| Storing a list in a Room column via a converter, then needing to filter by it | The column cannot be queried | A related table |
| No index on a `WHERE` column | Fine in testing, an ANR at real data volume | Index what you query; confirm with the query plan |
| Reading DataStore outside the updater and writing inside | Lost updates under concurrency | Read-modify-write inside the lambda |
| Treating the cache directory as storage | The system deletes it under pressure, without warning | Files directory for anything that must persist |
| Requesting broad storage permissions for an attachment flow | Rejection risk and a permission dialog users decline | Photo picker or SAF, no permission |
| Leaving `allowBackup` at its default with sensitive data | The data leaves the device by design | `dataExtractionRules` with explicit exclusions |
| Migrating data in Kotlin after opening the database | Runs against a partially migrated schema | Do it in the migration's SQL |

## Write Down What It Was

- **A schema or migration decision, and the SQL that finally worked**, is `artifacts/<kebab-name>.md` with its `## Boxes` line reading "read before touching the schema" — migrations are re-derived at exactly the wrong moment otherwise (`memory-template.md`).
- **A data-loss incident** (a destructive fallback, a failed restore, a corrupted DataStore) is a line in `## Pain Points` of `~/Clawic/data/android/memory.md` with the date and the cause.
- **An encryption or backup-exclusion decision** goes in the same artifact family, because it is also the answer to a Play data-safety question later (`play-console.md`).
