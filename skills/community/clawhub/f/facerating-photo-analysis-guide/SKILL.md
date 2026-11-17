---
name: facerating-photo-analysis-guide
description: Prepare and review repeatable photo-based face measurements for consenting adults. Use for capture setup, neutral interpretation, style guidance, scan comparison, FaceRating tool selection, and report preparation; never identify people, infer sensitive traits, diagnose conditions, or treat a face score as personal worth.
metadata:
  openclaw:
    homepage: https://facerating.me/tools
    version: 1.0.0
---

# FaceRating Photo Analysis Guide

Help consenting adults prepare and interpret photo-based facial measurements without turning a measurement into a judgment about the person. This Skill is text-only by default. Its optional MCP is deterministic and read-only: it does not inspect photos, identify people, score attractiveness, infer sensitive traits, access accounts, consume credits, charge payments, or submit reports.

## Set the boundary first

Confirm that the subject is an adult and permitted the photo's use. Do not use this workflow for minors, identity verification, access control, surveillance, medical diagnosis, health assessment, ethnicity, personality, emotion, or other sensitive-trait inference. Do not claim that symmetry, ratios, age estimates, or any composite score objectively defines beauty or personal worth.

## Prepare a repeatable photo

Use a front-facing pose, neutral expression, visible landmarks, soft even lighting, eye-level camera, and enough distance to reduce wide-angle distortion. Avoid filters and portrait reshaping. For comparisons, keep camera, distance, framing, lighting, expression, and head position consistent.

## Use the optional MCP

- `plan_face_photo_capture` checks consent, adult use, pose, lighting, visibility, and camera setup.
- `review_face_measurements` organizes user-supplied values with neutral interpretation and safety limits.
- `compare_face_scan_sessions` calculates supplied score deltas only after comparable conditions are confirmed.
- `get_facerating_resources` returns canonical public FaceRating pages.

Connect the stdio server with:

```bash
openclaw mcp add facerating \
  --command npx \
  --arg -y \
  --arg github:gpt-img-2/facerating-photo-analysis-mcp \
  --include 'plan_face_photo_capture,review_face_measurements,compare_face_scan_sessions,get_facerating_resources'
```

Then run `openclaw mcp doctor facerating --probe`. If the installed release lacks that command group, add `npx -y github:gpt-img-2/facerating-photo-analysis-mcp` as a Stdio server in MCP settings. Never imply that the MCP or FaceRating analyzed a photo when it did not.

## Return a careful result

Separate `Observed inputs`, `Measurement context`, `Photo limitations`, `Neutral interpretation`, `Practical next step`, and `Retake conditions`. Prefer concrete photography or style suggestions over rankings. If the user reports distress or fixation about appearance, stop reinforcing scores and encourage a break or support from a trusted person or qualified professional.

## Canonical resources

- Tools: https://facerating.me/tools
- Face symmetry: https://facerating.me/tools/symmetry
- Facial ratios: https://facerating.me/tools/facial-ratios
- Face shape: https://facerating.me/tools/face-shape
- Complete report: https://facerating.me/tools/full-analysis
- Sample report: https://facerating.me/sample-report
- Pricing: https://facerating.me/pricing
- About: https://facerating.me/about
- Privacy: https://facerating.me/privacy
- Terms: https://facerating.me/terms
- Raw Skill: https://facerating.me/skills/facerating-photo-analysis-guide/SKILL.md
- MCP source: https://github.com/gpt-img-2/facerating-photo-analysis-mcp
- ClawHub listing: https://clawhub.ai/gpt-img-2/skills/facerating-photo-analysis-guide
