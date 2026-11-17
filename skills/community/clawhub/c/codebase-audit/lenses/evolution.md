# Evolution and compatibility

Fires: when the project ships a client that cannot be force-updated, stores data on the device, or runs a database

Leading word: **version skew**. The client from six months ago talks to today's server; today's app opens the data the oldest shipped version wrote. With enough users, every observable behavior is depended on by somebody (Hyrum's law).

Artifact: a compatibility matrix (shipped versions still in use × server API and stored data formats → works?).

- **old-client** (when a shipped client calls a server): A client that cannot be forced to update calls today's API. Which removed fields, renamed routes, new required params or new enum values break it? Does the client decode unknown enum values and fields without crashing?
- **local-migrations** (when data is persisted on the device): Upgrade the local database, cache or persisted settings from every shipped schema version, not only the last one. What happens on a downgrade or a fresh restore from backup?
- **rollback**: This release is bad. Can you roll it back without losing or corrupting data written since? Server migrations follow expand-then-contract; the previous client and server still work with the new schema.
- **kill-switch** (when features ship to users who cannot be rolled back instantly): Each risky feature can be turned off remotely without a release. Flags have a safe default before remote config arrives. Stale flags that are always on or always off are dead branches.
- **forced-update** (when a shipped client calls a server): There is a minimum-version gate for when compatibility must break, and it fails safe when its own check fails.
- **config-drift**: Settings that differ between dev, staging and production; required environment variables that fail at first use instead of at startup; production-only code paths no test runs.
- **platform-drift**: Deprecated OS and framework APIs, minimum OS versions that cut off users, runtimes past end of life, store policy deadlines.

Done: the compatibility matrix covers every shipped version still in use, or states why that is unknown.
