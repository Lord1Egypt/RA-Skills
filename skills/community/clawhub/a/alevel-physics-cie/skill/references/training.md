# Training Pipeline Reference

## Overview

The model is trained through a 4-stage pipeline:
1. **Scrape** — Download all 9702 PDFs from cie.fraft.org
2. **Extract** — Parse text-based questions from Papers 2, 4, 5
3. **Build SFT** — Generate answer templates using DeepSeek as teacher
4. **Train** — MLX LoRA fine-tuning on Apple Silicon

## 1. Scraping

```bash
python -m scraper.scrape_9702
```

Uses FRANK CIE's backend API:
- `POST obj/Common/Fetch/renum` with `subject=9702`, `year`, `season`
- `GET obj/Common/Fetch/redir/<filename>` for PDF download
- Automatic 429 backoff and resume for rate-limited downloads
- Config: `config.yaml` → `scraper.years`, `scraper.request_delay_sec`

## 2. Extraction

```bash
python -m scraper.extract_questions
```

- Filters to text-based papers only (Paper 2, 4, 5; skips MCQ Paper 1)
- Splits by CIE question markers (Question N, (a), (b), etc.)
- Pairs each question with its matching mark scheme PDF when available
- Output: `data/questions.jsonl`

## 3. SFT Data Building

```bash
DEEPSEEK_API_KEY=<key> python scripts/build_sft.py --teacher-mode deepseek --max-samples 500
```

- Cleans extracted questions (removes constants pages, dotted lines, boilerplate)
- Pre-caches mark scheme excerpts for efficient API calls
- Sends question + mark scheme context to DeepSeek for template generation
- Falls back to heuristic bootstrap if API fails
- Output: `data/sft/train.jsonl`, `data/sft/valid.jsonl`

## 4. Training

```bash
python3 -m mlx_lm.lora --config configs/train_qwen35_4b.yaml --train
```

Key hyperparameters:
- Base model: `Qwen/Qwen3-4B-MLX-4bit`
- LoRA rank 8, 16 layers, dropout 0.05
- Batch size 1, grad accumulation 4 (effective batch 4)
- Learning rate 1e-5, 1000 iterations
- Max sequence length 2048
- Peak memory: ~4 GB

## Full Pipeline

```bash
python scripts/run_full_pipeline.py --teacher deepseek
```
