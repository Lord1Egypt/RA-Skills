---
name: deepsop-synth-clone
description: |
  声音复刻技能，使用 AI Artist API 进行音色克隆和语音合成。支持查询已有音色、上传音频创建新音色、使用指定音色合成语音。

  ⚠️ 使用前必须设置环境变量 AI_ARTIST_TOKEN 为你的 API Key！需要 API Key 授权。

  触发场景：
  - 用户要求生成语音，如"用蔡总的音色说..."、"生成一段语音"、"语音合成"等。
  - 用户要求克隆音色，如"上传音频创建音色"、"复刻这个声音"、"创建我的音色"等。
  - 用户查询已有音色，如"有哪些音色"、"列出音色"、"查看音色列表"等。
  - 用户指定音色名称或 ID 进行语音合成。
  - 用户发送语音消息后要求用该声音合成其他内容。
---

# Voice Clone - 声音复刻技能

使用 AI Artist API 进行音色克隆和语音合成的完整解决方案。基于 CosyVoice v3.5 Plus 模型，支持高质量的音色复刻和文本转语音。

## 🎯 技能概述

本技能提供三大核心功能：

| 功能 | 说明 | 典型场景 |
|------|------|----------|
| **查询音色** | 列出系统中所有可用音色 | 查看已有音色库，选择合适的声音 |
| **音色克隆** | 上传音频创建新的音色 | 复刻自己的声音、领导的声音、明星声音等 |
| **语音合成** | 使用指定音色生成语音 | 用特定声音朗读文本、生成配音、制作语音消息 |

## ⚠️ 首次使用必读

### 1. 获取 API Key

本技能需要 **API Key 授权**才能调用 AI Artist API：

