---
name: flyelep-ai-skills
description: >-
  Flyelep AI Agent 技能集合，可通过仓库 URL 被 OpenClaw、Claude Code 等 AI 工具加载。
  当前仓库中的技能全部基于 Flyelep API 接口文档整理，主要覆盖电商海报生成、AI 视频生成与 AI 图片工具三大类能力。
---
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
- 海报生图（`generate-poster`）、自由创作（`async-free-creation`）与视频生成（`generate-video`）也兼容在请求 body 中传 `secretKey`，两处都传时以请求头为准
- 任务查询只能查本账号（同一密钥所属客户）提交的任务

## 技能列表

### generate-poster

生成电商产品主图和详情图海报，适用于产品图、电商海报、Amazon 商品图、详情页图片等场景。

主要能力：

- 生成产品单图和产品详情图
- 支持跨境电商与中文电商
- 支持多平台、多语言文案；语种由平台推导，中文平台（淘宝、拼多多、京东等）默认 `中文简体`，跨境平台（Amazon、Temu、Shopee 等）默认 `英文`
- 默认模型为 `modelEdition=9`（Flyelep Image 2），用户未指定时显式传入；可选 `3`、`9`、`13`、`14`、`15`、`16`，历史值 `2` 已下线并自动按 `9` 处理
- 支持参考图输入和比例控制；Amazon A+ 详情图（`generateType=200`）另支持 `970x600`、`1464x600`、`600x450` 尺寸
- 支持特惠通道（`promotion`，默认）与尊享通道（`premium`），上述模型在特惠通道都可用；调用时默认显式传特惠，用户明确要求时才改传尊享
- 任务查询返回总状态 `status`（1 进行中、2 全部成功、3 全部失败、4 部分成功）及预估、实际消耗算力
- 同时提供异步（提交后轮询）与同步（一次请求出图）两种模式，参数完全一致

接口入口：

- 异步（推荐）：`POST /prod-api/poster-design/api/v1/poster/generateAsync` + `POST /prod-api/poster-design/api/v1/poster/queryTaskResult`
- 同步：`POST /prod-api/poster-design/api/v1/poster/generate`
- 同步（白底主图专属入口，等价于 `/generate` + `generateType=101`）：`POST /prod-api/poster-design/api/v1/poster/whiteBgMainImgGen`

同步模式服务端最长挂 15 分钟，返回的 `data` 是以英文分号 `;` 拼接的字符串，且不返回任务 ID，连接断开后结果无法找回；除用户明确要求一次请求出图外，优先用异步模式。

详细参数和映射规则请查看 [skills/generate-poster/SKILL.md](skills/generate-poster/SKILL.md)。

### intelligent-extension

对图片进行智能延展，支持批量处理，并可指定目标比例。

主要能力：

- 扩图、补边、延展画布
- 适配 `1:1`、`16:9`、`9:16` 等比例
- 支持多张图片批量处理，单次最多 20 张、单张不超过 10MB，服务端并发处理

接口入口：

- `POST /prod-api/poster-design/api/v1/poster/aiTool/intelligentExtension`

详细参数和比例规则请查看 [skills/intelligent-extension/SKILL.md](skills/intelligent-extension/SKILL.md)。

### image-translate

识别并翻译图片中的文字，返回翻译后的新图片地址。

主要能力：

- 图片文字识别与翻译
- 服务端自动识别源语言
- 支持整数枚举目标语言映射，可用 `toList` 一次翻译成多种语言（图片数 × 语言数不超过 20）

接口入口：

- `POST /prod-api/poster-design/api/v1/poster/aiTool/translate`

详细语言枚举和调用方式请查看 [skills/image-translate/SKILL.md](skills/image-translate/SKILL.md)。

### partial-redrawing

对图片局部区域进行重绘，可通过文本提示词控制生成结果，也可结合参考替换图。

主要能力：

- 局部替换
- 局部重绘
- 替换背景、文案或局部元素

接口入口：

- `POST /prod-api/poster-design/api/v1/poster/aiTool/partialRedrawing`

详细参数和提示词建议请查看 [skills/partial-redrawing/SKILL.md](skills/partial-redrawing/SKILL.md)。

### image-enlarge

对图片按倍数进行无损放大，支持单张或批量处理。

主要能力：

- 按倍数放大图片尺寸
- 提升放大后的成图分辨率
- 批量放大商品图

> 只想“变清晰”而不放大尺寸时，应改用 `image-clarity-enhance`。

接口入口：

- `POST /prod-api/poster-design/api/v1/poster/aiTool/enlarge`

图片入参：`imageUrlList`（数组，推荐）与 `imgUrls`（逗号分隔字符串）二选一，最多 20 张，建议单张 10MB 以内

放大倍率 `scalingRatio`：

- 支持 `2`、`4`、`8`（算力分别为 1、2、3 份），未指定时用 `2`
- 全部失败时 `code` 仍为 200，但结果列表为空，需检查结果是否为空

详细调用方式请查看 [skills/image-enlarge/SKILL.md](skills/image-enlarge/SKILL.md)。

