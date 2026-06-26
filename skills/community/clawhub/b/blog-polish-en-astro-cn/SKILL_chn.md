---
name: blog-polish-zhcn
description: Polish and translate a technical blog draft into a 1000–1200 word, 4-5 section Markdown article in Simplified Chinese (zh-CN), preserving technical terms and code blocks.
author: Jeff Yang
version: 1.0.9
tags: [openclaw, clawhub, blog, polish, translate, zh-cn, markdown]
metadata:
  openclaw:
    requires: ["jq"]
    platforms: ["linux", "darwin"]
  entrypoint: skill
inputSchema:
  type: object
  properties:
    draftPath:
      type: string
      description: Path to the draft markdown file.
      default: "~/.openclaw/workspace/contentDraft/latestDraft.md"
    outputDir:
      type: string
      description: Directory where polished file is saved.
      default: "~/.openclaw/workspace/contentPolished/"
  required: ["draftPath", "outputDir"]
outputSchema:
  type: object
  properties:
    outputPath:
      type: string
      description: Path to the final polished markdown file.
  required: ["outputPath"]


workflow:
  - name: init
    description: Set defaults and create timestamp
    run: |
      draftPath=${draftPath:-~/.openclaw/workspace/contentDraft/latestDraft.md}
      outputDir=${outputDir:-~/.openclaw/workspace/contentPolished/}
      ts=$(date +"%y%m%d%H%M")
      save_state ts "$ts"
      save_state draftPath "$draftPath"
      save_state outputDir "$outputDir"

  - name: verify_input
    description: Check if draftPath exists
    run: |
      if [ ! -f "$draftPath" ]; then
        echo "Error: Draft not found at $draftPath" >&2
        exit 1
      fi

  - name: prepare_output
    description: Define output filename variable
    run: |
      ts=$(load_state ts)
      outputDir=$(load_state outputDir)
      outputPath="${outputDir}/${ts}-polished.md"
      save_state outputPath "$outputPath"

  - name: read_draft
    inputs: ["draftPath"]
    outputs: ["draftText"]

  - name: polish_and_translate
    description: "LLM: Polish grammar → Translate zh-CN → Save to ${outputDir}/${ts}-polished.md"
    inputs: ["draftText", "ts", "outputDir"]
    outputs: ["outputPath"]
    llm: true  # or specific model
    set_output: outputPath

  - name: finalize
    description: Emit polished path only
    run: |
      outputPath=$(load_state outputPath)
      jq -n --arg outputPath "$outputPath" '{ outputPath: $outputPath }'
---

# Blog Polish (zh-CN)

This skill polishes a technical blog draft and translates it to Simplified Chinese while preserving technical accuracy.

## When to Use

Use when the user asks to polish/translate a technical blog draft to zh-CN **without images**. Triggers: "polish my draft", "translate blog to Chinese", "enhance latestDraft.md".

## Defaults

- `draftPath`: `~/.openclaw/workspace/contentDraft/latestDraft.md`
- `outputDir`: `~/.openclaw/workspace/contentPolished/`
- Output filename: `${ts}-polished.md` or `${ts}-${subject}.md`

## Workflow Summary

1. **Resolve paths** + create timestamp (`date +"%y%m%d%H%M"`)
2. **Read draft** from `draftPath`
3. **Polish English**: Fix grammar/spelling, improve clarity, structure into 4-5 sections, target 1000-1200 words
4. **Translate to zh-CN**: Preserve code blocks, inline code, technical terms (`openclaw`, `skill`, `cli`)
5. **Save polished markdown** to `${outputDir}/${ts}-polished.md`
6. **Return**: `{ outputPath: "/full/path/to/file.md" }`

## Output

## Example

**Input**: `~/.openclaw/workspace/contentDraft/latestDraft.md`  
{ "outputPath": "~/.openclaw/workspace/contentPolished/2603142134-openclaw-skills.md" }

