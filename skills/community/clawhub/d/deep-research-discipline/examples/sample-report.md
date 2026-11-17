# Sample report: OpenClaw 2026.11.1 release facts

> Sanitized worked example. All sources are public; no internal paths, accounts, or private data. It shows the labeling style, not a topic recommendation.

`capabilities: search=yes fetch=yes files=yes dates=partial documents=no social=no`

## One-line answer

OpenClaw 2026.11.1 is a patch release dated 2026-11-05 that adds no features, fixes Feishu streaming and action-card formatting, and changes Doctor to return a non-zero exit code on failed inspections.

## Key findings

1. 2026.11.1 is described as a patch release with no new features. [verified: release changelog, retrieved 2026-11-07; release tag body, same date]
2. It fixes Feishu losing streamed text across tool calls and sending action cards in the wrong format. [verified: changelog line, retrieved 2026-11-07; same wording in the release body]
3. Doctor now returns a non-zero exit code when inspection is blocked, config is invalid, or migrations are deferred. [verified: changelog, retrieved 2026-11-07]
4. Whether these fixes also apply to the 2026.10.x line is unresolved. [unresolved: no backport note found in the changelog; two queries tried]

## Key data

| Item | Value | Source | Retrieved |
|---|---|---|---|
| Version | 2026.11.1 | npm registry | 2026-11-07 |
| Published | 2026-11-05T09:41:26Z | npm registry time field | 2026-11-07 |
| Previous security release | 2026.10.9 | changelog heading | 2026-11-07 |

## Conflicting or missing evidence

- The release body does not enumerate CVEs for the preceding security release; it says only that dependency remediations are included. No CVE mapping was found, so no applicability claim is made.

## Analysis

The release sits after a security-oriented patch (2026.10.9) and a larger feature release (2026.10.10). Its own scope is narrow: messaging reliability, Doctor exit semantics, and Gateway configuration-write handling. That ordering matters for upgrade planning — a jump from 2026.10.8 accumulates three releases, not one.

## Limitations

- `documents=no`: linked PDFs were not opened.
- `social=no`: no community discussion was sampled.
- `dates=partial`: recency filtering was applied manually, not by the search tool.
- No claim is made about runtime behaviour; this report covers published statements only.

## Independent review record

Reviewer type: separate agent session, primary sources only, conclusion withheld until after re-check.

| Point | Verdict | Reviewer evidence |
|---|---|---|
| 2026.11.1 exists and is latest on the stable channel | PASS | registry dist-tags |
| Patch release wording | PASS | changelog first paragraph |
| Feishu fix wording | PASS | changelog Messaging section |
| Doctor exit-code change | PASS | changelog Updates and Maintenance section |

## References

- Release changelog: `https://raw.githubusercontent.com/openclaw/openclaw/main/CHANGELOG/2026.11.1.md` (retrieved 2026-11-07)
- npm registry metadata for `openclaw` (retrieved 2026-11-07)
