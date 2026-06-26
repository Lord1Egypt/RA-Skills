---
name: funasr-nano-transcribe
description: |
  使用 Fun-ASR-Nano-2512 轻量级模型进行语音转文字。
  提供快速准确的中文语音识别，识别结果实时输出到控制台，针对 CPU/GPU 环境优化。
  使用场景：(1) 将中文音频文件转写为文字，(2) 需要轻量级低内存占用的 ASR，
  (3) 处理包含领域特定热词的音频（医疗、保险等），
  (4) 需要高准确率的中文转写。

---

# Fun-ASR-Nano-2512 语音转写技能

使用阿里巴巴 Fun-ASR-Nano-2512 轻量级模型将中文音频文件转写为文字。

## 概述

本技能提供基于 FunASR Nano-2512 模型的语音转文字功能：

- **轻量级**：模型大小约 **1.85GB**，内存占用约 2-3GB
- **快速**：针对 CPU 和 GPU 推理优化
- **准确**：中文识别效果优秀，支持热词
- **领域优化**：预配置医疗/保险专业热词

## 环境要求

### 虚拟环境

本技能需 Python 3.12 虚拟环境，位于 `.venv/`。

**激活虚拟环境：**

```bash
source .venv/bin/activate
```

**或使用快捷脚本：**

```bash
source scripts/activate.sh
```

### 手动安装（如无虚拟环境）

```bash
# 创建 Python 3.12 虚拟环境
python3.12 -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install funasr modelscope numpy loguru transformers

# 模型文件位置
models/Fun-ASR-Nano-2512/    # 已提供（约 1.85GB）
```

### 模型管理

本技能需要完整的 Fun-ASR-Nano-2512 模型（约 1.85GB），支持**完全离线使用**。

#### 模型信息

| 属性       | 说明                          |
| -------- | --------------------------- |
| **模型名称** | Fun-ASR-Nano-2512           |
| **模型大小** | ~1.85GB                     |
| **存储位置** | `models/Fun-ASR-Nano-2512/` |
| **加载方式** | 本地加载（无需网络）                  |
| **内存需求** | CPU: ~2-3GB / GPU: ~2GB 显存  |
| **加载时间** | 首次约 30-40 秒                 |

如果从 `models/Fun-ASR-Nano-2512/` 加载模型时发现模型缺失，通过以下方式获取。 

#### 模型获取

**从 ModelScope 下载**

```bash
# 推荐使用下载脚本
python scripts/download_model.py --modelscope -o models

# 或使用 ModelScope CLI 下载
modelscope download --model FunAudioLLM/Fun-ASR-Nano-2512
```

#### 模型复制工具

技能提供 `download_model.py` 脚本用于模型管理：

```bash
# 检查模型是否完整
python scripts/download_model.py --check

# 查看模型信息（大小、文件列表）
python scripts/download_model.py --info

# 复制模型到指定目录（自动创建 Fun-ASR-Nano-2512 子目录）
python scripts/download_model.py --copy -o models
# 结果: models/Fun-ASR-Nano-2512/

# 从其他位置复制模型
python scripts/download_model.py --copy --source /path/to/source -o /path/to/parent_dir

# 清理模型目录中的临时文件夹
python scripts/download_model.py --cleanup
```

#### 离线使用

本技能支持**完全离线使用**：

- ✅ 模型文件本地加载（约 1.85GB）离线使用
- ✅ 无需 ModelScope 或 HuggingFace 账户
- ✅ 可在无网络环境下运行

#### 模型加载代码

```python
from funasr import AutoModel

# 本地加载模型
model = AutoModel(
    model="models/Fun-ASR-Nano-2512",  # 本地路径
    trust_remote_code=True,
    remote_code="./FunASRNano.py",
    device="cpu",  # 或 "cuda:0"
    disable_update=True,  # 禁用自动更新
)
```

#### 常见问题

**Q: 首次启动服务很慢？**
A: 首次加载 1.85GB 模型需要 30-40 秒，属于正常情况。后续使用 FastAPI 服务可避免重复加载。

