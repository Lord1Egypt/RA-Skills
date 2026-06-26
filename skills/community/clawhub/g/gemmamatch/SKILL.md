---
name: gemmamatch
description: "Auto-detect hardware and recommend the best Gemma 4 model for local deployment on PC, Mac, or mobile."
author: GemmaMatch
version: "1.0.0"
keywords:
  - gemma4
  - local-llm
  - hardware-matcher
  - ollama
  - gpu-detection
homepage: https://www.gemmamatch.com
source: https://github.com/walex8925/Gemma4local
---

# GemmaMatch — Gemma 4 Local Hardware Matcher

Find the best Gemma 4 model for your hardware in seconds.

**Website**: https://www.gemmamatch.com

## What it does

GemmaMatch auto-detects your GPU, VRAM, and system specs via WebGPU/WebGL APIs, then recommends the most suitable Gemma 4 model tier and provides a ready-to-use run command. All processing happens locally in your browser — no data leaves your device.

## Recommended model tiers

| Tier | Target hardware | Use case |
| --- | --- | --- |
| Gemma 4 E2B | Phones, tablets, low-VRAM devices | On-device inference, edge deployment |
| Gemma 4 26B MoE | Desktop GPUs (8-16 GB VRAM) | General local AI, coding assistance |
| Gemma 4 31B Dense | Workstations (24+ GB VRAM) | High-quality generation, research |

## Key features

- **Automatic GPU detection** — uses WebGPU and WebGL APIs, no install required
- **Personalized model recommendation** — matches your exact hardware to the optimal Gemma 4 variant
- **Platform-specific setup guides** — step-by-step instructions for Mac (MLX, Ollama), Windows (Ollama, LM Studio), iOS, and Android
- **One-click run commands** — get a copy-paste Ollama or LM Studio command tailored to your system
- **Manual comparison mode** — compare upgrade scenarios or override auto-detection
- **Privacy-first** — everything runs in-browser, zero data collection

## Quick start

1. Visit https://www.gemmamatch.com
2. Allow hardware detection (or enter specs manually)
3. Get your recommended model + run command
4. Copy the command and run it in your terminal

## Supported platforms

- **macOS** — Apple Silicon (M1-M4), Intel with discrete GPU
- **Windows** — NVIDIA (RTX 30/40/50 series), AMD (RX 7000 series)
- **Linux** — NVIDIA CUDA, AMD ROCm
- **iOS / Android** — on-device model recommendations

## Links

- Website: https://www.gemmamatch.com
- GitHub: https://github.com/walex8925/Gemma4local
- Product Hunt: https://www.producthunt.com/products/gemma-4-local-hardware-matcher
