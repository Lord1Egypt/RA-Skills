# Version and Update Evidence

Use this workflow when asked whether DCC-MCP is current, which release contains
a fix, whether an upgrade is compatible, or why an adapter embeds an older Core.
Read-only inspection does not authorize an installation, upgrade, rollback,
server restart, or issue submission.

## Select a Safe Entry Point

The new `update inspect`, `update discover`, and feedback preview paths require
a CLI build containing the read-only inspection entry point. Until that build is released, use the
explicitly selected candidate in an isolated test environment. Do not assume
an arbitrary installed CLI supports it.

Older CLI builds can apply a previously staged update **before parsing any
arguments**, including `--help`, `--version`, and `update check`. Do not run
those commands as capability probes when the task requires no installation
changes. Inspect package/release metadata without launching the binary, and
report the runtime version as unknown. If a newer CLI is required, present the
exact official artifact and obtain approval through the existing verified
installation workflow first.

For a verified inspection-capable binary:

Confirm command support from reviewed source/build provenance for an isolated
candidate, or from official release/capability metadata for a released artifact.
Record the artifact identity and evidence; a version number alone does not prove
support. Do not claim a minimum supported release until one is published.

If support cannot be established, report "This CLI has not been confirmed to
support the requested read-only command", keep runtime observations unknown,
and provide the [official releases](https://github.com/dcc-mcp/dcc-mcp-core/releases)
and [official source](https://github.com/dcc-mcp/dcc-mcp-core). Stop without invoking the
command, automatically upgrading, or retrying another installed binary. If an
already verified safe candidate rejects the subcommand, report it as unsupported
and return to metadata inspection rather than treating it as an update check.

```bash
dcc-mcp-cli --output json update inspect
dcc-mcp-cli --output json update inspect --offline
```

## Keep Version Observations Separate

- The executing CLI version identifies the selected binary, not every copy on
  PATH and not the version of a running gateway or DCC adapter.
- A package manager's installed version is a receipt. It can differ from the
  binary after self-update; preserve the source and the discrepancy.
- Bundled Core identifies the code shipped in the selected build. An adapter's
  declared minimum Core requirement is not its bundled or loaded Core version.
- A runtime version requires evidence from that concrete running process.
  Preserve `unknown` and its reason when no supported observation is available;
  never substitute the latest release or a package receipt.

Report the provider, source URL, retrieval time, source time when available,
cache age/TTL, and offline or stale status. A cached value is not proof that
upstream has no newer release. Do not call a failed check “up to date”.

## Evaluate a Candidate

Present the current observation, candidate, channel, official release/changelog
links, compatibility evidence, and the reasons for the recommendation. A stable
release or matching platform asset does not prove host compatibility. Treat
missing host/runtime/Core constraints as unknown. Preserve user/operator pins;
report a conflict without editing or ignoring the pin.

Only explicit upstream fix evidence can support a version/fix relation. A
release note's explicit issue-closing reference means the release declares the
fix; it does not prove the user's runtime is fixed. Similar wording, an issue
being closed, or an unreleased merged PR is insufficient. Without exact
evidence, return “fix not established” and the official issue/release links.

Inspection is a dry run. Before changing anything, show the specific component,
source and target versions, environment, compatibility gaps, and rollback
availability, then obtain approval. Use the owning install/update path. Do not
turn a pinned candidate into an unpinned `latest` install. Cancelling a staged
update is different from rolling back an already activated binary; do not invent
a rollback command when the installation owner provides no verified path.

## Discover the Ecosystem

Use the read-only official catalog and Marketplace providers:

```bash
dcc-mcp-cli --output json update discover --query "animation" --limit 20
dcc-mcp-cli --output json update discover --offline --provider official_install_catalog
```

The provider-qualified results include application targets, package metadata,
requirements, policy, and source evidence. New catalog entries require no
hardcoded software list. Catalog discovery does not require a live host.
An empty live inventory is not evidence that the ecosystem has no matching
adapter. A catalog entry is not proof that the component is installed, loaded,
compatible, or newly published.

Keep official source identity and freshness with each result. Respect the
signed catalog's validity and withdrawal policy. Installation discovery reuses
the verified cache or bundled catalog; Marketplace discovery has no offline
snapshot in this interface. Report partial/unavailable sources explicitly,
including refresh errors. Online reads do not persist caches. A signature's log
time is attestation evidence, not the component's publication time.

## Prepare an Issue Without Publishing It

Reuse `feedback route`, `feedback bundle`, and the plan-only `feedback file`
workflow when the selected CLI's entry point is safe. Preview explicitly chosen
files with the inspection-capable binary:

```bash
dcc-mcp-cli --output json feedback bundle reviewed-finding.json
dcc-mcp-cli --output json feedback file reviewed-finding.json
```

The bundle v2 is a minimal diagnostic summary, not a publishable Finding v1.
Default collection does not run doctor, query a gateway, or discover logs. An
install report or log directory must be explicitly selected. Typed versions,
loading categories, and error classes survive the allowlist; arbitrary text
does not. Review the fixed omission categories/counts and retained fields.

For the separately reviewed Finding and issue draft, collect only the fields
needed to explain the failure: version observations, loading-origin category,
bounded error classification/stack frames, minimal reproduction, and expected
versus actual behavior. Prefer a small synthetic reproduction.

Use a minimum-field allowlist. By default exclude credentials, usernames,
machine names, absolute home/project paths, private repository contents, chat
transcripts, environment dumps, raw logs, screenshots, and sensitive assets.
Show the actual projected JSON/issue body and which categories were omitted.
Pattern redaction and a `public_safe` flag do not guarantee that arbitrary text
contains no secrets; inspect the retained fields and disclose that limitation.

Search for duplicate issues only in the routed official repository, using a
fingerprint and fixed public categories. Do not send arbitrary tool slugs or
error text as search terms before review. A failed lookup is
unknown, not “no duplicates”. Present the candidate issues and the exact draft
title/body before asking whether to create an issue or comment on one.

Do not submit automatically. After explicit approval of the concrete content,
reuse the emitted `feedback file` authorization binding for the finding path
and digest, fingerprint, repository, catalog path/digest, and
`--expected-document-sha256`. The preview includes the exact title, issue body,
and comment body; the document digest binds all three. If those values or the
draft change, produce a fresh preview. The plan may contain local binding paths,
so do not publish the whole plan. Never upload the complete local diagnostic
bundle or private source tree as an attachment by default.


## Quick, non-blocking update guidance

Reuse Core's existing background refresh and cached `cli_update` evidence on
normal invocations. Its current default CLI TTL is 24 hours, failed checks
retry after one hour, and the cache lock prevents duplicate refresh workers.
Do not add a synchronous network request, catalog scan, or updater before each
command. An inspection-only entry point intentionally bypasses normal startup;
it need not spawn a refresh just to satisfy an “every invocation” slogan.

Deduplicate user-facing notices per component, source/target version and
environment for the current task. Preserve the source freshness and failure
reason; offline/unknown/stale is never “latest”. Do not keep asking about an
unchanged declined update. New catalog support can be discovered with
`update discover` even when the CLI's bundled product list is older. This is
not proof of a feature change or of a newly published release: show the official
release/changelog evidence and admit when no structured change diff exists.

An upgrade is the user's choice. Explain what changes, retain operator pins,
and use the existing installation owner. Do not update a different copy on
PATH, treat a package receipt as the loaded adapter version, restart the host
or gateway, or interrupt an active render/job to activate an update. Recheck
the selected executable and the separately running process after an approved
change. Exact-version requests must use a verified exact-version installation
path; `update apply --yes` currently stages latest and cannot enforce a pin.
