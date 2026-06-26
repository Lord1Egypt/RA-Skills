---
name: content-repurpose-studio
description: Transform one source asset into a coordinated pack for multiple channels
  such as WeChat, Xiaohongshu, TikTok, email, and slides.
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
      - python3
    emoji: 🧰
---

# Content Repurpose Studio

## Purpose

Transform one source asset into a coordinated pack for multiple channels such as WeChat, Xiaohongshu, TikTok, email, and slides.

## Trigger phrases

- 一稿多发
- repurpose this content
- 内容分发改写
- multi-channel content pack
- 同一内容改成多平台

## Ask for these inputs

- source article/video/transcript
- target channels
- brand voice
- CTA
- length constraints

## Workflow

1. Identify the core message, proof, and CTA from the source.
2. Map channel-specific constraints using the bundled channel specs.
3. Produce platform-native variants instead of shallow copies.
4. Keep a shared facts block so claims remain consistent across channels.
5. Return a launch checklist with filenames and publishing order.

## Output contract

- channel pack
- shared facts block
- launch checklist
- reuse matrix

## Files in this skill

- Script: `{baseDir}/scripts/channel_packager.py`
- Resource: `{baseDir}/resources/channel_specs.yaml`

## Operating rules

- Be concrete and action-oriented.
- Prefer preview / draft / simulation mode before destructive changes.
- If information is missing, ask only for the minimum needed to proceed.
- Never fabricate metrics, legal certainty, receipts, credentials, or evidence.
- Keep assumptions explicit.

## Suggested prompts

- 一稿多发
- repurpose this content
- 内容分发改写

## Use of script and resources

Use the bundled script when it helps the user produce a structured file, manifest, CSV, or first-pass draft.
Use the resource file as the default schema, checklist, or preset when the user does not provide one.

## Boundaries

- This skill supports planning, structuring, and first-pass artifacts.
- It should not claim that files were modified, messages were sent, or legal/financial decisions were finalized unless the user actually performed those actions.


## Compatibility notes

- Directory-based AgentSkills/OpenClaw skill.
- Runtime dependency declared through `metadata.openclaw.requires`.
- Helper script is local and auditable: `scripts/channel_packager.py`.
- Bundled resource is local and referenced by the instructions: `resources/channel_specs.yaml`.
