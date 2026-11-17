---
name: agnes-image
description: 调用 Agnes Image 2.1 Flash 生成图像，支持文生图、图生图、URL / Base64 输出。当用户说"帮我生成一张图"、"文生图"、"图生图"、"把这张图改成 XX 风格"时触发。
---

# Agnes Image 2.1 Flash 生图 Skill

> 基于 Agnes AI 官方文档：https://agnes-ai.com/zh-Hans/docs/agnes-image-21-flash

## 这个 Skill 做什么

调用 Agnes Image 2.1 Flash 模型生成图像，支持：

- 文生图（text-to-image）
- 图生图（image-to-image）
- URL 输出或 Base64 输出
- 自定义输出尺寸

## 何时使用

当用户出现以下任意意图时触发：

- "帮我生成一张图" / "用 Agnes 生成图片"
- "文生图" / "图生图"
- "把这张图改成 XX 风格"
- 明确提到 `agnes-image-2.1-flash` 或 `Agnes Image`

## 前置要求

1. 拥有 Agnes AI API Key。
2. 在 skill 目录下创建 `.env` 文件并填入 API Key（已提供 `.env.example` 模板）。
3. 可访问 `https://apihub.agnes-ai.cn`。

配置方式：

```bash
# 进入 skill 目录
cd C:/Users/hevin/.workbuddy/skills/agnes-image-skill

# 复制模板
cp .env.example .env

# 编辑 .env，把你的 key 填进去
# AGNES_API_KEY=sk-...
```

脚本启动时会自动读取 skill 目录下的 `.env` 文件，也支持当前工作目录下的 `.env` 文件。

> **安全提示**：`.env` 文件已被加入 `.gitignore`，请勿将 API Key 提交到代码仓库。

## 工作流

### Step 1 · 澄清需求

每次调用前确认：

| 问题 | 默认值 | 说明 |
|------|--------|------|
| 文生图还是图生图？ | 文生图 | 图生图需要提供输入图片路径或 URL |
| prompt 是什么？ | — | 生成或修改图像的文本指令 |
| 输出尺寸？ | `1024x1024` | 常见：`1024x1024`、`1024x768`、`768x1024` |
| 输出格式？ | `url` | 可选 `url` 或 `b64_json` |
| 保存路径？ | 当前目录 `output.png` | 仅 Base64 输出需要本地保存 |

### Step 2 · 调用脚本

使用 WorkBuddy 托管的 Node.js 运行时执行 skill 内置脚本 `generate.mjs`：

```bash
# 文生图 + URL 输出
"C:/Users/hevin/.workbuddy/binaries/node/versions/22.22.2/node.exe" \
  C:/Users/hevin/.workbuddy/skills/agnes-image-skill/generate.mjs \
  --prompt "日出时分薄雾峡谷上方的发光浮空城市，电影级写实风格，广角构图" \
  --size 1024x768 \
  --format url

# 文生图 + Base64 输出并保存
"C:/Users/hevin/.workbuddy/binaries/node/versions/22.22.2/node.exe" \
  C:/Users/hevin/.workbuddy/skills/agnes-image-skill/generate.mjs \
  --prompt "白色摄影棚中的玻璃立方体产品照，柔和阴影，高细节" \
  --size 1024x1024 \
  --format b64_json \
  --output product.png

# 图生图 + URL 输出
"C:/Users/hevin/.workbuddy/binaries/node/versions/22.22.2/node.exe" \
  C:/Users/hevin/.workbuddy/skills/agnes-image-skill/generate.mjs \
  --prompt "改为雨夜赛博朋克风格，保留原始构图" \
  --size 1024x1024 \
  --image https://example.com/input.png \
  --format url
```

### Step 3 · 处理结果

- **URL 输出**：脚本会打印图片 URL，直接展示给用户。
- **Base64 输出**：脚本自动解码并保存到 `--output` 指定路径，同时打印保存位置。

生成图片后，使用 `present_files` 工具将图片文件路径传递给用户查看。

## 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 固定为 `agnes-image-2.1-flash` |
| `prompt` | string | 是 | 图像生成或编辑的文本指令 |
| `size` | string | 是 | 输出尺寸，如 `1024x1024` |
| `image` | string | 图生图必填 | 输入图像 URL 或本地文件路径 |
| `format` | string | 否 | `url`（默认）或 `b64_json` |
| `output` | string | 否 | Base64 输出时保存的文件路径 |
| `timeout` | string | 否 | 请求超时毫秒数，默认 300000 |

## 重要规则

1. **不要**在请求体顶层放 `response_format`，必须放在 `extra_body` 内。
2. 图生图**不需要**传递 `tags: ["img2img"]`。
3. 输入图像必须是公开可访问的 HTTPS URL，或本地文件路径（脚本会自动转 Base64 Data URI）。
4. 客户端超时建议设置为 `60s - 360s`。
5. 当前官方标价为 `$0 / 张`（请以官方最新价格为准）。

## 提示词模板

### 文生图

```
[主体] + [场景/环境] + [风格] + [光照] + [构图] + [质量要求]
```

示例：

```text
日出时分薄雾峡谷上方的发光浮空城市，电影级写实风格，广角构图，丰富的建筑细节，柔和的金色光线，高视觉密度
```

### 图生图

```
[改变要求] + [新风格/场景] + [需要添加或移除的元素] + [需要保留的元素]
```

示例：

```text
将白天街道场景改为电影级赛博朋克夜景，添加霓虹招牌和湿滑路面倒影，同时保留原始街道布局、相机角度和主要建筑形状。
```

## 常见错误与排查

| 错误 | 原因 | 解决 |
|------|------|------|
| `response_format` 无效 | 放在了请求体顶层 | 移到 `extra_body.response_format` |
| 图生图失败 | 缺少 `extra_body.image` | 提供 `--image` 参数 |
| 图片 URL 无法访问 | 私有图片或需要登录 | 使用公开 URL 或本地文件路径 |
| 请求超时 | 生成需要数秒到几十秒 | 脚本默认 300s 超时 |
| 401 Unauthorized | API Key 未设置或无效 | 检查 `AGNES_API_KEY` |

## 资源

- 官方文档：https://agnes-ai.com/zh-Hans/docs/agnes-image-21-flash
- API 端点：`https://apihub.agnes-ai.cn/v1/images/generations`
