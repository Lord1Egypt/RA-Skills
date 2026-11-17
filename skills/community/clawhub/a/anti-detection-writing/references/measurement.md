# Optional detector measurement

Use the service and browser requested by the user through supported browser controls. Do not substitute a different session for an explicit browser request. Let the user complete sign-in if needed. Preserve the user's scan mode and spending constraints. Agree a bounded attempt count before an open-ended experiment.

1. Save the baseline, source evidence, claim inventory, and candidate. Select multiple cases before seeing scores and record selection reasons. Keep the original and candidate names unambiguous.
2. Review technical correctness before interpreting detector results. A score cannot resolve a factual objection. Keep the separate reviewer unaware of scores when assessing quality.
3. Paste the complete intended text, including code and qualifications. Read the effective editor text back and compare with the actual file. Preserve the original Markdown, exact submitted representation, and exact editor text separately if they differ.
4. Do not accept broad normalization that can hide changed words or code. An observed editor once merged adjacent `api` and `ui` spans into `apiui`; that input was invalid. If rendering changes content, repair entry and repeat verification before scanning. Keep invalid attempts in an audit log.
5. Run the selected scan. Confirm completion, mode, model, and a visibly current result. On GPTZero, `Text changed` or `Scan to update` means the displayed score may belong to an earlier input; wait for a completed `Text up-to-date` result.
6. Record AI, mixed, and human confidences separately, the timestamp, displayed length, any short-text warning, and exact input hashes. Save a private visible-result snapshot. If the UI or model differs between paired scans, report the mismatch rather than treating it as comparable evidence.
7. Any wording or code change after scanning invalidates that text's receipt for the new version. If the user requires a threshold, apply it to the final text only. Never call a lower AI confidence proof of human authorship.

The supplied strict receipt checker accepts only verbatim plain-text entry, apart from CRLF/LF line endings. Prefer an editor mode that preserves literal source text. If Markdown renders differently, the checker rejects the mismatch: do not rewrite a receipt to hide it. Either use a verified entry method preserving the intended source or explicitly report that this checker cannot validate that representation. Historical studies used separately recorded formatting checks and are not in the new strict receipt format.

For a quotation comparison, write and review the plain answer first, choose one short useful excerpt before scores, then hold the body fixed. Record the added words and retain unchanged outcomes. Prose edits and quotations are different interventions. Do not rotate excerpts or add unrelated material to lower a score.

Before sharing study artifacts, export only an allowlist of public fields. Remove session/document URLs, account details, credentials, quota UI, local paths, and unnecessary copies of other people's questions. Attribute necessary short excerpts. State whether the scores are observed UI records or authenticated service exports; do not imply one is the other.
