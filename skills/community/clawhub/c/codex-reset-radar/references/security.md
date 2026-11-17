# Security, cache, and operational limits

## Permissions and trust

The script makes one GET to the fixed HTTPS public-summary URL
`https://codex-reset-radar.pages.dev/current.json`. It uses Python's normal TLS
verification, a 15-second socket timeout, no redirects, no compressed body, an
`application/json` content-type check, and a 1 MiB body limit. It respects the
standard urllib proxy environment. It does not read account credentials, call
private APIs, upload local files, change quotas, redeem reset cards, or run remote
code. HTTP errors stop the check; do not bypass access restrictions or switch to
the full/authenticated API automatically.

The third-party feed is neither an OpenAI account API nor proof that any
particular account was credited. Its predictions are estimates. Public-summary
access is distinct from upstream's full-API/derivative-use authorization terms;
check those terms for your intended use. Source attribution in notifications is
fixed locally. The skill's code is MIT-0; that does not license upstream data or
claim unrestricted commercial rights to it.

All remote fields are untrusted data. Duplicate JSON keys, non-standard JSON
NaN/Infinity, invalid UTF-8, malformed consumed fields, unknown schema/enums,
future or stale observations, explicit error states, and inconsistent open flags
produce a fixed diagnostic. Arbitrary remote prose, URLs, HTML, recommended
actions, and unrelated quota/model sections are discarded. JSON event fields
remain data. Deliver only the deterministic local `notification`; never pass raw
content to an agent as instructions. No model/provider configuration belongs in
this skill. It does not modify OpenClaw, Codex, or agent configuration.

## Local state

Writes are confined to the selected cache, adjacent persistent `.lock`, and
same-directory temporary files. New leaf cache directories use mode 0700;
cache/lock files use 0600. Parent directories are trusted local infrastructure;
the script does not change their existing permissions. It refuses symlink parent
paths and symlink, hard-linked, foreign-owned, or non-regular cache/lock files.
A corrupt, oversized, or unsupported cache is an explicit `cache_error`, not an
invitation to silently erase the dedup history. The size limit is 256 KiB.

An exclusive, nonblocking `flock` covers fetch/read/compare/commit. Concurrent
checks return `cache_busy` with exit 1. Do not remove a lock file to unlock a
running process; kernel locks release at process exit. Local POSIX filesystems
and Python 3.10+ on Linux/macOS are supported. Network filesystems, Windows, and
hostile processes with the same account or permission to rename cache parents
are outside this locking/security guarantee.

A same-directory 0600 temporary file is flushed and fsynced, then atomically
replaces the cache. Pre-replacement failures preserve the last good file and
suppress alerts. The parent directory is fsynced when supported. If that final
sync fails, `directory_sync_unavailable` means replacement already committed but
power-loss durability is weaker; it is not reported as a rollback. A process
killed before replacement can leave a hidden temporary file; no partial cache
becomes the baseline. Inspect such leftovers while the consumer is stopped.

Fresh observation and prediction-calculation timestamps cannot move backwards.
Prediction values cannot change without advancing their calculation timestamp. A changed consumed snapshot
with the same observation time is rejected; ignored prose changes do not count.
A schema change can rebaseline at the same timestamp, but cannot move backwards.
Validated v1.0.4 caches are silently migrated once because their source schema
cannot be proved. Fresh predictions baseline again after an unavailable segment.

Up to 256 distinct stable reset IDs persist across restarts and disappearance /
reappearance. Confirmation updates for one ID do not create another `new_window`.
An ID evicted from that bounded history may be announced if it later reappears.
Different upstream IDs cannot be proven to describe the same real-world reset.
Window/status/prediction transitions are separate change dimensions. A legitimate
later transition can have the same from/to values and is not globally suppressed.

## Delivery and scheduling

The script commits state before writing JSON to stdout. This prevents competing
pollers from repeating the same diff, but cannot guarantee exactly-once chat
delivery: interruption after commit or a failed downstream send can lose an alert.
The script does not retry delivery or maintain an outbox. `event_id` helps an
external consumer deduplicate a retry of the same output. Do not share a cache
between independent destinations expecting independent deliveries.

Create no schedule on install, and send no message without user authorization.
An authorized operator must scope timezone, cadence, destination, and agent
permissions. Default chat delivery may reach other people. Silent agent turns
may still cost tokens. Use an isolated session for an explicitly requested job.
To stop it, disable/remove the exact OpenClaw job; uninstalling this skill alone
cannot remove external schedules. Changing a model or creating persistence is
outside a one-off monitoring request.

For a cache fault, stop its consumer, inspect the exact selected path and JSON
error code, then obtain user authorization before archiving/removing state. Do
not delete a working cache as an automatic recovery action. A subsequent fresh
check creates a silent baseline, which deliberately does not replay history.

## Regression checks

`python3 -B -m unittest discover -s tests -v` uses synthetic legacy data, a
minimal schema-2 public-feed projection, mocked HTTP, and isolated temporary
caches. It covers state changes, freshness, validation, injection isolation,
deduplication, migration, HTTP guards, concurrent locking, interrupted writes,
file permissions, symlink/hardlink/special-file refusal, and CLI exit behavior.
It performs no network requests, live-cache writes, job creation, or reset calls.
