# Intake Prompt

Use this prompt at the start of a request.

## Goal

Decide whether the user wants to create, update, correct, or list character skills.
If the request is for a new character skill and the intake bundle is incomplete, stop and ask the missing intake questions before generating anything.
If intake is incomplete, do not create or modify any character files.

## Collect

- canonical slot state:
  - `source_policy`
  - `input_mode`
  - `character_name`
  - `source_work`
  - `material_types`
  - `allow_low_confidence_persona`
  - `archive_mirror`
- source decision policy
- input mode: direct text or file path
- character name
- source work
- request type: create, update, correct, list
- source types provided: official, plot, quotes, wiki, user
- whether low-confidence persona inference is allowed
- expected output quality: fact fix, persona fix, style fix, or full build

## Minimum Intake Questions

Ask these questions in order whenever a new character request is underspecified.
Ask one question at a time, wait for the answer, and only then ask the next unresolved question.
Do not send the entire checklist in one message.
If a slot is already clearly resolved, do not ask it again unless the user answer is ambiguous, conflicting, or intentionally revised.

First ask only the source completion policy with these choices:

- only user information
- official plus wiki
- official plus user information
- quick generate from official-style defaults

Branching rules:

- if the user chooses quick generate, skip all remaining intake questions and move straight to a generated draft preview
- if the user chooses only user information or official plus user information, ask how the user will provide materials: direct text or file paths
- if the user chooses official plus wiki, do not ask input mode
- if the user chooses direct text, ask them to paste the source text or notes
- if the user chooses file paths, ask them to provide the file paths and read those first
- do not ask for the character name again if it was already present in the original request; instead ask for a direct confirmation like `Use <name> as the character name?`
- source work may be blank; blank means the character can be fully original and no public lookup should be assumed
- if public-material completion is allowed and source work exists, ask for public search scope: small, medium, or large
- ask whether low-confidence persona supplementation is allowed using the wording `If the materials are not enough, may I add a little personality supplementation for you`

Do not ask for target use during the hard intake gate unless the user explicitly wants to customize it.
When target use is not provided, default it to `openclaw roleplay conversation`.
Do not include a `minimal confirmation template` shortcut block.
Generate the draft in memory first, then repeat key personality and important factors back to the user for confirmation before any files are written.
The very first intake reply should contain only the source completion policy question and its options.
After the draft is confirmed, install the Codex package first and then ask whether the user also wants an OpenClaw export.

If the user only provides a name, or has not answered the unresolved required slots for the chosen branch, the intake is not complete yet.

## Routing Rule

- if the user wants a new character package and intake is incomplete, keep asking intake questions and do not write files
- if the user wants a new character package and intake is complete, go to `source_audit.md`
- if the user wants a correction, go to `correction_handler.md`
- if the user wants to merge new material, go to `evolution_merge.md`
- if the user wants to inspect existing characters, use `tools/skill_writer.py --action list`

## Output

Produce a short intake summary with:

- character
- source work
- request type
- source bundle summary
- low-confidence persona policy
- next prompt to use
