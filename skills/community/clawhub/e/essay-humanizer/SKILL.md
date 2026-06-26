---
name: essay-humanizer
description: "Rewrite AI-drafted essays into more human-like academic prose. Fine-tuned LoRA over Qwen3-8B guided by 24 Wikipedia-style AI-writing pattern weights plus MDD/ADD syntactic targets from CAWSE/LOCNESS vs DeepSeek baselines. Includes trained LoRA adapter and inference script. Requires Apple Silicon macOS with MLX. Optional FastAPI host for MCP/tool linking. Orchestrator: output plain text only (no LaTeX dollar delimiters)."
---

# Essay Humanizer (corpus-informed)

Rewrites **AI-generated** argumentative/academic essays toward **human baseline** style informed by **CAWSE** (M/D bands) **LOCNESS**, and contrast with **DeepSeek**-generated counterparts. Ships with a fine-tuned **LoRA adapter** (9.3 MB) and inference script.

## Skill contract

| Component | Path | Notes |
|---|---|---|
| Inference script | `scripts/inference.py` | Entry point — `humanize()` function or CLI |
| LoRA adapters | `assets/adapters/adapters.safetensors.json` | 12.3 MB base64 JSON; auto-decoded to binary on first run |
| Pattern weights | `data/analysis/weights.json` | Corpus-derived, loaded by inference at runtime |
| Decoder | `scripts/decode_adapters.py` | Reconstructs .safetensors binary from JSON (auto or manual) |
| Installer | `scripts/install_deps.sh` | One-time: `pip install mlx mlx-lm transformers` + decode |
| Base model | `Qwen/Qwen3-8B-MLX-4bit` | Downloaded from HuggingFace on first run (~4.5 GB, cached) |

**Requirements:** Apple Silicon macOS with Python 3.9+.

## Quick Start

```bash
bash scripts/install_deps.sh          # one-time: installs deps + decodes adapter
python scripts/inference.py --file draft.txt   # adapter auto-decodes if not already done
```

Or from Python:

```python
from scripts.inference import humanize
print(humanize("Your AI-drafted essay text here..."))
```

## Weighted pattern table (descending priority)

When humanizing, address **higher-weight** rows first. Weights are **data-driven** from corpus analysis (Mann-Whitney); zero-weight rows were not statistically significant.

| ID | Weight | Category | Pattern |
|---|---:|---|---|
| P06_CLICHE_METAPHORS | 0.1358 | vocabulary | Cliche metaphors |
| P15_EM_DASH_OVERKILL | 0.1358 | punctuation | Em dash overkill |
| P21_MARKDOWN_ARTIFACTS | 0.1358 | formatting | Markdown artifacts |
| P23_TEXTBOOK_BOLDING | 0.1358 | formatting | Textbook bolding |
| P12_PRESENT_PARTICIPLE_TAIL | 0.1133 | rhetorical | Present participle tailing |
| P10_RULE_OF_THREES | 0.0806 | rhetorical | Rule of threes |
| P04_AI_VOCABULARY | 0.0621 | vocabulary | AI vocabulary |
| P14_COMPULSIVE_SUMMARIES | 0.0598 | rhetorical | Compulsive summaries |
| P05_EXCESSIVE_ADVERBS | 0.0540 | vocabulary | Excessive adverbs |
| P13_OVER_ATTRIBUTION | 0.0529 | rhetorical | Over-attribution |
| P11_FALSE_RANGES | 0.0341 | rhetorical | False ranges |
| P17_TRANSITION_OVERUSE | 0.0001 | punctuation | Overuse of transition words |
| P01_UNDUE_EMPHASIS | 0.0000 | content | Undue emphasis |
| P02_SUPERFICIAL_ANALYSIS | 0.0000 | content | Superficial analysis |
| P03_REGRESSION_TO_MEAN | 0.0000 | content | Regression to the mean |
| P07_REDUNDANT_MODIFIERS | 0.0000 | vocabulary | Redundant modifiers |
| P08_FILLER_HEDGING | 0.0000 | vocabulary | Filler hedging |
| P09_NEGATIVE_PARALLELISM | 0.0000 | rhetorical | Negative parallelisms |
| P16_EN_DASH_AVOIDANCE | 0.0000 | punctuation | En dash / hyphen misuse for ranges |
| P18_COLLABORATIVE_REGISTER | 0.0000 | register | Collaborative register |
| P19_LETTER_FORMALITY | 0.0000 | register | Letter-style formality |
| P20_INSTRUCTIONAL_CONDESCENSION | 0.0000 | register | Instructional condescension |
| P22_EXCESSIVE_LISTS | 0.0000 | formatting | Excessive bulleted/numbered lists |
| P24_EMOJI_SYMBOL | 0.0000 | formatting | Emoji/symbol injection |

## Syntactic complexity (MDD / ADD advisory)

Human **Merit / Distinction**-range writing in CAWSE often shows **variable** mean dependency distance (MDD); AI prose may cluster more tightly. When humanizing:

- Reference MDD means from analysis: human ~2.333775514332394, AI ~2.4553791855163483.
- **Variance ratio** (human/AI) ~1.7153931408079544: prefer natural mix of shorter and longer dependency links, not uniformly smoothed sentences.
- Avoid flattening every sentence to minimal dependency length; that can read as a different kind of machine polish.


## Mandatory rule (orchestrator)

1. Output **continuous prose** suitable for submission (no chat-signoffs, no "hope this helps").
2. **Plain text** only for math if any — no raw `$$` LaTeX unless user explicitly requests LaTeX.
3. Preserve **author stance** and **citations** if present; do not fabricate references.

## Hosted HTTP API (optional, for non-Mac or remote use)

For non-Apple-Silicon machines or multi-user deployments, run the optional **FastAPI** server on a Mac host and connect via HTTP/OpenAPI:

1. Install: `pip install fastapi uvicorn[standard]`
2. Run: `uvicorn api.main:app --host 0.0.0.0 --port 8765` (set `HUMANIZE_API_KEY` env var for auth)
3. Point MCP / OpenAPI tools at `https://<your-host>/openapi.json`
4. Call `POST /v1/humanize` with JSON `{"text":"..."}` (+ `Authorization: Bearer …`)

See [references/hosted_api.md](references/hosted_api.md) for details.

## References

- [references/patterns.md](references/patterns.md) — 24 pattern details with detection/fix hints
- [references/training.md](references/training.md) — full training pipeline
- [references/hosted_api.md](references/hosted_api.md) — HTTP API / MCP tool linking
