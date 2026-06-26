# Training pipeline — Essay Humanizer

## 1. Environment

```bash
cd ~/EssayHumanizer
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## 2. Corpora

Paths are in [`config.yaml`](../../config.yaml). Defaults:

- CAWSE: `~/CAWSE`
- LOCNESS: `~/Downloads/LOCNESS-corpus-files`

## 3. Steps

```bash
# Normalize human essays
python scripts/load_corpus.py

# Generate AI counterparts (requires DEEPSEEK_API_KEY)
export DEEPSEEK_API_KEY=...
python scripts/generate_ai_essays.py --max 150

# Pattern + MDD analysis
python scripts/analyze_patterns.py

# Regenerate weighted SKILL.md from weights.json
python scripts/render_skill_md.py

# SFT pairs (parallel human/AI + optional teacher)
python scripts/build_sft.py --teacher

# Fit each row to max_seq_length (stops MLX “sequence longer than 1024” truncation warnings)
python scripts/chunk_sft_for_training.py

# Train (uses data/sft_token_limited by default — see configs/train_qwen3_8b.yaml)
chmod +x scripts/train.sh
./scripts/train.sh

# Resume from latest adapter checkpoint (example)
# ESSAYHUMANIZER_RESUME_ADAPTER_FILE=$(ls -t adapters/*adapters.safetensors 2>/dev/null | head -1) ./scripts/train.sh
```

### Early stopping

**Not built in.** Apple’s `mlx_lm` LoRA trainer uses a fixed `iters` loop; it logs validation loss on `steps_per_eval` but has **no patience / best-checkpoint selection / automatic stop** in the versions typically used with Python 3.9.

**Practical options:**

1. **Tune `iters` by hand** after watching val loss in the console (reduce `iters` once loss flattens or rises).
2. **Tighter monitoring:** lower `steps_per_eval` in `configs/train_qwen3_8b.yaml` (e.g. `50`) so you see val more often.
3. **Checkpoints:** `save_every` writes periodic adapters; `mlx_lm` does **not** automatically keep “best val” only—pick the step with the lowest logged val loss if you care, or reduce `save_every` to snapshot more often.
4. **Future:** if you upgrade `mlx-lm`, check release notes for early-stopping callbacks; you could also wrap training in your own loop with `resume_adapter_file` once upstream supports clean stop-and-resume (not wired in this repo).

## 4. Inference

```bash
python skill/scripts/inference.py --file my_ai_draft.txt
```

Use the same base model as in `configs/train_qwen3_8b.yaml`. If 8B OOMs on your machine, switch both config and `inference.py` default to `Qwen/Qwen3-4B-MLX-4bit` and retrain.

## Training: `jinja2.UndefinedError: dict object has no element 0`

If LoRA dies inside `apply_chat_template` during `mask_prompt: true`, your `mlx_lm` build passes a **single message dict** where the template expects a **list**. In `configs/train_qwen3_8b.yaml` we set **`mask_prompt: false`** so only the full user+assistant sequence is tokenized (slightly more loss on prompt tokens; training still valid). Upgrade `mlx-lm` when upstream fixes `CompletionsDataset` (`[messages[0]]` instead of `messages[0]`).

## MLX / training: `libmlx.dylib` / Anaconda

If training fails with `Library not loaded: @rpath/libmlx.dylib`, your **conda** Python usually has a broken MLX wheel. Do **not** use `base` for MLX on macOS unless you know it works.

1. **Deactivate conda** and use Apple-friendly Python:
   ```bash
   conda deactivate
   /usr/bin/python3 -m pip install --upgrade mlx mlx-lm
   ./scripts/train.sh
   ```
2. Or create a **venv outside conda** and install `requirements.txt` there, then:
   ```bash
   export MLX_PYTHON="$PWD/.venv/bin/python"
   ./scripts/train.sh
   ```
3. `scripts/train.sh` now auto-picks: `$MLX_PYTHON` → `/usr/bin/python3` → `python3` (first where `import mlx.core` succeeds).

## 5. Legal / ethics

- CAWSE and LOCNESS have their own licenses; keep usage non-commercial if required.
- This tool is for **style revision** and learning support, not to circumvent academic integrity policies.
