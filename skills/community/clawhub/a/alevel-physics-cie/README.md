# alevel-physics-cie

Structured answer templates for **CIE A-Level Physics (9702)** exam questions, powered by a fine-tuned **Qwen3-4B** model with LoRA adapters.

Given any text-based 9702 question, the model produces:
- **Question type** — calculation / definition / explain / describe / derive
- **Given** — extracted quantities and conditions
- **Required** — what to find or state
- **Formulae / principles** — relevant equations and laws
- **Answer frame** — step-by-step approach
- **Check** — unit, sign, and reasonableness verification

## Quick Start

```bash
pip install mlx mlx-lm

# Interactive mode
python skill/scripts/inference.py --interactive

# Single question
python skill/scripts/inference.py "Define specific heat capacity and explain how it is measured."
```

## Example Output

**Q:** A ball of mass 0.15 kg is thrown vertically upwards with a speed of 20 m/s. Calculate the maximum height.

```
## Question type
Calculation

## Given
- Mass of ball, m = 0.15 kg
- Initial speed, u = 20 m/s
- Final speed at maximum height, v = 0 m/s
- g = 9.81 m/s²

## Required
Calculate the maximum height h.

## Formulae / principles
- v² = u² + 2as

## Answer frame
1. At max height v = 0, a = -g
2. Rearrange: 0 = u² - 2gh → h = u²/(2g)
3. Substitute: h = 400/19.62 ≈ 20.4 m

## Check
- Units: m²s⁻² / ms⁻² = m ✓
- Magnitude reasonable ✓
```

## Model Details

| | |
|---|---|
| Base model | `Qwen/Qwen3-4B-MLX-4bit` |
| Fine-tuning | LoRA rank 8, 16 layers, 1000 iters |
| Training data | 414 examples from 1652 CIE 9702 PDFs (2001–2025) |
| Teacher | DeepSeek with mark-scheme context |
| Best val loss | 0.746 (iter 900) |
| Peak memory | 4.0 GB |
| Hardware | Any 8GB+ Apple Silicon Mac |

## Project Structure

```
alevel-physics-cie/
├── skill/
│   ├── SKILL.md              # Skill definition (Codex/Clawhub)
│   ├── scripts/
│   │   ├── inference.py      # Standalone inference CLI & library
│   │   └── adversarial_eval.py # Adversarial robustness evaluation
│   └── references/
│       ├── training.md       # Full pipeline documentation
│       └── answer_template_format.md
├── adapters/
│   ├── adapters.safetensors  # Final LoRA weights (28 MB)
│   └── adapter_config.json   # Training config snapshot
├── scraper/                  # CIE 9702 paper scraper (cie.fraft.org)
├── scripts/                  # Data pipeline & training scripts
├── configs/                  # MLX LoRA training YAML
├── data/sft/                 # Training data (train.jsonl + valid.jsonl)
├── clawhub.json              # ClawHub marketplace metadata
├── config.yaml               # Project configuration
└── requirements.txt
```

## Retraining

To retrain with more data or a different teacher model:

```bash
# Full pipeline: scrape → extract → build SFT → train
DEEPSEEK_API_KEY=<key> python scripts/run_full_pipeline.py --teacher deepseek

# Or step by step:
python -m scraper.scrape_9702              # Scrape all 9702 PDFs
python -m scraper.extract_questions        # Extract text questions
python scripts/build_sft.py --teacher-mode deepseek --max-samples 500
python3 -m mlx_lm.lora --config configs/train_qwen35_4b.yaml --train
```

## Robustness Evaluation

Test the model's adversarial robustness using three physics-adapted attack strategies (adapted from [Xie et al. 2024](https://arxiv.org/abs/2402.17916)):

```bash
# Run all three strategies on the validation set
python skill/scripts/adversarial_eval.py

# Run only numeric perturbation with 5 variants on 10 questions
python skill/scripts/adversarial_eval.py --strategies numeric --variants 5 --max-questions 10

# Run specific strategies
python skill/scripts/adversarial_eval.py --strategies numeric,context,type
```

| Strategy | Attack | What it tests |
|----------|--------|---------------|
| `numeric` | M3-style value perturbation with physics constraints | Formula selection stability under changed numbers |
| `context` | Swap surface-level objects (ball/stone, car/truck) | Physics invariance to scenario wording |
| `type` | Swap action verbs (explain/describe, calculate/estimate) | Question-type classification accuracy |

Reports OA (Original Accuracy), AA (Adversarial Accuracy), and ASR (Attack Success Rate) per strategy, saved to `data/eval/adversarial_report.json`.

## Requirements

- Python 3.9+
- Apple Silicon Mac (MLX)
- `pip install mlx mlx-lm pdfplumber pyyaml requests beautifulsoup4 tqdm`

## License

MIT. CIE past papers are © Cambridge Assessment International Education.
