# Agnes Image 2.1 Flash

> 升级版图像生成模型，优化高信息密度图像生成，支持文生图与图生图工作流。

## 触发条件

当用户需要以下功能时触发此技能：

- **高质量图像生成**：生成细节丰富、布局复杂的高质量图像
- **高信息密度图像**：复杂场景、丰富构图、多元素画面
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
- "高信息密度"、"复杂场景"、"丰富构图"

## 前置条件

API Key 与 Agnes Image 2.0 共用同一个环境变量：

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
| 文生图 | 根据自然语言提示词生成高质量图像 | `text` |
| 图生图 | 根据提示词转换或优化现有图像 | `img2img` |
| 高信息密度 | 优化细节丰富、布局复杂、视觉元素密集的图像生成 | 默认 |
| 构图保留 | 编辑输入图像时保留原始构图和主体布局 | `img2img` |
| 灵活尺寸 | 支持 `1024x768`、`1024x1024`、`768x1024` 等自定义尺寸 | 自定义 |
| URL/Base64 | 支持图像 URL 或 Base64 数据返回 | 输出格式 |

## 适用场景

- **创意设计**：概念艺术、视觉探索、海报草稿
- **营销内容**：活动图片、产品视觉、社交媒体创意
- **高密度视觉**：精细场景、复杂环境、丰富构图
- **图像转换**：风格迁移、场景重打光、背景变换
- **产品可视化**：产品照片、模型图、商业视觉
- **社交媒体素材**：封面、横幅、缩略图、帖子图片

## 使用方法

### 1. 文生图 (Text-to-Image)

```bash
./scripts/agnes-image-2.1.sh text "prompt" SIZE [OUTPUT_FILE]
```

**示例**：

```bash
./scripts/agnes-image-2.1.sh text "A luminous floating city above a misty canyon at sunrise, cinematic realism" 1024x768 output.png
```

### 2. 图生图 (Image-to-Image)

```bash
./scripts/agnes-image-2.1.sh img2img "prompt" SIZE IMAGE_URL [OUTPUT_FILE]
```

**示例**：

```bash
./scripts/agnes-image-2.1.sh img2img "Transform into a rain-soaked cyberpunk night with neon reflections" 1024x768 "https://example.com/input.jpg" output.png
```

### 3. 多图合成 (Multi-Image)

```bash
./scripts/agnes-image-2.1.sh multi "prompt" SIZE IMAGE1 IMAGE2 [...] [OUTPUT_FILE]
```

**示例**：

```bash
./scripts/agnes-image-2.1.sh multi "Combine these two characters in a fantasy scene" 1024x768 "https://example.com/a.png" "https://example.com/b.png" output.png
```

### 4. 保存为 Base64

输出文件名追加 `.base64` 即可获取 Base64 编码：

```bash
./scripts/agnes-image-2.1.sh text "a sunset" 1024x768 image.base64
```

## 提示词模板

### 文生图
```
[主体] + [场景/环境] + [风格] + [光照] + [构图] + [质量要求]
```

**示例**：
> 日出时分薄雾峡谷上方的发光浮空城市，电影级写实风格，广角构图，丰富的建筑细节，柔和的金色光线，高视觉密度

### 图生图
```
[改变要求] + [新风格/场景] + [需要添加或移除的元素] + [需要保留的元素]
```

**示例**：
> 将白天街道场景改为电影级赛博朋克夜景，添加霓虹招牌和湿滑路面倒影，同时保留原始街道布局、相机角度和主要建筑形状

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `workflow` | 是 | 工作流类型：`text` / `img2img` / `multi` |
| `prompt` | 是 | 图像生成或编辑的指令 |
| `size` | 是 | 输出尺寸，如 `1024x768`、`1024x1024`、`768x1024` |
| `image` | img2img | 输入图像 URL（通过 extra_body 传递） |
| `output` | 否 | 输出文件路径，默认打印 URL |

## 注意事项

- `response_format` 必须放在 `extra_body` 内，**不能**放在顶层
- 图生图**不需要**传递 `tags: ["img2img"]`
- 输入图像 URL 必须是公开可访问的 HTTPS
- 推荐超时时间：60s - 360s

## 与 2.0 版本的区别

| 特性 | 2.0 Flash | 2.1 Flash |
|------|-----------|-----------|
| 模型 | `agnes-image-2.0-flash` | `agnes-image-2.1-flash` |
| 高信息密度 | 基础支持 | **优化增强** |
| 复杂构图 | 一般 | **显著提升** |
| 细节表现 | 标准 | **更精细** |
| API 接口 | 相同 | 相同 |

## 参考文档

- [API 文档](references/API.md)
- [提示词指南](references/PROMPT_GUIDE.md)
