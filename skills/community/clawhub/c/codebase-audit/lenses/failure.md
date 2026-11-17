# Failure and concurrency

Fires: always

Leading word: **pull the plug**. Every await is a place another task runs, every step a place the process dies, every error a place the user can be lied to. Assume the fallacies of distributed computing are all true at once: the network is unreliable, latency is not zero, the topology changes.

Artifact: a failure-to-screen table (failure → path → what the user sees → finding).

- **await-race** (when the code is async, threaded or talks to a shared store): A read and a dependent write with an `await`, lock release, callback or network call between them. Inside actors this is reentrancy; across a database it is a missing transaction or `FOR UPDATE`.
- **pull-the-plug** (when a write spans more than one step or store): For each multi-step write (local then remote, file then index, two tables, upload then record), kill the process between step N and N+1. What is on disk and on the server, and does the next launch recover? Fix family: one transaction, write-temp-then-rename, an outbox.
- **silent-catch**: List every swallowed error and silent fallback (`?? []`, `|| default`, `try?`, empty catch). Which one hides a wrong answer from the user?
- **no-screen**: Map each failure path (offline, 401, 500, timeout, decode error, permission denied, quota hit) to the screen state it ends in. A path with no screen is a spinner forever or a silent no-op.
- **logs-only-debug**: When this fails in production, can logs alone tell which branch ran, for which request and user, with which inputs? Check correlation IDs and error context, and the opposite failure: tokens, emails or health data in logs or crash reports.
- **timeouts-retries**: Every network and IPC call has a timeout. Retries back off with jitter, have a cap, and only retry idempotent operations. A retry or sleep that papers over a race is a finding: name the race.
- **dependency-outage** (when the app calls third-party services): A provider (payments, auth, model API, maps, email, push) is down or slow for an hour. Does the app degrade to something the user can act on, queue and retry later, or hang and lose work? Look for fallbacks, a cached last-known-good, circuit breakers, and a status the user can see.

Done: every swallowed error is listed with a verdict, every multi-step write has a kill-point answer, and every failure path maps to a screen.
