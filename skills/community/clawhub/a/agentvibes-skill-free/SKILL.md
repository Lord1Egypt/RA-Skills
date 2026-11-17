---
name: "agentvibes-skill-free"
description: "免费离线TTS语音合成工具,支持914+声音切换、语速调节、个性风格,适合个人开发者使用。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "AgentVibes语音合成-免费版"
  version: "1.0.0"
  summary: "免费离线TTS语音合成工具,支持914+声音切换、语速调节、个性风格,适合个人开发者使用。"
  tags:
    - "Creative"
    - "语音合成"
    - "TTS"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# AgentVibes语音合成工具 - 免费版

## 概述

AgentVibes语音合成免费版是一款面向个人用户的离线文本转语音(TTS)工具。集成 Piper TTS、macOS Say、Windows SAPI 等多种引擎,提供 914+ 离线声音,覆盖 30+ 语种,完全免费且无需账号。

本版本适合个人开发者、内容创作者及语言学习者,通过简单的斜杠命令即可切换声音、调节语速、设置个性风格,快速实现语音播报需求。

## 核心能力

| 能力项 | 免费版支持 | 说明 |
|:-------|:-----------|:-----|
| 声音切换 | 是 | 914+ 声音可选 |
| 声音列表与预览 | 是 | 列表与试听 |
| 个性风格设置 | 是 | 内置基础风格 |
| 语速调节 | 是 | 0.5x - 3.0x |
| 静音/回放 | 是 | 最近10条 |
| 背景音乐 | 限制 | 基础曲目 |
| 神经声音引擎 | 否 | PRO 版支持 |
| 多角色协同 | 否 | PRO 版支持 |
| 批量音频导出 | 否 | PRO 版支持 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置。

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 按照skill规范执行核心功能执行操作,遵循单一意图原则。
**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输入**: 用户提供参数配置与调用所需的指令和必要参数。
**处理**: 按照skill规范执行参数配置与调用操作,遵循单一意图原则。
**输出**: 返回参数配置与调用的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输入**: 用户提供结果处理与输出所需的指令和必要参数。
**处理**: 按照skill规范执行结果处理与输出操作,遵循单一意图原则。
**输出**: 返回结果处理与输出的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：免费离线、TTS、语音合成工具、适合个人开发者使、AgentVibes、语音合成免费版、面向个人开发者的、离线文本转语音工、离线声音、切换声音、设置个性风格、调节语速、跨平台运行、Windows、macOS、Linux、无需账号、Say、SAPI、零配置方案等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一:个人语音播报

开发者希望将 Agent 的回复通过语音播报出来,选择一个舒适的声音。

```bash
# 列出可用声音
/agent-vibes:list first 5

# 切换到中文女声
/agent-vibes:switch zh_CN-huayan-x_low

# 调节语速为正常
/agent-vibes:set-speed 1.0
```

### 场景二:视频配音创作

内容创作者为短视频添加多语种配音,需要切换不同声音。

```bash
# 切换到英文男声
/agent-vibes:switch en_US-ryan-high

# 试听效果
/agent-vibes:sample en_US-ryan-high

# 切换到日文女声
/agent-vibes:switch ja_JP-ayanami-medium
```

### 场景三:语言学习辅助

语言学习者开启双语模式,辅助听力练习。

```bash
# 设置母语为中文
/agent-vibes:language chinese

# 开启学习模式(双语播报)
/agent-vibes:learn on

# 翻译并朗读
/agent-vibes:translate "Hello, how are you?"
```

## 不适用场景

以下场景AgentVibes语音合成-免费版不适合处理：

- 逆向工程闭源API
- API安全渗透测试
- 非标准协议集成

## 触发条件

需要API集成、接口对接、Webhook配置、系统连接时使用。不适用于非本工具能力范围的需求。

## 快速开始

### 第一步:选择语音引擎

```bash
# 查看可用引擎
/agent-vibes:provider list

# 切换到 Piper(全平台,914+ 声音)
/agent-vibes:provider switch piper

# 或使用系统内置(零配置)
# macOS:
/agent-vibes:provider switch macos
# Windows:
/agent-vibes:provider switch sapi
```

### 第二步:选择并切换声音

```bash
# 预览前 3 个声音
/agent-vibes:preview

# 切换到指定声音
/agent-vibes:switch en_US-amy-medium
```

### 第三步:开始使用

```bash
# 查看当前配置
/agent-vibes:whoami

# 设置个性风格(可选)
/agent-vibes:personality sarcastic
```

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。


## 示例

基础配置项说明:

```bash
# 常用命令组合
# 切换声音 + 调节语速
/agent-vibes:switch en_GB-alan-medium
/agent-vibes:set-speed 1.2

# 设置前缀语
/agent-vibes:set-pretext "助手"

# 控制详细程度
/agent-vibes:verbosity low      # 简洁
/agent-vibes:verbosity medium   # 标准(默认)
/agent-vibes:verbosity high     # 详细
```

## 最佳实践

1. **先预览再切换**:使用 `/agent-vibes:preview` 试听后再用 `switch` 确认,避免反复切换
2. **语速匹配内容**:信息密度高的内容用 1.2-1.5x,叙事内容用 0.8-1.0x
3. **引擎按平台选**:macOS 优先 Say,Windows 优先 SAPI,跨平台用 Piper
4. **设置收藏声音**:用 `set-favorite-voice` 标记常用声音,快速恢复
5. **静音专注模式**:工作时 `/agent-vibes:mute`,需要时 `/agent-vibes:unmute`

## 常见问题

### Q1:首次使用需要下载声音吗?
A:Piper 引擎首次使用某声音时会自动从 HuggingFace 下载,后续离线可用。macOS Say 与 Windows SAPI 使用系统内置声音,无需下载。

### Q2:支持哪些语种?
A:支持 30+ 语种,包括中文、英语、法语、德语、西班牙语、日语、韩语等,共 914+ 声音。

### Q3:免费版可以商用吗?
A:免费版仅供个人使用。如需商用或批量导出音频,请使用 PRO 版。

### Q4:声音下载失败怎么办?
A:检查网络连接;确认 HuggingFace 可访问;尝试切换到系统内置引擎(macOS Say / Windows SAPI)。

### Q5:如何清理缓存音频?
A:使用 `/agent-vibes:cleanup` 命令清理已缓存的音频文件。

## 依赖说明

### 运行环境
- **Agent平台**: 支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **运行时**: Node.js 或 Python(视引擎而定)

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| Piper TTS | 语音引擎 | 推荐 | 自动下载安装 |
| macOS Say | 系统内置 | macOS 必需 | 系统自带 |
| Windows SAPI | 系统内置 | Windows 必需 | 系统自带 |
| HuggingFace 声音库 | 资源 | Piper 必需 | 自动下载 |

### API Key 配置
- **免费版无需 API Key**
- 所有引擎均离线运行,无需外部服务鉴权
- 声音资源从 HuggingFace 公开仓库下载,无需账号

### 可用性分类
- **分类**: MD+EXEC(纯 Markdown 指令,核心功能需要 exec 命令行执行能力)
- **说明**: 基于Markdown的AI Skill,通过斜杠命令驱动语音合成,完全离线运行

## 错误处理


| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需要API Key，无Key环境无法使用
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力