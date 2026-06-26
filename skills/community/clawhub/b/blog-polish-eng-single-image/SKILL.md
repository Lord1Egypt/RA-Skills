---
name: blog-polish-eng-single-image
description: Polish a technical blog draft into a 1000–1200 word, 4–5 section en-US article, preserve technical terms/code, and generate one consistent hero image prompt.
author: Jeff Yang
version: 1.0.5
tags: [openclaw, clawhub, blog, polish, translate, markdown, images, prompts]
triggers: ["polish blog", "technical blog images", "blog draft images"]
metadata:
  openclaw:
    requires: []
    platforms: ["linux", "darwin"]
    env: []
inputSchema:
  type: object
  properties:
    draftPath:
      type: string
      description: Path to the draft markdown. Defaults to ~/.openclaw/workspace/contentDraft/latestDraft.md
    outputDir:
      type: string
      description: Directory to save outputs. Defaults to ~/.openclaw/workspace/contentPolished/
    subject:
      type: string
      description: Short subject slug used in output filename (e.g. openclaw-skills). If omitted, infer from the draft title.
    style:
      type: string
      description: Visual style phrase reused for the hero image (e.g. "clean flat vector illustration, minimal isometric").
    background:
      type: string
      description: Background phrase reused for the hero image (e.g. "white background with subtle grid").
    aspectRatioHero:
      type: string
      description: Aspect ratio for hero image (e.g. "16:9 horizontal").
  required: []
outputSchema:
  type: object
  properties:
    polishedPath:
      type: string
      description: Path to the final polished markdown file.
    imagePath:
      type: string
      description: Path of the generated hero image, or intended filename if only a prompt was produced.
    imagePrompt:
      type: string
      description: Single-line prompt for the hero image.
---

# Blog Polish Skill

This skill rewrites a technical blog draft into a polished English article and generates exactly one hero image as a PNG, using one matching hero prompt. It is intended for drafts that already contain technical content, code, commands, or product details that should be preserved while improving clarity, structure, and reading flow.

## Purpose

Use this skill when you want to turn a rough technical draft into a publishable article without losing domain-specific detail. The output should read naturally in en-US English, stay faithful to the original meaning, and keep technical terms, identifiers, code blocks, file paths, and command examples intact unless a correction is clearly needed.

This skill generates one hero image only. It does not create per-section images. The single hero image should summarize the whole article visually at a high level and should be consistent with the article’s subject and tone.

## When to use

Use this skill when the source draft is one of the following:

- A technical blog post that needs editing for clarity and flow.
- A translated draft that should be rewritten into natural en-US English.
- A markdown article that needs a better structure and cleaner sectioning.
- A post that should include one matching hero image prompt for later image generation.

Do not use this skill for short notes, changelogs, marketing copy, or posts that do not need technical preservation.

## Editing behavior

The rewrite should preserve the author’s intent while improving readability. Prefer shorter paragraphs, clearer transitions, and section headings that guide the reader through the main idea.

Rewrite the article in spoken, unofficial English that feels natural, clear, and conversational, while still preserving technical accuracy.

The skill should:

- Keep technical terms, product names, API names, file names, and command syntax accurate.
- Preserve code blocks, inline code, quoted commands, and URLs unless they are obviously wrong.
- Improve grammar, sentence flow, and article structure.
- Expand thin or fragmented notes into a coherent article when the source material supports it.
- Avoid inventing facts, results, benchmarks, or claims that are not present in the draft.

The skill should not:

- Rewrite code into prose.
- Remove essential technical details.
- Add unnecessary marketing language.
- Split the article into section images or multiple image prompts.

## Input fields

`draftPath` points to the source markdown draft. If omitted, the skill reads the default latest draft file from the workspace. This should contain the original article text, headings, and any code samples that need preservation.

`outputDir` sets where the polished markdown file and image filename should be saved. If omitted, the skill uses the default polished-content directory.

`subject` is used to build the output filename. If not provided, the skill should infer a short slug from the article title.

`style` defines the visual language for the hero image. Use one style phrase consistently so the image matches the article’s mood.

`background` defines the backdrop for the hero image. Keep it simple and reusable across posts for consistency.

`aspectRatioHero` controls the hero image shape. Typical values are `16:9 horizontal` or similar wide formats suitable for blog headers.

## Output

The skill produces one polished markdown file and one hero image prompt.

The polished file should contain:

- A cleaned-up title.
- A strong introduction.
- 3 to 5 content sections, depending on the source material.
- A concise closing section if appropriate.
- Preserved technical content where relevant.

The image output should contain:

- The image file must be written in the same directory as the markdown file and must use the same basename with a .png extension.
- One hero image filename or intended image path.
- One single-line hero prompt.
- A high-level visual summary of the article, not a section-by-section breakdown.

## Image policy

This skill intentionally generates one image only.

The image should be:

- A hero image for the whole article.
- Visually aligned with the topic and style.
- Broad enough to represent the subject without depending on individual section contents.
- Consistent with the same visual style and background settings used across posts.

The image should not be:

- A separate illustration for each section.
- A collage of unrelated concepts.
- Overly literal if the topic is abstract.
- Packed with too many technical labels or small details.

## Workflow

1. Resolve the draft and output paths.
2. Read the markdown draft.
3. Extract the title and basic structure.
4. Rewrite the article into polished en-US prose.
5. Save the polished markdown file.
6. Create one hero image prompt only.
7. Return the final file path, hero image path, and image prompt.

## Constraints

Maintain the meaning of the original draft. If the source contains code snippets, commands, paths, or configuration examples, keep them intact and formatted correctly. If the draft is sparse, improve clarity and organization, but do not fabricate missing technical content.

Keep the article focused and practical. Prefer specific explanations over generic filler. If the article has a narrow technical subject, the hero image should stay broad and conceptual rather than trying to depict every detail.

## Example usage

A draft about a Linux file synchronization workflow might be polished into a clear article with headings such as introduction, setup, common pitfalls, and conclusion. The hero image prompt could describe a clean technical illustration showing a laptop, file paths, and subtle sync arrows, but only as one overall image for the post.

## Implementation notes

The workflow should emit a single structured output object with these fields:

- `polishedPath`
- `imagePath`
- `imagePrompt`

The image must be written as a PNG file. It must use the same basename as the markdown file and be saved in the same directory as the markdown file. The skill should not emit arrays of images or prompts. It should not reference per-section image generation in the description, schema, or workflow.

Generate the image using OpenClaw’s default image model (`agents.defaults.imageModel`) unless an explicit image generation model is provided by the environment.
