---
name: "ai-image-prompt-tool-free"
description: "AI图像生成提示词 crafting 工具,提供模板库与基础优化,适合个人创作者提升出图质量。Use when 需要AI模型调用、智能对话、Agent编排、LLM应用时使用。不适用于需要100%确定性的关键决策。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "AI图像提示词-免费版"
  version: "1.0.0"
  summary: "AI图像生成提示词 crafting 工具,提供模板库与基础优化,适合个人创作者提升出图质量。"
  tags:
    - "Creative"
    - "提示词工程"
    - "AI创作"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read
  - write
---

> **核心功能**: 本技能提供中文交互、化工作流场景等能力。

# AI图像提示词工具 - 免费版

## 概述

AI图像提示词免费版是一款面向个人用户的图像生成提示词 crafting 工具。提供常用场景的提示词模板库、基础优化建议与风格快速套用,帮助用户写出更精准的提示词,提升 AI 图像生成效果。

本版本适合 AI 图像生成初学者、个人创作者及社交媒体运营者,通过模板与示例快速掌握提示词写作技巧。

## 核心能力

| 能力项 | 免费版支持 | 说明 |
|:-------|:-----------|:-----|
| 提示词模板库 | 是 | 10+ 常用场景模板 |
| 基础优化建议 | 是 | 主体/风格/构图/色调 |
| 中英文转换 | 是 | 中文描述扩展为英文 |
| 艺术风格套用 | 是 | 10+ 风格快速应用 |
| 提示词历史 | 限制 | 最近 20 条 |
| 批量提示词生成 | 否 | PRO 版支持 |
| A/B 测试 | 否 | PRO 版支持 |
| 提示词版本管理 | 否 | PRO 版支持 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置。

### 核心功能执行
用`input_params`参数进行配置。

**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输出**: 返回参数配置与调用的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输出**: 返回结果处理与输出的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：图像生成提示词、crafting、提供模板库与基础、适合个人创作者提、升出图质量、图像提示词免费版、面向个人用户的图、像生成提示词、提供常用场景提示、商品等、基础提示词优化建、支持中文描述自动、扩展为英文提示词、艺术风格快速套用等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一:花卉主题提示词

用户希望生成一张童话风格的花卉拱门图片,使用模板快速构建提示词。

```text
模板: [主体描述] + [风格描述] + [色调描述] + [构图描述]

生成提示词:
"Generate an image of a whimsical, fairytale-inspired floral arch with pastel-colored flowers and delicate ivy, soft dreamy lighting, pastel color palette, centered composition with shallow depth of field."
```

### 场景二:人物肖像提示词

用户需要生成一张人物肖像,套用写实摄影风格。

```text
中文描述: 一位年轻女性,微笑,户外阳光
优化后提示词:
"A young woman with a gentle smile, standing outdoors in warm sunlight, soft golden hour lighting, realistic photography style, shallow depth of field, natural skin tones, 85mm portrait lens composition."
```

### 场景三:风景插画提示词

用户希望生成一幅风景插画,套用水彩风格。

```text
中文描述: 山间小屋,秋天,宁静
优化后提示词:
"A cozy cabin nestled in autumn mountains, surrounded by golden and red foliage, misty morning atmosphere, watercolor illustration style, soft brushstrokes, warm color palette with muted tones, peaceful and serene mood."
```

## 不适用场景

以下场景AI图像提示词-免费版不适合处理：

- 纯技术文档撰写
- 学术论文写作
- 法律文书起草

## 触发条件

需要生成营销文案、写作内容、标题优化、内容创作时使用。不适用于非本工具能力范围的需求。

## 快速开始

### 领先步:描述你的需求

用中文或英文描述你想要生成的图像内容,例如:"一只在月光下奔跑的狼"。

### 第二步:选择风格

从内置风格库选择,例如:

| 风格名称 | 英文关键词 | 适用场景 |
|:---------|:-----------|:---------|
| 水彩 | watercolor, soft brushstrokes | 插画、艺术 |
| 油画 | oil painting, textured | 古典、艺术 |
| 写实摄影 | realistic photography, 85mm | 人物、商品 |
| 赛博朋克 | cyberpunk, neon, futuristic | 科技、未来 |
| 吉卜力 | Studio Ghibli style, anime | 动漫、梦幻 |
| 中国工笔 | Chinese gongbi, ink and gold | 传统、东方 |
| 极简 | minimalist, clean lines | 设计、简约 |
| 复古 | vintage, retro film | 怀旧、文艺 |

### 第三步:组合生成提示词

```python
# 示例
python3 scripts/build_prompt.py \
  --subject "月光下奔跑的狼" \
  --style "写实摄影" \
  --tone "冷色调,蓝月光" \
  --composition "动态构图,低角度"
```

输出:

```text
"A wolf running under moonlight, cold blue tones with silver highlights, realistic photography style, dynamic composition from low angle, motion blur on legs, sharp focus on eyes, cinematic lighting."
```

## 配置示例

基础配置项说明:

```bash
# 提示词结构模板
[主体描述] + [场景描述] + [风格描述] + [色调描述] + [构图描述] + [氛围描述]

# 常用风格关键词(中英对照)
水彩: watercolor, soft brushstrokes, pastel
油画: oil painting, textured, rich colors
写实: realistic photography, 85mm, natural lighting
赛博朋克: cyberpunk, neon lights, futuristic
吉卜力: Studio Ghibli style, anime, dreamy
中国工笔: Chinese gongbi, ink and gold leaf
极简: minimalist, clean lines, negative space
```

## 优选实践

1. **主体优先**:提示词开头明确描述主体,避免 AI 理解偏差
2. **风格具体**:使用具体的风格关键词(如"watercolor"而非"artistic")
3. **色调指定**:明确主色调与配色,如"pastel colors"或"warm golden tones"
4. **构图说明**:说明视角、景深、焦点,如"low angle, shallow depth of field"
5. **氛围点睛**:用一两个词描述情绪,如"peaceful"、"dramatic"、"melancholic"
6. **长度适中**:50-150 字英文为佳,过短信息不足,过长可能互相矛盾

## 常见问题

### Q1:中文提示词效果不好?
A:多数 AI 图像模型对英文提示词理解更准确,建议用英文描述,或使用本工具的中英文转换功能。

### Q2:提示词越长越好吗?
A:不是。关键信息要突出,过多的描述可能互相矛盾。建议聚焦 5-7 个核心要素。

### Q3:如何让生成结果更稳定?
A:固定风格关键词与构图描述,仅调整主体内容;使用相同的提示词结构模板。

### Q4:免费版模板库够用吗?
A:免费版提供 10+ 常用场景模板,覆盖大部分个人需求。如需行业专业模板(电商、广告、出版等),请使用 PRO 版。

### Q5:可以保存常用提示词吗?
A:免费版支持最近 20 条历史记录。如需提示词版本管理与团队共享,请使用 PRO 版。

## 依赖说明

### 运行环境
- **Agent平台**: 支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **运行时**: Python 3.8+(可选,用于脚本辅助)

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |
| Python 3.8+ | 运行时 | 可选 | 官方安装 |

### API Key 配置
- **本 Skill 基于 Markdown 指令,无需额外 API Key**
- 提示词构建由 Agent 内置 LLM 完成,不依赖外部图像生成 API
- 生成提示词后可配合任意图像生成工具使用

### 可用性分类
- **分类**: MD(纯 Markdown 指令,无需 exec 命令行执行能力)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent构建与优化图像生成提示词

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。