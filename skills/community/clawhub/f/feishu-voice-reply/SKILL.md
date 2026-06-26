---
name: feishu-voice-reply
description: 飞书语音消息自动回复技能 - 使用 Edge TTS 生成语音并通过飞书 API 发送
metadata:
  tags: feishu, voice, tts, audio, edge-tts
  version: 1.0.1
  author: OpenClaw Community
  license: MIT
---

# 飞书语音回复技能

## 功能

自动将文本转换为飞书原生语音消息并发送，支持波形播放格式。

## 适用场景

- 用户希望收到语音回复时
- 需要更自然的对话体验时
- 想要发送语音通知时

## 核心组件

### 1. Edge TTS 语音生成
- 使用微软 Edge Neural TTS 引擎
- 支持多种声音（xiaoxiao, xiaoyi, yunyang 等）
- 完全免费，无需 API Key
- **安全**：只使用官方 API，不访问外部服务器

### 2. 飞书语音发送
- 使用 OpenClaw 内置消息工具
- 飞书原生语音格式（msg_type: audio）
- 支持私聊和群聊
- 波形播放显示
- **安全**：不依赖未声明的凭据

## 安全特性

### ✅ 已修复的安全问题

1. **不修改全局文件**
   - 所有文件操作都在技能目录内
   - 不修改系统文件或配置

2. **不创建持久规则**
   - 语音回复规则内置在 SKILL.md 中
   - 会话启动时自动读取，无需外部文件

3. **使用公开 API**
   - 使用 OpenClaw 内置 `message` 工具
   - 通过 OpenClaw Gateway 安全发送
   - 不依赖未声明的本地 API 服务

4. **清晰的依赖说明**
   - edge-tts：Python 包，官方 PyPI 源
   - OpenClaw 消息工具：内置功能
   - 无需额外的 API 密钥或服务

## 安装

### 前置要求

```bash
# 安装 Python Edge TTS（使用官方 PyPI）
pip3 install edge-tts

# 或使用国内镜像加速
pip3 install edge-tts -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 安装技能

```bash
# 使用 ClawHub 安装
clawhub install feishu-voice-reply

# 或手动安装
mkdir -p ~/.openclaw/workspace/skills/feishu-voice-reply
# 复制 SKILL.md 和相关文件到该目录
```

## 使用方法

### 方法 1：自动检测（推荐）

当用户消息包含语音相关关键词时，自动触发：

```python
# 触发关键词示例
- "用语音回复"
- "发语音给我"
- "语音说"
- "念给我听"
```

### 方法 2：使用命令行

```bash
# 生成语音
cd /root/.openclaw/workspace/skills/feishu-voice-reply
python3 edge_tts_async.py "你好，世界！" xiaoxiao voice.mp3
```

### 方法 3：通过 OpenClaw 消息工具

使用 OpenClaw 内置的 `message` 工具发送语音：

```python
# OpenClaw 会自动处理飞书 API 调用
message(
    action="send",
    channel="feishu",
    filePath="/path/to/voice.mp3"
)
```

## 支持的声音

| 声音 | 性别 | 特点 | 推荐场景 |
|------|------|------|----------|
| xiaoxiao | 女 | 活泼专业 | ⭐⭐⭐⭐⭐ 通用 |
| xiaoyi | 女 | 温柔亲切 | ⭐⭐⭐⭐ 情感类 |
| yunyang | 男 | 沉稳 | ⭐⭐⭐⭐ 正式 |
| yunxi | 男 | 北京话 | ⭐⭐⭐ 幽默 |
| yunze | 男 | 活力 | ⭐⭐⭐ 年轻 |

## 语音回复规则（内置）

**规则位置**：本文件（SKILL.md）

**核心规则**：
```
语音发送后，绝对不做任何回复操作！
```

**禁止行为**（零容忍）：
1. 语音发送后，不要发送任何文字消息
2. 不要说"已发送语音"、"语音已发送"等
3. 不要说"遵守规则"、"记住了"等
4. 不要加任何表情符号（😄、✅等）
5. 语音发送后，立即彻底停止

**唯一例外**：只有语音生成失败时，才可以用文字说明

## 工作流

```
用户消息 → 触发关键词检测
    ↓
文本内容提取
    ↓
Edge TTS 生成语音（2-5秒）
    ↓
使用 OpenClaw 消息工具发送
    ↓
✅ 完成（绝对静默）
```

## 文件结构

```
skills/feishu-voice-reply/
├── SKILL.md              # 本文件
├── README.md             # 说明文档
├── INSTALL.sh            # 安装脚本
└── edge_tts_async.py     # Edge TTS 异步生成脚本
```

**注意**：
- 所有文件都在技能目录内
- 不修改系统文件或配置
- 不创建外部持久文件

## 性能指标

- **语音生成速度**：3-5 秒（100 字）
- **音频质量**：高（微软 Neural）
- **文件大小**：20-30 KB（每 100 字）
- **成本**：完全免费

## 依赖项

### 必需依赖

- **Python 3.7+**
- **edge-tts**（Python 包，官方 PyPI）
  ```bash
  pip3 install edge-tts
  ```

### 可选依赖

- **OpenClaw 消息工具**
  - OpenClaw 内置功能
  - 用于发送语音消息到飞书

## 故障排查

### 语音生成失败
```bash
# 检查 edge-tts 安装
pip3 show edge-tts

# 测试语音生成
python3 -c "import edge_tts; print('OK')"

# 重新安装
pip3 install edge-tts -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 语音发送失败

**检查 OpenClaw Gateway**：
```bash
# 检查 Gateway 状态
systemctl status openclaw-gateway

# 查看 Gateway 日志
journalctl -u openclaw-gateway -f
```

**检查飞书连接**：
- 确保 OpenClaw 已配置飞书凭据
- 检查飞书机器人权限

## 相关技能

- **feishu-bot** - 飞书 Bot 基础功能
- **feishu-file** - 飞书文件发送
- **edge-tts** - Edge TTS 语音生成

## 更新日志

### v1.0.1 (2026-03-11)
- 🔒 **安全修复**
  - 移除全局文件修改
  - 移除持久规则文件
  - 使用 OpenClaw 内置消息工具
  - 添加安全说明文档
  - 声明所有依赖和 API 使用

### v1.0.0 (2026-03-11)
- 初始版本
- 支持 Edge TTS 语音生成
- 支持飞书语音消息发送
- 添加 5 种中文声音

## 许可证

MIT License

## 贡献

欢迎提交问题和改进建议！
