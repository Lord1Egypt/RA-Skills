# Verification Policy

## Evidence hierarchy

1. Crossref is the fastest and strongest default primary source for journal DOI, title, authors, journal, publisher, and year.
2. PubMed is the second evidence line for biomedical records, PMID mapping, and wrong PMID/title-pair detection.
3. OpenAlex is the third default evidence line for fast DOI/PMID external-ID corroboration and title recovery when Crossref is weak.
4. A DOI match from Crossref is the primary batch verification result. PubMed and OpenAlex matches can corroborate it, but should not block reporting.
5. Semantic Scholar, Europe PMC, bioRxiv/medRxiv, DataCite, and OpenCitations are backup channels, not default full-batch channels.
6. Search snippets, AI summaries, formatted APA/GB/T entries, and plausible journal names are not proof.
7. `biomedical-reference-verifier.records.v1` is the source-of-truth input layer. Source fields must come from the user's text; database-returned fields must stay in evidence/report/output objects.

## Error types

- `verified`: DOI/PMID or title search resolves to a canonical record and title, year, and first-author evidence agree.
- `verified_identifier_only`: DOI/PMID resolves to a canonical record, but the source title is missing or unreliable, so only the identifier is verified.
- `parser_error`: the input row is malformed or the parsed/source title is an author line, table header, metadata field, or other non-title text; stop before treating the row as a bibliographic conflict.
- `formatted_only`: formatting executed, authenticity not checked; not eligible for use on that basis.
- `minor_fix` / `minor_format_error`: the paper is real and metadata agree; only DOI casing, punctuation, URL style, initials, journal abbreviation, or minor year formatting needs correction.
- `partial_attribute_corruption`: the paper is real, but one or more attributes are corrupted, such as author, title, journal, year, volume/pages, DOI, or PMID.
- `identifier_hijacking`: DOI, PMID, or URL is real, but it points to a different paper than the reference text.
- `shifted_identifier`: DOI or PMID appears to belong to a nearby reference, commonly because one entry's DOI was attached to the previous or next citation.
- `semantic_hallucination`: the paper exists, but a surrounding claim or summary is not supported by that paper.
- `placeholder_generation`: the entry contains AI-like placeholder traces: generic title, invented DOI suffix, fake pages/volume, missing journal fields, or overly tidy but unverifiable metadata.
- `total_fabrication`: title, authors, journal, year, DOI/PMID, and searches fail to identify any canonical record.
- `unresolved`: automatic checks are insufficient; stop and ask before expensive manual recovery.

## Matching thresholds

- Title similarity >= 0.90: strong match.
- Title similarity 0.86-0.89: acceptable match if year and first author agree.
- Title similarity 0.78-0.85: possible match; mark as partial unless corroborated by DOI/PMID.
- Title similarity < 0.70 for a supplied DOI/PMID: identifier hijacking unless adjacent-entry checks prove shifted identifier.
- A one-year difference may be online-first drift, but remains a field difference unless source dates establish equivalence. Missing year/author evidence cannot satisfy full verification.
- Author disagreement prevents automatic approval. Compare available authors and report differences. A differing journal is a conflict unless an explicit provider abbreviation matches.

## Short-circuit rules

