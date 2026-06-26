---
name: bookmorph-magic
description: Orchestrate a book-to-content workflow when the user wants to turn one book into multiple content assets such as video, audio, and cover images for an episode or campaign. Use for requests like “制作 ep38 内容”, “turn this book into an episode package”, or “generate multi-format content from a book”. This is a publishable template skill: it defines the adapter contracts for selecting a source book, generating longform media, generating covers, and bundling outputs.
---

# BookMorph Magic

Use this skill as a publishable template for book-to-content orchestration. It is not a private, fixed workflow.

## What this template does

- Takes one book or one episode-style request
- Produces a package of multi-format content
- Bundles the final outputs into a stable episode directory with a manifest

Typical outputs:

- one video
- one audio file
- three cover images (`3:4`, `4:3`, `1:1`)
- one `manifest.json`

## Important constraints

- This is a template, not a turnkey SaaS workflow.
- To run end to end, you must provide 3 adapters:
  - `book selector`
  - `longform content generator`
  - `cover generator`
- If you already have existing skills or scripts for those adapters, wire them to the contracts in `references/integration-template.md`.

## Inputs

- A book file path, or
- A request containing one episode identifier such as `ep38`, `EP38`, `episode 38`, or `第38期`

## Output contract

- Output root is configurable
- Episode directory prefix is configurable; default is `episode-`
- Stable output filenames:
  - `epNN-video.<ext>`
  - `epNN-audio.<ext>`
  - `epNN-cover-3x4.<ext>`
  - `epNN-cover-4x3.<ext>`
  - `epNN-cover-1x1.<ext>`
  - `manifest.json`

## Workflow

1. Parse the episode identifier with `scripts/episode_bundle.py parse-episode`.
2. Create or reset the target episode directory with `prepare-dest`.
3. Run your `book selector` adapter until it chooses exactly one source book.
4. Run your `longform content generator` adapter to produce a video and an audio output.
5. Run your `cover generator` adapter to produce `3:4`, `4:3`, and `1:1` images.
6. Run `bundle` to copy the final artifacts into the episode directory and write `manifest.json`.

## Adapter requirements

### Book selector

Must return enough information to identify one selected source:

- book title
- author
- local source file path
- selection round or attempt count
- optional selector checkpoint path

### Longform content generator

Must return:

- video file path
- audio file path
- attempt count
- optional generator checkpoint path

### Cover generator

Must return:

- image path for `3:4`
- image path for `4:3`
- image path for `1:1`
- attempt count
- optional prompt archive path
- optional generator checkpoint path

## Failure rules

- If the episode number cannot be parsed, fail immediately.
- If no source book can be selected, stop and write a failed manifest.
- If longform media is incomplete, stop and write a failed or partial manifest.
- If any required cover image is missing, stop and write a failed or partial manifest.

## Commands

```bash
python3 {baseDir}/scripts/episode_bundle.py parse-episode --text "制作ep38内容" --output-root "/abs/output/root"
python3 {baseDir}/scripts/episode_bundle.py prepare-dest --episode 38 --clear-existing --output-root "/abs/output/root"
python3 {baseDir}/scripts/episode_bundle.py bundle --episode 38 --video "/abs/video.mp4" --audio "/abs/audio.m4a" --image-3x4 "/abs/3x4.png" --image-4x3 "/abs/4x3.png" --image-1x1 "/abs/1x1.png" --book-title "Example Book" --author "Example Author" --book-path "/abs/book.epub" --selector-adapter "my-book-selector" --selector-reference "round-1" --selection-round 1 --longform-attempts 1 --cover-attempts 1 --prompt-archive "/abs/prompts.md" --output-root "/abs/output/root"
python3 {baseDir}/scripts/episode_bundle.py bundle --episode 38 --selection-round 3 --longform-attempts 0 --cover-attempts 0 --status failed --failure "selector=no valid source book" --output-root "/abs/output/root"
```

## References

- Adapter contracts: `references/integration-template.md`
- Manifest fields: `references/manifest-schema.md`
