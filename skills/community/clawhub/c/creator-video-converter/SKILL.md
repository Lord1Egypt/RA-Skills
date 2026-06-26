---
name: video-converter
description: Convert videos into more compatible formats, containers, and codec profiles for publishing, sharing, ecommerce workflows, and platform uploads. Use when the source format is inconvenient, unsupported, too heavy, or hard to reuse.
---

# Video Converter

Convert videos into formats people and platforms can actually use.

## Problem it solves
A file may technically be a video and still be wrong for the task: unsupported codec, annoying container, oversized export, hard-to-preview format, or poor platform compatibility. This skill converts video into a more practical delivery format without overcomplicating the workflow.

## Use when
- A platform rejects the current file format
- A teammate cannot preview or open the source file easily
- A video needs to be converted to a more common format for reuse
- A file should move from editing format to delivery format

## Do not use when
- The user needs heavy editing instead of format conversion
- The user expects restoration or quality enhancement from conversion alone
- The source is already in the ideal delivery format

## Inputs
- Source video file
- Current format if known
- Target platform or target format
- Quality tolerance and compatibility priority
- Optional size, codec, or audio constraints

## Workflow
1. Identify why conversion is needed: compatibility, size, sharing, upload, or archive.
2. Choose a common target format and codec profile.
3. Preserve useful quality without keeping unnecessary weight.
4. Keep the output easy to preview, share, and upload.
5. Explain the format tradeoff in plain language.

## Output
Return:
1. Recommended target format
2. Codec/container decision
3. Compatibility rationale
4. Any quality or size tradeoffs
5. Suggested alternate format if needed

## Quality bar
- Prefer widely supported delivery formats
- Keep outputs practical for non-technical teams
- Avoid unnecessary quality loss during simple format conversion
- Make compatibility the default unless the user asks otherwise

## Resource
See `references/output-template.md`.