### ai-image-matting

自动去除图片背景，适合商品抠图、透明底素材生成等场景。

主要能力：

- 去背景
- 抠出主体
- 批量抠图，推荐用 `imageUrlList` 数组传图，单次最多 20 张

接口入口：

- `POST /prod-api/poster-design/api/v1/poster/aiTool/aiImageMatting`

详细参数和批量处理方式请查看 [skills/ai-image-matting/SKILL.md](skills/ai-image-matting/SKILL.md)。

### scene-replace

将图片中的背景场景替换为指定场景，可结合参考图和文本提示词控制效果。

主要能力：

- 更换背景场景
- 替换商品展示环境
- 保留主体不变，仅替换环境

接口入口：

- `POST /prod-api/poster-design/api/v1/poster/aiTool/sceneReplace`

模型类型：

- `9`：`Flyelep Image 2`（当前仅支持该取值）

必传 `sourceUrl`、`textPrompt`、`modelType`，场景参考图 `replaceImageUrl` 可选且只支持单图。

详细参数说明请查看 [skills/scene-replace/SKILL.md](skills/scene-replace/SKILL.md)。

### product-replace

将图片中的商品替换为指定商品图，同时尽量保留原图背景及光影效果。

主要能力：

- 更换商品主体
- 保留原场景和展示环境
- 支持目标商品图和文本补充约束

接口入口：

- `POST /prod-api/poster-design/api/v1/poster/aiTool/productReplace`

模型类型：

- `9`：`Flyelep Image 2`（当前仅支持该取值）

详细参数说明请查看 [skills/product-replace/SKILL.md](skills/product-replace/SKILL.md)。

### product-color-change

对图片中的商品进行智能换色处理，适合制作同款不同颜色展示图。

主要能力：

- 修改商品颜色
- 保留商品主体和背景
- 支持通过提示词约束换色范围和效果

接口入口：

- `POST /prod-api/poster-design/api/v1/poster/aiTool/productColorChange`

模型类型：

- `9`：`Flyelep Image 2`（当前仅支持该取值）

详细提示词建议请查看 [skills/product-color-change/SKILL.md](skills/product-color-change/SKILL.md)。

### image-clarity-enhance

增强图片清晰度，支持单张或批量处理，适合做 AI 超清增强。

主要能力：

- 清晰度增强
- 批量超清处理
- 根据强度控制增强程度

接口入口：

- `POST /prod-api/poster-design/api/v1/poster/aiTool/imageClarityEnhance`

增强强度 `enhanceStrength`（不传时按 `light` 处理，只对成功的图片计费）：

- `light`（基础单价，约 2 倍放大）
- `standard`（2 倍单价，约 4 倍放大）
- `strong`（3 倍单价，约 8 倍放大）

图片规格限制：

- 最短边不少于 `256px`
- 最长边不超过 `2048px`
- 文件大小不超过 `10MB`
- 图片链接必须可直接下载

详细参数说明请查看 [skills/image-clarity-enhance/SKILL.md](skills/image-clarity-enhance/SKILL.md)。

### async-free-creation

异步自由创作，适用于根据提示词和可选参考图生成产品图或创意图片。

主要能力：

- 通过异步任务生成 1-20 张图片（默认 4 张）
- 支持参考图数组 `fileUrlList`，最多 6 张（旧字段 `apiImgUrlList` 仍兼容）
- 支持 `1:1`、`16:9`、`9:16` 等比例
- 默认走特惠通道（`promotion`），仅在用户明确要求时改传尊享通道 `premium`
- 使用新版任务查询接口轮询获取结果

模型类型：

| modelEdition | 模型 |
|--------------|------|
| `9` | Flyelep Image 2（默认） |
| `3` | Flyelep Nano 2 |
| `13` | Flyelep Image 2.5 |
| `14` | Flyelep Nano 2.1 |
| `15` | Flyelep Image 2.6 Flare |
| `16` | Flyelep Image 2.6 |

历史值 `2`、`4` 会自动按 `9` 处理。

接口入口：

- `POST /prod-api/poster-design/api/v1/poster/allAroundCreationAsync`
- `POST /prod-api/poster-design/api/v1/poster/queryTaskResult`

详细参数和轮询规则请查看 [skills/async-free-creation/SKILL.md](skills/async-free-creation/SKILL.md)。

### ai-writing-assist

AI 帮写，辅助生成创意文案，可用于优化用户提示词或获取创意灵感。

主要能力：

- AI 辅助生成创意文案
- 优化产品描述和提示词
- 支持图片和视频两种场景（`creativeType`：1 图片、2 视频），视频场景可出分镜脚本或口播脚本
- 返回多个创意选项供选择

接口入口：

- `POST /prod-api/poster-design/api/v1/aiTool/assistedGeneration`

详细参数和文案结构说明请查看 [skills/ai-writing-assist/SKILL.md](skills/ai-writing-assist/SKILL.md)。

### gen-hot-image

爆款图片复刻，基于爆款参考图的风格生成产品复刻图。

