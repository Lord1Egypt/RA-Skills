---
name: book-launch-campaign-kit
description: Create a reusable launch system for an English book or digital guide, including positioning, posters, promo videos, Amazon/Kindle conversion copy, people-holding-book ad concepts, polished campaign videos, and ready-to-publish launch packs. Use when the user wants to launch, market, package, or promote a book with English-facing assets; when they need Amazon-ready metadata; or when they want to turn one cover + one core hook into a full creative campaign.
---

# Book Launch Campaign Kit

Build a launch system, not isolated assets.

## Core Workflow

1. Lock the core positioning line before designing anything.
2. Build a 3-size poster set first.
3. Build short English promo videos next.
4. Upgrade voice quality early if TTS sounds weak.
5. Create a launch pack with platform copy and Amazon metadata.
6. Build stronger visual ad directions with people-holding-book concepts when static cover ads are not enough.
7. Split the video lane into:
   - brand / premium campaign version
   - sales / conversion version
8. Finish with an Amazon-ready publishing pack.

## Required Deliverables

Produce at least these outputs:
- vertical poster
- square poster
- horizontal poster
- one short promo video
- one stronger conversion-oriented video
- one launch pack folder
- one Amazon ready-to-publish metadata pack

## Scripts

Use `scripts/scaffold_launch_pack.py` to create a clean launch project structure:

```bash
python scripts/scaffold_launch_pack.py <target-project-dir>
```

## References

Read `references/openclaw-book-launch-tutorial.md` when you need the full end-to-end playbook in English, including:
- creative sequence
- poster logic
- video workflow
- people-holding-book ad directions
- brand vs conversion split
- Amazon packaging logic

Read `references/openclaw-book-launch-tutorial-zh.md` when you want the same workflow in Chinese.

Read `references/case-study-openclaw-book.md` when you want a concrete example of the workflow applied to a real project.

## People-Holding-Book Concept Rule

Use celebrity-level energy, not exact real celebrity endorsement, unless the user explicitly confirms legal/authorized usage.

## Amazon Positioning Rule

Default positioning:
**This is not another AI theory book. It is a practical guide to execution.**

## Output Standard

Deliver work in a folderized system so the user can keep iterating:
- launch-assets/
- openclaw-launch-pack/
- source cover files
- ready-to-publish metadata docs

Keep naming consistent and make the launch package easy to reuse in future book launches.
