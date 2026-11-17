# External source intake and obligation coverage

Project Manager separates external source provenance from the canonical
requirement model. The source registry records document versions and a reviewed
inventory of obligations. The compliance matrix records an applicability
decision and engineering links for each obligation. Neither registry changes
requirement IDs, revision semantics, allocation, or verification strategy.

**Coverage is not conformity.** A covered row has linked, compatible PASS
evidence for each mapped current requirement revision. This does not establish
regulatory compliance, contractual conformity, certification, or a SPICE
assessment result. Source interpretation, inventory completeness, exclusions,
and sufficiency of engineering evidence require competent review.

## Authorities and files

| Location | Authority |
|---|---|
| `01-requirements/intake/SOURCES.json` | Source versions, provenance, obligation inventory and review history |
| `01-requirements/intake/COMPLIANCE.json` | Exact source-obligation applicability, requirement/proof links and assessment history |
| Corresponding `.md` files | Rebuildable generated views; never edit these as authoritative state |
| A distinct staged file for each source version, for example `inputs/specification-v1.pdf` | Original source artifact, protected by its recorded SHA-256 |

IDs use `SRC-0001` and `CMP-0001`. Each source version has a `source_key`,
external version label, descriptive source reference, declared license or usage
rights, confidentiality classification, and artifact path/hash. Obligations
have a source-local key, a locator such as section/page/paragraph, and extracted
text. Each compliance record preserves that locator/text and the reviewed
source snapshot hash, then links to exact internal requirement revisions and
existing verification evidence IDs.

Source files must already be staged within the project. These tools do not
download documents, follow reference URLs, copy material into the skill, or
assume that a license declaration grants rights. Keep each version's original
bytes at its own path, including after supersession. Stage source Markdown
under `inputs/` or `01-requirements/intake/`, which is excluded from canonical
engineering requirement discovery. Other parts of `01-requirements/` are scanned
for engineering requirements. Intake registries cannot themselves be source artifacts.

Keep confidential sources, customer documents, project-specific provenance and
working registries out of any shared skill distribution. A confidentiality label
is metadata, not access control. Use project repository permissions and the
approved storage/retention policy. Do not include credentials in source
references or license declarations.

## Source lifecycle

```text
DRAFT -> REVIEWED -> SUPERSEDED
```

The source's obligation inventory can be corrected while DRAFT. Review seals
the source definition, original file digest, inventory, reviewer, and review
rationale. Historical snapshots independently prevent rewriting a reviewed
version, even if a mutation attempts to recompute its review hash. A REVIEWED
source can only be superseded by a distinct REVIEWED version of the same
`source_key`. Keep all older records and staged files.

Review requires at least one obligation, or an explicit
`--no-obligations-rationale` establishing why the document has none to assess.
An empty inventory alone never counts as completed source review. A zero-
obligation rationale is for a non-normative source; exclude an actual obligation
through the compliance matrix instead of omitting it from the inventory.

To replace a source: create its new version, inventory and review it, then
supersede the former version. These are separate, logged transactions. Multiple
reviewed versions of the same source and unfinished DRAFT source reviews block
release until resolved; ordinary audits report these as development warnings.
Duplicate `(source_key, version)` pairs are rejected.

## Applicability and coverage

```text
UNASSESSED -> IN_SCOPE | EXCLUDED
IN_SCOPE / EXCLUDED -> UNASSESSED (reopen)
```

An explicit new assessment may remap an IN_SCOPE row or change an exclusion;
every assessment records actor, timestamp and rationale. The history preserves
earlier assessments. Source version, obligation key, original text/locator and
reviewed source hash cannot be changed on an existing row. Compliance rows
belonging to superseded sources are historical and cannot be edited through the
CLI; assess the new source version with new rows.

- **UNASSESSED:** applicability is unresolved.
- **IN_SCOPE:** at least one exact current non-cancelled requirement revision
  is mapped. Evidence links may initially be empty while work is planned.
- **EXCLUDED:** an explicit reviewer rationale excludes this obligation from
  the project's agreed scope; requirement and evidence links are cleared.

