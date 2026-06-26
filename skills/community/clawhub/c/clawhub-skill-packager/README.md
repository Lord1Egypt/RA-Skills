# clawhub-skill-packager

A ClawHub / OpenClaw skill for reviewing, repairing, packaging, and self-auditing other ClawHub/OpenClaw skills.

## Display Name
ClawHub Skill Packager

## Goal
Take any combination of:
- a user description
- existing skill files
- partial metadata
- draft naming
- invocation ideas
- packaging notes

and turn it into exactly two user-facing outputs:
1. a publish-ready skill package zip
2. a separate plain-text review file

## Core philosophy
This skill is built for low-friction handoff.

The user should be able to hand over draft material and receive:
- a completed release-style package zip
- a separate review file
- a clear summary of what was inferred, fixed, changed, or flagged

The package is the main product.
The review file is the support layer.

## Unified identity
This package uses one identity everywhere:
- Display name: `ClawHub Skill Packager`
- Slug: `clawhub-skill-packager`
- Runtime name: `clawhub-skill-packager`
- Folder name: `clawhub-skill-packager`
- Skill key: `clawhub-skill-packager`

## Invocation
This skill is designed for explicit invocation.

Recommended invocation:
- `/skill clawhub-skill-packager`

Direct skill alias:
- `/clawhub-skill-packager`

Compatibility note:
- some OpenClaw surfaces may not dispatch dedicated per-skill slash aliases consistently
- if the direct alias does not trigger, use `/skill clawhub-skill-packager`
- this is usually a surface/runtime invocation difference, not a packaging defect in the skill itself

## What it does

This skill:
- audits what is already present
- identifies what is missing
- fills gaps using safe defaults when needed
- repairs naming and frontmatter issues
- aligns display name, slug, runtime name, folder name, and skill key
- builds the final folder
- performs a second-pass self-review
- produces one pure publish bundle zip
- produces one separate plain-text review file

## Release-style boundary

The publish zip should contain only files that directly belong to the skill as a release artifact.

The review file should remain outside the publish zip and should contain:
- inputs received
- missing information
- assumptions
- changes made
- review flags
- publish-readiness
- handoff details

## Included support files in this skill package

These are part of the packager skill itself:
- `REVIEW-CHECKLIST.txt`
- `REVIEW-RECORD-TEMPLATE.txt`

## Publish fields
- Slug: `clawhub-skill-packager`
- Runtime name: `clawhub-skill-packager`
- Skill key: `clawhub-skill-packager`
- Version: `1.5.2`
- Tags: `latest, clawhub, openclaw, packaging, review, audit, skills`

## Notes for maintainers
- Keep runtime identity unified unless there is a strong reason not to.
- Prefer one finished package plus one separate review file over extra artifact classes.
- Preserve the low-friction, inference-first stance.
- For user-facing docs, prefer documenting `/skill clawhub-skill-packager` as the most reliable invocation path across surfaces.
