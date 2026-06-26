#!/bin/bash
# ComfyUI 启动脚本（RTX 3080 + WSL）
# 用法: bash start-comfyui.sh

export LD_LIBRARY_PATH=~/.local/lib/python3.12/site-packages/nvidia/cudnn/lib:~/.local/lib/python3.12/site-packages/nvidia/nccl/lib:$LD_LIBRARY_PATH

cd ~/ComfyUI
source venv/bin/activate
python3 main.py --port 8188 --listen 127.0.0.1
