# Changelog

## 1.5.2
- Clarified invocation guidance across OpenClaw surfaces
- Documented `/skill clawhub-skill-packager` as the most reliable invocation path
- Documented `/clawhub-skill-packager` as a direct alias that may depend on surface support
- Clarified that direct alias failures are usually surface/runtime dispatch differences, not a packaging defect
- No intended functional behavior change; documentation and release metadata only

## 1.5.0
- Unified runtime, package, and registry identity to `clawhub-skill-packager`
- Removed the deliberate split between short runtime name and fuller skill key
- Promoted the package-first product promise so the publish-ready bundle is clearly the main output
- Preserved the exact two-deliverable contract:
  - one pure publish bundle zip
  - one separate plain-text review file
- Tightened naming rules so display name, slug, runtime name, folder name, and skill key align by default
- Clarified that split identities are opt-in exceptions, not the default design
- Kept `disable-model-invocation: true` for explicit invocation behavior
- Preserved low-friction, inference-first packaging and self-audit behavior

## 1.4.0
- Tightened the output contract to exactly two user-facing artifacts:
  - one pure publish bundle zip
  - one separate plain-text review file
- Removed support-file concepts that implied extra user-facing artifact classes
- Clarified that review, inference, and build commentary must stay out of the publish bundle
- Clarified that the packager defaults to the full release-bundle standard, not the minimal valid skill standard
- Added a deliverable-separation review category to the checklist
- Added a visibility rule requiring both final artifacts to be surfaced directly to the user
- Preserved the intentional short runtime name vs fuller skill key identity split
- Preserved slash-only explicit invocation via `disable-model-invocation: true`

## 1.3.0
- Added explicit mapping between support files and their output roles
- Added named operating modes for package-from-scratch, repair-existing-skill, audit-only, republish/update, and rename/rebrand
- Connected the two-pass workflow to each named mode
- Added skill type awareness for instruction-only, code, API, env-var, binary, and mixed packages
- Added runtime and security declaration review guidance
- Added `PUBLISH-HANDOFF.txt` as a standard artifact
- Defined severity markers explicitly
- Documented the intentional split between short runtime name and fuller skill key identity
- Preserved low-friction, inference-first packaging stance
- Preserved slash-only explicit invocation via `disable-model-invocation: true`

## 1.1.0
- Polished the skill around low-friction, inference-first packaging behavior
- Added explicit no-question-loop operating stance
- Added stronger delivery contract for package + review summary
- Clarified second-pass workflow after user revisions
- Strengthened emphasis on clear assumptions, fixes, and review flags
- Preserved two-pass audit and packaging design

## 1.0.0
- Initial release
- Added two-pass audit and package generation workflow
- Added plain-text review record requirement
- Added frontmatter normalization guidance
- Added naming alignment rules for display name, slug, skill key, and folder
- Added ClawHub/OpenClaw package review checklist
- Added highlighted review markers for inferred or risky fields
