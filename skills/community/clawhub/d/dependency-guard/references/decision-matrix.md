# Decision Matrix

Use this matrix after collecting either a Socket `depscore` result or a Socket CLI package report.

When only a Socket CLI package report is available, use score-based rules only if the report includes current category scores. If it does not, treat score-based checks as unavailable and do not classify above `block_pending_human_review` without a fresh `depscore` result.

## Default Thresholds

Treat Socket category scores on a `0-100` scale.

## Capability And Footprint Heuristics

Use these heuristics when scores alone are not decisive:

- `network`: acceptable for package classes whose main purpose is remote I/O; otherwise escalate
- `filesystem`: acceptable for local build, bundling, or file-processing tools; otherwise escalate
- `environment`: `allow_with_warning` only for narrow, obvious use such as reading a specific config variable; broad environment access should be at least `block_pending_human_review`
- `shell`, `eval`, `unsafe`: at least `block_pending_human_review` unless clearly inseparable from the package purpose and directly surfaced to the user
- leaf or runtime utility packages: treat fewer than 20 transitive deps as the default `allow` range, `20-49` as warning territory when justified, and `50+` as human-review territory
- frameworks, bundlers, test runners, and SDKs: treat fewer than 100 transitive deps as the default `allow` range, `100-299` as warning territory when justified, and `300+` or any surprising tree shape as human-review territory

## `allow`

Choose `allow` only when all of the following are true:

- all category scores are `>= 85`
- no medium, high, or critical alerts are present
- no install scripts are present
- no clearly risky capabilities are present without a strong project-specific justification
- the transitive dependency footprint fits the default `allow` guidance for its package class

## `allow_with_warning`

Choose `allow_with_warning` when the package may be acceptable but should be called out explicitly, and any of the following are true:

- any category score is `70-84`
- only low alerts are present
- capabilities such as filesystem or network access exist but are expected for the package class (e.g., an HTTP client using network, a build tool using filesystem and shell)
- the transitive tree falls into warning territory for the package class but remains explainable

The agent may proceed only after presenting the warning clearly.

## `block_pending_human_review`

Choose `block_pending_human_review` when the package is not clearly safe but might still be justified, and any of the following are true:

- any category score is `50-69`
- any category score is missing or unavailable
- any medium alert is present
- install scripts are present
- obfuscation or minified installer logic prevents a confident review
- shell, eval, unsafe, or broad environment access appears in a package that does not obviously require it (e.g., a date-formatting library spawning subprocesses)
- the dependency tree falls into human-review territory for the package class or is unexpectedly deep or broad
- the package replaces a simple in-house or standard-library implementation for convenience only
- tooling is unavailable and the package cannot be reviewed

The agent should stop and ask for explicit approval or propose an alternative.

## `block`

Choose `block` when any of the following are true:

- any category score is `< 50`
- any critical or high alert is present
- the package shows obvious typosquatting or maintainer anomalies
- obfuscation appears designed to conceal install-time or privileged behavior
- the package requests privileged behavior that is inconsistent with its purpose
- the package introduces risk disproportionate to the value it provides

The agent should not proceed with the dependency change. Recommend a safer package or a no-dependency implementation.

## Version-Upgrade Fast-Path

Minor or patch upgrades of a dependency that was previously classified `allow` may use a shortened review, but not skip a current Socket check, if a fresh Socket review confirms all of the following:

- no new alerts have appeared since the prior review
- category scores have not dropped below `85`
- the changelog does not introduce new capabilities, install scripts, or significant transitive additions

In that case, the agent may reuse the prior rationale and summarize only what changed.

Otherwise, perform a full review as if the package were new.

## Tie-Break Rule

If the evidence is mixed (e.g., strong scores but an unexpected capability, or borderline scores with no alerts), choose the stricter outcome. When in doubt between two adjacent tiers, escalate.
