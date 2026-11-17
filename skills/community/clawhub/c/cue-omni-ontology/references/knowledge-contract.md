# Knowledge input and package contract — schema 0.1.0, skill 0.2.0

## Input

Input is host-extracted JSON, not a URL request. The offline tool does not invoke Omni or an LLM. Use `assets/demo/r1.json` as an executable shape example. Its organizations, products, facts and example.org URLs are synthetic, not real disclosures.

Required root keys: `schema_version: "0.1.0"`, `scope: {title, as_of}`, `entities`, `definitions`, `sources`, `assertions`. `as_of` is YYYY-MM-DD and describes the package observation cut-off, not every fact's effective date. Keep the same title across a lineage.

IDs match `[A-Za-z][A-Za-z0-9_.:-]{0,119}`. Entity types are Organization, Product, BusinessSegment, Topic. Do not encode every metric as an entity. Entities need id, type, name. Identity resolution is an explicit host/expert responsibility.

Definitions need id, kind (`metric|relation|attribute`), name, description, value_type (`number|string|boolean|entity|set`), status (`candidate`). Relations use entity values referencing a known entity. Set values are sorted unique nonempty strings, not evidence of an exhaustive universe. Extra meanings cannot reuse an old ID.

Each source needs id, URL, title, published_at (YYYY-MM-DD or null), accessed_at (YYYY-MM-DD), public_status (`user_confirmed|retrieved_public|synthetic`), parse_origin (`omni_live|omni_replay|synthetic|other`), content_file (relative UTF-8 file), sha256, and optional page_spans. `omni_replay` means saved Omni output; it must not be described as a fresh parse. Keep unrelated response metadata and credentials out.

`page_spans` is an ordered nonoverlapping list of `{page,start_utf8,end_utf8,basis}`. Pages are positive, unique and 1-based; ranges are half-open UTF-8 byte ranges. Basis is `omni_native_source_pdf_page`, `manual_page` or `synthetic_page`. Copy actual Omni page ranges/anchors, preserving the text they index; `ontology.py omni-source` derives them from a saved grounded result (source-PDF page anchors only). The checker tests the supplied alignment; it cannot authenticate the origin of a sidecar. Without a supported page mapping use no page spans and text-range evidence.

Source IDs represent immutable snapshots. Reuse the exact old record for the same snapshot (including original retrieval metadata), or use a new version ID. Changed source content cannot reuse an old source ID. Input file paths must remain inside the input JSON directory; parent traversal and escaping symlinks are rejected. Files are capped at 32 MiB each. URL checks do not establish actual public accessibility.

Each assertion needs entity_id, concept_id, value, unit, period, basis, qualifiers (flat scalar object), valid_from/valid_to (YYYY-MM-DD or null), claim_kind (`reported`), evidence (nonempty). Use explicit `not_applicable` rather than a blank unit/period/basis for nonnumeric relationships. Preserve raw disclosure units or normalize explicitly with recorded rationale; the tool performs no currency/unit conversion. Do not assume differently worded periods or concepts are equivalent.

Each evidence item is `{source_id,start_utf8,end_utf8,span_sha256,role,page,locator_basis}`. Use `page: null, locator_basis: "text_range"` if no grounded page is available. Otherwise locator_basis must match a containing source page span. Roles can identify value, unit header, period header or qualifying footnote. All bytes must come from the referenced parsed file. Evidence must semantically support the assertion; the checker only verifies ranges/hashes/declared alignment.

Build inputs cannot inject acceptance or reviews. The packager adds status `candidate`, reviews `[]`, fact_id and assertion id. Facts are keyed by entity, concept, unit, period, basis, qualifiers and validity. Source assertions additionally include value and supporting evidence. Numeric spellings such as 100 and 100.0 compare equal for conflict/support classification; original values and assertion IDs remain unchanged. No approximate tolerance or unit conversion is applied. Equivalent evidence reorderings deduplicate; changed ranges may create another supporting assertion. IDs are local content-derived identifiers, not externally certified identities.

The skill version is independent of schema version. Skill 0.2.0 continues to read and write schema 0.1.0; existing knowledge hashes and IDs are not migrated. Queries return available `scopes`; `--fact` selects one whole scope, including any conflict. `--unit`, `--valid-from` and `--valid-to` match exact values. They do not resolve effective-date precedence.

## Package

- `knowledge.json`: full normalized graph-shaped data and preserved review records.
- `sources.jsonl`: exact source records, one canonical JSON object per line.
- `changes.json`: previous/current hashes and change categories; missing batch entries are not removals.
- `run.json`: skill/schema version, local operation, counts and hashes. No parser cost is inferred.
- `report.md`: generated review table, conflicts and source references. It is not an independent factual assessment.
- `evidence/*.txt`: exact snapshots for reproduction; source URLs remain available separately.
- `extraction-notes.md`: supplied separately by the host, recording model, extraction scope, failed sources, gaps and semantic review. Not generated by the offline tool.

Use a new output directory for each version. The tool validates before final rename and does not overwrite existing versions. It records local decisions, not IAM, concurrent transactions, signatures or tamper-proof history. An actor able to rewrite all hashes can rewrite the package. Keep production authority in enterprise systems.

## Outputs and sharing

Keep necessary source snapshots in the authorized task workspace. Publishing a complete package may redistribute its full parsed sources; select only authorized evidence and appropriate short excerpts for public examples. Do not treat public availability as permission to republish entire materials. Share feedback drafts separately from knowledge packages.

OKF export emits candidate concept files with `type`, `title`, `status: draft`, source references and claims. `index.md` is navigation. It targets the v0.2 core subset, has no `verified` claim, embeds no authority to execute, and has not established compatibility with any external consumer. Core source: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md .

## Convenience workflows in 0.2

`prepare` converts verbatim quote evidence to the same 0.1.0 schema; see [quote-input.md](quote-input.md). `brief` emits searchable offline HTML, Markdown and JSON with up to 400 characters per evidence range. Truncation is explicit. Briefs do not embed complete source files and are derivatives, not a replacement for the integrity-checked package. When comparing versions, every baseline entity, definition, source, assertion and review prefix must be retained; an unrelated package is rejected.

`demo --out NEW_DIRECTORY` runs the synthetic build/update/brief without API access. `query --with-evidence` returns excerpts plus source URLs and locators. The host must still assess semantic support and answer the user's business questions. No automatic claims about causality, ROI or business events are generated.
