# Data — JSON, HTTP, Persistence, and Offline

The data layer owns three responsibilities and should own nothing else: talk to the network, keep a local copy, and hand the rest of the app domain objects that never mention JSON (`architecture.md`).

## JSON

- `jsonDecode` returns `dynamic`. Every field access on it is an unchecked runtime cast; a backend that returns `null` where you expected a string throws deep inside the widget tree with no useful stack. Parse into typed models at the boundary, always.
- Hand-written `fromJson` scales to a few dozen models. Past that, generation (`json_serializable`, `freezed`) stops the class of bug where a new field is added to `toJson` and forgotten in `fromJson`. Honor `codegen` from config (SKILL.md Configuration).
- Defensive parsing that matters: `num` vs `int` (a backend that sends `1` where you typed `double` throws on cast — use `(v as num).toDouble()`), dates as strings (`DateTime.tryParse`, not `parse`), enums from strings (map with a documented fallback, never `values.byName` on untrusted input), and missing keys (`json['x'] as String? ?? ''`).
- Parse large payloads off the main isolate (SKILL.md rule 6): `Isolate.run(() => parseUsers(body))` where the function takes the raw STRING and returns the model list, so both the decode and the mapping move (`async.md`). Passing an already-decoded `Map` in defeats the purpose — the expensive part already ran on the UI thread.
- `jsonEncode` on a model needs `toJson`; on an arbitrary object it throws `Converting object to an encodable object failed` — the error names the type, which is the fastest way to find the missing `toJson`.

## HTTP Clients

| Need | Choice | Note |
|---|---|---|
| A handful of endpoints | `package:http` | Minimal; you write the interceptor logic you need |
| Interceptors, cancellation, upload progress, retries | `dio` | `CancelToken` is the only clean cancellation path in Flutter (`async.md`) |
| Typed client generated from an interface | `retrofit` (codegen) | Only with `codegen: allowed` |
| GraphQL | A GraphQL client package | Its cache is a state store — do not also cache the same data yourself |

- **Set a timeout explicitly.** `package:http` has no default request timeout: a request to a black-holed host hangs until the OS gives up, and the user sees a spinner forever. Wrap with `.timeout()` or configure `connectTimeout`/`receiveTimeout` on the client.
- Reuse one `Client` instance for the app. A per-request client opens a new connection each time, loses keep-alive, and must be `close()`d — most code forgets.
- Retry only idempotent requests (GET, PUT, DELETE), with exponential backoff plus jitter, and cap the attempts. Retrying a POST duplicates orders unless the server takes an idempotency key.
- Interceptors are where auth belongs: attach the token, and on a 401 refresh once and retry once. A refresh path without a mutex produces a stampede of refresh calls on the first expired-token screen — serialize it.
- Translate transport errors into domain failures at this boundary: `SocketException` → offline, `TimeoutException` → timeout, 4xx → a typed client error carrying the server's message, 5xx → server failure. The UI should never `catch (DioException)`.

## Local Persistence

| Data | Store | Why |
|---|---|---|
| A few flags, ids, the last-seen version | `shared_preferences` | Key-value, async writes, loaded into memory at startup |
| Tokens, refresh tokens, anything secret | `flutter_secure_storage` | Keychain / Keystore-backed; preferences are plain text on a rooted device |
| Structured rows you query, sort, or paginate | `sqflite`, `drift`, or `isar` | An actual database; `drift` adds type-safe queries and reactive streams |
| Cached images and downloaded files | The filesystem via `path_provider` | Never the database; blobs bloat it and slow every query |
| Large JSON blobs "for now" | Still a database | The blob-in-preferences shortcut is the thing that gets rewritten |

- `shared_preferences` reads the whole store into memory on first access — fine for dozens of small keys, wrong for a cache. Its writes are async and can be lost if the process dies immediately after (`state.md`, app lifecycle: persist on `paused`).
- Anything under `getApplicationDocumentsDirectory()` is backed up by the OS and survives updates; `getTemporaryDirectory()` can be purged at any time. Caches belong in the second, and a cache in the first is a support ticket about storage usage.
- Database migrations need a version number and an upgrade path from every shipped version, not just the last one. Users skip releases. A migration that throws leaves an app that cannot start — wrap it and have a documented "wipe and re-sync" fallback.
- Encryption at rest is a platform feature (`EncryptedSharedPreferences`, SQLCipher) — do not roll your own with a key stored beside the data.

## Caching and Offline

- **Make the local store the source of truth.** The UI reads from the database (ideally as a stream); the network writes into the database. Screens then work offline with no extra code, and there is exactly one place where "the data" lives.
- The alternative — network-first with the cache as a fallback — is simpler for read-only content and forces every screen to handle three states rather than one.
- Cache invalidation needs an explicit policy per resource, written down: TTL (list feeds), ETag/`If-None-Match` (rarely changing documents), or push-driven (server tells you). "Refresh on screen open" is a policy too; it just costs a request per navigation.
- Pagination stores need a cursor, not a page index, when the underlying list can change: page 2 of a shifting list re-shows or skips rows.
- Optimistic updates: write locally, mark the row pending, send, then confirm or roll back. Without the pending marker there is no way to render "not yet saved", and a failed rollback silently loses the user's edit.
- A write queue for offline mutations needs idempotency keys and a bounded retry, or a flaky reconnection replays the whole queue twice.

## Streams from the Database

- Reactive queries (`drift`, `isar`, `sqflite` with a manual notifier) turn "refresh after write" into a non-problem: the write updates the table and every watching screen updates itself.
- Watch narrowly. A stream over the whole table re-emits on any row change; a stream over one query re-emits only when its result set changes.
- Every subscription still needs cancelling in `dispose` (SKILL.md rule 3) — a reactive store makes leaks easier, not harder.

## Files and Uploads

- Large downloads stream to disk; `response.bodyBytes` on a 200 MB file allocates 200 MB. Use a streamed response and write chunks.
- Uploads: multipart with a progress callback (`dio`'s `onSendProgress`), and cancellation wired to the screen's disposal.
- Never assume a picked file path stays valid: on both platforms the picker may hand back a temporary copy that is purged later. Copy into your own directory immediately if you need it after this session.

## Security Notes

- Certificate pinning goes through `HttpClient.badCertificateCallback` or the client's own hook — and `return true` there disables validation entirely. If pinning ships, pin a backup key too, or a certificate rotation bricks every installed app.
- Secrets compiled into the app are readable: an API key in Dart source is extractable from the release binary regardless of obfuscation (`release.md`). Anything that must stay secret lives behind your own backend.
- Log request bodies only in debug builds, and never log tokens: `assert` blocks are stripped in release and are the cheapest way to guarantee that (`release.md`).
