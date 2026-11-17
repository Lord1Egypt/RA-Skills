# Asset record fields

A version 1 inventory contains an `assets` array. Each row has a stable ID, relative image path or null, intended use, factual visible-content description, alt text, a source/provenance note, and review state (`approved`, `needs_review`, or `rejected`).

Only approved rows may point to a deliverable file. Paths must remain inside the inventory directory and may not traverse a symlink outside it. Accepted formats are static PNG, JPEG and WebP. The image is decoded locally; its actual format and pixel dimensions are returned in the summary.

A pending row remains pending and contributes no usable file. An alt-text string is not proof that it matches the image. The tool does not validate copyright ownership; the source field is a record supplied by the operator.
