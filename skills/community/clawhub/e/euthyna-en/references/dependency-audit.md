# Stage A: dependency audit

> This audits "what you depend on", not "your own code". Answer: **what risk does this newly introduced / upgraded dependency bring?**
>
> Prerequisite: the three non-skippable rules in `../SKILL.md`. **This stage never reads a dependency's source.**

---

## A.0 What this stage does and does not do

| Does | Does not |
|---|---|
| verify manifest files and lockfiles, resolve exact versions | judge whether the project can install or build (**never installs, never builds, never executes**) |
| fetch vulnerabilities, staleness, and maintenance status with deterministic tools | license compliance audit |
| translate tool output into judgments | scan the target's own source for vulnerabilities or secrets (that is Stage B / Stage C) |
| state clearly which criteria are **not evaluable** | improvise for ecosystems the collector does not support (say "not supported", do not force it) |

**This stage only reads registries, advisories, and repository metadata.**

---

## A.1 Why not build your own measurement tools

This framework **deliberately does not reimplement** dependency scanning. Not out of laziness:

1. Mature tools already cover this; rewriting only introduces new risk, and the measurement logic itself must be deterministic
2. Vulnerability data sources (OSV and others) are continuously updated; a self-maintained copy is guaranteed to go stale
3. **This stage's value is in the judgment, not in the measurement**

So this stage's producer is an **orchestration layer**: it calls off-the-shelf tools, normalizes their output into facts, and marks what was not measured.

Available discovery sources (use whichever is installed — **audit the source before installing**):

| Purpose | Candidates |
|---|---|
| dependency vulnerabilities (with fixed versions) | any OSV-based scanner |
| lockfile and manifest parsing | built into the tool, or package-manager commands such as `npm ls` / `pnpm why` |
| introduction time (which commit added it) | `git log --oneline --follow -- <lockfile>` |

> ⚠️ **Load detection and fallback**: the process must still run to completion when **none** of these tools are installed.
> On fallback, mark the criterion "not evaluated" truthfully — **do not** fill the gap with CVE data from model memory:
> that is exactly what this framework forbids.

---

## A.2 Step one: confirm the inputs

**The target directory must have one of** `package.json` / `pyproject.toml` / `requirements*.txt` / `go.mod`.
If none exists, **say so and stop** — do not improvise an audit for an ecosystem the collector does not parse.

**Manifests are located from the repository root only.** A multi-package repository's per-package locks are not measured by
`euthyna audit` or `euthyna deps --repo` (🧪 measured 2026-10-10: the root `package-lock.json` pins `root-a` while
`packages/app/package-lock.json` pins `sub-b` and `sub-c`, and the output reports only `root-a`, **with no declaration at
all**). Measuring a sub-package means running `euthyna deps --lockfile <path>` per package; if that is not done, say the
sub-packages were not measured — do not treat the root manifest's facts as facts about the whole monorepo.

**Exactly resolvable**: `package-lock.json`, `npm-shrinkwrap.json`, `uv.lock`, `go.mod` for Go 1.17+.

**Not resolvable**: `yarn.lock`, `pnpm-lock.yaml`, `poetry.lock`.
When these are present, **say so**, fall back to the pinned or latest published version, and mark it as an approximation.

**Check the network identity**: the unauthenticated GitHub API allows only 60 requests/hour. The collector issues several requests per dependency;
unauthenticated, repository-class criteria will be broadly not evaluable — **say so, instead of silently degrading or retrying to death**.

---

## A.3 Three states, not two

Every dependency, every criterion, lands in exactly one of three states:

| State | Meaning |
|---|---|
| evaluated · clean | actually checked, and no problem under this criterion |
| evaluated · flagged | actually checked, and there is a problem |
| **not evaluable for a stated reason** | could not be checked — **the reason must be written down for this item** |

**A missing measurement is never a clean conclusion.**

When the collector exits non-zero, it is **refusing to report** — **quote its message verbatim; do not retry, do not work around**.
A run that measured nothing produces "not evaluable", **not** "no issues found".

### Quoting discipline

- "no advisories" only means "none **within the evaluated scope**" — look at the coverage table before citing a clean conclusion
- **numbers must be quoted verbatim** — no re-deriving, no rounding, no dressing up
- **finding nothing is not an endorsement**

---

## A.4 What the model can add and the collector cannot

Measurement belongs to the tools; judgment belongs to the model. This is the value the model should add:

| Add | Caveat |
|---|---|
| which one **this reader should act on first** | order by risk, not alphabetically |
| upgrade path | patch or major? a major version means breaking changes |
| replacement candidates for deprecated dependencies | **verify the candidate actually exists in the registry before naming it**, and mark this as judgment, not measurement |
| install-script risk | can the flagged install script be avoided with `--ignore-scripts` |

---

## A.5 Report style

This stage's reports are often **pasted into tickets verbatim**, so:

- no person, no abbreviations, no exclamation marks
- active voice with **the matter as the subject**: write "upgrading to 1.19.0 clears all 25 advisories", not "I recommend upgrading axios"
- no intensifiers (very / significant / fortunately)
- **no guesses about motives**
- tense: audit actions in past tense, dependency state in present tense, consequences in future tense
- recommendations state only **the action and its cost** — **no naming of responsible parties**

---

## A.6 Handoff to Stage C

Issues reported by the dependency audit usually do **not** need Stage C — their evidence comes from vulnerability databases and is already determinate.

But there is one class of exception: **"is this vulnerability actually reachable in this project"**.
If the affected function of a dependency vulnerability has no call path here at all, that is an **assertion to be adjudicated**,
not an established fact. When you meet this, go to Stage C.