- **已有账号** → 前往 [https://ai.deepsop.com/login?source=4](https://ai.deepsop.com/login?source=4) 登录获取
- **没有账号** → 前往 [https://ai.deepsop.com/register?source=4](https://ai.deepsop.com/register?source=4) 注册后获取

登录后在复制您的 API Key（`sk-` 开头）。

### 2. 设置环境变量

**在使用前，你必须先设置自己的 API Key：**

```bash
# Windows PowerShell
$env:AI_ARTIST_TOKEN="sk-your_api_key_here"

# Linux/macOS/Git Bash (Windows)
export AI_ARTIST_TOKEN="sk-your_api_key_here"
```

### 3. 验证配置

```bash
python scripts/voice_clone.py --list
```

如果看到音色列表，说明配置成功！

## 🚀 快速开始

### 基础用法

```bash
# 1. 列出所有可用音色
python scripts/voice_clone.py --list

# 2. 使用音色 ID 合成语音
python scripts/voice_clone.py --synthesize --id 10 --text "大家好，我是测试语音"

# 3. 使用音色名称合成语音
python scripts/voice_clone.py --synthesize --name "蔡总的音色" --text "你好世界"

# 4. 下载合成的音频到本地
python scripts/voice_clone.py --synthesize --id 10 --text "你好" --download
```

### 创建新音色

```bash
# 使用本地音频文件创建音色
python scripts/voice_clone.py --create --name "我的音色" --audio "./my_voice.mp3"

# 使用在线音频 URL 创建音色
python scripts/voice_clone.py --create --name "我的音色" --audio-url "https://example.com/voice.mp3"

# 指定音色前缀
python scripts/voice_clone.py --create --name "客服音色" --audio "./cs.mp3" --prefix "CustomerService"
```

## 📋 详细使用指南

### 一、查询可用音色

列出系统中所有音色及其状态：

```bash
python scripts/voice_clone.py --list
```

**输出示例：**
```
[INFO] 共有 4 个音色

可用音色列表:
  [13] 王俏的音色 [OK] - cosyvoice-v3.5-plus
  [12] 测试 11 [OK] - cosyvoice-v3.5-plus
  [10] 蔡总的音色 [OK] - cosyvoice-v3.5-plus
  [4] 测试音色 [OK] - cosyvoice-v3.5-plus
```

**状态说明：**
| 状态 | 说明 | 是否可用 |
|------|------|----------|
| `OK` | 音色已就绪 | ✅ 可用 |
| `DEPLOYING` | 音色部署中 | ❌ 暂不可用 |
| 其他 | 音色异常 | ❌ 不可用 |

### 二、语音合成

#### 方式 1：使用音色 ID

```bash
python scripts/voice_clone.py --synthesize --id 13 --text "真正重要的东西，用眼睛是看不见的，只有用心才能看清。"
```

#### 方式 2：使用音色名称

```bash
python scripts/voice_clone.py --synthesize --name "王俏的音色" --text "你好，欢迎使用库阔 AI"
```

#### 方式 3：合成并下载

```bash
# 下载到默认目录 (~/.openclaw/workspace/audio/)
python scripts/voice_clone.py --synthesize --id 13 --text "测试语音" --download

# 下载到指定目录
python scripts/voice_clone.py --synthesize --id 13 --text "测试语音" --download --output-dir "./my_audio"
```

### 三、创建新音色

#### 从本地音频文件创建

```bash
# 支持 MP3、WAV 等常见格式
python scripts/voice_clone.py --create --name "我的声音" --audio "./my_voice.mp3"

# 使用完整路径
python scripts/voice_clone.py --create --name "领导音色" --audio "C:\Users\admin\Downloads\leader_voice.wav"
```

#### 从在线 URL 创建

```bash
python scripts/voice_clone.py --create --name "网络音色" --audio-url "https://example.com/voice.mp3"
```

#### 指定音色前缀

```bash
python scripts/voice_clone.py --create --name "客服小王" --audio "./wang.mp3" --prefix "CustomerService"
```

## 🎙️ 音色克隆最佳实践

### 音频素材要求

| 要求 | 说明 |
|------|------|
| **格式** | MP3、WAV、M4A 等常见音频格式 |
| **时长** | 10-60 秒（推荐 30 秒左右） |
| **音质** | 清晰的人声，无明显背景噪音 |
| **内容** | 纯人声朗读，无背景音乐 |
| **采样率** | 16kHz 或以上 |

### 录制建议

1. **环境安静** - 选择安静的房间，关闭空调、风扇等噪音源
2. **距离适中** - 麦克风距离嘴巴 10-15 厘米
3. **语速均匀** - 用正常语速朗读，不要过快或过慢
4. **情感自然** - 用自然的情感朗读，不要过于夸张
5. **内容多样** - 包含不同的音调、韵律，有助于模型学习

### 推荐的录音文本

```
你好，我是 XXX。这是一段用于音色克隆的录音样本。
我希望用我的声音来生成各种语音内容，包括问候语、通知、
故事朗读等。请确保录音清晰，语速适中，情感自然。
谢谢你的配合。
```

## 📊 参数说明

### 全局参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--list` | 三选一 | 列出所有可用音色 |
| `--synthesize` | 三选一 | 语音合成模式 |
| `--create` | 三选一 | 创建新音色模式 |

### 合成模式参数

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `--id` | 与 --name 二选一 | 音色 ID | `--id 13` |
| `--name` | 与 --id 二选一 | 音色名称 | `--name "王俏的音色"` |
| `--text` | ✅ | 要合成的文本 | `--text "你好世界"` |
| `--download` | 否 | 下载音频到本地 | `--download` |
| `--output-dir` | 否 | 音频保存目录 | `--output-dir "./audio"` |

### 创建音色参数

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `--name` | ✅ | 音色名称 | `--name "我的音色"` |
| `--audio` | 与 --audio-url 二选一 | 本地音频路径 | `--audio "./voice.mp3"` |
| `--audio-url` | 与 --audio 二选一 | 在线音频 URL | `--audio-url "https://..."` |
| `--prefix` | 否 | 音色前缀 | `--prefix "DeepSop"` |

## 🔧 环境配置

### 方式 1：临时设置（当前终端有效）

```bash
# Windows PowerShell
$env:AI_ARTIST_TOKEN="sk-5c6c262755dc43d59ec5a742a7e80202"

# Linux/macOS
export AI_ARTIST_TOKEN="sk-5c6c262755dc43d59ec5a742a7e80202"
```

### 方式 2：永久设置（推荐）

创建 `.env` 文件（在脚本同目录或技能根目录）：

```bash
AI_ARTIST_TOKEN=sk-your_api_key_here
```

### 方式 3：系统环境变量

**Windows:**
```powershell
[System.Environment]::SetEnvironmentVariable('AI_ARTIST_TOKEN', 'sk-your_api_key_here', 'User')
```

**Linux/macOS:**
```bash
echo 'export AI_ARTIST_TOKEN="sk-your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

## 💡 实用场景示例

### 场景 1：用特定音色发送语音消息

```bash
# 用蔡总的音色发送通知
python scripts/voice_clone.py --synthesize --name "蔡总的音色" \
  --text "各位同事，下午三点在会议室召开周会，请准时参加。" --download
```

### 场景 2：批量生成语音

```bash
# 生成多个语音片段
python scripts/voice_clone.py --synthesize --id 13 --text "第一章：开始" --download --output-dir "./audiobook/ch1"
python scripts/voice_clone.py --synthesize --id 13 --text "第二章：发展" --download --output-dir "./audiobook/ch2"
python scripts/voice_clone.py --synthesize --id 13 --text "第三章：高潮" --download --output-dir "./audiobook/ch3"
```

### 场景 3：创建多人音色库

```bash
# 为团队创建音色库
python scripts/voice_clone.py --create --name "客服小王" --audio "./wang.mp3"
python scripts/voice_clone.py --create --name "客服小李" --audio "./li.mp3"
python scripts/voice_clone.py --create --name "客服小张" --audio "./zhang.mp3"

# 查看音色列表
python scripts/voice_clone.py --list
```

### 场景 4：语音消息回复

```bash
# 收到语音后，用相同音色回复
# 1. 从语音消息提取音频
# 2. 创建音色（如果不存在）
python scripts/voice_clone.py --create --name "用户音色" --audio "./user_voice.wav"
# 3. 用该音色合成回复
python scripts/voice_clone.py --synthesize --name "用户音色" --text "收到，我会尽快处理。" --download
```

## ⚠️ 注意事项

### 必须遵守

1. **API Key 安全**
   - 不要将 API Key 提交到代码仓库
   - 使用 `.env` 文件时加入 `.gitignore`
   - 定期更换 API Key

2. **音色状态检查**
   - 只有 `status: "OK"` 的音色可用于语音合成
   - `DEPLOYING` 状态的音色需要等待部署完成

3. **音频格式要求**
   - 上传的音频建议为 MP3 或 WAV 格式
   - 时长 10-60 秒效果最佳
   - 确保音频清晰，无明显噪音

4. **文本长度限制**
   - 合成文本建议控制在 500 字以内
   - 过长文本可能失败或效果不佳

### 性能优化

| 优化项 | 建议 |
|--------|------|
| 音频素材 | 使用 30 秒左右的清晰录音 |
| 文本长度 | 单次合成不超过 200 字 |
| 并发请求 | 避免同时发起多个合成请求 |
| 错误处理 | 检查返回状态码，失败时重试 |

## 🔍 故障排查

### 问题 1：提示 "未配置 API_ARTIST_TOKEN"

**原因：** 环境变量未设置

**解决：**
```bash
# Windows PowerShell
$env:AI_ARTIST_TOKEN="sk-your_api_key_here"

# 或创建 .env 文件
echo "AI_ARTIST_TOKEN=sk-your_api_key_here" > .env
```

### 问题 2：音色状态为 DEPLOYING

**原因：** 音色正在部署中

**解决：** 等待几分钟后重新查询状态
```bash
python scripts/voice_clone.py --list
```

### 问题 3：语音合成失败

**可能原因：**
- 音色状态不是 OK
- 文本过长
- 网络问题

**解决：**
1. 检查音色状态：`python scripts/voice_clone.py --list`
2. 缩短文本长度
3. 检查网络连接

### 问题 4：文件上传失败

**可能原因：**
- 文件路径不正确
- 文件格式不支持
- 文件过大

**解决：**
1. 确认文件路径正确（使用绝对路径）
2. 转换为 MP3 或 WAV 格式
3. 确保文件大小合理（< 10MB）

## 📁 相关文件

| 文件 | 说明 |
|------|------|
| `scripts/voice_clone.py` | 主脚本，包含所有功能实现 |
| `references/api.md` | API 详细文档，包含接口说明 |
| `.env` | 环境配置文件（需自行创建） |

## 📚 API 接口速查

| 接口 | 方法 | 说明 |
|------|------|------|
| `/ai/voice/clone/list` | GET | 查询音色列表 |
| `/ai/voice/clone/sync/create` | POST | 创建新音色 |
| `/ai/voice/clone/synthesize` | POST | 语音合成 |
| `/system/fileUpload/upload` | POST | 文件上传 |

详细 API 文档请查看 `references/api.md`

## 🎯 后续扩展

本技能支持以下扩展场景：

- **批量合成** - 循环调用合成接口生成多个语音文件
- **音色管理** - 添加删除、重命名音色的功能
- **音频处理** - 集成音频剪辑、合并功能
- **Web 界面** - 构建图形化操作界面
- **API 服务** - 封装为 REST API 供其他系统调用

---

_如有问题或建议，请联系技能维护者。_
