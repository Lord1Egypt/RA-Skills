---
name: expertpack-export
description: Export an OpenClaw instance's accumulated knowledge into a structured ExpertPack composite. Use when backing up an agent's identity, exporting for migration, or creating a portable knowledge snapshot. Handles auto-discovery (scanning workspace state to identify constituent packs), distillation (compressing raw state into structured EP files), and packaging (writing EP-compliant packs + composite manifest). Output is Obsidian-compatible — includes YAML frontmatter on all content files and can be opened as an Obsidian vault. NOT for importing/hydrating from an existing EP.
metadata:
  openclaw:
    homepage: https://expertpack.ai
    requires:
      bins:
        - python3
---

# ExpertPack Export

Part of the [ExpertPack](https://expertpack.ai) framework — a structured, portable knowledge format for AI agents.

Export an OpenClaw instance into a composite ExpertPack — an agent pack (subtype: agent) as the voice, plus person/product/process packs as knowledge constituents.

**Learn more:** [expertpack.ai](https://expertpack.ai) · [GitHub](https://github.com/brianhearn/ExpertPack) · [Schema docs](https://expertpack.ai/#schemas)

## Prerequisites

- Read `references/schemas-summary.md` for the EP schema rules this export must follow.
- The export writes to a target directory (default: `{workspace}/export/`). It does NOT modify the agent's live workspace files.

## Export Flow

### 1. Scan

Run `scripts/scan.py` to inventory the workspace. It outputs a JSON manifest of discovered files, their categories, and proposed pack assignments.

```bash
python3 {skill_dir}/scripts/scan.py --workspace /root/.openclaw/workspace --output /tmp/ep-scan.json
```

Review the scan output. It proposes:
- Which files map to which pack type (agent, person, product, process)
- Which knowledge domains were detected
- Confidence scores for ambiguous classifications

### 2. Propose

Present the proposed composite to the user:
- List each proposed pack with type, slug, and key content sources
- Flag ambiguous classifications for user decision
- Note any gaps (e.g., "No process packs detected — skip or create stubs?")

Wait for user confirmation before proceeding.

### 3. Distill

Run `scripts/distill.py` for each proposed pack. It reads source files, extracts knowledge, deduplicates, and writes EP-compliant output.

```bash
python3 {skill_dir}/scripts/distill.py \
  --scan /tmp/ep-scan.json \
  --pack agent:easybot \
  --output /root/.openclaw/workspace/export/packs/easybot/
```

Repeat for each pack. The script:
- Reads source files listed in the scan manifest
- Extracts and classifies knowledge assertions
- Deduplicates (prefers newest for conflicts)
- Writes structured .md files with proper headers and frontmatter
- Writes manifest.yaml per pack
- Strips secrets (API keys, tokens, passwords) automatically

### 4. Compose

Run `scripts/compose.py` to generate the composite manifest and overview.

```bash
python3 {skill_dir}/scripts/compose.py \
  --scan /tmp/ep-scan.json \
  --export-dir /root/.openclaw/workspace/export/
```

### 5. Validate

Run `scripts/validate.py` to check the export against schema rules.

```bash
python3 {skill_dir}/scripts/validate.py --export-dir /root/.openclaw/workspace/export/
```

It checks:
- All required files exist per schema
- manifest.yaml fields are valid
- No secrets leaked (scans for API key patterns)
- File sizes within guidelines
- Cross-references resolve

### 6. Review & Ship

Present the validation report and a summary of what was exported. The user decides whether to commit/push or adjust.

## Important Rules

- **Never include secrets.** The scan and distill scripts strip known patterns, but always review `operational/tools.md` and `operational/infrastructure.md` manually.
- **Distill, don't copy.** Raw journal entries and session states should be compressed into structured knowledge. The export should be 10-20% the volume of raw state.
- **Respect privacy.** Flag personal information about the user for access tier review. Default user-specific content to `private` access.
- **Preserve provenance.** Each distilled file should note its source files in frontmatter.
- **Don't modify the live workspace.** All output goes to the export directory.
