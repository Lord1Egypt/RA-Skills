---
name: dgx-spark-setup
version: 1.0.0
description: Set up and maintain an NVIDIA DGX Spark (GB10 Blackwell, 128GB unified memory) as a local LLM inference server running vLLM + LiteLLM + OpenClaw. Use when installing vLLM from source on a DGX Spark, troubleshooting Blackwell/sm_121 GPU compatibility, configuring LiteLLM virtual keys for multi-user access, setting up Tailscale for private remote access, or recovering from a broken vLLM environment (torch downgrade, Triton mismatch, flashinfer version conflict).
---

# DGX Spark Setup

Complete setup guide for running Nemotron Super 120B (NVFP4) on a DGX Spark as a private OpenClaw backend with multi-user LiteLLM routing.

## Architecture

```
MacBook (remote) ──Tailscale──► Mac Mini (OpenClaw host, SatPicks worker)
                                      │ LAN SSH
                                      ▼
                               DGX Spark (192.168.1.234)
                               ├── vLLM :8000  (inference)
                               └── LiteLLM :4000 (auth/routing)
```

## Prerequisites

- DGX Spark with Ubuntu (user: `jhernandez`)
- Model downloaded to `/home/jhernandez/models/nemotron-super-120b-nvfp4`
- Python 3.12 available (`python3 --version`)
- `uv` installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

## 1. vLLM Environment Setup

The DGX Spark uses the GB10 Blackwell chip (sm_121). Stock PyPI packages do NOT support sm_121 — everything must be custom built or sourced from specific index URLs.

```bash
mkdir -p ~/vllm-install
cd ~/vllm-install
uv venv .vllm --python 3.12
source .vllm/bin/activate
```

### Install PyTorch (CUDA 13.0)

Must use `uv pip install` with the cu130 index — regular pip may resolve the wrong CUDA variant:

```bash
uv pip install torch torchvision torchaudio \
  --index-url https://download.pytorch.org/whl/cu130
```

Verify: `python3 -c "import torch; print(torch.__version__)"` → should show `2.11.0+cu130`

### Build Custom Triton (sm_121 support)

Stock Triton does not support sm_121. Must build from this exact commit:

```bash
cd ~/vllm-install
git clone https://github.com/triton-lang/triton.git
cd triton
git checkout 4caa0328bf8df64896dd5f6fb9df41b0eb2e750a
pip install ninja cmake wheel
pip install -e python/
```

Verify: `python3 -c "import triton; print(triton.__version__)"` → should show `3.5.0+git4caa0328`

### Install flashinfer

Versions must match exactly — mismatched cubin/flashinfer causes silent failures:

```bash
pip install flashinfer-python
pip install flashinfer  # cubin package — must match flashinfer-python version
```

### Install vLLM from Source

```bash
cd ~/vllm-install
git clone https://github.com/vllm-project/vllm.git
cd vllm
git checkout 66a168a197ba214a5b70a74fa2e713c9eeb3251a
pip install -e . --no-build-isolation
```

## 2. Running vLLM

Always launch inside the tmux session so it survives SSH disconnects:

```bash
tmux new-session -s nemotron   # or: tmux attach -t nemotron

export PATH=$HOME/.local/bin:$PATH
source ~/vllm-install/.vllm/bin/activate

TORCH_CUDA_ARCH_LIST=12.1a \
VLLM_USE_FLASHINFER_MXFP4_MOE=1 \
TRITON_PTXAS_PATH=/usr/local/cuda/bin/ptxas \
  python -m vllm.entrypoints.openai.api_server \
  --model /home/jhernandez/models/nemotron-super-120b-nvfp4 \
  --trust-remote-code --max-model-len 8192 \
  --gpu-memory-utilization 0.85 --port 8000
```

Startup takes ~8 minutes (loading 17 safetensor shards). Ready when log shows `Application startup complete`.

**Note:** `nvidia-smi` shows `N/A` for memory on the GB10 (unified memory architecture) — this is normal, not a bug.

## 3. LiteLLM Setup

LiteLLM proxies vLLM and handles per-user auth and rate limiting.

### Install

```bash
pip install litellm
```

### Config (`~/litellm-config.yaml`)

See `references/litellm-config-template.yaml` for a full config with virtual keys and rate limits.

### Run as systemd service

```bash
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/litellm.service << 'EOF'
[Unit]
Description=LiteLLM Proxy
After=network.target

[Service]
ExecStart=/home/jhernandez/.local/bin/litellm --config /home/jhernandez/litellm-config.yaml --port 4000
Restart=on-failure
RestartSec=5
StandardOutput=append:/home/jhernandez/litellm.log
StandardError=append:/home/jhernandez/litellm.log
Environment=PATH=/home/jhernandez/.local/bin:/usr/local/bin:/usr/bin:/bin

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable litellm
systemctl --user start litellm
```

Verify: `curl http://localhost:4000/health/liveliness` → `"I'm alive!"`

## 4. Tailscale

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
# Visit the auth URL shown, then approve in Tailscale admin
tailscale ip -4  # note this IP for OpenClaw client configs
```

## 5. OpenClaw Client Config

Point any OpenClaw instance at LiteLLM:

```yaml
model:
  provider: openai-compatible
  baseUrl: http://<dgx-tailscale-ip>:4000/v1
  apiKey: <virtual-key>
  model: nemotron-super
```

## Troubleshooting

See `references/troubleshooting.md` for common failure modes and fixes.
