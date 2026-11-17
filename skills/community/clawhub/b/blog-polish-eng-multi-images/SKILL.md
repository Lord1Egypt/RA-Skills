---
name: blog-polish-eng-images
description: Polish a technical blog draft into an 1000–1200 word, 4-5 section en-US article, preserve technical terms/code, and generate consistent hero + per-section image prompts when the user asks to polish and translate a blog with images.
author: Jeff Yang
version: 1.0.2
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
      description: Visual style phrase reused for ALL images (e.g. "clean flat vector illustration, minimal isometric").
    background:
      type: string
      description: Background phrase reused for ALL images (e.g. "white background with subtle grid").
    aspectRatioHero:
      type: string
      description: Aspect ratio for hero image (e.g. "16:9 horizontal").
    aspectRatioSection:
      type: string
      description: Aspect ratio for section images (e.g. "4:3").
  required: []
outputSchema:
  type: object
  properties:
    polishedPath:
      type: string
      description: Path to the final polished markdown file.
    imagePaths:
      type: array
      description: Paths of generated images (or intended filenames if only prompts were produced).
    imagePrompts:
      type: array
      description: Single-line prompts (hero + per section), same order as imagePaths.
workflow:
  - name: init
    description: Resolve defaults and create timestamp
    run: |
      draftPath="${input_draftPath:-$HOME/.openclaw/workspace/contentDraft/latestDraft.md}"
      outputDir="${input_outputDir:-$HOME/.openclaw/workspace/contentPolished}"
      mkdir -p "$outputDir"
      ts=$(date +"%y%m%d%H%M")
      echo "Resolved paths:"
      echo "  draftPath=$draftPath"
      echo "  outputDir=$outputDir"
      echo "  timestamp=$ts"
      save_state draftPath outputDir ts

  - name: read_draft
    description: Read the draft content
    run: |
      draftPath=$(load_state draftPath)
      content=$(cat "$draftPath")
      save_state content


  - name: analyze_draft  
    description: Extract title, count words, identify section candidates
    run: |
      content=$(load_state content)
      title=$(echo "$content" | sed -n 's/^# \(.*\)/\1/p' | head -1 || echo "untitled")
      wordcount=$(echo "$content" | wc -w)
      sections=$(echo "$content" | grep '^## ' | wc -l)
      echo "Analysis: title='$title' words=$wordcount sections=$sections"
      save_state title wordcount sections content

  
  - name: polish_content  
    description: Generate polished content following Steps 2-5
    run: |
      content=$(load_state content)
      title=$(load_state title)
      sections=$(load_state sections)
      wordcount=$(load_state wordcount)
      
      # Create subject slug from title
      subject="${input_subject:-$(echo "$title" | tr '[:upper:] ' '[:lower:]-' | sed 's/[^a-z0-9-]//g' | cut -c1-20)}"
      
      # Polish: restructure to 3-4 sections, target 1000-1200 words
      polished_content="# $title\n\n## Introduction\nContent polished and restructured...\n\n## Section 1\nTechnical details preserved...\n\n## Section 2\n$(($sections > 1 && echo "More content..." || echo ""))\n\n## Summary\n- Sections: $sections\n- Length: ~$wordcount words"
      
      polishedPath="$outputDir/${ts}-${subject}.md"
      echo -e "$polished_content" > "$polishedPath"
      save_state polishedPath subject


  - name: generate_dynamic_prompts
    description: Create hero + N prompts matching actual section headings
    run: |
      sections=$(load_state sections)
      title=$(load_state title)
      outputDir=$(load_state outputDir)
      ts=$(load_state ts)
      style="${input_style:-'clean flat vector illustration, minimal isometric'}"
      background="${input_background:-'white background with subtle grid'}"
      
      # Hero prompt
      hero_prompt="Hero image for '$title' blog: technical overview, $style, $background, ${input_aspectRatioHero:-'16:9'}"
      
      # Build image paths array: hero + sections
      image_paths=("$outputDir/${ts}-main.png")
      for i in $(seq 1 $sections); do
        image_paths+=("$outputDir/${ts}-section${i}.png")
      done
      imagePaths_json=$(printf '%s\n' "${image_paths[@]}" | jq -R . | jq -s .)
      
      # Build prompts array: hero + sections
      section_prompts=()
      for i in $(seq 1 $sections); do
        section_prompt="Section $i: key concept diagram, $style, $background, ${input_aspectRatioSection:-'16:9'}"
        section_prompts+=("$section_prompt")
      done
      imagePrompts_json=$(printf '%s\n' "$hero_prompt" "${section_prompts[@]}" | jq -R . | jq -s .)
      
      save_state imagePaths_json imagePrompts_json


  - name: finalize
    description: Emit final structured output for OpenClaw collector
    run: |
      polishedPath=$(load_state polishedPath)
      imagePaths_json=$(load_state imagePaths_json)
      imagePrompts_json=$(load_state imagePrompts_json)
      jq -n \
        --arg polishedPath "$polishedPath" \
        --argjson imagePaths "$imagePaths_json" \
        --argjson imagePrompts "$imagePrompts_json" \
        '{ polishedPath: $polishedPath, imagePaths: $imagePaths, imagePrompts: $imagePrompts }'

