# Installation Guide

## System Requirements

- GPU: ≥24GB for inference, A800/H200 recommended
- Python: ≥3.10, Python 3.12 recommended
- OS: Linux / WSL (--compile not supported on Windows)

## System Dependencies

```bash
apt install portaudio19-dev libsox-dev ffmpeg
```

## Conda

```bash
conda create -n fish-speech python=3.12 && conda activate fish-speech
pip install -e .[cu129]    # CUDA versions: cu126/cu128/cu129
pip install -e .[cpu]      # CPU
pip install -e .           # Default PyTorch index
```

## UV (Faster)

```bash
uv sync --python 3.12 --extra cu129
```

## pip Minimal Installation

```bash
pip install fish-speech   # Runtime dependencies only, no source code
```

## Intel Arc XPU

```bash
conda create -n fish-speech python=3.12 && conda activate fish-speech
conda install libstdcxx -c conda-forge
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/xpu
pip install -e .
```

## Docker

```bash
docker pull fishaudio/fish-speech

# Compose
docker compose --profile webui up          # Port 7860
COMPILE=1 docker compose --profile webui up # ~10x speedup
docker compose --profile server up          # Port 8080
BACKEND=cpu docker compose --profile webui up

# Manual build
docker build -f docker/Dockerfile --build-arg BACKEND=cuda --build-arg CUDA_VER=12.9.0 --build-arg UV_EXTRA=cu129 --target webui -t fish-speech:webui .

# Run
docker run --gpus all -v ./checkpoints:/app/checkpoints -e COMPILE=1 -p 7860:7860 fish-speech:webui
```

Environment variables: `BACKEND` (cuda/cpu), `COMPILE` (0/1), `CUDA_VER`, `UV_EXTRA`, `GRADIO_PORT`, `API_PORT`

⚠️ Docker image does not include model weights; mount checkpoints.

## Download Model

```bash
hf download fishaudio/s2-pro --local-dir checkpoints/s2-pro
# or: git clone https://huggingface.co/fishaudio/s2-pro checkpoints/s2-pro