- Build `biomedical-reference-verifier.records.v1` first. Do not let remote lookup run against raw mixed notes when the source can be converted to explicit source objects.
- Required machine fields are `index`, `source.original_text`, `source.title`, `source.authors`, `source.year`, `source.journal`, `source.identifiers.doi`, `source.identifiers.pmid`, `source.identifiers.urls`, `source.source_lines`, and `source.context`.
- During machine-record construction, AI may only extract values present in the source text. It must not use Crossref/PubMed/OpenAlex results, memory, or plausible completions to fill source fields.
- Build `reference-normalized-records.json` before remote lookup. `reference-normalized-input.md` is a human-readable view of the same records.
- If `source.title` is missing, too short, an author list, a table/header label, a DOI/PMID line, or metadata placeholder, mark the title unreliable.
- If a DOI/PMID resolves but title is unreliable, mark `verified_identifier_only`; do not mark `identifier_hijacking`.
- If a row has no reliable title and no resolvable DOI/PMID, mark `parser_error` and stop.
- Use DOI verification first: `GET https://api.crossref.org/works/{doi}`. This is the primary source of DOI/title/author/journal/year truth.
- Start enabled evidence lines together. Fast stops after primary evidence, Balanced allows a 2.5-second auxiliary grace period after primary DOI lookup and enabled supplied-PMID lookup, and Strict waits for every enabled line to complete or explicitly fail. Network timeout, rate limiting, not-found, parsing failure, mode skip, and expired budget must remain distinguishable.
- If PubMed and OpenAlex are disabled with `--pubmed-mode off --openalex-mode off`, do not apply the grace timer to Crossref; Crossref DOI verification must complete because it is the primary authority.
- OpenAlex checks use `GET https://api.openalex.org/works/doi:{doi}` or external IDs such as `pmid:{pmid}` for PMID, and `GET https://api.openalex.org/works?search={title}&per_page=3` for DOI-missing title recovery.
- If an entry has no DOI, use title recovery in this order: Crossref title query first, OpenAlex title query only if the Crossref match is weak, PubMed title query only if biomedical corroboration is still needed. Record recovered DOI values in the report and ask before adding them to formatted citations.
- Run quality-checked DOI-missing title recovery before full identifier verification, deduplicated and with provider-specific bounded concurrency. A recovered DOI may drive verification but must not silently modify the user source.
- Do not use title search to silently override an existing DOI result. Existing DOI conflicts should be reported as conflicts, hijacking, or shifted identifiers.
- Run near official limits without exceeding them: Crossref polite requests use no more than 10 requests/second and 3 concurrent requests; PubMed E-utilities uses no more than 3 requests/second without an API key and 10 requests/second with an NCBI API key; OpenAlex is budget/cost governed, so keep default concurrency conservative unless an API key and live limit headers justify more.
- Use one bounded retry only for timeout, temporary connection failure, HTTP 429, or HTTP 5xx. Respect `Retry-After` within a bounded wait. Do not retry permanent 4xx responses. If a PubMed DOI batch fails, split it recursively until the failing DOI is isolated.
- For large DOI-heavy documents, Crossref parallel DOI lookup is the primary full-batch path. PubMed and OpenAlex are corroboration channels, not reasons to block report generation.
- If DOI/PMID resolves and title similarity is < 0.70, stop trusting that identifier for the current entry and mark `identifier_hijacking`.
- Apply the < 0.70 hijacking rule only when the source title passed input quality checks.
- Before finalizing `identifier_hijacking`, compare the resolved title against entries within two positions. If adjacent similarity is >= 0.86, mark `shifted_identifier`.
- If several consecutive identifiers are shifted by the same offset, report a possible column/line offset instead of repairing each item manually.
- For entries with DOI, run DOI lookup and report the DOI result; do not automatically title-search to replace the DOI.
- For entries without DOI, run at most one Crossref title recovery query. If title recovery fails, mark `unresolved`, `placeholder_generation`, or `total_fabrication`; do not keep prompting the model to guess.
- Do not run title recovery when `source_title` failed input quality checks. Rebuild the worksheet row first.
- Use backup channels conditionally: Semantic Scholar only for title/abstract/citation corroboration after default lines are inconclusive; Europe PMC for biomedical PMCID/full-text evidence; bioRxiv/medRxiv for `10.1101/...` and published-DOI mapping; DataCite for non-journal dataset/software/report DOIs; OpenCitations for citation-network existence checks.
- Parse every channel response by code into one canonical record shape: `source`, `title`, `authors`, `journal`, `year`, `doi`, `pmid`, `url`, and `score`. AI must not manually interpret structured API responses when parser adapters are available.
- If the severe-error rate is high, stop after batch recovery and ask the user whether to continue AI-assisted per-paper search.

## Network risk policy

- Default DOI/PMID verification is low risk and should run without asking the user each time. The payload is limited to public identifiers required for the skill's purpose.
- Default requests must not include `original_text`, manuscript paragraphs, abstracts, local evidence notes, or unpublished claims.
- DOI-missing recovery may send only a short, quality-checked `source.title`.
- Any deep search that sends title plus abstract, surrounding context, or manuscript-derived claims is higher risk and must be separated from default batch verification.
- If Codex sandbox approval blocks external lookup, continue with local records normalization and report that external evidence was not executed.

## Channel parser contract

