# generate-image

`generate-image` 是文章配图 skill，对应的 ClawHub 发布名是 `content-system-generate-image`。它从文章主稿中提取主题和关键信息，生成公众号配图；如果外部图片生成不可用，会自动降级到本地信息图。

## 这个 skill 能做什么

- 从文章主稿里提取标题、摘要和关键信息
- 默认通过香蕉画图生成配图，默认模型是 `nano-nx`
- 调用外部图片生成能力生成配图
- 在外部生成失败时，自动回退到本地信息图渲染
- 输出标准化 `ready/*-img-1.png`
- 可作为 `wechat-studio` 的图片来源

## 安装

### 基础依赖

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### 可选：高质量外部生成

当前 runtime 会优先调用本机 `md2wechat generate_image`，并默认注入这组图片配置：

```text
IMAGE_PROVIDER=openai
IMAGE_API_BASE=https://new.suxi.ai/v1
IMAGE_MODEL=nano-nx
```

也就是说，这个 skill 默认把香蕉画图当成 OpenAI-compatible 图片接口来调用；你只需要准备令牌即可。

如果你本地已经有这套 CLI 和图片 provider，就会走外部生成；如果没有，也能自动退回本地信息图。

### 香蕉画图登录方式

- 已有制作平台的用户可直接使用
- 没有制作平台的用户，打开 [job.suxi.ai](https://job.suxi.ai/)
- 把生成的 `SK` 放到令牌位置后点登录

本 skill 不会改你的全局 `md2wechat` 配置，而是在运行时注入默认的 provider / base URL / model。令牌仍建议通过 `IMAGE_API_KEY` 或你现有的 `md2wechat` 配置提供。

可以先这样验证：

```bash
md2wechat generate_image --help
```

如果这条命令不可用，也不影响本 skill 的基础使用。

## 输入和输出

**输入**

- `content-production/drafts/<slug>-article.md`
- 可选 frontmatter 覆盖字段：
  - `image_provider`
  - `image_api_base`
  - `image_model`

**输出**

- `content-production/ready/<slug>-img-1.png`

## 使用方法

### 单独运行

```bash
.venv/bin/python -m skill_runtime.cli run-skill generate-image \
  --input content-production/drafts/harness-engineering-一人公司-article.md
```

### 常见上游 / 下游

- 上游：`case-writer-hybrid`
- 下游：`wechat-studio` 或人工挑图

### 覆盖默认模型或地址

如果你想按文章单独覆盖默认配置，可以在文章 frontmatter 里加：

```yaml
---
title: 示例文章
digest: 示例摘要
image_provider: openai
image_api_base: https://new.suxi.ai/v1
image_model: nano-nx
---
```

如果调用方直接走 runtime，也可以显式传 `image_provider`、`image_api_base`、`image_model`。

## 什么时候用

- 你已经有一篇主稿，想快速得到头图或信息图
- 你想把文章里最重要的几个判断可视化
- 你需要一个“即使外部模型挂了也能继续产出”的稳妥配图节点

## 注意事项

- 外部生成可用时效果更好，但不是必需条件
- 默认图片链路是香蕉画图 `nano-nx`，平台兼容 OpenAI 格式
- 本地 fallback 输出的是“可用信息图”，不是高度定制视觉设计
- 当前主输出是单张 `img-1.png`

## 相关文件

- [SKILL.md](./SKILL.md)
- [runtime.py](./runtime.py)
- [generate-image-execution-spec.md](../../docs/generate-image-execution-spec.md)
