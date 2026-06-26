# LoRA Fine-tuning

⚠️ Not recommended for models after RL training. Only fine-tune Slow AR (LLAMA).

## 1. Data Preparation

```
data/SPK1/
├── 21.15-26.44.lab    # Plain text transcription
├── 21.15-26.44.mp3    # Audio
└── ...
```

Format: `.mp3/.wav/.flac` + matching `.lab`. Recommended loudness normalization: `fap loudness-norm data-raw data --clean`

## 2. Extract Semantic Tokens

```bash
hf download fishaudio/openaudio-s1-mini --local-dir checkpoints/openaudio-s1-mini
python tools/vqgan/extract_vq.py data --num-workers 1 --batch-size 16 \
  --config-name modded_dac_vq --checkpoint-path checkpoints/openaudio-s1-mini/codec.pth
# Generates .npy alongside source files
```

## 3. Package Protobuf

```bash
python tools/llama/build_dataset.py --input data --output data/protos --text-extension .lab --num-workers 16
```

## 4. LoRA Fine-tuning

```bash
hf download fishaudio/openaudio-s1-mini --local-dir checkpoints/openaudio-s1-mini
python fish_speech/train.py --config-name text2semantic_finetune \
  project=my_project +lora@model.model.lora_config=r_8_alpha_16
# Adjust batch_size/gradient_accumulation_steps to fit VRAM
# For Windows: +trainer.strategy.process_group_backend=gloo
```

## 5. Merge Weights

```bash
python tools/llama/merge_lora.py --lora-config r_8_alpha_16 \
  --base-weight checkpoints/openaudio-s1-mini \
  --lora-weight results/my_project/checkpoints/step_xxx.ckpt \
  --output checkpoints/merged/
```

It is recommended to use the earliest checkpoint that meets requirements (better OOD performance).

## Notes

- By default, only speaking style is learned, not timbre
- Prompts are required to ensure timbre stability
- Increasing training steps can learn timbre but may lead to overfitting