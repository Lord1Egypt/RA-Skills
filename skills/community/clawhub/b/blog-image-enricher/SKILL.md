---
name: markdown-image-enricher
description: >
  Read a plain Markdown file (e.g. 260321_openclawConfig.md), generate header
  and section images using the default OpenClaw image model and API key from
  ~/openclaw/.env, create a new *_img.md copy with embedded PNGs, and move all
  generated images into an img/ folder next to the original file.
license: MIT-0
metadata:
  openclaw:
    skillKey: markdown-image-enricher
    # This skill expects the core image generation tool to be available.
    # The agent must NOT ask the user for API keys; it must read and reuse
    # the default image model and apiKey from the existing OpenClaw config
    # in ~/openclaw/.env or equivalent runtime config.
    required-tools:
      - image_generate
    # Recommended: expose as a slash command in chat UIs
    commands:
      - name: enrich-markdown-images
        description: >
          Generate main title and section images for a Markdown file, create
          a new *_img.md with embedded images, and move all images into img/.
        arg-mode: raw
---

# Markdown Image Enricher Skill

You are a specialized **OpenClaw** skill that enriches an existing Markdown file
by generating and wiring in header and section images, without altering the
original source file. [web:2][web:6]

Your job is to:
- Read a specified plain Markdown file.
- Infer the main title and section headings.
- Generate PNG images for the main title and for each section using OpenClaw’s
  default image model and its existing API key (no user prompts for secrets).
- Create a new Markdown file named with `_img` suffix that embeds those images
  under the corresponding headings.
- Create an `img` directory next to the original file (if it does not exist)
  and move all generated images into that folder. Keep the image link in new Markdown file correctly
- Keep the original Markdown file unchanged.

The skill must be **safe**, **deterministic**, and **transparent** to the user.
Never attempt to access unrelated files, secrets, or network resources. Only
operate on the paths and files explicitly specified in the user’s request. 

---

## When to use this skill

Trigger this skill when the user asks you to:

- Add or generate images/banners/diagrams for an existing Markdown document.
- Create a new Markdown version with embedded images while preserving the
  original file.
- Standardize blog post or documentation assets into an `img` folder next to
  the Markdown file.
- Automatically use OpenClaw’s default image generation configuration, without
  the user pasting API keys.

Examples of suitable user requests:

- “Take 260321_openclawConfig.md and generate header + section images, then
  create a new *_img.md with embedded PNGs.”
- “For this Markdown file under ~/notes/, create an enriched version with
  section images and an img folder.”
- “Auto-generate images for each heading in my Markdown and wire them into a
  new file without touching the original.”

Do **not** use this skill for:

- Arbitrary image generation that is not tied to a specific Markdown file.
- Modifying binary files or non-Markdown documents.
- Editing the user’s OpenClaw configuration or secrets.

---

## Input expectations

The skill expects the user (or calling tool) to provide:

- A path to the original Markdown file, or at least the filename relative to a
  known base directory (for example `260321_openclawConfig.md`).
- Optionally, explicit overrides for:
  - Main title (if the Markdown does not have a clear top-level `#` heading).
  - Output directory (if different from the original file’s directory).

If the path is ambiguous or the file does not exist, ask the user to clarify
or correct the path **before** proceeding. Do not guess other directories.

---

## File discovery and naming rules

Follow these rules strictly when handling files:

1. **Locate the original Markdown file**
   - Prefer an explicit path if provided (e.g. `~/docs/260321_openclawConfig.md`).
   - If only a filename is provided, interpret it relative to the user’s
     configured working directory for the session (or default content root).
   - Verify the file exists and is a plain Markdown text file before reading.

2. **Do not modify the original file**
   - Open the original file in read-only mode.
   - Never overwrite or delete it.
   - Any changes must be written into a separate file.

3. **Name the enriched Markdown**
   - If the original is `260321_openclawConfig.md`, the enriched file MUST be:
     `260321_openclawConfig_img.md`.
   - In general, insert `_img` before the final `.md` extension.
   - Save the new file in the **same directory** as the original file.