**Q: 能否与其他语言识别技能共存？**
A: 技能专注于中文轻量级识别与领域热词优化场景，可与处理英文或多模态的 ASR 技能通过语义场景路由机制共存。

## 文件结构

```
funasr-nano-transcribe/
├── .venv/                          # Python 3.12 虚拟环境
├── scripts/
│   ├── activate.sh                 # 激活虚拟环境脚本
│   ├── verify_env.sh               # 环境验证脚本
│   ├── api_server.py               # FastAPI 服务（端口 11890）⭐
│   ├── api_client.py               # API 客户端 ⭐
│   ├── download_model.py           # 模型下载/复制工具 ⭐
│   ├── FunAsrTranscriber.py       # 转录主类
│   ├── FunASRNano.py              # 官方模型实现
│   ├── transcribe.py              # 单文件 CLI
│   └── batch_transcribe.py        # 批量处理脚本
├── models/
│   └── Fun-ASR-Nano-2512/         # 模型文件（约 1.85GB）
├── temp/                           # 临时目录（可存放测试模型）
├── start_server.sh                 # 启动 API 服务 ⭐
├── stop_server.sh                  # 停止 API 服务 ⭐
├── references/                     # 参考文档
│   ├── model_info.md              # 模型信息
│   └── persistent_usage.md        # 持久化使用指南
├── QUICKSTART.md                   # 快速开始指南
└── SKILL.md                        # 本文件
```

## 快速开始

技能提供两种使用方式：**FastAPI 服务**（模型只加载一次，适合高频使用）和 **CLI 脚本**（即开即用，适合偶尔使用）。

> ⚠️ **智能使用原则（让语音识别无感）**：
> 
> **自动识别模式：**
> - 如果只收到语音文件，**没有任何文字说明** → 直接识别语音内容，根据识别结果**自然回应**（不添加"识别结果"等标记）
> - 如果对话中**已转写过语音**（第2次及以后）→ **自动启动 FastAPI 服务**，后续语音秒级响应
> 
> **显式请求模式：**
> - 用户明确要求"识别语音"、"转写语音"等 → 可展示识别过程
> - 用户要求"启动语音识别服务" → 启动服务并告知状态
> 
> **回应风格原则：**
> - **未要求识别时**：直接根据语音内容回应，就像收到文字消息一样自然
> - **要求识别时**：可展示"识别结果：xxx"等标记性内容
> - **目标：让语音交互像文字一样自然，无需每次询问，不暴露技术细节。**

### 使用场景示例

| 场景 | 用户输入 | 处理方式 | 回应示例 |
|------|---------|---------|---------|
| **纯语音** | [仅发送语音文件] | 自动识别 → 自然回应 | 语音说"几点了" → 直接回答时间，不加"你说的是" |
| **第2条语音** | 第2次发语音 | 自动启动 API 服务 → 秒级识别 | 同上，自然回应 |
| **明确请求** | "帮我识别这段语音" | 启动 API 服务 → 展示识别结果 | "识别结果：xxx" |
| **带文字的首条** | "听一下这个" + 语音 | 询问后决定 | 根据用户选择 |

**回应风格对比：**

❌ **避免（未要求识别时）：**
> 语音转写完成！你刚才说的是："告诉我几点了？"  
> 现在时间是...

✅ **推荐（自然回应）：**
> 现在时间是 **08:47**，周六早上。

**原则：用户没要求看识别结果时，直接像回复文字消息一样回应语音的实际内容。**

### 方式一：FastAPI 服务（高频/多文件场景）

**适用场景：** 
- 用户第2次及以上发送语音
- 需要连续转写多个音频文件
- 用户明确要求语音识别/转写

**自动启动时机（无需询问）：**

- ✅ 仅收到语音文件，无文字说明 → 识别后直接回应内容
- ✅ 对话中已有语音转写历史 → 自动启动服务
- ✅ 用户明确要求识别/转写语音 → 默认使用API服务
- ❌ 首次单个语音 + 有明确文字指令 → 询问后决定

