---
name: artifact-redactor
description: Public OpenClaw skill for redacting private paths, secret-like strings, private URLs, and common PII from Markdown, JSON, logs, and other text artifacts before sharing.
version: 1.0.7
homepage: https://github.com/zack-dev-cm/artifact-redactor
license: MIT-0
user-invocable: true
metadata: {"openclaw":{"homepage":"https://github.com/zack-dev-cm/artifact-redactor","skillKey":"artifact-redactor","requires":{"anyBins":["python3","python"]}}}
---

# Artifact Redactor

## Goal

Take a directory or file full of text artifacts and produce a safer share bundle:

- one scan of obvious sensitive text patterns
- one redacted output directory for supported text files
- one structural check of the redacted output plus a manual-review decision for skipped files
- one markdown report that explains what was found, what was redacted, and what still needs manual review

This skill is for text artifacts such as Markdown, JSON, logs, YAML, CSV, shell output, and similar files.
It does not claim to sanitize screenshots, PDFs, or other binary files.
It requires Python 3.9+.

## Use This Skill When

- a bug bundle, browser trace, experiment report, or release note needs to be shared outside the immediate team
- logs or manifests contain private paths, local URLs, token-like strings, email addresses, or phone numbers
- you want a safer public issue attachment without rewriting the artifact by hand
- you need a clear manual-review list for files the automatic pass did not rewrite

## Quick Start

1. Scan the source artifacts.
   - Use `python3 {baseDir}/scripts/scan_sensitive_text.py --root <source> --out <scan.json>`.
   - Point `--root` at either one file or a directory.

2. Write a redacted copy.
   - Use `python3 {baseDir}/scripts/redact_artifacts.py --root <source> --out-dir <safe-dir> --out <redaction.json>`.
   - This writes only supported text files into the output tree.
   - Binary or unsupported files are skipped and called out for manual review.

3. Check the output.
   - Use `python3 {baseDir}/scripts/check_redaction_output.py --root <safe-dir> --redaction <redaction.json> --out <check.json>`.
   - The check returns `share-ready` only when no supported-text findings remain and no skipped files still require manual review.
   - If skipped files exist, expect `manual-review-required` rather than a full-clear result.

4. Render the report.
   - Use `python3 {baseDir}/scripts/render_redaction_report.py --scan <scan.json> --redaction <redaction.json> --check <check.json> --out <report.md>`.
   - Share the report with the redacted output directory instead of the raw artifacts.

## Operating Rules

### Safety rules

- Keep the promise narrow: supported text files only.
- Treat screenshots, videos, PDFs, and other binary files as manual-review items.
- Prefer preserving public context when safe. Public URLs may stay, but query strings and fragments should be removed.
- Replace sensitive values with stable placeholders instead of deleting surrounding context.

### Review rules

- Re-scan the redacted output before sharing it.
- If the output check returns `fix-required` or `manual-review-required`, do not present the full bundle as cleared.
- Manual-review lists are part of the deliverable, not optional cleanup.

## Bundled Scripts

- `scripts/scan_sensitive_text.py`
  - Scan files for obvious sensitive text patterns and emit JSON findings.
- `scripts/redact_artifacts.py`
  - Write a redacted copy of supported text files into a separate output directory.
- `scripts/check_redaction_output.py`
  - Re-scan the redacted output and emit `share-ready`, `manual-review-required`, or `fix-required`.
- `scripts/render_redaction_report.py`
  - Render a concise markdown summary from the scan, redaction, and check JSON outputs.
