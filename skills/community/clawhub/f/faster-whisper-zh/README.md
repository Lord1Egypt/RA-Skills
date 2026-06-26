# Faster-Whisper 中文版

基于 faster-whisper 的高性能本地语音转文字工具的中文优化版本。音频转文字、语音转文字等需求，均可通过该技能实现。

## 版本特点

### 🎯 中文优化
- 完整的中文文档和说明
- 默认语言设置为中文（zh）
- 针对中文语音的优化配置
- 中文错误提示和帮助信息

### 🚀 性能增强
- 自动硬件检测和优化配置
- 国内镜像加速（HF_MIRROR）
- GPU/CPU 自动切换
- 智能模型选择建议

### 📚 完整文档
- 详细的使用指南
- 故障排除手册
- 性能优化建议
- 批量处理脚本

### 🔧 实用工具
- 批量转录脚本
- 配置文件示例
- 硬件检测功能
- 多种使用场景预设

## 文件结构

```
faster-whisper-zh/
├── SKILL.md                    # 技能主文档（中文）
├── setup.sh                    # 安装脚本（中文）
├── requirements.txt            # 依赖包列表
├── _meta.json                  # 元数据
├── config_example.sh           # 配置示例
├── README.md                   # 本文件
└── scripts/
    ├── transcribe.py           # 转录脚本（中文优化）
    └── batch_transcribe.sh     # 批量转录脚本
```

## 快速开始

### 1. 安装
```bash
# 进入技能目录
cd faster-whisper-zh

# 运行安装脚本
./setup.sh
```

### 2. 基本使用
```bash
# 设置环境变量（国内用户推荐）
export HF_HOME=/config/huggingface
export HF_ENDPOINT=https://hf-mirror.com

# 转录音频文件（使用的是虚拟环境内的python3，因此不需要刻意激活虚拟环境）
.venv/bin/python3 scripts/transcribe.py --model large-v3-turbo --language zh 音频文件.mp3
```

### 3. 批量处理
```bash
# 设置环境变量（国内用户推荐）
export HF_HOME=/config/huggingface
export HF_ENDPOINT=https://hf-mirror.com

# 处理目录中的所有音频文件
.venv/bin/python3 scripts/batch_transcribe.sh ./audio_files

# 使用 GPU 加速批量处理
.venv/bin/python3 scripts/batch_transcribe.sh --device cuda --model large-v3-turbo ./recordings
```

## 配置说明

### 环境变量
```bash
# 设置 HuggingFace 缓存目录
export HF_HOME=/config/huggingface

# 使用国内镜像加速
export HF_ENDPOINT=https://hf-mirror.com

# 指定 GPU 设备（多 GPU 环境）
export CUDA_VISIBLE_DEVICES=0
```

### 转录参数
```bash
# 模型选择
--model large-v3-turbo      # （默认）最高准确度，支持多语言
--model distil-large-v3      #平衡速度与准确性
--model small                # 快速转录，资源需求低

# 语言设置
--language zh                # 中文（默认）
--language en                # 英文
--language auto              # 自动检测

# 设备配置
--device auto                # 自动检测（推荐）
--device cuda                # 强制使用 GPU
--device cpu                 # 强制使用 CPU

# 计算类型
--compute-type int8          # CPU 优化（4倍加速）
--compute-type float16       # GPU 优化
--compute-type float32       # 最高精度
```

## 使用场景

### 会议录音转录
```bash
export HF_HOME=/config/huggingface
export HF_ENDPOINT=https://hf-mirror.com
.venv/bin/python3 scripts/transcribe.py 会议录音.mp3 \
  --model large-v3-turbo \
  --language zh \
  --word-timestamps \
  --output 会议纪要.txt
```

### 访谈录音整理
```bash
export HF_HOME=/config/huggingface
export HF_ENDPOINT=https://hf-mirror.com
.venv/bin/python3 scripts/transcribe.py 访谈.wav \
  --model large-v3-turbo \
  --language zh \
  --json \
  --output 访谈记录.json
```

### 实时语音转写
```bash
export HF_HOME=/config/huggingface
export HF_ENDPOINT=https://hf-mirror.com
.venv/bin/python3 scripts/transcribe.py 实时音频.m4a \
  --model small \
  --device cpu \
  --compute-type int8 \
  --beam-size 3
```

### 批量处理会议录音
```bash
export HF_HOME=/config/huggingface
export HF_ENDPOINT=https://hf-mirror.com
.venv/bin/python3 scripts/batch_transcribe.sh ./会议录音 \
  --model large-v3-turbo \
  --language zh \
  --output ./转录结果
```

## 性能建议

### 硬件配置推荐
| 硬件配置 | 推荐模型 | 预期速度 |
|---------|---------|---------|
| 高端 GPU (RTX 4090) | large-v3-turbo | 20-30x 实时 |
| 中端 GPU (RTX 3060) | distil-large-v3 | 10-15x 实时 |
| Apple Silicon M2 | distil-large-v3 | 3-5x 实时 |
| 高性能 CPU (i7/i9) | small/distil-large-v3 | 1-3x 实时 |
| 普通 CPU | small/tiny | 0.5-1x 实时 |

### 内存要求
- `tiny`: 约 150MB
- `small`: 约 500MB  
- `distil-large-v3`: 约 756MB
- `large-v3-turbo`: 约 1.5GB

## 故障排除

### 常见问题

1. **CUDA 不可用**
   ```bash
   # 检查 CUDA 安装
   nvidia-smi
   
   # 重新运行安装脚本
   ./setup.sh
   ```

2. **内存不足**
   ```bash
   # 使用更小的模型
   --model small --compute-type int8
   
   # 减少束搜索大小
   --beam-size 3
   ```

3. **下载速度慢**
   ```bash
   # 设置国内镜像
   export HF_ENDPOINT=https://hf-mirror.com
   export HF_HOME=/config/huggingface
   ```

4. **音频格式不支持**
   ```bash
   # 使用 ffmpeg 转换格式
   ffmpeg -i input.m4a output.wav
   ```

### 错误代码
- `ERROR_CUDA_UNAVAILABLE`: CUDA 不可用，切换到 CPU 模式
- `ERROR_MODEL_DOWNLOAD`: 模型下载失败，检查网络或使用镜像
- `ERROR_AUDIO_FORMAT`: 音频格式不支持，转换为 wav/mp3 格式
- `ERROR_MEMORY`: 内存不足，使用更小的模型或 int8 量化

## 更新计划

### 近期更新
- [ ] 添加实时麦克风输入支持
- [ ] 添加 Web 界面
- [ ] 支持更多音频格式
- [ ] 添加语音翻译功能

### 长期规划
- [ ] 集成到 OpenClaw 技能市场
- [ ] 添加模型微调工具
- [ ] 支持方言识别
- [ ] 添加语音合成功能

## 贡献指南

欢迎贡献代码、文档或提出建议：

1. Fork 本仓库
2. 创建功能分支
3. 提交更改
4. 创建 Pull Request

## 许可证

本项目基于 MIT 许可证开源。

## 致谢

- 感谢 [faster-whisper](https://github.com/guillaumekln/faster-whisper) 项目
- 感谢 [OpenAI Whisper](https://github.com/openai/whisper) 团队
- 感谢所有贡献者和用户

---

**提示**: 首次使用需要下载模型文件，请确保有足够的磁盘空间（约 1-2GB）和稳定的网络连接。