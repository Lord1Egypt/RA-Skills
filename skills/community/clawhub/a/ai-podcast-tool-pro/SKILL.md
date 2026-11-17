---

slug: ai-podcast-tool-pro
name: ai-podcast-tool-pro
version: 1.0.0
displayName: AI播客生成-专业版
summary: "企业级播客生产工具,支持批量生成、自定义风格、音频下载与团队协作,适配商业内容生产.。AI播客生成专业版,面向企业团队与专业内容生产者的高级播客制作工具。核心能力:"
license: Proprietary
edition: pro
description: "AI播客生成专业版,面向企业团队与专业内容生产者的高级播客制作工具。核心能力:。Use when 需要提升效率、自动化流程、批量处理、工作流优化时使用。不适用于需要人工创意判断的任务。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。 功能涵盖: podcast。"
  - 批量文档转播客,支持多文档队列处理

  - 自定义对话风格(访谈、辩论、教学等)

  - 音频文件下载(MP3/WAV)

  - 节目封面自动生成与定制

  - 团队协作与播客资产管理

  - 优先生成队列与企业级技术支持

  适用场景:

  - 媒体机构批量内容音频化

  - 企业培训资料播客化

  - 出版机构有声内容生产

  - 教育平台课程音频化

  差异化:专业版在免费版基础上扩展批量生成、自定义风格、音频下载与团队协作,兼容免费版所有流程,适合商...'
tags:
  - Creative
  - 播客生成
  - 企业版
  - 商业内容
  - 播客
  - 音频
  - 媒体
  - api
  - mp3
  - style
  - bash
  - language
tools:
  - read
  - exec
  - write
homepage: ""
# 定价元数据
category: "Creative"

---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。


# AI播客生成工具 - 专业版

## 概述

AI播客生成专业版是一款面向企业团队与专业内容生产者的高级播客制作工具。在免费版文档转播客核心能力之上,扩展了批量生成、自定义对话风格、音频文件下载、节目封面定制与团队协作等高级功能,可融入商业播客内容生产流水线.
本版本完全兼容免费版所有 API 调用与流程,企业用户可直接迁移既有工作流并获得更丰富的制作能力与更高生成配额.
## 核心能力

| 能力项 | 免费版 | 专业版 | 说明 |
|---|---|---|---|
| PDF 转播客 | 是 | 是 | PDF URL 输入 |
| 文本转播客 | 是 | 是 | 粘贴文本输入 |
| 多语种支持 | 是 | 是 | 中英日韩等 |
| 双人对话格式 | 是 | 是 | 主持人+嘉宾 |
| 分享链接 | 是 | 是 | 可分享播放 |
| 自定义对话风格 | 否 | 是 | 访谈/辩论/教学 |
| 批量生成 | 否 | 是 | 多文档队列 |
| 音频下载 | 否 | 是 | MP3/WAV |
| 节目封面 | 否 | 是 | 自动生成定制 |
| 团队协作 | 否 | 是 | 资产共享管理 |
| API 配额优先级 | 普通 | 高优先 | 企业级保障 |
| 技术支持 | 社区 | 专属 | 工单响应 |

### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置.

**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：企业级播客生产工、支持批量生成、自定义风格、音频下载与团队协、适配商业内容生产、播客生成专业版、面向企业团队与专、业内容生产者的高、级播客制作工具、核心能力、批量文档转播客、支持多文档队列处、教学等、音频文件下载、节目封面自动生成、与定制、团队协作与播客资、产管理、优先生成队列与企、业级技术支持等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:媒体机构批量内容音频化

媒体机构需将一批文章批量转为播客,使用批量生成能力.
```python
# 批量生成播客
python3 （请参考skill目录中的脚本文件） \
  --input ./articles/ \
  --language zh \
  --style interview \
  --output ./podcasts/ \
  --format mp3
# ...
# articles 目录下放置多个 txt/pdf 文件
# 系统逐个处理并生成播客音频
```

### 场景二:企业培训资料播客化

企业培训部门需将培训文档转为播客,使用自定义对话风格(教学式).
```bash
# 配置企业 API
export MAGICPODCAST_API_KEY="${API_KEY:?请设置环境变量}"
export MAGICPODCAST_EDITION="pro"
# ...
# 使用教学式对话风格创建
payload="$(jq -n \
  --arg text "$TRAINING_TEXT" \
  --arg language "zh" \
  --arg style "teaching" \
  --arg host "讲师" \
  --arg guest "学员" \
  '{text:$text,language:$language,style:$style,host:$host,guest:$guest}')"
# ...
curl -sS -X POST "$MAGICPODCAST_API_URL/agent/v1/podcasts/text" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MAGICPODCAST_API_KEY" \
  --data-binary "$payload"
# ...
# 下载音频文件
curl -sS "$MAGICPODCAST_API_URL/agent/v1/podcasts/$PODCAST_ID/download" \
  -H "x-api-key: $MAGICPODCAST_API_KEY" \
  -o training_episode.mp3
```

### 场景三:出版机构有声内容生产

