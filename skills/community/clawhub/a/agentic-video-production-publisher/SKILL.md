---
name: agentic-video-production-publisher
description: Review AI video production packages for creative consistency, asset provenance, platform metadata, disclosure wording, and publishing readiness. Use when a user asks whether a video package is ready for YouTube, TikTok, or short-form release without uploading or scheduling content.
---

# Agentic Video Production Reviewer

Use this skill to review an AI video production package before a human-controlled publish step. The skill is instruction-only and should produce a readiness verdict, not operate accounts or upload media.

## Review Workflow

1. Confirm the target platform, audience, video file, title, description, thumbnail, captions, and disclosure requirements.
2. Check that character, setting, music, prompt, source-asset, and generated-asset provenance are documented.
3. Verify platform metadata for policy-sensitive claims, attribution, affiliate disclosure, copyright risk, and audience settings.
4. Confirm that private local paths, account names, unpublished prompts, and production notes are not present in client-facing copy.
5. Separate creative quality notes from release blockers.
6. Return a release verdict: `ready`, `ready_with_notes`, `blocked`, or `do_not_publish`.

## Boundaries

- Do not upload, publish, schedule, delete, monetize, or modify any video.
- Do not operate logged-in YouTube, TikTok, browser, or creator-studio sessions.
- Do not request credentials, cookies, account recovery steps, billing access, or private analytics.
- Do not expose internal production notes, local paths, private prompts, or unredacted source-asset links in client-facing output.

## Output Shape

Return:

- `Package`: files and metadata reviewed.
- `Creative`: consistency and quality findings.
- `Policy`: disclosure, copyright, platform, and audience risks.
- `Public surface`: client-facing wording issues.
- `Verification`: checks still needed before manual publish.
- `Verdict`: one of `ready`, `ready_with_notes`, `blocked`, or `do_not_publish`.
