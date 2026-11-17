# gcloud — Configurations, Credentials, Output, and Safety

The CLI's two hard parts are credentials (there are two independent login systems and they are not interchangeable) and output shaping (which is the difference between a readable answer and a page of JSON).

**Contents:** [Two Logins, Two Purposes](#two-logins-two-purposes) · [Configurations](#configurations) · [Impersonation](#impersonation) · [Shaping Output](#shaping-output) · [Filtering](#filtering) · [Finding Anything: Asset Inventory](#finding-anything-asset-inventory) · [Reading Logs](#reading-logs) · [Safety](#safety) · [Storage and Data Transfer](#storage-and-data-transfer) · [Quotas and Services](#quotas-and-services) · [When the CLI Is the Wrong Tool](#when-the-cli-is-the-wrong-tool)

Where `cli_profile`-style settings exist here, they are `gcloud_configuration` in `config.yaml`; while it is unset, examples assume the active configuration and the assumption is stated out loud (SKILL.md Rule 7).

## Two Logins, Two Purposes

This is the single most common source of "it works in my terminal but not in my code".

| Command | Writes | Used by |
|---|---|---|
| `gcloud auth login` | The CLI's own credential store | `gcloud`, `bq`, and the CLI only |
| `gcloud auth application-default login` | Application Default Credentials on disk | Client libraries, Terraform, anything using an SDK |

- Running only the first leaves client libraries unauthenticated; running only the second leaves the CLI unauthenticated. Local development usually needs both.
- ADC resolution order matters: the `GOOGLE_APPLICATION_CREDENTIALS` environment variable wins, then the ADC file, then the attached service account's metadata server. A stale environment variable pointing at an old key file overrides everything and explains a large share of confusing local 403s.
- On GCP, nothing needs either: the attached service account is delivered by the metadata server. Any key file on a VM or in a container is an unnecessary credential (`iam.md`).
- ADC carries a quota project, which is the project billed and rate-limited for API calls. When calls fail with a quota error naming a project you did not expect, that is why — set it explicitly.
- `gcloud auth print-access-token` exists for scripting against raw APIs. It prints a live credential: never into a log, a file, or anything written under `~/Clawic/data/`.

## Configurations

Named sets of properties — account, project, region, zone — switched as a unit.

- One configuration per project or environment, activated by name. Far safer than editing the active project, because the account switches with it and you cannot end up authenticated as production's identity against staging's project.
- `--configuration <name>` on a single command overrides the active one without switching it, which is the right form inside scripts.
- Properties can also be set per-command (`--project`, `--region`) and via environment variables. Precedence runs command flag → environment variable → configuration → unset.
- **Print the active configuration before any destructive operation.** "Which project am I in" is the question behind most avoidable incidents, and it costs one command to answer.

## Impersonation

- `--impersonate-service-account=<email>` runs a single command as that service account, using your own identity to mint a short-lived token. Needs `roles/iam.serviceAccountTokenCreator` on that service account (`iam.md`).
- This is the correct way to reproduce a CI failure locally: run the failing command impersonating the exact service account CI uses. It eliminates the "different principal" class of bug in one step (`debug.md`).
- It is also the correct replacement for a downloaded key in local development. Any workflow that starts with "download the JSON key" has this as its answer.
- Impersonation chains are possible and are worth knowing exist, because they are an escalation path a reviewer should look for.

## Shaping Output

Every `gcloud` command supports the same output flags, and knowing four of them removes most of the friction.

| Flag | Effect |
|---|---|
| `--format=json` | Full structured output, for piping into a JSON processor |
| `--format="value(field)"` | Bare values, no headers — the form to use in a shell pipeline |
| `--format="table(a,b,c)"` | A readable table with chosen columns |
| `--format="csv(a,b)"` | For a spreadsheet or a report |
| `--flatten="items[]"` | Expands a repeated field into one row per element, which is how you make nested resources tabular |

- `--format="value(...)"` is what should feed a loop. Parsing the default human-readable output is fragile and breaks when a field is added.
- Field paths are the API's own field names. When a path returns nothing, print the resource as JSON once and read the actual names rather than guessing.
- Projections support transforms (formatting dates, extracting the last path segment of a resource name), which removes most of the post-processing people write by hand.

## Filtering

- `--filter` runs server-side or client-side depending on the API, and either way it beats piping into a text search: it understands types, so a comparison on a number or a timestamp behaves correctly.
- Supports `AND`, `OR`, `NOT`, parentheses, `:` for substring or has-value, `=` for equality, and comparisons on numbers and dates.
- Labels and metadata are filterable, which is how a label discipline pays off operationally as well as in billing (SKILL.md Rule 6).
- `--limit` and `--page-size` control result volume. On large estates, always bound a list command — the default can be a very long wait against a big project.
- Combine filter and format to answer a question in one command: filter to the resources that matter, project the two or three fields that answer the question.

## Finding Anything: Asset Inventory

The most valuable and least-known part of the CLI.

- Searches every resource across a project, folder or organization, including services nobody remembers enabling. It is the correct first step on any inherited estate (SKILL.md Rule 1).
- Searchable by resource type, name, labels, location and free text; also searches IAM policies, which answers "who has access to anything named prod" in one call.
- Exports a full inventory snapshot to Cloud Storage or BigQuery, which is how you diff the estate month over month and how you produce an audit artifact.
- It can return a point-in-time view from the recent past, which is the fastest way to answer "what changed since Friday".
- Write the result of a discovery pass into `## Current Infrastructure` in `~/Clawic/data/gcp/memory.md`, and any host it finds into the shared `servers.md`. The next session should start from the gaps, not repeat the sweep (`memory-template.md`).

## Reading Logs

- The logging read command takes the same query language as Log Explorer, so a filter developed in the console pastes straight into a script.
- Bound every read by time. An unbounded read over a busy project is slow and, against a log bucket, is scanning you pay for (`costs.md`).
- `--format="value(...)"` on a log read extracts just the fields you need — principal, method, error — which turns an audit-log investigation into one readable column instead of pages of JSON (`debug.md`).
- Streaming (tail) reads exist for watching a deploy in real time. They have a small delay and are not a substitute for a metric.
- The three filters worth memorizing as shapes: by resource type and severity, by `protoPayload.methodName` for an audit investigation, and by `trace` to reconstruct one request across services.

## Safety

- **Read-only by default.** Nothing destructive is emitted inside a copy-paste block of read commands.
- **`--dry-run` exists on some commands and not others**; `--help` is the only reliable check. Where there is no dry run, the pattern is: list what would be affected with a filter, review the list, then act on that explicit list.
- **Destructive commands ship with their blast radius stated** and an explicit confirmation step: deleting a project, dropping a dataset, destroying a KMS key version, detaching a billing account, deleting a node pool, removing a bucket. Several of those are irreversible in ways the confirmation prompt does not convey.
- **`--quiet` suppresses confirmation prompts.** It belongs in automation that has already been reviewed, never in a command handed to a human to paste.
- Where `safety_posture` says confirm-each, every mutating command is presented on its own with what it will change, not batched.
- **A command's project is the most dangerous implicit argument.** State it explicitly in anything destructive rather than relying on the active configuration.

## Storage and Data Transfer

- The CLI's storage commands replaced the older standalone tooling and are substantially faster, particularly on many small objects — they parallelize by default where the old tool needed a flag.
- Recursive copies, rsync-style synchronization, and parallel composite uploads for large single files are all built in. Composite uploads produce an object whose checksum behaves differently, which surprises anything verifying a hash.
- Always transfer with checksum verification on, and verify object counts at both ends. A transfer that silently skipped a fraction of the files is worse than one that failed loudly.
- For anything large, scheduled, or from another cloud, Storage Transfer Service is the managed answer and removes the machine you would otherwise babysit (`storage.md`).

## Quotas and Services

- Listing enabled services on a project is the ten-second check that resolves the most common false 403 (`debug.md`).
- Enabling a service is asynchronous enough that an immediately following create can race. Expect one retry, and add an explicit dependency in IaC (`iac.md`).
- Quota listing and increase requests are available from the CLI and the console. Whichever is used, record the result — project, region, quota, limit, observed peak, date — in `## Quotas` in `memory.md` (`memory-template.md`).
- Disabling a service can delete its resources. It is a destructive operation wearing an administrative name.

## When the CLI Is the Wrong Tool

- **Durable infrastructure** belongs in IaC. A `gcloud` command that creates something permanent is drift the moment it succeeds (`iac.md`).
- **Bulk or repeated operations** belong in a client library, where retries, pagination and backoff are handled properly rather than approximated in a shell loop.
- **Anything a human will run twice** should be a script in version control with the project stated explicitly, not a line in someone's history.
- The CLI is at its best for exploration, one-off investigation, and reading state — which is most of what this skill does with it.

Anything a session discovers with these commands and will want again — the inventory from an Asset Inventory pass, a quota value and its observed peak, a service account and its purpose, a host — goes to its box in the same turn: `## Current Infrastructure`, `## Quotas` or `## Service Accounts` in `~/Clawic/data/gcp/memory.md`, hosts to the shared `~/Clawic/data/servers/servers.md`. A command output that lives only in the terminal will be run again next month (`memory-template.md`).
