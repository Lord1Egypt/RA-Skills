# Expected Output Notes

A successful run should provide:

- a handoff pack with one independent prompt per job
- generated prompts that separate visual freedom from readable factual text
- stored fact sensitivity, selected render strategy, readable-text allowlist, and forbidden patterns
- a text-overlay plan when a high-sensitivity job routes to `mixed` or `deterministic`
- a checksum-locked mixed-render report when a generated background is finished with exact local typography
- a visibly preserved generated composition for every result reported as `mixed`; localized text failures are patched locally, while text-free backgrounds are reserved for widespread failures
- `jobs.json` with `backend=auto`, inspected capabilities, the selected backend, and a readable selection reason
- a safe pause immediately before the first Computer Use submission or reference upload
- a manual prompt-pack route when Computer Use is unavailable
- stable imported filenames, checksums, dimensions, and per-image visual QA
- a required `text_policy_qa=passed` record before strict jobs can pass visual QA
- a contact sheet for overview review
- `human_confirmation=pending` until the user actually approves the outputs
- a downstream handoff to `cards-to-images`, `article-to-illustrations`, or `md-img-r2` plan mode

The output should not contain account details, stored browser state, hardcoded UI selectors, paid-generation assumptions, invented hashes or identifiers, readable facts outside a strict allowlist, a `mixed` label on a visually deterministic result, or a claim that prompt preparation equals completed image delivery.
