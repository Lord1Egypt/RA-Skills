# Academic Composer

Academic writing assistant for **research and learning purposes**: search peer-reviewed sources, build evidence-mapped outlines, and produce fully cited essays in APA, MLA, or Chicago format.

> **Academic Integrity Notice**
> Intended for personal research drafts, study aids, and learning to construct evidence-based arguments. **NOT** for submitting AI-generated content as your own original work or any form of academic dishonesty. You are solely responsible for complying with your institution's academic honesty requirements.

## What It Does

1. **Source collection** — searches Semantic Scholar (free, no API key needed) for peer-reviewed papers, or accepts sources you provide (title, DOI, URL, BibTeX). Builds a curated Source List before writing begins.
2. **Evidence-based outline** — each body paragraph maps to specific sources. You approve the outline before the skill proceeds.
3. **Fully cited draft** — expands the outline into a complete essay with in-text citations and a formatted Reference List / Works Cited / Bibliography.
4. **Writing style improvement** *(optional, fully local)* — quantitative analysis of 24 stylistic markers, sentence complexity (MDD), and vocabulary richness (TTR) against human-corpus baselines. Citations are protected and never altered. No data leaves your machine.

## Citation Styles

| Style | In-Text | Reference Section |
|-------|---------|------------------|
| APA 7th (default) | (Smith & Lee, 2023) | Reference List |
| MLA 9th | (Smith and Lee 45) | Works Cited |
| Chicago 17th | (Smith and Lee 2023, 45) | Bibliography |

## Data Flow

| Component | Network | Data Sent |
|-----------|---------|-----------|
| Source search (`scholar.py`) | api.semanticscholar.org | Keywords only |
| Style analysis (`pipeline.py`, `measure.py`) | **None** | Fully local |
| Essay generation & rewriting (LLM) | **Depends on agent config** | See below |

**Note on LLM data flow:** Essay generation and rewriting are performed by the agent's language model. If your agent uses a remote model provider, essay content is sent to that provider. If your agent runs a local model, essay content stays on-device. Check your agent configuration to understand your data flow.

## Prerequisites

- Python 3.10+
- spaCy with `en_core_web_sm` *(for writing style analysis)*

## Setup

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Configuration

| Config | Required | Default | Description |
|--------|----------|---------|-------------|
| `citation_style` | No | APA | APA, MLA, or Chicago |
| `max_style_passes` | No | 3 | Max local style improvement passes |

## Usage

Trigger phrases:
- "Write an argumentative essay about climate change with APA citations"
- "Find academic sources on machine learning in healthcare"
- "Write a research paper outline on urban planning, MLA format"

## License

MIT
