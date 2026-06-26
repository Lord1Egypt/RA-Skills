# 本地 SDXL 部署说明（RTX 3080 + WSL）

## 环境

- 显卡：NVIDIA RTX 3080 (10GB VRAM)
- 系统：WSL Ubuntu
- Python：3.12
- CUDA：12.1
- PyTorch：2.5.1+cu121

## 目录结构

```
~/ComfyUI/               — ComfyUI 主程序
~/models/sdxl/           — SDXL 模型文件
  sdxl-base-1.0.safetensors   (6.5GB)
```

## 启动 ComfyUI

```bash
export LD_LIBRARY_PATH=~/.local/lib/python3.12/site-packages/nvidia/cudnn/lib:~/.local/lib/python3.12/site-packages/nvidia/nccl/lib:$LD_LIBRARY_PATH
cd ~/ComfyUI && source venv/bin/activate
python3 main.py --port 8188 --listen 127.0.0.1
```

## 验证运行

```bash
curl http://localhost:8188/system_stats | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['devices'][0]['Name'])"
```

预期输出：`cuda:0 NVIDIA GeForce RTX 3080`
