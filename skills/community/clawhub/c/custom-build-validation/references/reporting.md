# Structured result and native comment publisher

The worksheet remains the only authored ledger. At closeout derive a private
JSON export and sanitized Markdown draft from it; regenerate both after edits.
These are exports, not independent progress stores. Use schema
`openclaw.custom-build-report/v1`; never the official campaign/vote schema.

Required object fields (unknown keys rejected by the helper):

- `schema`: exact schema name above.
- `runId`: stable UUID for this validation, reused for retries.
- `baseSha`, `candidateSha`, `candidateTree`: full 40-character Git hashes.
- `patches`: ordered full commit hashes, possibly empty.
- `result`: passed, failed, blocked, or not-evaluated.
- `cleanup`: complete, retained, failed, or not-required.
- `tests`: entries containing `surface`, `result` (passed/failed/blocked), and
  `proof` (source/automated/runtime/human). These are observations, not plans.
- `artifacts`: entries containing `component`, SHA-256 `sha256`, and `platform`.
  Local paths belong only in the worksheet.
- `summary`: sanitized concise observed result.

A pass requires observed passing tests and no failed/blocked test; a required
gap is blocked. A failed test requires a failed overall result. The helper
checks consistency, not whether measurements are genuine or text is secret-free.
Baseline reproduction gaps and untested platforms must remain visible in the
summary. A local dirty patch must be represented by the recorded candidateTree
and ordered patch evidence; do not attribute it to candidateSha alone.

Test results describe whether each named validation check met its expectation.
For example, `Baseline reproduces lost completion` passes when that loss was
observed as expected; preserve the actual baseline failure in the worksheet and
summary. Do not relabel an unexpected candidate failure as successful reproduction.
Keep candidate recovery as a separate check. Reserve `retained` for intentional
retention; give the reason and any remaining action without private paths.
If attempted cleanup fails, use `failed`, including when other artifacts were
intentionally retained. Do not relabel failed, unknown, or unfinished cleanup as
retention. Use `complete` for completed cleanup and `not-required` when none was
required; keep unattempted required cleanup explicit before final closeout.

Render before review (stdout is the complete comment draft):

```sh
node <skill-directory>/scripts/report.mjs <sanitized-export.json>
```

It validates the contract, produces visible Markdown and an escaped hidden JSON
envelope, and enforces the 60,000 UTF-8 byte limit. Capture output to a private
draft using the host's supported artifact mechanism. Review all text, including
the hidden payload; escaping HTML is not redaction. Never include raw logs,
telemetry, private paths, usernames, credentials or private conversation content.

## Publish comments, not campaigns

Select exact PR/issue destinations from the relevant findings and verify their
repository/number/title. Keep OCM and Crabbox findings with their own owners.
Prepare one complete draft per destination and show it to the operator.
Approval must cover those bytes and destinations; approval to write this skill
is not permission to post. No workflow dispatch, issue creation or labels.

Use GitHub's native issue-comment API (also applies to PR conversation comments),
not a new credential-bearing publisher service. With the verified `owner/repo`
and number, first resolve the current login via `gh api user`, then read all
pages of `repos/<owner>/<repo>/issues/<number>/comments`. Match only comments by
that login containing the exact runId envelope. Zero matches permits creation;
one identical body means already published; one different body needs approved
replacement; multiple matches or malformed envelopes block publishing.

Create using the reviewed Markdown file:

```sh
gh api --method POST repos/<owner>/<repo>/issues/<number>/comments -F body=@<approved-comment.md>
```

For a specifically approved replacement, use PATCH on
`repos/<owner>/<repo>/issues/comments/<verified-comment-id>` with the same body
file. Immediately before PATCH, re-read the comment; if its body differs from
the reviewed previous body, stop to avoid overwriting concurrent edits.
GitHub issue comments offer no transactional compare-and-swap here; if exclusive
ownership cannot be established, keep the draft and report the conflict.

After any write, GET the returned comment ID and require author, parent issue,
visible body, marker and JSON to match the approved draft. An uncertain POST
response requires the lookup above before any retry. Reuse the same runId;
never blindly create a duplicate. Each new validation run gets a new runId and
comment, preserving prior evidence without rewriting another person's post.

Return verified comment URLs. If requested, give a copy-ready Discord summary
with candidate/base SHA, tested platforms/surfaces, outcome, caveats and links.
Do not post to Discord automatically.