**1. 启动服务**

```bash
cd {baseDir}
./start_server.sh
```

服务启动后访问 http://localhost:11890/docs 查看 API 文档。

**特点：**

- 服务启动模型只加载一次，后续免模型加载时间
- 端口默认为 **11890**

⚠️ **注意**：服务启动后会持续占用内存（约 2-3GB），**启动后应提醒用户不使用服务时记得告知我予以关闭**，以释放系统资源：

```bash
./stop_server.sh
```

**2. 使用客户端转写（自动检查服务可用性）**

```bash
# 转写单个文件（结果输出到控制台）
python scripts/api_client.py /path/to/audio.wav

# 如服务未运行，自动启动并转写
python scripts/api_client.py /path/to/audio.wav --start-server

# 检查服务健康状态
python scripts/api_client.py --health
```

**客户端特点：**

- 识别结果**立即同步输出到控制台**，方便即时查看

**3. 停止服务**

当用户明确发出"停止音频转写服务"或"停止音频识别服务"指令时：

```bash
./stop_server.sh
```

**4. API 端点**（端口 11890）

| 端点                 | 方法   | 说明        |
| ------------------ | ---- | --------- |
| `/`                | GET  | 服务状态      |
| `/health`          | GET  | 健康检查      |
| `/transcribe`      | POST | 上传音频文件转写  |
| `/transcribe/path` | POST | 转写服务器本地文件 |
| `/stats`           | GET  | 服务统计信息    |

**5. 使用 cURL 调用**

```bash
# 上传音频转写
curl -X POST "http://localhost:11890/transcribe" \
  -H "accept: application/json" \
  -F "audio=@/path/to/audio.wav" \
  | jq '.text'

# 转写服务器本地文件
curl -X POST "http://localhost:11890/transcribe/path?file_path=/path/to/audio.wav"

# 检查服务状态
curl http://localhost:11890/health
```

**6. Python 调用示例**

```python
import requests

# 上传音频
with open('audio.wav', 'rb') as f:
    files = {'audio': f}
    response = requests.post('http://localhost:11890/transcribe', files=files)

result = response.json()
if result['success']:
    print(result['text'])
```

**安全说明：**

- 服务默认只监听 **127.0.0.1**（本地地址），不对外暴露
- 如需远程访问，请配置反向代理（如 Nginx）并设置访问控制

### 方式二：命令行转写（适合单次/偶尔使用）

**适用场景：** 首次转写单个或少量音频文件，不需要持续使用语音识别功能。

如果不需要高频调用，可以使用 CLI 脚本：

```bash
cd {baseDir}
source .venv/bin/activate

# 单文件转写
python scripts/transcribe.py /path/to/audio.wav

# 批量转写
python scripts/batch_transcribe.py /path/to/audio_directory/
```

## 脚本说明

### `scripts/transcribe.py` - 单文件转写

转写单个音频文件。

**使用方法：**

```bash
scripts/transcribe.py <音频文件> [选项]

选项：
  -o, --output <文件>     输出文本文件（默认：<输入>.txt）
  -d, --device <设备>     设备：cpu, cuda:0（默认：cpu）
```

**示例：**

```bash
# 基础转写（CPU）
scripts/transcribe.py meeting.wav

# 使用 GPU（cuda:0）
scripts/transcribe.py meeting.wav --device cuda:0

# 自定义输出
scripts/transcribe.py meeting.wav -o transcript.txt
```

### `scripts/batch_transcribe.py` - 批量转写

批量处理多个音频文件。

**使用方法：**

```bash
scripts/batch_transcribe.py <目录> [选项]

选项：
  -o, --output <目录>     输出目录（默认：transcripts/）
  -d, --device <设备>     设备：cpu, cuda:0（默认：cpu）
  -j, --jobs <数量>       并行任务数（默认：1）
```

**示例：**