The calculated coverage report considers every obligation in every current
REVIEWED source. Missing matrix rows remain unresolved. For an IN_SCOPE row,
each mapped exact revision needs at least one explicitly linked evidence record
whose status is PASS and whose strategy matches the requirement. An existing
FAIL, BLOCKED, SKIPPED or SUPERSEDED record does not provide coverage. A PASS
record elsewhere in the evidence registry is not automatically linked to a row.
Unrelated evidence and unknown IDs are rejected. Moving a requirement to a new
revision makes an old mapping stale; review and update the mapping and proof
references. Old evidence never automatically covers a new revision.

The report uses `COVERED`, `EXCLUDED`, or `UNRESOLVED` for operational coverage.
It deliberately does not generate a conformity verdict or certification claim.

## Example workflow

Run from the skill location, replacing `PROJECT` with the canonical project
root. The sample labels are synthetic; select project-appropriate ownership,
rights and confidentiality.

```bash
python3 scripts/intake_manager.py --project PROJECT init --actor "Coordinator"
python3 scripts/compliance_manager.py --project PROJECT init --actor "Coordinator"

# First stage the original specification at inputs/specification-v1.pdf.
python3 scripts/intake_manager.py --project PROJECT create \
  --title "External specification" --owner "Requirements lead" \
  --source-key CLIENT-SPEC --version 1 \
  --file inputs/specification-v1.pdf --reference "Supplied specification, revision 1" \
  --license "Authorized internal project use" --confidentiality CONFIDENTIAL \
  --actor "Requirements lead"

python3 scripts/intake_manager.py --project PROJECT obligation SRC-0001 \
  --key CLIENT-001 --locator "Section 3.2, page 8" \
  --text "The product shall provide the specified interface." \
  --actor "Requirements lead"

# Repeat for every obligation; use --replace to correct a DRAFT entry.
python3 scripts/intake_manager.py --project PROJECT review SRC-0001 \
  --actor "Reviewer" --rationale "Inventory and extraction checked against the original"

python3 scripts/compliance_manager.py --project PROJECT create \
  --source SRC-0001 --obligation CLIENT-001 --owner "Requirements lead" --actor "Reviewer"

# Internal requirements and evidence are created using their existing tools.
python3 scripts/compliance_manager.py --project PROJECT map CMP-0001 \
  --requirement DEMO_SWE1_REQ_001@R1 --evidence EV-001 \
  --actor "Reviewer" --rationale "Interface obligation allocated and verified"

python3 scripts/intake_manager.py --project PROJECT audit --release
python3 scripts/compliance_manager.py --project PROJECT audit --release
python3 scripts/compliance_manager.py --project PROJECT report
```

To exclude a row, run `exclude CMP-0001 --actor ACTOR --rationale REASON`.
To reconsider applicability, use `reopen` with the same actor/rationale options.
To replace a source, run `supersede SRC-0001 --by SRC-0002 --actor ACTOR
--rationale REASON` after reviewing the new version. Source `list`/`report`
prints the authoritative record inventory. `render` reconstructs either
generated Markdown view after an interrupted view write.

## Audit and transaction guarantees

Both engines expose `audit(project, release=False) -> (errors, warnings)` and
`validate_registry(project, data) -> errors`; validation includes the common
registry shape and replayable hash-chained history. Release mode turns unresolved
applicability, missing rows and incomplete evidence coverage into blockers.
Stale links, invalid provenance, source/artifact modification, invalid ledgers
and duplicate identities are errors in every mode. Valid reviewed exclusions
are allowed. Existing legacy projects with neither registry are left untouched;
the combined management audit detects deletion of previously enabled stores.

The shared store serializes and atomically commits one changed record per
operation. Rejected transitions and invalid references leave authoritative
JSON unchanged. Views are generated after the authoritative commit; if view
generation fails, inspect the committed record and rerun `render` rather than
blindly retrying creation. No operation promises an atomic change spanning
source, compliance, requirement and evidence registries. Normal intermediate
states are explicit and prevent premature release.

History hashes detect inconsistent records; actor labels and hashes are not
authenticated signatures or protection against rewriting the entire Git
history. Keep independent Git review and repository access controls.

`intake_compliance_tests.py` covers lifecycle, immutable source review, duplicate
identities, source tampering, source version replacement, missing obligations,
exact revision/proof coverage, reviewed exclusions, stale revisions, malformed
JSON, legacy skip behavior and no-write rejection paths.
