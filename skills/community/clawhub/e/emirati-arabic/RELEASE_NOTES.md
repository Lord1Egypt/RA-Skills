# 0.2.1-rc.1 — experimental community review candidate

## Purpose

Emirati conversation, contextual understanding, writing, and revision, with an explicit opt-in Abu Dhabi specialization. General Emirati remains the default. The lexicon supports the task; it does not turn ordinary conversation into vocabulary explanations.

The maintainer has authorized experimental publication on GitHub and ClawHub. This is not a final stable release or a main-branch merge. This ClawHub distribution differs from reviewed GitHub commit `5aa437cd1366b4c4e0407a7d6121cdbec071a9d4` only in license metadata/text and publication-status documentation; its behavior, examples, code and tests are unchanged. The version is distinct from `0.2.0` already on `main`.

## Changes from main

- Incorporate the previously reviewed conversation-first instruction contract and its examples/tests: direct task completion, preserved facts, restrained self-directed humor, grounded practical drafts, conversation-scoped language changes, and local user corrections.
- Clarify actors, actions, and referents in spoken scripts when pronouns or ambiguous kinship/body-part spellings obscure what happened. Do not replace one event with a different mishap; do not prohibit a regional word globally.
- Preserve all prior source rules, historical/source boundaries, owner-authorized example spellings, lexicon entries, and offline conversion fixtures.
- Add an allowlisted source ZIP builder with SHA-256 manifest, defensive distribution tests, and separate handling of private evidence.
- Update review-branch installation and Abu Dhabi usage instructions.

## Limits and evidence

Offline Python tests check the instruction contract, package integrity, references, metadata, privacy patterns, and scoped conversion constraints. They are not a fluency benchmark. The prior real-response comparison belongs to an earlier reviewed source revision; its scores must not be advertised as newly measured performance of this candidate.

No independent native-speaker certification is claimed. Naturalness, regional coverage, and contextual interpretation remain open to human review. Minor wording issues can remain even when all offline checks pass. Rule changes alone do not prove every future model response is fixed.

Raw conversation outputs, live-test logs, session identifiers, local paths, private calibration, credentials, internal archives, copyrighted PDFs, and page images are not release assets. Owner-contributed examples explicitly authorized for publication remain in their attributed references.

## Files

The builder creates `emirati-arabic-0.2.1-rc.1.zip` and `SHA256SUMS` outside the repository. The ZIP contains only the files in `distribution-files.json` plus a generated `MANIFEST.json`, under `emirati-arabic/`. See [distribution policy](DISTRIBUTION.md). No tag or release asset is assumed to exist merely because these filenames are documented.

## License

Original project material in this ClawHub distribution is MIT-0, authorized by and credited to Binablan. The separate GitHub distribution remains MIT. Third-party references retain their own rights; their books and media are not bundled and are not relicensed. See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
