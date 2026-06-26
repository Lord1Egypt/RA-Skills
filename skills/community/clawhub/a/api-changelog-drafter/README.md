# API Changelog Drafter

Converts code diffs, PR descriptions, and API spec changes into a developer-facing changelog entry, deprecation notice, and migration guide.

## What It Does

Classifies each API change and produces a structured DRAFT output covering:

- Change classification per Keep a Changelog categories (Added / Changed / Deprecated / Removed / Fixed / Security)
- Breaking change identification with semantic version bump recommendation (MAJOR / MINOR / PATCH)
- Keep-a-Changelog-format entry ready to paste into CHANGELOG.md
- Deprecation notices with suggested sunset timeline and replacement guidance
- Migration guide steps for each breaking change
- Upgrade-impact summary sentence for announcement posts or release emails

## Who It's For

- Technical writers drafting release notes and changelogs
- Developer advocates producing migration guides
- Backend and platform engineers maintaining public or internal APIs
- API product managers preparing release communications

## When To Use

Use when an API version is about to ship and you need to communicate changes clearly to downstream consumers. Accepts a code diff, an OpenAPI/GraphQL schema diff, a list of changed endpoints, PR descriptions, or a plain-English summary of what changed.

## Supported API Types

REST / HTTP, GraphQL, gRPC, SDK/library, CLI tools.

## Important Limitations

All output is a **DRAFT** for technical writer and engineering review before publication. The skill classifies changes based on the input provided — if the diff is incomplete or ambiguous, classifications may be incorrect. Engineers must verify that breaking-change flags and version recommendations match their actual compatibility guarantees before release.

## Reference

- Keep a Changelog specification: https://keepachangelog.com/en/1.1.0/
- Semantic Versioning specification: https://semver.org/spec/v2.0.0.html

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
