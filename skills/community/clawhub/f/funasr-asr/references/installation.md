# FunASR 安装指南

## 系统要求

- Python 3.8+
- 内存: 至少 2GB 可用（小内存模式 500MB）
- 存储: 约 3GB（模型文件）

## 安装步骤

### 1. Python 依赖

```bash
pip install funasr onnxruntime psutil
```

### 2. 视频处理工具（可选）

```bash
# yt-dlp（推荐）
pip install yt-dlp

# ffmpeg
apt install ffmpeg  # Ubuntu/Debian
brew install ffmpeg # macOS
```

### 3. 首次运行

首次运行会自动下载模型：

```bash
python3 scripts/transcribe.py test.wav
```

模型下载位置：`~/.cache/modelscope/hub/`

## GPU 加速

如有 NVIDIA GPU：

```bash
pip uninstall onnxruntime
pip install onnxruntime-gpu
```

## 验证安装

```bash
python3 -c "from funasr import AutoModel; print('✅ FunASR 已安装')"
```

## 常见问题

### 模型下载慢

使用国内镜像：

```bash
export MODELSCOPE_CACHE=~/.cache/modelscope
pip install modelscope
modelscope download --model iic/SenseVoiceSmall
```

### 内存不足

使用小内存模式：

```bash
python3 scripts/transcribe.py audio.wav --mode small
```

### 权限问题

确保脚本有执行权限：

```bash
chmod +x scripts/*.py scripts/*.sh
```
