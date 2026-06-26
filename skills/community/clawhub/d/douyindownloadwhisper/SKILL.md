
## 一、技能基础信息


name: douyin-download-whisper
description: 抖音无水印视频下载和文案提取工具，适配Windows系统，支持无水印视频解析下载、语音文案提取（锁定Whisper base模型）及文案语义分段。
metadata:
  openclaw:
    emoji: 🎵
    requires:
      bins: [ffmpeg, whisper]
    config:
      whisper_model: base  # 锁定Whisper base模型，确保转写效率与兼容性，适配Windows本地运行



## 二、技能介绍

douyin-download 是一款适配 Windows 系统的抖音辅助工具，核心功能为无水印视频下载、视频文案提取（含语音转文字）及文案语义分段，依托本地 Whisper 实现语音转写，调用 OpenClaw 内置 LLM 完成语义分段，操作简单、可直接通过命令行调用。

## 三、核心功能

- 🎬 获取无水印视频下载链接：解析抖音分享链接，提取无水印视频源地址

- 📥 下载抖音视频：将解析后的无水印视频直接下载至指定目录

- 🎙️ 语音文案提取：通过本地 Whisper 工具，将视频中的语音内容转写为文字文案

- ✂️ 文案语义分段：自动调用 OpenClaw 内置 LLM，对提取的文案进行自然语义分段，提升可读性

## 四、环境依赖（Windows 系统必配）
- **Windows 安装（推荐使用阿里云镜像）**
  ```powershell
  pip install -i https://mirrors.aliyun.com/pypi/simple/ --upgrade openai-whisper
  ```

该技能依赖以下工具，需提前安装并配置，否则无法正常运行：

1. **ffmpeg**：用于视频解析与处理，需安装后添加至 Windows 系统环境变量 PATH（安装后可在命令行输入 `ffmpeg -version` 验证是否配置成功）。

2. **whisper**：用于语音转文字，通过 Python 命令安装，安装命令：`pip install -U openai-whisper`，安装后可在命令行输入 `whisper --version` 验证是否可正常调用。

3. **Node.js**：需提前安装 Node.js 环境，确保 `node` 命令可在命令行正常使用（用于执行 JS 脚本）。

## 五、环境变量

（此技能无需配置额外环境变量，仅需确保上述依赖工具正常安装并配置完成即可）

## 六、使用方法（Windows 命令行专用）

所有命令均需在 Windows 命令提示符（CMD）或 PowerShell 中执行，复制命令后替换「抖音分享链接」为实际链接即可使用，路径可根据需求自行修改。

### 6.1 获取视频信息

功能：解析抖音链接，获取无水印视频地址、视频标题等基础信息。

```bash
node "%USERPROFILE%.openclawworkspaceskillsdouyin-downloaddouyin.js" info "抖音分享链接"
```

### 6.2 下载视频

功能：将无水印视频下载至指定目录，默认下载至 C:Tempdouyin-download，可通过 -o 参数修改下载路径。

```bash
node "%USERPROFILE%.openclawworkspaceskillsdouyin-downloaddouyin.js" download "抖音链接" -o C:Tempdouyin-download
```

说明：若指定的下载目录不存在，工具会自动创建该目录。

### 6.3 提取文案（自动语义分段）

功能：下载视频并提取语音文案，自动进行语义分段，生成可读性强的文字内容。

```bash
# 如需使用本地 Whisper，请确保已安装 whisper 可执行文件（安装命令：pip install -U openai-whisper）
node "%USERPROFILE%.openclawworkspaceskillsdouyin-downloaddouyin.js" extract "抖音链接"
```

- 核心逻辑：先下载视频 → 提取视频中的语音 → 通过本地 Whisper（已锁定base模型）转写为文字 → 调用 OpenClaw 内置 LLM 进行自然语义分段，base模型体积小、运行高效，适配Windows本地环境。

- 注意：首次使用 Whisper 时，会自动下载锁定的base模型，体积较小，无需等待过长时间，需保持网络通畅。

### 6.4 跳过语义分段

功能：提取文案但不进行语义分段，直接输出完整的转写文字。

```bash
node "%USERPROFILE%.openclawworkspaceskillsdouyin-downloaddouyin.js" extract "抖音链接" --no-segment
```

## 七、常见问题

- 问题1：执行命令时提示「node 不是内部或外部命令」？
解决：未安装 Node.js 或未将 Node.js 添加至系统环境变量，重新安装 Node.js 并重启命令行。

- 问题2：提取文案时提示「whisper 不是内部或外部命令」？
解决：Whisper 安装未成功或未添加至环境变量，重新执行 `pip install -U openai-whisper`，并检查 Python 的 Scripts 目录是否在系统 PATH 中。

- 问题3：下载视频失败？
解决：检查抖音链接是否有效（需为完整的抖音分享链接），网络是否通畅，目标下载目录是否有写入权限。

## 八、注意事项

1. 本工具仅用于个人学习、研究使用，请勿用于商业用途或下载侵权视频，遵守抖音平台规则。

2. 若抖音平台接口更新，可能导致工具解析失败，需等待技能更新适配。

3. Whisper 转写精度受视频语音清晰度影响，模糊语音可能出现转写误差。


