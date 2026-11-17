# Changelog

All notable changes to this skill are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [SemVer](https://semver.org).

## [0.0.2] - 2026-09-17

### Changed

- Perceive now documents the blocked-read contract: a detected content-free block is a `200` with
  `is_blocked: true`, empty `outputs` and `billed: false`; `billed` is also `false` when
  `deductions` contain `http_error` or `login_wall`. `render_quality` under 0.40 must not be
  presented as content.
- Errors section gains `429` / `Retry-After` and the blocked-page shape.
- README: the publish command is inlined; the link to the removed `clawhub-enconvert-deploy/`
  folder is gone.

## [0.0.1] - 2026-08-27

### Fixed before first publish (verified against the live API, 2026-08-31)

- Web Search documented `POST /v2/search`, which 404s. The endpoint is `POST /v2/lookup`.
- Perceive's response shape was wrong: every artifact under `outputs` is a 15-minute signed
  URL, markdown included — nothing is inline text. `structured` is returned at the top level,
  not under `outputs`.
- Extract Structured's response shape was wrong: fields are per URL in `results[].data`, with
  `extraction_tier` per result. There is no top-level `data` or `extraction_tier`.
- `scripts/convert.sh` failed on every input: it downloaded to a bare `mktemp` name, and the
  API detects the input format from the file extension (`400 Invalid file format '.lJzoMq6Akq'`).
  It now keeps the source filename, surfaces the API's error body instead of a bare curl code,
  and no longer dies in `set -e` when the response has no `presigned_url`.

### Added

- Initial release. `SKILL.md` instructs an OpenClaw agent to drive EnConvert's six operations
  against `https://api.enconvert.com`: Perceive URL, Web Search, Discover URLs, Extract
  Structured (distill), Convert File to Markdown, and Convert File to PDF.
- Auth via the `ENCONVERT_API_KEY` secret (private `sk_` key); the key is never hardcoded, and
  the download of source file URLs and the fetch of signed/presigned output URLs deliberately
  omit it. `GET /v1/whoami` validates a key.
- Emphasises the `render_quality` (0.0-1.0) honesty score on every perceive.
- `scripts/convert.sh` — curl helper that downloads a file URL (no key), multipart-posts it as
  `file` (with key), and prints the result's `presigned_url`.
