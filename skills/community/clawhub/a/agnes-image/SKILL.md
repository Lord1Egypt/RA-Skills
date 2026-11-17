# Agnes Image 2.0 Flash

> 使用 Agnes Image 2.0 Flash 模型生成和编辑图像。支持文生图、图生图和多图合成工作流。

## 触发条件

当用户需要以下功能时触发此技能：

- **图像生成**：根据文字描述生成高质量图像
- **图像编辑**：修改现有图像的样式、背景、风格
- **多图合成**：将多张图片融合到同一场景中
- **风格转换**：将照片转换为艺术风格（动漫、油画、水彩等）
- **产品可视化**：生成产品照片、商业视觉内容
- **创意设计**：概念艺术、海报草稿、视觉探索

**触发关键词**：
- "生成图片"、"创建图像"、"画一张"
- "编辑图片"、"修改图像"、"换背景"
- "风格转换"、"转动漫"、"变油画"
- "合成图片"、"融合图像"、"合并"
- "文生图"、"图生图"、"image generation"

## 前置条件

设置 API Key 环境变量：

```bash
export ANGES_API_KEY="your_api_key_here"
```

或使用替代变量：

```bash
export AGENT_ANGES_API_KEY="your_api_key_here"
```

## 核心能力

| 能力 | 说明 | 工作流 |
|------|------|--------|
| 文生图 | 根据文字描述生成高质量图像 | `text` |
| 图生图 | 根据提示词编辑/转换现有图像 | `img2img` |
| 多图合成 | 将多张图片融合到统一场景 | `multi` |
| 灵活尺寸 | 支持多种分辨率和宽高比 | 自定义 |
| 风格控制 | 通过提示词控制艺术风格 | 提示词 |
| 质量优化 | 高质量商业级图像输出 | 默认 |

## 使用方法

### 1. 文生图 (Text-to-Image)

```bash
./scripts/agnes-image.sh text "prompt" SIZE [OUTPUT_FILE]
```

**示例**：

```bash
./scripts/agnes-image.sh text "A cat sitting on a windowsill, golden hour lighting, photorealistic" 1024x768 output.png
```

### 2. 图生图 (Image-to-Image)

```bash
./scripts/agnes-image.sh img2img "prompt" SIZE IMAGE_URL [OUTPUT_FILE]
```

**示例**：

```bash
./scripts/agnes-image.sh img2img "Transform into anime style" 1024x768 "https://example.com/photo.jpg" output.png
```

### 3. 多图合成 (Multi-Image)

```bash
./scripts/agnes-image.sh multi "prompt" SIZE IMAGE1 IMAGE2 [...] [OUTPUT_FILE]
```

**示例**：

```bash
./scripts/agnes-image.sh multi "Combine these two characters in a fantasy scene" 1024x768 "https://example.com/a.png" "https://example.com/b.png" output.png
```

### 4. 保存为 Base64

输出文件名追加 `.base64` 即可获取 Base64 编码：

```bash
./scripts/agnes-image.sh text "a sunset" 1024x768 image.base64
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `workflow` | 是 | 工作流类型：`text` / `img2img` / `multi` |
| `prompt` | 是 | 图像生成或编辑的指令 |
| `size` | 是 | 输出尺寸，如 `1024x768`、`1024x1024`、`768x1024` |
| `image` | img2img | 输入图像 URL（通过 extra_body 传递） |
| `output` | 否 | 输出文件路径，默认打印 URL |

## 提示词模板

### 文生图
```
[主体] + [场景/背景] + [风格] + [光照] + [构图] + [质量要求]
```

**示例**：
> A professional product photo of wireless headphones on white background, soft studio lighting, sharp details, commercial photography

### 图生图
```
[编辑指令] + [要保留的元素] + [目标风格/场景] + [光照] + [构图] + [质量要求]
```

**示例**：
> Change background to a futuristic city at night while keeping the person's face, outfit, and pose unchanged

## 注意事项

- 输入图像 URL 必须是公开可访问的 HTTPS
- `response_format` 必须放在 `extra_body` 内
- 图生图不需要传递 `tags: ["img2img"]`
- 推荐超时时间：60s - 360s

## 参考文档

- [API 文档](references/API.md)
- [提示词指南](references/PROMPT_GUIDE.md)