4. **Image folder**
   - After generating all images, create (if needed) an `img` directory under
     the same parent directory as both the original and the `_img` file.
   - Move or save all generated PNG images into that `img` directory.
   - Use paths relative to the enriched Markdown file (e.g. `img/header.png`)
     when embedding images.

---

## Interpreting the Markdown structure

When parsing the source Markdown file:

1. **Main title (`{mainTitle}`)**
   - If there is a first-level heading `# Some Title` near the top of the file,
     treat it as `{mainTitle}`.
   - If there is no `#` heading, use the filename (without extension) as a
     fallback main title.
   - The main title gets exactly **one** image.

2. **Sections (`{section}`)**
   - Treat any second-level or deeper headings (`##`, `###`, etc.) as sections.
   - For each heading, generate **one** image.
   - Preserve the heading text exactly; do not rename or re-number headings.

3. **Order**
   - Respect the original order of headings in the file.
   - Only insert images immediately **after** their corresponding heading
     lines.

Do not attempt to “fix” or refactor the document structure. Work with it as-is.

---

## Image generation rules

All images are generated using the **default** image model and API key that are
already configured in OpenClaw. The agent must not prompt the user for keys,
tokens, or secret values. Instead:

- Read the image model and credentials from the existing OpenClaw runtime
  configuration (for example the `.env` file under `~/openclaw/` or equivalent
  environment variables).
- Use the core `image_generate` tool (or host-provided equivalent) with those
  defaults.
- Do not override the model name unless the user explicitly requests a
  compatible alternative.

Apply these concrete constraints for every image:

1. **Format**
   - Always generate **PNG** images.

2. **Dimensions**
   - `{mainTitle}` image: width 1500, height 500 (1500x500).
   - `{section}` images: width 1200, height 675 (1200x675).

3. **Resolution / quality**
   - Use **medium** or **low** resolution mode supported by the image model.
   - Prefer **medium** when available for clearer text and diagrams.
   - If the model exposes a quality or detail setting, choose the option that
     corresponds to medium fidelity, not maximum.

4. **File size**
   - Target 2–3 MB per image.
   - Never exceed 5 MB per image.
   - If the model exposes a compression or quality parameter, adjust it to keep
     within the size limits. Prefer slight downscaling or higher compression
     rather than failing the task, but do not change the requested pixel
     dimensions.

5. **Stylistic consistency**
   - Use a minimalist, dark-tech aesthetic aligned with the following prompt
     patterns (do not embed these comments in the output Markdown; they are
     for style guidance):

     - Minimalist dark-tech banner of a glowing lobster claw integrated with
       circuit board patterns and AI neural nodes, wide blog header, deep navy
       and cyan palette.
     - Clean diagram of OpenClaw as a hub: messaging apps on left, LLM models
       on right, OpenClaw gateway in center connected by glowing lines, dark
       minimalist infographic style.
     - Skill ecosystem visualization: concentric rings of skill categories
       around a central claw logo, with developer tools, AI, search, social
       labels, dark tech palette.
     - Four-layer stack architecture diagram: Model Brain / Memory State /
       Tool Muscles / Orchestrator Hub, each layer with icon and connecting
       arrows, dark background with gradient layer colors, tech infographic.
     - Split illustration: left side shows future tech landscape with fewer
       workers and more AI agents, right side shows a developer-turned-
       orchestrator commanding AI tools, minimalist dark editorial style.

   - For each heading, blend its text into the prompt so the image concept
     reflects that section’s topic while retaining the same clean dark-tech
     visual language.

---

## Prompt construction for images

For each heading, construct an image prompt that:

- Includes the heading text (as a title or concept).
- References the preferred dark-tech, minimalist aesthetic.
- Specifies the desired aspect ratio implicitly via content (wide header vs
  16:9-like section image) and explicitly via the size parameters passed to
  the image tool.

Example prompt for a main title:

> “Minimalist dark-tech banner for ‘{mainTitle}’, glowing lobster claw integrated
> with circuit board patterns and AI neural nodes, wide blog header, deep navy
> and cyan palette, clean typography, no extra text.”

