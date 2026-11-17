# Update policy

1. Validate the previous package before reading it as a baseline. Reuse its exact definitions and stable IDs.
2. Extract the new source material independently, including all definitions/entities required by new claims. Keep source evidence complete and versioned.
3. Add claims; never infer deletion from absence. The updater is append-only for sources, entities, definitions and assertions.
4. Identical assertions are duplicates. New support for the same fact/value is additional support. Numeric spellings such as 100 and 100.0 are equal for support/conflict checks while original values and IDs remain preserved. A different value under the same fact key creates a conflict until reviewed; this includes restatements. No source wins automatically.
5. A different period/basis/unit/exclusion is a different fact. Describe comparability explicitly, not by matching labels. Product-name list differences alone do not establish renames or retirement.
6. Existing definition/source IDs cannot silently change content. Diagnose extraction mistakes first. For genuine new meanings, create a candidate with a new ID, preserving historical definitions and explaining the proposed relationship in extraction notes.
7. Repeated updates retain prior review decisions. `review` creates a new version; it changes a specific assertion's selection status, not the business rule or source truth.
8. Acceptance does not automatically resolve conflicting assertions. A user may explicitly reject an obsolete assertion with a reason, retaining its history. Formal effective-date resolution and enterprise approval are outside v0.2.

Before interpreting a candidate change, check source completeness, time scope, identity, units, synonyms, extraction coverage and whether a list is exhaustive. “New to this package” is the only automatic novelty claim.