```bash
# 处理目录中所有音频文件
scripts/batch_transcribe.py ./audio_files/

# 使用 GPU（cuda:0）并并行处理
scripts/batch_transcribe.py ./recordings/ --device cuda:0 -j 4
```

## 配置

### 设备选择

编辑 `scripts/FunAsrTranscriber.py` 更改默认设备：

```python
self.model = AutoModel(
    model="../models/Fun-ASR-Nano-2512",
    trust_remote_code=True,
    remote_code="./FunASRNano.py",
    device="cpu",  # 改为 "cuda:0" 使用 GPU
    disable_update=True,
)
```

### 自定义热词

编辑 `FunAsrTranscriber.py` 中的 `HOT_WORDS` 列表：

```python
HOT_WORDS = [
    "你的热词1",
    "你的热词2",
    # ...
]
```

### 热词（领域专用）

预配置热词以提高识别准确率：

- 吴晓阳（人名）
- 统账结合、单建统筹（社保术语）
- 个账、异地、门特（医疗术语）
- 大爱无疆、共济账户、家庭共济（保险术语）
- 零星报销

### 支持的音频格式

- WAV（推荐，16kHz 单声道）
- MP3
- M4A/AAC
- 原始 PCM（自动转换）

## 性能

### CPU 模式（4 核心）

- 设备参数：`--device cpu`
- 内存：~2-3GB（模型 1.85GB + 运行时）
- 速度：2-3 倍实时
- 推荐场景：功能验证

### GPU 模式（CUDA）

- 设备参数：`--device cuda:0`
- 内存：~2GB 显存（模型 1.85GB + 运行时）
- 速度：5-10 倍实时
- 推荐场景：实时应用

## 故障排除

### 模型未找到

```
错误：在 models/Fun-ASR-Nano-2512 未找到模型
```

**解决方案**：确保模型文件存在于 `{baseDir}/models/Fun-ASR-Nano-2512/`

### CUDA 内存不足

```
RuntimeError: CUDA out of memory
```

**解决方案**：使用 CPU 模式 `--device cpu`

### 音频格式问题

```
错误：无法解码音频
```

**解决方案**：先转换为 WAV 16kHz 单声道格式

### 缺少依赖

```
ModuleNotFoundError: No module named 'transformers'
```

**解决方案**：`pip install transformers`

## 高级用法

### FastAPI 服务详细说明

服务默认在本地 **11890** 端口，提供 HTTP API 接口。

**服务管理命令：**

```bash
# 启动服务
./start_server.sh

# 停止服务（用户明确指令后执行）
./stop_server.sh

# 查看服务状态
curl http://localhost:11890/health
```

**特点：**

- 服务启动后持久化运行，根据用户指令关闭
- 模型只在启动时加载一次（节省 3-5 秒）
- 支持并发转写请求
- 自动清理临时文件

### 持久化转录器

高效处理多个文件：

```python
import sys
sys.path.insert(0, '{baseDir}/scripts')
from FunAsrTranscriber import AsrTranscriber

# 只加载一次模型
transcriber = AsrTranscriber()

# 处理多个文件
files = ['audio1.wav', 'audio2.wav', 'audio3.wav']
for f in files:
    text = transcriber.transcribe_sync(f)
    print(f"{f}: {text}")
```

### 异步处理

```python
import asyncio
import sys
sys.path.insert(0, '{baseDir}/scripts')
from FunAsrTranscriber import AsrTranscriber, speech_to_text_local

transcriber = AsrTranscriber()
audio_files = []  # 跟踪临时文件

# 读取音频字节
with open('audio.wav', 'rb') as f:
    audio_data = f.read()

# 异步处理
text = asyncio.run(speech_to_text_local(transcriber, audio_data, audio_files))
print(text)
```

## 参考链接

- [FunASR GitHub](https://github.com/alibaba-damo-academy/FunASR)
- [模型详细信息](references/model_info.md) - 包含模型规格、性能指标、对比等
- [持久化使用指南](references/persistent_usage.md) - Python API 使用示例
- [快速开始](QUICKSTART.md) - 快速上手指南
