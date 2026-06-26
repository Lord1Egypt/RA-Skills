---
name: bozo-aigc
description: 文生图与图生图 AI 图片生成工具。使用 BizyAir GPT_IMAGE_2 API 进行文本转图片和多图参考生成。当用户需要生成图片、创建配图、文生图、文本转图片、AI 绘画、图生图、参考图片生成、多图融合、设置图片尺寸比例、生成横版/竖版图片时触发此技能。即使用户只说"帮我画一张"、"生成图片"、"根据这些图片生成"也应触发。
---

# BOZO AIGC - 文生图与图生图工具

基于 BizyAir GPT_IMAGE_2 API 的 AI 图片生成工具，支持两种模式：**文生图（T2I）** 和 **图生图（I2I）**。

## 功能特点

- **文生图**：将文本描述转换为高质量图片
- **图生图**：根据 1-8 张参考图片生成新图片
- 自动保存到 `pic` 文件夹，按时间戳命名
- 支持多种图片尺寸比例

## 前置要求

需要设置 BizyAir API 密钥环境变量：

```bash
export BIZYAIR_API_KEY='你的API密钥'
```

## 重要：API 响应时间说明

BizyAir GPT_IMAGE_2 是远程推理服务，生成图片需要较长的等待时间：

| 场景 | 预计耗时 |
|------|----------|
| 最快（简单提示词） | ~90 秒 |
| 一般情况 | 2-5 分钟 |
| 最慢（复杂提示词 / 多图） | 5-10 分钟 |

脚本已内置超时保护：
- **API 请求超时**：600 秒（10 分钟），覆盖最慢情况
- **连接超时**：30 秒，防止网络不通时无限等待
- **图片下载超时**：120 秒

调用脚本前应告知用户"图片生成需要几分钟，请耐心等待"。

## 模式一：文生图（Text-to-Image）

当用户只有文本描述、没有参考图片时使用此模式。

### API 参数

| 参数 | 值 |
|------|-----|
| 端点 | `https://api.bizyair.cn/w/v1/webapp/task/openapi/create` |
| web_app_id | `52416` |
| 模型 | BizyAir_GPT_IMAGE_2_T2I_API |
| 提示词键 | `4:BizyAir_GPT_IMAGE_2_T2I_API.prompt` |
| 比例键 | `4:BizyAir_GPT_IMAGE_2_T2I_API.aspect_ratio` |

### 使用方式

调用脚本 `scripts/text-to-image.sh`：

```bash
./scripts/text-to-image.sh "提示词内容" [比例]
```

示例：
- `./scripts/text-to-image.sh "一只可爱的猫咪"` — 使用默认比例 9:16
- `./scripts/text-to-image.sh "风景画" 16:9` — 指定横版比例

## 模式二：图生图（Image-to-Image）

当用户提供参考图片 URL 时使用此模式，支持 1-8 张参考图片。

### API 参数

根据参考图片数量自动选择 web_app_id：

| 图片数量 | web_app_id | LoadImage 节点 ID |
|----------|------------|-------------------|
| 1 | 52418 | 7 |
| 2 | 52420 | 7, 8 |
| 3 | 52423 | 7, 8, 9 |
| 4 | 52343 | 7, 8, 9, 10 |
| 5 | 52431 | 7, 8, 9, 10, 11 |
| 6 | 52435 | 7, 8, 9, 10, 11, 12 |
| 7 | 52437 | 7, 8, 9, 10, 11, 12, 18 |
| 8 | 52442 | 7, 8, 9, 10, 11, 12, 18, 20 |

- 模型：BizyAir_GPT_IMAGE_2_I2I_API
- 提示词键：`6:BizyAir_GPT_IMAGE_2_I2I_API.prompt`
- 比例键：`6:BizyAir_GPT_IMAGE_2_I2I_API.aspect_ratio`

### 使用方式

调用脚本 `scripts/image-to-image.sh`：

```bash
./scripts/image-to-image.sh "提示词" "图片URL1" ["图片URL2" ...] [比例]
```

示例：
- `./scripts/image-to-image.sh "将风格改为水彩画" "https://example.com/img.png"`
- `./scripts/image-to-image.sh "融合这些风格" "url1" "url2" 16:9`

## 图片尺寸比例

支持以下比例，默认使用 **9:16**：

| 比例 | 适用场景 |
|------|----------|
| 1:1 | 头像/方图 |
| 2:3 | 标准竖图 |
| 3:2 | 标准横图 |
| 4:5 | Instagram 竖图 |
| 5:4 | Instagram 横图 |
| 3:4 | 竖版海报 |
| 4:3 | 横版海报 |
| **9:16** | **手机壁纸/短视频（默认）** |
| 16:9 | 视频封面/横屏 |
| 21:9 | 超宽屏/电影感 |

## 输出说明

- 图片保存到 `pic` 文件夹
- 文件名格式：`YYYYMMDD_HHMMSS.png`（或 `.jpg`）
- macOS 系统自动在预览中打开图片

## 工作流程

1. 根据用户请求判断使用文生图还是图生图模式
2. 解析用户输入：提取提示词、图片URL（如有）、比例参数
3. **告知用户图片生成需要 2-10 分钟，请耐心等待**
4. 调用对应的脚本（Bash 工具，timeout 建议 600000ms）
5. 等待 API 返回结果并下载图片
6. 告知用户图片保存路径
