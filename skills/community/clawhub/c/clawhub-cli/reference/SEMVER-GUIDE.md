# SemVer Guide (for Skill Publishing)

ClawHub skills should use **Semantic Versioning**: `MAJOR.MINOR.PATCH`

## What to Bump

- **PATCH** (`1.2.3` → `1.2.4`)
  - typo fixes
  - documentation-only updates
  - small behavior tweaks that do not change expected inputs/outputs

- **MINOR** (`1.2.3` → `1.3.0`)
  - new optional features
  - new commands/workflows added that do not break existing usage

- **MAJOR** (`1.2.3` → `2.0.0`)
  - breaking changes to how the skill is invoked
  - removing/renaming required inputs
  - changing default behavior in a way that can surprise existing users

## Pre-1.0.0 Convention

For early-stage skills (`0.y.z`):

- bump **PATCH** for most changes
- bump **MINOR** when you add notable features or reshape the playbook
- consider `1.0.0` when the skill is stable and widely usable

