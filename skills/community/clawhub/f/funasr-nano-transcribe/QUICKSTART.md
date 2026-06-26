# Fun-ASR-Nano-2512 快速开始指南

## ✅ 环境状态

| 组件         | 状态  | 版本/路径                                |
| ---------- | --- | ------------------------------------ |
| Python     | ✅   | 3.12.3                               |
| 虚拟环境       | ✅   | .venv/                               |
| PyTorch    | ✅   | 2.10.0+                              |
| FunASR     | ✅   | 1.3.1                                |
| ModelScope | ✅   | 1.34.0                               |
| 模型文件       | ✅   | models/Fun-ASR-Nano-2512/ (23 files) |

## 🚀 快速使用（两种方式）

技能提供 **FastAPI 服务** 和 **CLI 脚本** 两种使用方式。

> ⚠️ **FastAPI服务启动原则**：
> 
> 1. 用户**明确要求**启动服务（如"启动语音识别服务"）
> 2. 对话**上下文中有语音转录的历史需求**（如之前已转写过音频文件），**询问**是否启动 FastAPI 服务。
> 
> 如不满足上述条件，优先使用 CLI 单文件脚本（`transcribe.py`）进行一次性转写，无需询问。

---

## 方式一：FastAPI 服务（适合高频使用场景）

**适用场景：** 需要连续转写多个音频文件、或需要频繁调用语音识别功能时。

### 1. 启动服务（模型只加载一次）

```bash
cd ~/.openclaw/workspace/skills/funasr-nano-transcribe
./start_server.sh
```

服务启动后：

- API 文档：http://localhost:11890/docs
- 服务地址：http://localhost:11890

⚠️ **重要提醒**：服务启动后根据用户指令进行关闭，不关闭则一直保持运行并占用内存（约 2-3GB）。**记得提醒用户在不使用时关闭服务**，以及时释放系统资源：

```bash
./stop_server.sh
```

### 2. 转写音频（自动检查服务可用性）

```bash
# 转写单个文件（识别结果实时输出到控制台）
python scripts/api_client.py /path/to/audio.wav

# 如服务未运行，自动启动并转写
python scripts/api_client.py /path/to/audio.wav --start-server

# 检查服务健康状态
python scripts/api_client.py --health
```

**客户端行为说明：**

- 识别结果**实时输出到控制台**，方便即时查看

### 3. 停止服务（用户明确指令后执行）

```bash
./stop_server.sh
```

### 4. 使用 cURL 直接调用

```bash
curl -X POST "http://localhost:11890/transcribe" \
  -F "audio=@/path/to/audio.wav" \
  | jq '.text'
```

**安全说明：** 服务默认只监听本地地址（127.0.0.1），不对外暴露。

---

## 方式二：CLI 脚本（适合单次/偶尔使用）

**适用场景：** 仅需转写单个或少量音频文件，不需要持续使用语音识别功能。

**使用方法（直接使用，无需询问）：**

```bash
# 激活虚拟环境
source scripts/activate.sh

# 转写单个文件
python scripts/transcribe.py /path/to/audio.wav

# 批量转写目录
python scripts/batch_transcribe.py /path/to/audio_directory/
```

**特点：**

- 即开即用，无需启动服务
- 每次转写需要重新加载模型（约 3-5 秒）
- 适合偶尔使用，不占用常驻内存

---

## 📁 文件结构

```
funasr-nano-transcribe/
├── .venv/                      # Python 3.12 虚拟环境
├── models/
│   └── Fun-ASR-Nano-2512/      # 模型文件
├── scripts/
│   ├── activate.sh             # 激活虚拟环境
│   ├── verify_env.sh           # 环境验证
│   ├── api_server.py           # FastAPI 服务（端口 11890）⭐
│   ├── api_client.py           # API 客户端 ⭐
│   ├── FunASRNano.py           # 官方模型实现
│   ├── FunAsrTranscriber.py    # 转录主类
│   ├── transcribe.py           # 单文件 CLI
│   └── batch_transcribe.py     # 批量 CLI
├── start_server.sh             # 启动 API 服务 ⭐
├── stop_server.sh              # 停止 API 服务 ⭐
├── references/                 # 文档
├── requirements.txt            # 依赖列表
└── SKILL.md                    # 技能文档
```

## 🔧 可用脚本

| 脚本                            | 用途                  |
| ----------------------------- | ------------------- |
| `start_server.sh`             | 启动 API 服务（端口 11890） |
| `stop_server.sh`              | 停止 API 服务           |
| `scripts/api_client.py`       | 调用 API 服务（自动检查可用性）  |
| `scripts/download_model.py`   | 模型下载/复制/检查工具        |
| `scripts/transcribe.py`       | 单文件转写（CLI 模式）       |
| `scripts/batch_transcribe.py` | 批量转写（CLI 模式）        |

## 📦 模型管理

本技能需要完整的 Fun-ASR-Nano-2512 模型（约 1.85GB），支持**完全离线使用**。如果从 `models/Fun-ASR-Nano-2512/` 加载模型发现模型缺失，通过以下方式获取。

### 模型获取

**从 ModelScope 下载**

```bash
# 推荐使用下载脚本直接下载至技能所在的目录中
python scripts/download_model.py --modelscope -o models

# 或使用 ModelScope CLI 下载后再复制或移动至技能所在的目录中
modelscope download --model FunAudioLLM/Fun-ASR-Nano-2512
```

### 模型复制工具

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

### 模型加载说明

- **首次启动**：加载 1.85GB 模型需要 30-40 秒，属于正常情况
- **内存需求**：CPU 模式约 2-3GB RAM，GPU 模式约 2GB 显存
- **离线使用**：模型文件如果本地包含，则无需网络连接即可使用

## ⚡ 两种使用方式对比

| 方式                 | 适用场景         | 模型加载       | 速度  |
| ------------------ | ------------ | ---------- | --- |
| **FastAPI 服务（默认）** | 高频调用、批量处理    | 启动时加载一次    | ⭐ 快 |
| CLI 脚本             | 偶尔转写 1-2 个文件 | 每次加载（约30秒） | 慢   |

## 🐛 故障排除

### 服务无法启动

```bash
# 检查端口是否被占用
lsof -i:11890

# 查看服务日志
tail -f /tmp/funasr_api.log
```

### 服务未运行

```bash
# 检查服务状态
curl http://localhost:11890/health

# 重新启动服务
./stop_server.sh
./start_server.sh
```

### 依赖缺失

```bash
source scripts/activate.sh
pip install -r requirements.txt
```

## 💡 使用提示

- **默认端口**：11890
- **服务模式**：服务启动后持久化运行，不会自动关闭
- **自动检查**：客户端会自动检查服务可用性
- **设备设置**：当前默认为 `cpu`
- **首次加载**：启动服务时加载 1.85GB 模型需要 30-40 秒
- **离线使用**：模型文件已本地包含，无需网络连接
- **内存需求**：CPU 模式约 2-3GB RAM