主要能力：

- 复刻爆款图片风格
- 将产品素材融合到爆款视觉中
- 支持多种比例和语言
- 异步接口，需轮询获取结果

接口入口：

- `POST /prod-api/poster-design/api/v1/aiTool/generateHotImage`
- `POST /prod-api/poster-design/api/v1/poster/queryTaskResult`

详细参数、模型类型和轮询规则请查看 [skills/gen-hot-image/SKILL.md](skills/gen-hot-image/SKILL.md)。

### gen-hot-video

爆款视频复刻，基于爆款参考视频的风格生成产品复刻视频。

主要能力：

- 两种模式：创意复刻（参考风格和分镜重新生成）、1:1 复刻（照搬原片镜头与节奏，替换商品、模特、服饰、人脸或背景）
- 支持 `pro`/`fast`/`ultra`/`mini` 四种模型档位，分辨率 480p 到 4K
- 1:1 复刻按原片时长成片（最长 60 秒），比例跟随原片
- 可先把抖音、TikTok、小红书等分享链接识别成视频地址，再作为原片复刻
- 异步接口，需轮询获取结果

接口入口：

- `POST /prod-api/poster-design/api/v1/aiTool/generateHotVideo`
- `POST /prod-api/poster-design/api/v1/aiTool/parseShortVideo`（分享链接识别）
- `POST /prod-api/poster-design/api/v1/poster/queryTaskResult`

详细参数、模型类型和轮询规则请查看 [skills/gen-hot-video/SKILL.md](skills/gen-hot-video/SKILL.md)。

### generate-video

通过 Flyelep 异步生成视频 API，根据文本提示词生成产品视频或创意视频，适用于产品展示视频、品牌宣传视频、种草视频等场景。

主要能力：

- 根据文字描述和参考图、参考视频或首尾帧，异步生成 1 条商品视频或创意视频
- 自由创作可以纯文生视频，其余类型至少提供参考图、参考视频或首帧之一
- 可选分辨率随模型不同（最高 4K，h3 为 768p/2K），比例支持 1:1/16:9/9:16 等
- 电商视频最长 60 秒；首尾帧模式和自由创作最长 15 秒（ultra 为 30 秒）
- 支持生成或关闭配音音频，口播视频自动开启配音
- 异步接口，需轮询获取结果

接口入口：

- `POST /prod-api/poster-design/api/v1/poster/generateVideo`
- `POST /prod-api/poster-design/api/v1/poster/queryTaskResult`

模型类型：

- `pro`：`Flyelep Dance 2.0`（高质量，默认）
- `fast`：`Flyelep Dance 2.0 Fast`（快速生成）
- `ultra`：`Flyelep Dance 2.5`（最高画质）
- `mini`：`Flyelep Dance 2.0 Mini`（轻量）
- `wan`：`Wan 3`
- `h3`：`H3`

视频业务标签：

- `主图视频`：产品主图展示（默认）
- `种草视频`：产品种草推荐
- `品牌TVC`：品牌形象宣传（旧值 `品牌宣传` 仍兼容）
- `口播视频`：真人口播讲解
- `自由创作`：不限题材，可纯文生视频

详细参数说明、素材规则和轮询策略请查看 [skills/generate-video/SKILL.md](skills/generate-video/SKILL.md)。

### file-upload

把本地图片、视频、音频文件上传到云存储，返回公网可访问的直链，用于为其它技能准备素材入参。

主要能力：

- 上传本地图片、视频、音频，换回公网可访问的 URL
- 返回的直链不带签名，按 24 小时限时链接对待，拿到后直接用于本次调用，不要长期保存
- 图片在上传前自动执行内容审核，视频和音频不审核；进桶的是原始文件，不会被压缩降质
- 上传不消耗算力，对象会重命名为 UUID，原文件名不进 URL，中文名可直接上传

接口入口：

- `POST /prod-api/poster-design/api/v1/file/upload`

请求方式为 `multipart/form-data`，文件字段名为 `file`，单次只能上传一个文件。

支持格式：

- 图片：`bmp`、`gif`、`jpg`、`jpeg`、`png`
- 视频：`mp4`、`mov`、`m4v`、`webm`、`avi`、`mkv`
- 音频：`mp3`、`wav`、`m4a`、`aac`、`ogg`、`flac`

详细参数说明和错误处理请查看 [skills/file-upload/SKILL.md](skills/file-upload/SKILL.md)。

## 使用建议

- 所有技能均以各自目录中的 `SKILL.md` 为准
- 对于需要高稳定性的调用，优先使用可公网访问、格式规范的图片直链
- 用户提供的是本地文件而非直链时，先用 `file-upload` 上传换取直链，再调用其它技能
- 涉及素材入参的技能都在自己的 `SKILL.md` 里内联了「本地文件上传」章节作为兜底，只单独安装某一个技能也能完成上传；**上传接口若有变动，需同步更新这些章节**
- 对于场景替换、商品替换、商品换色这类生成型接口，建议尽量同时提供清晰原图和明确的文本描述

## License

MIT