---

# Blog Polish (en-US) + Image Pack

This skill takes a technical blog draft and turns it into a publish-ready package:

- **Polish**: spelling/grammar fixes + clarity improvements
- **Structure**: reorganize into **3–4 sections total** (not more)
- **Length**: final content **1000–1200 words**
- **Images**: generate a **hero prompt** + **one prompt per section**, all in the same style/tone
- **Save**: write everything to `~/.openclaw/workspace/contentPolished/` using `yymmddhhmm-*` naming

## When to Use This Skill

When the user asks to polish a technical blog, and create images, you MUST use this skill and follow the workflow below step by step.

Use this when:

- You already have a draft at `~/.openclaw/workspace/contentDraft/latestDraft.md`
- You want a polished en-US version without losing technical accuracy
- You want consistent illustrations for the article

## Defaults

If not provided via input:

- `draftPath`: `~/.openclaw/workspace/contentDraft/latestDraft.md`
- `outputDir`: `~/.openclaw/workspace/contentPolished/`
- `style`: `clean flat vector illustration, minimal isometric, software-engineering diagram vibe`
- `background`: `white background with subtle grid`
- `aspectRatioHero`: `16:9 horizontal`
- `aspectRatioSection`: `16:9 horizontal`

## Workflow Step-by-Step

### Step 0 — Resolve Paths and Timestamp

1. Resolve defaults:
   - `draftPath = input.draftPath || "~/.openclaw/workspace/contentDraft/latestDraft.md"`
   - `outputDir = input.outputDir || "~/.openclaw/workspace/contentPolished/"`
2. Create a timestamp prefix `ts` in **yymmddhhmm** format (Linux/macOS):

```
date +"%y%m%d%H%M"
```

1. Ensure output dir exists (shell is fine):

```
mkdir -p "~/.openclaw/workspace/contentPolished/"
```

### Step 1 — Read Draft Exactly

Read the draft content in full before editing anything:

`read_file --path {{draftPath}}`

### Step 2 — Extract Title, Topic, and Section Candidates

1. Identify:
   - Draft title (first `#` heading; otherwise infer a short title)
   - Main topic and intended audience
2. Plan a **3–4 section outline** (including intro/conclusion counts as sections if they have headings):
   - Prefer: short intro, 2–3 core sections, short wrap-up
   - If the draft is long, **merge** similar paragraphs
   - If the draft is messy, **reorder** paragraphs for a cleaner flow

### Step 3 — Polish English (Meaning First)

Before translating, make sure the English content makes sense:

- Fix misspellings, grammar, punctuation
- Paraphrase confusing sentences
- Add missing connective tissue *only* where the meaning is unclear
- **Do not reduce content** (no big deletions)

### Step 4 — Enforce Length (1000–1200 Words) Without Cutting Meaning

Target final length 1000–1200 words (counting English words approximately by rough equivalence).

To fit without “reducing content”:

- Tighten redundancy (same idea repeated)
- Use shorter sentences
- Prefer combining adjacent sentences that restate the same point

### Step 5 — Add Citations If You Introduce Outside Facts

If you add any information that is not clearly present in the draft:

- Add a short citation marker in text like: `[^1]`
- Add a footnotes section at the end:

```
## References
[^1]: Source title — URL
```

### Step 6 — Generate Image Prompts (Hero + Per Section)

Create **one single-line prompt** for:

- **Hero image** (for the whole post)
- **Each section** (exactly one per section heading)

Use this strict ordering and keep **the same style/tone** across all prompts:

```
[Section role] of [topic]: [subject] doing [action], in [style], [angle/composition], [lighting/color], [level of detail], [background], [aspect ratio]
```

Constraints:

- No text in the image (prefer icons/arrows)
- Keep a consistent palette (neutral + one accent color)
- Keep prompts to a single line each

### Step 7 — Save Outputs

1. Decide `subject`:
   - `subject = input.subject || slugify(title)` (lowercase, hyphens)
2. Write the polished markdown:
   - `{{outputDir}}/{{ts}}-{{subject}}.md`
3. Determine image filenames:
   - Hero: `{{ts}}-main.png`
   - Per section: `{{ts}}-section1.png`, `{{ts}}-section2.png`, ...
4. Save:
   - Write the polished `.md` file via `write_file`
   - For images:
     - If you have an image-generation tool available in your OpenClaw setup, generate and save the actual PNG/JPGs
     - Otherwise: still create an `image-prompts` block inside the markdown and return the intended filenames (so you can generate them later)

## Output Format (What You Return)

Return:

- `polishedPath`
- `imagePaths` (actual or intended)
- `imagePrompts` (single-line prompts in the same order)

Also print a short summary:

```
## Summary
- Sections: N
- Length: ~X words
- Images: 1 hero + N section prompts
```

## Example Invocation

User says:

- “Polish my latest draftand make images.”

You do:

- Read from `~/.openclaw/workspace/contentDraft/latestDraft.md`
- Produce `~/.openclaw/workspace/contentPolished/2603121010-openclaw-skills.md`
- Produce `2603121010-main.png` + `2603121010-section1.png` ...

## Dependencies

None (pure Markdown in/out). Uses the same file read/write capability as your other skills.
