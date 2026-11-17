# JavaScript and TypeScript review

Use --lang javascript for a selected workspace. Read patterns.md for reachability,
redundancy and gate decisions.

## Behavior and cost

Trace synchronous work on the event loop, awaited/rejected operations, state
updates and user-input flows. Missing local try/catch is not inherently a bug:
the framework or caller may own rejection handling. Verify that boundary.

Object spread, assignment and merges have different behavior; establish an
actual prototype-pollution path before reporting one. A DOM operation is not an
XSS finding without its input/trust/sanitization context.

Measure event-loop delay, latency and memory for realistic payloads. Do not
derive a defect or severity from the presence of JSON.parse or a synchronous loop.

## Unused code

Prefer an existing configured Knip run. Verify entry/project globs, workspace
boundaries, package exports/bin/scripts and framework plugins first. Missing
roots or dynamic imports can cascade into false unused-file/export/dependency
reports. Knip's configuration loading can execute tooling configuration;
inspect it before running in an untrusted checkout.

Check computed imports, generated routes, build-tool conventions, workers,
service workers, public assets and external package consumers. Do not mark a
public export dead simply because internal production code does not import it.
Inspect disconnected cycles as well as zero-reference symbols.

## Gates

Inspect package scripts, feature flags, route guards, CI triggers and final status
consumers. A frontend visibility flag is not necessarily an authorization control;
trace server enforcement for protected operations.
Check that disabled/failed/empty tests and stale reports cannot yield an accepted
required check. Validate both sides of an active flag with representative inputs.

For repeated UI components, distinct accessibility, ownership and framework
contracts may justify separate implementations; visual similarity is insufficient.

## Validation and dependencies

Use the installed project runner. The bundled helper invokes an existing npm test
script with CI=true and a timeout; it does not use npx to fetch missing tools.
It recognizes Jest/Vitest summaries, node:test TAP or spec output and mocha
summaries, and adds up every summary block, because workspace runs print one per
project. It also reads a fresh JUnit report from an explicit --command. Unknown
output remains incomplete even with exit 0.

Respect npm aliases, workspace/file/git sources, peer/optional declarations and
configured registries. The dependency helper applies scoped registries from the
project .npmrc and npmRegistryServer from .yarnrc.yml; pnpm-workspace.yaml and
lerna.json only produce a warning, so audit each member package (the units from
collect_facts.sh) with its own --root. A public-registry match does not validate
a locked version, package provenance or API.

Primary sources, checked 2026-11-03:
[Knip roots](https://knip.dev/explanations/entry-files),
[Knip issue interpretation](https://knip.dev/guides/handling-issues).