Example prompt for a section:

> “Clean dark-tech diagram illustrating section ‘{sectionHeading}’, OpenClaw
> components and data flows as glowing lines, minimalist infographic on dark
> navy background, cyan and teal highlights, no body text.”

Do not include actual Markdown comments (`<!-- ... -->`) in the prompts sent to
the image tool. Those comments were examples only.

---

## File naming for images

Use deterministic, readable filenames so users can understand which image maps
to which section. All files go under the `img/` folder.

Recommended patterns:

- Main title: `img/{baseName}_main.png`
- First-level section: `img/{baseName}_section_{index}.png`
- Deeper sections: `img/{baseName}_section_{index}.png` as well, using a
  sequential index in document order.

Where:

- `{baseName}` is the original Markdown filename without extension
  (e.g. `260321_openclawConfig`).
- `{index}` starts at 1 and increments for each section heading.

Ensure that the file paths you embed in the `_img` Markdown are **relative** to
that file, for example:

```markdown
# Title



## Section A


```

---

## Updating the enriched Markdown file

When writing the new `{original}_img.md` file:

1. Start from the original Markdown content.
2. For each detected heading:
   - Preserve the heading line exactly as in the source.
   - Immediately after the heading line, insert a standard Markdown image tag
     that references the corresponding PNG in `img/`.
3. Do not remove or alter any other content (paragraphs, lists, code blocks,
   etc.).
4. If the file already contains image references beneath a heading:
   - Append the new generated image after existing images unless the user
     explicitly requests replacement.
   - Never delete or rewrite user-authored content unless instructed.

If any step fails (e.g. image generation error, file write permissions), stop
and surface a clear, concise error message to the user, describing which step
failed and what they can do to fix it.

---

## Security and safety constraints

To remain compatible with ClawHub’s scanner and OpenClaw best practices: [web:1][web:8]

- Do not instruct the agent to read arbitrary system files, dotfiles, or
  unrelated directories.
- Limit all filesystem access to:
  - The explicitly provided Markdown file.
  - The sibling `_img` output file.
  - The `img/` directory under the same parent folder.
- Do not bundle or execute shell scripts, package managers, or external
  binaries.
- Do not exfiltrate file contents to external services.
- Only use the platform’s sanctioned image generation tool; do not call remote
  APIs directly with handwritten HTTP requests.
- Avoid storing or logging API keys, tokens, or full environment dumps.

---

## Operational checklist

When this skill triggers, follow this sequence:

1. Confirm path to the original Markdown file and verify it exists.
2. Read the file content into memory in a safe, text-only way.
3. Parse headings to identify `{mainTitle}` and `{section}` list.
4. Resolve the OpenClaw default image model and API key from the host
   configuration (no user prompts).
5. For each heading:
   - Construct a clean, dark-tech prompt incorporating the heading text.
   - Call the image generation tool with:
     - Format: PNG
     - Dimensions: 1500x500 for main title, 1200x675 for sections
     - Quality: medium (or low if medium is not available)
     - Any size/quality parameters needed to target 2–3 MB (max 5 MB).
6. Ensure the `img/` directory exists next to the original file; create it if
   needed.
7. Save or move all images into `img/` with deterministic filenames.
8. Generate the new `{original}_img.md` content by inserting Markdown image
   tags under each heading.
9. Write the enriched Markdown file next to the original without overwriting it.
10. Report back:
    - The path of the enriched Markdown file.
    - The list of generated images and their relative paths.
    - Any warnings about size or quality adjustments.

If the user requests a dry run or preview, you may:

- Parse the headings.
- Show the planned filenames and sample prompts.
- Wait for confirmation before generating images and writing files.

---

## Notes for maintainers

- Keep this SKILL.md focused on behavior, constraints, and workflows.
- If you need to document implementation details (e.g. parser limitations,
  internal helper scripts), place them in separate files under a `references/`
  directory rather than expanding this file.
- Ensure this skill’s `name` and `description` remain accurate and specific
  so that OpenClaw can route only relevant tasks here and keep context usage
  efficient. [web:1][web:2][web:6]