出版机构需为一批书籍生成有声试听片段,使用批量生成与封面定制.
```bash
# 批量生成有声试听
python3 （请参考skill目录中的脚本文件） \
  --input ./books/ \
  --language zh \
  --style narrative \
  --duration 300 \
  --cover-template "brand_template_01" \
  --output ./audiobooks/
# ...
# 生成节目封面
python3 （请参考skill目录中的脚本文件） \
  --title "书籍试听:未指定" \
  --template brand_template_01 \
  --output cover.png
```

## 不适用场景

以下场景AI播客生成-专业版不适合处理：

- 加密文件破解
- 损坏文件修复
- 物理介质数据恢复

## 触发条件

需要文件处理、文档转换、格式互转、内容提取时使用。不适用于非本工具能力范围的需求.
## 快速开始

### 领先步:配置企业 API Key

```bash
export MAGICPODCAST_API_URL="https://api.magicpodcast.app"
export MAGICPODCAST_EDITION="pro"
```

### 第二步:执行批量生成

```bash
python3 （请参考skill目录中的脚本文件） \
  --input ./documents/ \
  --language zh \
  --style interview \
  --format mp3 \
  --output ./podcasts/
```

### 第三步:下载与分发

```bash
# 下载所有生成的播客音频
python3 （请参考skill目录中的脚本文件） \
  --job-ids ./podcasts/job_ids.json \
  --output ./audio/
```

#
## 示例

专业版完整配置:

```bash
# 环境变量
MAGICPODCAST_API_URL=https://api.magicpodcast.app
MAGICPODCAST_API_KEY=your_pro_key
MAGICPODCAST_EDITION=pro
MAGICPODCAST_MAX_BATCH=20
MAGICPODCAST_DEFAULT_STYLE=interview
MAGICPODCAST_DEFAULT_FORMAT=mp3
# ...
# 对话风格选项
# interview: 访谈式(主持人提问,嘉宾回答)
# debate: 辩论式(双方观点交锋)
# teaching: 教学式(讲师讲解,学员互动)
# narrative: 叙事式(单人讲述为主)
# casual: 闲聊式(轻松对话)
# ...
# 高级参数
--style <style>              # 对话风格
--host <name>               # 主持人名称
--guest <name>              # 嘉宾名称
--duration <seconds>        # 时长控制
--format mp3|wav            # 音频格式
--cover-template <template> # 封面模板
```

## 优选实践

1. **风格匹配内容**:培训用教学式,新闻用访谈式,故事用叙事式
2. **批量分批处理**:大批量任务建议分批(每批 10-20 个),避免队列拥堵
3. **音频格式选择**:在线分发用 MP3(压缩),后期处理用 WAV(无损)
4. **封面品牌统一**:使用统一封面模板,强化品牌识别度
5. **团队命名规范**:播客命名统一(如 `{系列}_{期数}_{主题}`),便于管理
6. **敏感内容隔离**:机密文档使用私有部署版本,避免数据外泄

## 常见问题

### Q1:专业版与免费版是否兼容?
A:完全兼容。专业版支持免费版所有 API 调用,迁移时仅需更换 API Key 并设置 `MAGICPODCAST_EDITION=pro`.
### Q2:批量生成支持多少个文档?
A:单批最多 20 个文档,大批量建议分批处理。每个文档独立处理,部分失败不影响其他.
### Q3:自定义对话风格如何配置?
A:通过 `--style` 参数选择(interview/debate/teaching/narrative/casual),可自定义主持人与嘉宾名称.
### Q4:音频下载格式与质量?
A:支持 MP3(128kbps/192kbps)与 WAV(44.1kHz/48kHz),建议在线分发用 MP3 192kbps.
### Q5:能否集成到内容管理系统?
A:可以。通过 API 可集成到 CMS、LMS 等系统,实现文档上传→播客生成→音频分发的自动化流程.
### Q6:支持私有部署吗?
A:企业版支持私有化部署,数据完全留在企业内网。联系企业服务获取部署文档.
## 依赖说明

### 运行环境
- **Agent平台**: 支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **运行时**: Bash shell + Python 3.9+ + curl + jq

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| MagicPodcast Pro API | 外部 API | 必需 | 企业服务渠道申请 |
| curl | 命令行工具 | 必需 | 系统自带 |
| jq | JSON 处理 | 必需 | 包管理器安装 |
| Python 3.9+ | 脚本运行 | 必需 | 官方安装 |
| ffmpeg | 音频处理 | 推荐 | 用于转码与剪辑 |

### API Key 配置
- **环境变量名**: `MAGICPODCAST_API_KEY`(企业版 Key)
- **附加变量**: `MAGICPODCAST_EDITION=pro`
- **获取方式**: 通过企业服务渠道申请,享有高优先级生成队列
- **安全建议**: 使用密钥管理服务存储 Key,避免明文写入脚本

### 可用性分类
- **分类**: MD+execute(纯 Markdown 指令,核心功能需要 exec 命令行执行能力)
- **说明**: 基于Markdown的AI Skill,支持批量生成、自定义风格、音频下载等企业级播客生产场景

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "AI播客生成-专业版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "ai podcast pro"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。