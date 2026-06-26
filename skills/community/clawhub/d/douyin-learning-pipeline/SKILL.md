---
name: douyin-learning-pipeline
description: >
  抖音链接总控工作流（精简版）：自动区分"下载解析"和"文案提取"两类需求，并在需要时串联完成转写、智能修顺、结构拆解与后置仿写。Use when 用户发送抖音链接，要求"解析抖音""下载无水印""提取抖音文案""抖音转文字""提取口播稿""拆解这条视频""基于这条抖音做仿写"时触发。
  固定主链：链接 → 转写 → 修顺 → 拆解 → 仿写。默认转写模型：TeleAI/TeleSpeechASR；默认纠错模型：cpa/gpt-5.4。
  自包含特性：缺配置会问用户要；缺依赖会自动安装；可独立迁移到其他系统。
---

# douyin-learning-pipeline（精简版）

这是抖音相关任务的总控 skill，负责统一判断任务意图，并完成下载、转写、修顺、拆解与仿写。

## 零、启动时自检（必须先执行）

每次收到抖音相关任务，先执行环境自检：

### 自检清单
1. **Python 3** 是否可用
2. **ffmpeg** 是否已安装
3. **yt-dlp** 是否已安装（用于备用下载）
4. **douyin-downloader** 是否已部署
5. **SiliconFlow API Key** 是否已配置
6. **飞书文档写入能力** 是否可用（如用户要求写飞书）

### 自检脚本
```bash
bash scripts/check_env.sh
```

### 自检失败时的处理
- **缺安装**：自动尝试安装（Python包用pip，系统包用apt/brew）
- **缺配置**：直接问用户要，例如：
  - `请提供 SiliconFlow API Key：`
  - `请提供抖音 Cookie（msToken, ttwid 等）：`
  - `请提供飞书文档目标位置：`
- **无法自动解决**：明确告诉用户缺什么、怎么补

## 一、先做需求分流

### A. 下载解析路线
当用户要的是素材文件，走这条：
- 无水印视频
- 图集原图
- 本地文件
- 真实下载地址

触发词示例：
- 解析这个抖音
- 下载这个视频
- 无水印下载
- 提取原图
- 图集下载
- 给我视频文件

### B. 文案提取路线
当用户要的是内容文本，走这条：
- 提取口播稿
- 抖音转文字
- 提取台词/话术
- 整理成文案稿

触发词示例：
- 提取这条抖音文案
- 抖音转文字
- 提取口播稿
- 提取这条视频内容
- 拆话术

### C. 混合路线
如果用户同时要下载和提文案，则顺序固定：
1. 先下载/解析
2. 再转写/提文案

### D. 模糊情况
如果只给链接、目标不明确：
- 先做轻量识别（视频/图集、能否下载）
- 若上下文已明确在做文案，则继续文案链路
- 若仍模糊，只问一句短确认：
  - `这是要我帮你下载无水印，还是提取文案？`

## 二、文案主链（固定顺序）

主链固定为：
**链接 → 转写 → 修顺 → 拆解 → 仿写**

### 1. 转写
- 优先用自带的下载脚本获取音轨
- 默认 ASR：`TeleAI/TeleSpeechASR`
- 备选 ASR：`FunAudioLLM/SenseVoiceSmall`
- 不默认回退到本地 Whisper，除非用户明确要求

### 2. 修顺
- 默认模型：`cpa/gpt-5.4`
- 备选：`cpa/claude-sonnet-4-6`
- 输出要明确区分：
  - 原始转写稿
  - 智能纠错修复稿
  - 可能仍有误的片段（如有）

### 3. 拆解
默认可做：
- 结构拆解
- 钩子提炼
- 平台改写

### 4. 仿写（后置步骤）
只有在以下情况才做：
- 用户明确要仿写
- 或者用户明确要模板/套写版本

仿写应基于已经提取和修顺好的内容进行，不要擅自和原始转写混写。

## 三、自带脚本

### 1. 环境自检脚本
`scripts/check_env.sh`
- 检查所有依赖
- 缺什么补什么
- 无法自动补的就问用户

### 2. 抖音下载脚本
`scripts/download_douyin.sh`
- 支持短链解析
- 支持视频/图集下载
- 支持音轨提取
- 自动处理 Cookie

### 3. ASR 转写脚本
`scripts/transcribe.sh`
- 默认用 TeleAI/TeleSpeechASR
- 支持备选 SenseVoiceSmall
- 自动调用 SiliconFlow API

## 四、配置管理（缺就问）

### 必需配置项
1. **SiliconFlow API Key**
   - 环境变量：`SILICONFLOW_API_KEY`
   - 缺失时问用户：`请提供 SiliconFlow API Key：`

2. **抖音 Cookie**
   - 文件：`assets/douyin-downloader/config.yml`
   - 缺失时问用户：`请提供抖音 Cookie（msToken, ttwid, odin_tt, passport_csrf_token, sid_guard）：`

3. **飞书文档目标**
   - 可选，默认不写飞书
   - 如需写入，问用户：`请提供飞书文档链接或token：`

### 配置存储
- 分发包只保留模板：`assets/config.template.json`
- 用户真实配置写入本地文件：`local/config.json`
- 首次运行时自动引导用户配置

## 五、依赖安装（缺就装）

### Python 依赖
```text
requests
yt-dlp
```
自动用 pip 安装

### 系统依赖
- **ffmpeg**：音轨提取必需
  - Ubuntu/Debian: `apt install ffmpeg`
  - macOS: `brew install ffmpeg`
  - 缺失时先提示用户确认，再执行高权限安装

### douyin-downloader
- 如果未部署，自动克隆：
  ```bash
  git clone https://github.com/jiji262/douyin-downloader.git
  ```
- 引导用户配置 Cookie

## 六、默认交付规则

- 定稿、长文、成体系内容：优先写飞书文档（如已配置）
- 聊天里只回：链接 + 一句结论
- 本 skill **不自建知识库 / 不自建索引**
- 如果宿主系统本身有知识库、记忆、归档能力，优先调用宿主本体能力
- 如果宿主没有，就只完成当前任务结果，不额外做入库动作

## 七、迁移到其他系统

### 最小要求
1. Python 3.8+
2. 能联网
3. 有 SiliconFlow 账号

### 迁移步骤
1. 复制整个 `douyin-learning-pipeline` 目录
2. 运行 `scripts/check_env.sh`
3. 按提示补齐配置
4. 开始使用

### 一键安装
```bash
# 下载 skill
git clone <skill-repo> douyin-learning-pipeline
cd douyin-learning-pipeline
# 自检并补依赖
bash scripts/check_env.sh
# 配置
python scripts/setup_config.py
```

## 八、与旧 skill 的关系

下面三个能力现在视为这个总控 skill 的子能力来源：
- `douyin-copy-extractor`
- `transcript-polisher`
- `script-analyzer`

但这个精简版已经内嵌了它们的核心能力，可以独立运行。
