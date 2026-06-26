---
name: easypaper
description: "Generate academic papers from metadata using EasyPaper Python SDK. Use when user wants to create structured LaTeX papers programmatically. References the EasyPaper repository, especially plugins/easypaper/ directory for detailed workflows, commands, and skills."
---

# EasyPaper Skill

Generate structured academic papers from metadata using the EasyPaper multi-agent system via Python SDK.

## Repository

**Source**: https://github.com/PinkGranite/EasyPaper

**Primary Reference Directory**: [`plugins/easypaper/`](https://github.com/PinkGranite/EasyPaper/tree/master/plugins/easypaper)

This directory contains comprehensive guidance for OpenClaw agents:
- **Commands**: Workflow execution contracts in `plugins/easypaper/commands/`
- **Skills**: Domain-specific skills in `plugins/easypaper/skills/`
- **Plugin Documentation**: Setup and usage in `plugins/easypaper/.claude-plugin/README.md`

## Installation

### Python Package

**Important**: Install EasyPaper in an isolated environment (recommended for dependency management).

**Using venv**:
```bash
python -m venv easypaper-env
source easypaper-env/bin/activate  # On Windows: easypaper-env\Scripts\activate
pip install easypaper
```

**Using conda**:
```bash
conda create -n easypaper python=3.11
conda activate easypaper
pip install easypaper
```

**Direct install** (not recommended):
```bash
pip install easypaper
```

### LaTeX Toolchain

EasyPaper requires LaTeX toolchain (`pdflatex` + `bibtex`) for PDF compilation. Install based on your system:

**macOS**:
```bash
# Using Homebrew (recommended)
brew install --cask mactex

# Or minimal installation
brew install basictex
sudo tlmgr update --self
sudo tlmgr install collection-basic collection-latex collection-bibtexextra
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt-get update
sudo apt-get install texlive-latex-base texlive-bibtex-extra texlive-latex-extra
```

**Linux (Fedora/RHEL)**:
```bash
sudo dnf install texlive-scheme-basic texlive-bibtex texlive-latex
```

**Windows**:
- Download and install [MiKTeX](https://miktex.org/download) (full installer recommended)
- Or use [TeX Live](https://www.tug.org/texlive/windows.html)
- Ensure `pdflatex` and `bibtex` are in your PATH

### Poppler (for PDF-to-image conversion)

**macOS**:
```bash
brew install poppler
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt-get install poppler-utils
```

**Linux (Fedora/RHEL)**:
```bash
sudo dnf install poppler-utils
```

**Windows**:
- Download from [Poppler for Windows](http://blog.alivate.com.au/poppler-windows/)
- Extract and add `bin` directory to PATH
- Or use [conda](https://anaconda.org/conda-forge/poppler): `conda install -c conda-forge poppler`

## Quick Start

**Recommended workflow:** Prepare a `metadata.json` (see [`examples/meta.json`](https://github.com/PinkGranite/EasyPaper/blob/master/examples/meta.json)), parse it as `PaperGenerationRequest`, then run with `to_metadata()` + `to_generate_options()`.

**Typesetter behavior (SDK + Server):** PDF compilation prefers in-process Typesetter when available (SDK self-contained). If no local peer is available, EasyPaper falls back to the HTTP Typesetter endpoint (`AGENTSYS_SELF_URL`).

### Load from file and generate

```python
import asyncio
from pathlib import Path
from easypaper import EasyPaper, PaperGenerationRequest

async def main():
    ep = EasyPaper(config_path=str(Path("configs/dev.yaml").resolve()))
    
    request = PaperGenerationRequest.model_validate_json_file("metadata.json")
    metadata = request.to_metadata()
    options = request.to_generate_options()

    result = await ep.generate(metadata, **options)
    print(f"Status: {result.status}, Words: {result.total_word_count}")

asyncio.run(main())
```

### Inline metadata

```python
import asyncio
from easypaper import EasyPaper, PaperMetaData

async def main():
    ep = EasyPaper(config_path="configs/dev.yaml")
    
    metadata = PaperMetaData(
        title="My Paper Title",
        idea_hypothesis="...",
        method="...",
        data="...",
        experiments="...",
        references=["@article{...}"],
    )
    
    result = await ep.generate(metadata)
    print(f"Status: {result.status}, Words: {result.total_word_count}")

asyncio.run(main())
```

## Key Reference Files

When working with EasyPaper, refer to these files in the repository:

### Commands (Workflow Execution)

- [`plugins/easypaper/commands/easypaper.md`](https://github.com/PinkGranite/EasyPaper/blob/master/plugins/easypaper/commands/easypaper.md) - End-to-end metadata workflow contract
- [`plugins/easypaper/commands/paper-from-metadata.md`](https://github.com/PinkGranite/EasyPaper/blob/master/plugins/easypaper/commands/paper-from-metadata.md) - Direct metadata-to-paper generation
- [`plugins/easypaper/commands/paper-section.md`](https://github.com/PinkGranite/EasyPaper/blob/master/plugins/easypaper/commands/paper-section.md) - Single section generation

### Skills (Domain Guidance)

- [`plugins/easypaper/skills/setup-environment/SKILL.md`](https://github.com/PinkGranite/EasyPaper/blob/master/plugins/easypaper/skills/setup-environment/SKILL.md) - Automatic environment setup (Python, LaTeX)
- [`plugins/easypaper/skills/paper-from-metadata/SKILL.md`](https://github.com/PinkGranite/EasyPaper/blob/master/plugins/easypaper/skills/paper-from-metadata/SKILL.md) - Full paper generation workflow
- [`plugins/easypaper/skills/venue-selection/SKILL.md`](https://github.com/PinkGranite/EasyPaper/blob/master/plugins/easypaper/skills/venue-selection/SKILL.md) - Venue-specific formatting (NeurIPS, ICML, ICLR, ACL, AAAI, COLM, Nature)
- [`plugins/easypaper/skills/academic-writing-rules/SKILL.md`](https://github.com/PinkGranite/EasyPaper/blob/master/plugins/easypaper/skills/academic-writing-rules/SKILL.md) - Academic writing and LaTeX conventions

### Configuration and Examples

- [`configs/example.yaml`](https://github.com/PinkGranite/EasyPaper/blob/master/configs/example.yaml) - Complete configuration template
- [`economist_example/metadata.json`](https://github.com/PinkGranite/EasyPaper/blob/master/economist_example/metadata.json) - Full metadata example with all fields
- [`user_case/`](https://github.com/PinkGranite/EasyPaper/tree/master/user_case) - Standalone usage example
- [`README.md`](https://github.com/PinkGranite/EasyPaper/blob/master/README.md) - Main documentation
- [`AGENTS.md`](https://github.com/PinkGranite/EasyPaper/blob/master/AGENTS.md) - Repository-level agent instructions

## PaperMetaData Fields

**Required**:
- `title`, `idea_hypothesis`, `method`, `data`, `experiments`, `references`

**Optional**:
- `style_guide` (venue name), `target_pages`, `template_path`, `figures`, `tables`, `code_repository`, `export_prompt_traces`

See [`examples/meta.json`](https://github.com/PinkGranite/EasyPaper/blob/master/examples/meta.json) and [`economist_example/metadata.json`](https://github.com/PinkGranite/EasyPaper/blob/master/economist_example/metadata.json) for full examples. Treat `examples/meta.json` as a full `PaperGenerationRequest` sample: use `request = PaperGenerationRequest.model_validate_json_file(...)`, then `request.to_metadata()` and `request.to_generate_options()` for SDK generation.

## Final PDF Selection

When review loop is enabled, multiple iteration PDFs can exist. Always report the final artifact using this priority:

1. `result.pdf_path` (authoritative final output)
2. Under `result.output_path`: `iteration_*_final/**/*.pdf`
3. Under `result.output_path`: latest `iteration_*` directory PDF
4. `result.output_path/paper.pdf` (last fallback)

If no PDF is found, report that final PDF is unavailable and include recent compile errors.

## Streaming Generation

```python
from easypaper import EasyPaper, PaperMetaData, EventType

async for event in ep.generate_stream(metadata):
    if event.event_type == EventType.PHASE_START:
        print(f"▶ [{event.phase}] {event.message}")
    elif event.event_type == EventType.COMPLETE:
        result = event.data["result"]
        print(f"Done! {result['total_word_count']} words")
```

## When to Use This Skill

Use this skill when:
- User wants to generate academic papers programmatically
- User needs to understand EasyPaper SDK usage
- User asks about paper generation workflows
- User needs venue-specific formatting guidance

**For detailed workflows and execution contracts, refer to files in `plugins/easypaper/` directory.**
