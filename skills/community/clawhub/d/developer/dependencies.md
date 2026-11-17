# Adding, Pinning, and Upgrading Dependencies

Every dependency is code you ship, cannot review, and did not write. The decision is not "does it work" but "what does it cost to keep, and what does it cost to remove".

**Before adding or upgrading**, read `## Dependencies` in `~/Clawic/data/developer/repos/<repo>.md`: a package may already be banned here, pinned for a reason, or replaced by something the repo standardizes on. Constraints the user declared — banned libraries, license policy — are in `config.yaml` under `constraints`.

## Before Adding One

Answer all five, in the PR description:

1. **What does it replace?** If the answer is "50 lines I would have written", read those 50 lines first. Left-pad problems come from dependencies that were cheaper to write than to audit.
2. **What does it drag in?** Count transitive dependencies and total install size before, and after. A one-function utility that brings 40 packages is 40 packages.
3. **Is it alive?** Last release date, open-issue trend, number of maintainers. One maintainer with no release in 18 months is a fork you have not made yet.
4. **What is the license?** Copyleft in a product you distribute is a legal question, not a technical one. Check the transitive licenses, not just the direct.
5. **What does removing it cost?** If its types, its idioms or its patterns will be spread across the codebase, wrap it behind your own interface at the boundary (SKILL.md Reversibility).

Two extra checks for anything young or unfamiliar: does the download count match the popularity claim, and is the package name a typo away from a famous one? Typosquats are the most common supply-chain hit that reaches a developer laptop.

## Pinning

| Artifact | Rule |
|---|---|
| Application, lockfile | Committed, always. The lockfile is the reproducibility of your builds; without it "works on my machine" is unanswerable |
| Application, manifest | Caret/tilde ranges are fine because the lockfile decides; exact pins only where a minor bump has already burned you |
| Library you publish | Widest range you actually test, so consumers can resolve. Pinning exact versions in a library forces conflicts on everyone downstream |
| CI base images and toolchain | Exact version or digest. "latest" turns an unrelated upstream release into a red build on a Monday |
| Anything security-relevant (crypto, auth, parsers) | Exact pin plus an alert, so upgrades are deliberate and fast |

Semver is a promise, not a mechanism: minor and patch releases break behavior regularly, because "breaking" is judged by the author's model of your usage. Treat the lockfile as the truth and the range as the intent.

## Upgrading

- **One dependency per commit**, so a bisect can name it (`bugs.md`).
- **Read the changelog between your exact versions**, not the latest release notes. Look for the behavior you rely on, not for the word "breaking".
- **Major upgrades get their own PR** with the migration notes in the description and a manual pass over the risky call sites.
- **Upgrade on a cadence, not on an incident.** Monthly is enough for most repos; the row goes in `## Due`. A repo two years behind cannot take a security patch without a project.
- **After a breaking upgrade, the lockfile diff is the diagnosis** — the direct dependency is rarely the thing that changed (`bugs.md`).
- **Framework major versions**: check that your ecosystem moved too. Being first to a new major means you debug the plugins as well.

## Security and Supply Chain

- Run the ecosystem's audit in CI and treat *reachable* criticals as blocking. A vulnerability in a dev-only dependency, or in a code path you never call, is a ticket, not a fire.
- A CVE with no patched version is a decision: pin around it, patch locally, vendor it, or accept and document. Write the decision down (`artifacts/`), because it will be asked again at the next audit.
- Install scripts run arbitrary code at install time — that is the actual supply-chain surface. Disable them where the ecosystem allows and the build still works.
- Lockfile changes deserve review attention on their own: a diff that adds 200 transitive packages is a change of risk profile, whatever the feature was (`reviews.md`).
- Never install from a URL or a branch in a production build. Publish or vendor it instead.

## Deprecations and Removal

- The moment a dependency is replaced, delete it from the manifest in the same PR. Unused dependencies still install, still get audited, and still get "upgraded" by bots.
- A deprecation warning in the build log is a deadline with no date. Convert it into a ticket with the version that removes it, or it becomes an emergency during an unrelated upgrade.
- Vendoring is a legitimate option for something small, unmaintained, and load-bearing: copy it in with its license and a comment naming the origin and the reason.

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Adding a library for one function | You inherit its whole tree and its release cadence | Write the function, or check what the standard library already has |
| Upgrading everything at once "to catch up" | Any failure is unattributable; the PR is unreviewable | One per commit, majors alone |
| Trusting the range in the manifest | Ranges resolve differently on different days and machines | Commit the lockfile; the range is intent, the lock is truth |
| Ignoring transitive dependencies | Where the CVEs and the breakage actually live | Audit and diff the lockfile |
| Automated upgrade PRs merged on green CI | Green means your tests passed, not that behavior is unchanged | Read the changelog for anything not patch-level; group patch, review minor |
| Keeping a dependency because removing it is work | The work grows with every new usage | Wrap it now, or remove it now |
| Forking to fix one bug and never upstreaming | You own it forever and the fork drifts | Upstream the patch; vendor only with a note and a plan |
| A pin with no reason recorded | Somebody unpins it next quarter and rediscovers the bug | Pin with the reason in `## Dependencies` |

## Write Down the Verdict

- **A dependency added, refused, pinned, or banned** → a row in `## Dependencies` of `repos/<repo>.md`: package, pin, and the reason in one line (`memory-template.md`). "Why is this pinned to 3.2.1" must be answerable without the original author.
- **A painful upgrade** — what broke, how it was found, what the lockfile diff showed → `## Gotchas` in the same profile, so the next major does not re-run the discovery.
- **A choice between two libraries with real tradeoffs**, or an accepted unpatched CVE → `artifacts/adr-<topic>.md` with the alternatives, the date, and the condition to revisit; add its `## Boxes` line in the same turn.
- **A review cadence agreed with the team** → a row in `## Due` of `memory.md`.
