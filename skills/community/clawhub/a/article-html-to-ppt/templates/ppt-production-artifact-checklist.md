# PPT Production Artifact Checklist

Resolve the production profile first, then generate only the artifacts required by that profile. Keep internal process files under `.ppt-work/`; keep the user-facing folder limited to the delivery package.

| Artifact | Fast | Standard | Premium |
|---|---:|---:|---:|
| Content Lock | Required | Required | Required |
| Storyboard | Optional | Required | Required |
| PPT IR | Required | Required | Required |
| Style Contract | Required | Required | Required |
| Asset Manifest | If used | Required if used | Required |
| Delivery Plan | Required | Required | Required |
| Build Manifest | Required | Required | Required |
| Full Render | Optional | Representative | Required |
| QA Report | Basic | Required | Required |
| Benchmark Score | No | Optional | Required |
| Verification Report | No | Required | Required |
| Delivery Manifest | Required | Required | Required |

## Internal Workspace

- [ ] `.ppt-work/contracts/production-profile.json` records `selected_profile`, `reason_codes`, required artifacts, required gates, and allowed skips.
- [ ] `.ppt-work/analysis/` contains profile-required analysis files only.
- [ ] `.ppt-work/contracts/` contains profile-required contracts only.
- [ ] `.ppt-work/renders/`, `.ppt-work/qa/`, `.ppt-work/logs/`, and `.ppt-work/checkpoints/` preserve evidence needed for the selected profile.
- [ ] Failed builds preserve `.ppt-work/` and record `resume_from`, `last_successful_stage`, and `failed_stage` in Build Manifest when available.

## User-Facing Delivery

- [ ] `deck.pptx` exists and is a readable PPTX package.
- [ ] `deck-preview.pdf` exists for Standard and Premium.
- [ ] `verification-report.md` exists for Standard and Premium.
- [ ] `delivery-manifest.json` validates against `schemas/delivery-manifest.schema.json`.
- [ ] Every user-facing file has a `sha256:` hash in Delivery Manifest.
- [ ] Delivery Manifest uses relative paths only.
- [ ] Privacy scan reports no private paths, tokens, temp files, undeclared private assets, or local-only links.
- [ ] The status is calculated by `scripts/package_delivery.py` or `scripts/verify_deck.py`, not written by hand.

## Status Gates

- [ ] Fast reaches at least `created`; `verified` requires passing hard gates.
- [ ] Standard reaches `verified` only when structural/readback QA passes with zero errors.
- [ ] Premium reaches `final` only with real full-render evidence, read back, zero QA errors, zero whole-slide raster, editability threshold met, rubric score at least 14, and fallbacks disclosed.
- [ ] Premium without render is never marked `final`.
