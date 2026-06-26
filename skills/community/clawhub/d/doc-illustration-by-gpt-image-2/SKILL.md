---
name: doc-illustration-by-gpt-image-2
description: Generate technical-document illustrations, design-note infographics, and repo architecture visuals using OpenAI GPT Image 2. Use when agent needs to turn AI notes, engineering docs, Markdown design specs, or codebase explanations into polished insertable images. Supports text-only generation, reference-image-plus-text style-guided generation, and prompt-only dry-run review.
---

# Doc Illustration

Use this skill to create polished illustrations for technical writing.

## Quick workflow

1. Identify the illustration type:
   - architecture diagram
   - process diagram
   - knowledge card
   - repo or module relationship diagram
   - technical infographic
2. Pick a style profile:
   - default: `flat-tech-infographic`
   - optional: `flat-illustration`, `sketchnote`, `soft-tech-diagram`, `repo-architecture-clean`
3. If the user supplied reference images, treat them as style guidance only.
4. Prefer document-friendly landscape output unless the user requests another ratio.
5. Prefer concise bilingual labels and short notes over paragraph-heavy copy.
6. If the user wants to inspect the prompt first, use `--dry-run`.
7. For live generation, run the bundled script.

## Script

Use:

```bash
uv run scripts/generate_doc_illustration.py \
  --title "RAG Pipeline Overview" \
  --brief "Create a technical infographic showing ingestion, chunking, embedding, retrieval, reranking, and answer synthesis." \
  --style-profile flat-tech-infographic
```

Use `--mode reference+text --reference-image <path>` when the new image should follow the style of one or more reference images.

Use `--dry-run` when the user wants the exact prompt and parameters without calling the API.

Default output settings:
- `--size auto` for best compatibility with GPT image providers
- `--quality auto` for high-fidelity default behavior without over-constraining the request
- use `--size doc-hd` for an explicit landscape document illustration size (`1536x1024`)
- use `--size doc-2k` for a 2K landscape document illustration size (`2048x1152`)
- use `--size doc-4k` for a 4K landscape document illustration size (`3840x2160`)

## Authentication

- Read `OPENAI_API_KEY` from the current shell first.
- Read `OPENAI_BASE_URL` from the current shell second.
- If `OPENAI_API_KEY` is missing for a live generation run, prompt temporarily in an interactive shell or tell the user to export the environment variable.
- Do not write credentials to disk.

## Model selection

- Use `gpt-image-2` for official OpenAI and for `https://aihubmix.com/v1`.
- Use `openai/gpt-image-2` for `https://api.ofox.ai/v1`.
- Default back to `gpt-image-2` unless a provider requires a namespaced model name.

## References

- Read `references/style-profiles.md` when selecting or explaining styles.
- Read `references/prompt-patterns.md` when the requested illustration type needs prompt refinement.
- Read `references/openai-image-workflow.md` when debugging auth, request modes, or output behavior.
- Read `references/openai-official-links.md` when you need the official OpenAI docs for GPT Image, Images API, or Python examples.