- Crossref `/works/{doi}` returns a `message` object; parse `title`, `author`, `container-title`, `issued`/published dates, `DOI`, and `URL`.
- PubMed EFetch returns XML; parse `ArticleTitle`, `Author`, `Journal`, `PubDate`, `ArticleId IdType="doi"`, and `PMID`.
- OpenAlex works return work objects; parse `display_name`/`title`, `authorships`, `primary_location.source.display_name`, `publication_year`, `doi`, and `ids.pmid`.
- Europe PMC search results return result objects; parse `title`, `authorString`, `journalTitle`, `pubYear`, `doi`, `pmid`, and `pmcid`.
- Semantic Scholar Graph results return paper objects; parse `title`, `authors`, `venue`/`journal`, `year`, `externalIds.DOI`, `externalIds.PubMed`, and `url`.
- DataCite DOI records return JSON:API objects; parse `data.attributes.titles`, `creators`, `publisher`/`container`, `publicationYear`, `doi`, and `url`.
- bioRxiv/medRxiv API results return collection items; parse `title`, `authors`, `date`, `doi`, and `published_doi`.

## Auto-fix policy

Auto-fix only when canonical evidence is strong:

- normalize DOI casing and links
- strip trailing DOI punctuation
- normalize DOI links in reports
- record missing DOI candidates from canonical metadata and ask before appending them
- include PMID only as secondary metadata when DOI-backed evidence exists
- standardize journal title or abbreviation
- normalize author initials and year formatting
- report shifted DOI/PMID as a candidate relationship; retain the original until the proposed move is reviewed

Do not auto-delete or silently replace severe items. For identifier-only, shifted, hijacked, fabricated, unresolved, and any partial/conflicting records, retain the original and report. Only verified/minor results may be automatically reformatted. Keep per-field before/after evidence.

Do not create hidden persistent caches. Reuse prior results only from an explicitly supplied structured verifier artifact, and re-query new, changed, or incomplete records.

## Format policy

- Detect citation style before repair: APA, GB/T 7714, Vancouver/AMA, free-text, or mixed.
- Preserve original format in the automatic fixed copy when possible.
- If the list is mixed, recommend standardizing to the majority format after authenticity checks.
- Formatting correctness is never authenticity evidence.

## Body-vs-bibliography audit

Only execute this section when the user explicitly requests manuscript-body checking or cleanup. Bibliography verification alone does not authorize changing body claims.

- Scan body text for narrative citations like `Author et al. (2023)` and parenthetical citations like `(Author, 2023)`.
- Compare author/year/title semantics, not just numbered reference markers.
- After deleting or flagging a fabricated reference, remove or flag body claims that depend on it.
- Report uncertain claims separately instead of silently preserving them.

## Eligibility, reuse and cleanup

- The user requires a positive-use gate: references that cannot be verified are not usable. Identifier existence alone is insufficient. Formatting-only results are not authenticity passes. Preserve detailed reasons alongside this gate.
- Results record verification coverage, eligibility, repair state and field differences independently. HTML groups are navigation aids, not replacements for these fields.
- Reuse only complete compatible evidence checked within 30 days under the current policy, with all source fields unchanged. Stronger modes and additional channels require fresh checks. Regenerate formatted output under the current options.
- Clean current-run redundant parser views/extracted copies by default; retain normalized source records and requested evidence artifacts. Honor `--cleanup-process-files none`. Ask after each round about retaining the remaining process files; no answer means keep. Never erase prior evidence just because an output option was omitted.

## Real-reference matching details

Trailing `et al.` denotes author truncation, not a named author. Compare the named prefix after conservative typographic normalization. Do not approve a different second or third author. Parse PubMed collective authors. A title containing commas is valid unless the comma-separated pieces actually have author-name syntax.

Recognized publisher placeholder titles are inadequate metadata. A matching record from an enabled channel for the same DOI may supply the bibliographic title, with the fallback recorded. Without such evidence, retain an unresolved result; do not declare hijacking from the placeholder.

Page forms such as `E5503-12` and `E5503-E5512`, or `e136-e136` and `e136`, are equivalent. Distinct electronic article numbers are not normalized into one another. Same-DOI journal aliases and explicit provider publication-year values are evidence of legitimate variants. Retain provider-specific records in the audit JSON.
