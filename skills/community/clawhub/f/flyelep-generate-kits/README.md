# Flyelep AI Agent 技能集合

可通过仓库 URL 被 OpenClaw、Claude Code 等 AI 工具加载。仓库中的技能全部基于 Flyelep API 接口文档整理，主要覆盖电商海报生成与 AI 图片工具两大类能力。

## 可用技能

| 技能 | 描述 |
|------|------|
| [generate-poster](skills/generate-poster/SKILL.md) | 生成电商产品主图和详情图海报 |
| [intelligent-extension](skills/intelligent-extension/SKILL.md) | 智能延展图片，支持批量处理和目标比例适配 |
| [image-translate](skills/image-translate/SKILL.md) | 识别并翻译图片中的文字，返回翻译后的新图片 |
| [partial-redrawing](skills/partial-redrawing/SKILL.md) | 对图片局部区域进行重绘，可结合文本提示词和参考图 |
| [image-enlarge](skills/image-enlarge/SKILL.md) | 无损放大图片，支持单张或批量增强 |
| [ai-image-matting](skills/ai-image-matting/SKILL.md) | 自动去除图片背景，支持批量抠图 |
| [scene-replace](skills/scene-replace/SKILL.md) | 替换图片背景场景，可结合参考图和文本描述 |
| [product-replace](skills/product-replace/SKILL.md) | 替换图片中的商品主体，保留背景和光影效果 |
| [product-color-change](skills/product-color-change/SKILL.md) | 智能识别商品并进行换色处理 |
| [image-clarity-enhance](skills/image-clarity-enhance/SKILL.md) | AI 超清增强图片清晰度，支持批量处理 |
| [async-free-creation](skills/async-free-creation/SKILL.md) | 异步自由创作，可选模型生成多张创意图片 |
| [ai-writing-assist](skills/ai-writing-assist/SKILL.md) | AI 帮写，辅助生成创意文案和优化提示词 |
| [gen-hot-image](skills/gen-hot-image/SKILL.md) | 爆款图片复刻，基于爆款风格生成产品复刻图 |
| [gen-hot-video](skills/gen-hot-video/SKILL.md) | 爆款视频复刻，基于爆款风格生成产品复刻视频 |
| [generate-video](skills/generate-video/SKILL.md) | 文本生成视频，通过 AI 根据提示词生成产品视频或创意视频 |
| [file-upload](skills/file-upload/SKILL.md) | 上传本地图片、视频、音频到云存储，返回可公网访问的直链 |

## 环境要求

- 用户需从 Flyelep 开放平台获取 API 密钥
- Flyelep 平台地址：https://www.flyelep.cn
- 本仓库中的技能统一要求在请求头中传入 `secretKey`
- 海报生图（`generate-poster`）与视频生成（`generate-video`）也兼容在请求 body 中传 `secretKey`，两处都传时以请求头为准

## 使用建议

- 所有技能均以各自目录中的 `SKILL.md` 为准
- 对于需要高稳定性的调用，优先使用可公网访问、格式规范的图片直链
- 用户提供的是本地文件而非直链时，先用 `file-upload` 上传换取直链，再调用其它技能
- 涉及素材入参的技能都在自己的 `SKILL.md` 里内联了「本地文件上传」章节作为兜底，只单独安装某一个技能也能完成上传；**上传接口若有变动，需同步更新这些章节**
- 对于场景替换、商品替换、商品换色这类生成型接口，建议尽量同时提供清晰原图和明确的文本描述

## 技能总览

各技能的能力概述与接口入口汇总见 [SKILL.md](SKILL.md)，完整参数说明见对应目录下的 `SKILL.md`。

## License

MIT
