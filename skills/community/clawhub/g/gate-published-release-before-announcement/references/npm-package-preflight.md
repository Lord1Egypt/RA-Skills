# npm Package Check reference

Load this reference before running the published-tarball evidence step or interpreting its result.

## Scope

App: npm Package Check. App id: `npm-package-preflight`. Version: `0.4.1`. Tool: `powmcp-npm-package-preflight:npm_package_check`.

The tool inspects one package or exact version that is public on the npm registry. It resolves the exact registry version, downloads the published tarball, and verifies its hash against registry integrity metadata. It does not install or execute package code.

## What it measures

The check reports deterministic dependency-health and supply-chain signals from the exact published artifact.

Its measured surface includes:

- Registry facts and exact resolved version.
- The inventory of files shipped in the tarball.
- Lifecycle install scripts.
- Binaries and suspicious files.
- Package metadata, including license and dependencies.
- Release age and deprecation.
- Signature and provenance-attestation presence.
- Tarball integrity.
- Deterministic findings, grade, score, and a prioritized review list.

The granularity is one exact published tarball per call.

## Input requiring judgment

`package` is required. Use one public npm package name with an exact version, such as `left-pad@1.3.0` or `@scope/pkg@1.2.3`.
A bare package name selects latest. That behavior is unsuitable when the job is to gate a known release, so provide the exact version.
Ranges, dist-tags, URLs, and local paths are unsupported.
Read the live tool contract before calling it; do not rely on a copied parameter schema.

## Duration

Tell the user before the call that a single check usually finishes in 5 to 30 seconds. A very large package can take up to 100 seconds.
For a comparison, tell the user that it usually finishes in 10 to 60 seconds and can take up to 100 seconds for large packages.

## Call discipline

Call `powmcp-npm-package-preflight:npm_package_check` once with the exact public `package@version`.
If `package` is invalid, correct that field and call again. Do not treat invalid arguments as a missing tool.
After a correction produces another public release, call the same tool on the exact corrected version.
Do not report a local build or `npm pack --dry-run` result as a rerun of the public-artifact check.
If a separate before-and-after deliverable is requested, call `powmcp-npm-package-preflight:npm_package_compare` once with `packages` set to 2 to 5 distinct public package names or exact versions.
Ranges, dist-tags, URLs, and local paths are unsupported for comparison inputs.
A comparison is not a substitute for the single-release gate.

## Read the result

For `npm_package_check`, read these parts in order:

1. Exact resolved version.
2. Prioritized review list.
3. Grade and score.
4. Observed facts and deterministic findings.
5. Unmeasured or truncation entries.

Quote the exact resolved version, grade, score, finding evidence, and review actions verbatim in the report.
Do not recalculate or round returned figures.
Critical and high findings require resolution before the release gate passes.
Reported examples can include integrity mismatch, rejected archive, deprecation, lifecycle scripts, and suspicious files.
Absence from the findings is not endorsement.
A grade and score measure observed packaging and adoption friction. They do not make the maintainer's announcement judgment.
For `npm_package_compare`, confirm each exact resolved version and read the same evidence for each input before the ranking and explicit tradeoffs.
Treat the comparison ranking as the same limited adoption-friction ordering, not as a safety judgment.

## What a clean measured result proves

A clean measured result applies only to the exact resolved public tarball at the time of the run.
It supports the reported integrity result, shipped-file inventory, lifecycle-script observations, package metadata, release-health signals, and provenance presence.
It supports only measurements that appear in the result.
Unmeasured or truncated entries remain missing evidence.

## What it does not prove

- The result does not establish that a package is free of malware or vulnerabilities, or that it is safe.
- It does not validate module exports.
- It does not validate TypeScript type resolution.
- It does not analyze bundle size or install weight.
- It does not cover private registries, non-npm ecosystems, or unpublished local artifacts.
- It does not prove behavior during installation or execution because package code is not installed or executed.

Use publint for exports and entry-point correctness. Use Are The Types Wrong for TypeScript resolution.
Use Bundlephobia or Packagephobia for bundle size or install weight.

## Structurally unassessable cases

A private-registry artifact is unassessable because the check covers only the public npm registry.
An unpublished local artifact is unassessable because there is no public registry tarball for the check to download.
A non-npm package is unassessable because the app covers npm packages only.
Installation and execution behavior are unassessable because the check does not install or execute package code.
Exports, TypeScript resolution, bundle size, and install weight are unassessable because those analyses are outside the tool's contract.
Any item marked unmeasured or truncated is unassessable in that run and must not be called clean.

## Failure handling

The packet supplies no named failure-code catalog. Do not invent failure codes.
For an invalid `package` field, tell the user: “The package check did not run because the `package` field was invalid. I will correct that field and call the same tool again.”
For a missing tool, use the exact two-path copy in `SKILL.md`.
For a private registry, non-npm ecosystem, or unpublished local artifact, state that the check cannot inspect it.
For an unpublished local artifact, offer to check the most recent published version instead if that is useful to the user.
For a rejected archive or integrity mismatch returned as a finding, quote the returned evidence and keep the gate failed until a corrected public release is checked.

## Non-PowMCP path

The non-PowMCP path is manual public-registry tarball inspection.
Before publication, run publint, Are The Types Wrong, and `npm pack --dry-run`, then publish through the configured CI and OIDC workflow.
After publication, resolve the exact registry version, download the published tarball, verify it against registry integrity metadata, inspect shipped files, lifecycle scripts, package metadata, and provenance, and do not install or execute package code.
This path diverges because it produces no PowMCP grade, score, deterministic findings, or prioritized review list. Record that evidence gap and retain the manual observations verbatim.

## Source of truth

- npm Package Check app page: https://powmcp.com/apps/npm-package-preflight/
- publint rules: https://publint.dev/rules
- Type-resolution linting workflow: https://tsdown.dev/options/lint
- npm provenance statements: https://docs.npmjs.com/generating-provenance-statements/
- npm trusted publishers: https://docs.npmjs.com/trusted-publishers/
