# Snapshot input

A UTF-8 JSON object has `schema_version: 1`, `dataset_kind` (`user_provided` or `synthetic_fixture`), and `pages`. Each page contains an absolute HTTP(S) `url`, a relative local `.html`/`.htm` filename, optional source kind and capture timestamp, and an optional source-reported HTTP status. A page with no saved body may instead record `login_required`, `fetch_failed`, or `not_run` plus a reason.

Local HTML paths must resolve inside the JSON file's directory. Duplicate URLs are processed once; `--max-pages` limits attempts. Records are capped at 2 MiB each. The URL is used only to resolve relative links while parsing; it is never fetched.

Output records source metadata, the SHA-256 of each read file, extracted signals and explicit limitations. A missing field means only that it was not extracted from this snapshot. It is not evidence about live HTML or the rest of the site.
