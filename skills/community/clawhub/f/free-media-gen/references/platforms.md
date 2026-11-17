# 免费媒体模型平台参考（free-media-gen）

记录各平台媒体生成端点的真实形态、限流、与水印/取片等 quirks。供 `media_auditor.py` 与各生成脚本使用。
**所有路径与参数均来自官方文档或 2026-08-28 实测验证**，与 `config.json`、`model_catalog.md` 保持一致。

> 与 `free-model-auditor` 的约定一致：**`models.json` 内全部是对话补全模型，媒体生成模型不在其中**。
> 本技能通过 `config.json` 的 `api_key_ref` 复用其平台密钥，但调用的是独立的
> `/v1/images/generations` 或 `/v1/videos` 端点。

---

## Agnes（国内版 api.agnes-ai.cn / 国际版 api.agnes-ai.com，账号不互通）

### 图像
- 端点：`POST https://api.agnes-ai.cn/v1/images/generations`
- 入参：`{"model": <id>, "prompt": <str>, "n": 1, "size": "1024x1024"}`
- 响应：`data[0].url`（图片直链），脚本下载到 `generated-images/`
- **实测可用模型（2026-08-28 查 `/v1/models`）**：仅 **`agnes-image-2.1-flash`**
- ⚠️ **`agnes-image-2.0-flash` 不存在**：平台目录未列出，调用持续返回 **503**，已移入排除名单
- 国内站免 VPN；繁忙时 503 属瞬态，脚本内置指数退避

### 视频 —— 两套互不兼容的接口，脚本按 model 自动分支

**【A】`agnes-video-2.5-flash`（新版）**
- 创建：`POST https://api.agnes-ai.cn/v1/videos`
- 入参：`{"model","prompt","mode","seconds","size","aspect_ratio","n"}`
  - `mode` **必填**：`text` | `keyframe`（需 first_frame/last_frame）| `reference`（images≤5）
  - `size` 固定字符串 `"720P"`；`seconds` 字符串 `"4"`–`"12"`；`aspect_ratio` 默认 `16:9`
- 响应：`{"id","task_id","video_id"}`
- 轮询：`GET /agnesapi?video_id=<vid>&model_name=agnes-video-2.5-flash` → `status == "completed"`
- 计费：限时免费（原价 ¥0.15/秒，现价 ¥0/秒）

**【B】`agnes-video-v2.0`（旧版）**
- 创建：`POST https://api.agnes-ai.cn/v1/video/generations` → `{"task_id","video_id"}`
- 轮询：`GET /v1/video/generations/<task_id>` → `data.status == "SUCCESS"`

**取片（两者通用，务必两步）**
1. 拿到 `video_id`（**≠ task_id**；若创建响应未返回，用 `GET /v1/videos/<task_id>` 取）
2. `GET https://api.agnes-ai.cn/agnesapi?video_id=<video_id>&model_name=<模型id>`
   → `metadata.url` 即 MP4 直链
3. **必须带 `model_name`**，否则响应不返回 `metadata.url`（这是旧脚本一直取不到片的根因）
4. 下载直链为 MP4

> 注意：公共 API 提交的任务**不在网页控制台展示**，取片只能走上述 API，不要去控制台找。
> 另：`/v1/models` 目录端点**必须保留 `/v1` 前缀**，剥离后返回 403。

---

## 商汤 SenseNova（token.sensenova.cn）

- 端点：`POST https://token.sensenova.cn/v1/images/generations`（OpenAI 图像接口兼容）
- 入参：`{"model","prompt","n","size","watermark"}`，`watermark=false` 可去水印
- **实测差异（两个模型行为不同）**：

| 模型 | 实测响应 | 尺寸要求 | 默认 |
|---|---|---|---|
| `sensenova-u1.5-lite` | 返回 **`b64_json`** | 接受 `1024x1024` | 1024x1024 |
| `sensenova-u1-fast` | 返回 **图片 URL** | **严格白名单**，`1024x1024` 会 400 | 2048x2048 |

- `u1-fast` 合法尺寸：`1664x2496 / 2496x1664 / 1760x2368 / 2368x1760 / 1824x2272 /
  2272x1824 / 2048x2048 / 2752x1536 / 1536x2752 / 3072x1376 / 1344x3136 / 2560x720 / 3072x864`
- 免费：公测免费（约每 5 小时 1500 次）；国内免 VPN；与混元（腾讯）无关

---

## 硅基流动 SiliconFlow（api.siliconflow.cn）

- 端点：`POST https://api.siliconflow.cn/v1/images/generations`
- 免费模型：`Kwai-Kolors/Kolors`（实测返回图片 URL）
- 入参同时带 `image_size` 与 `size`，兼容不同版本
- **排除**：`Qwen/Qwen-Image` 为付费（¥0.3/张）；`Qwen-Image-Edit*` 为编辑类且付费
- 目录端点需保留 `/v1` 前缀（`https://api.siliconflow.cn/v1/models`），剥离会 404

---


## 排除清单

| 模型 | 平台 | 排除原因 |
|---|---|---|
| `agnes-image-2.0-flash` | Agnes | 平台 `/v1/models` 目录**不存在**该模型，调用持续 503 |
| `agnes-video-2.5`（非 Flash） | Agnes | 付费 ¥0.15–0.35/秒 |
| `Qwen/Qwen-Image` | 硅基流动 | 付费 ¥0.3/张 |
| `Qwen/Qwen-Image-Edit(-2509)` | 硅基流动 | 图像编辑类且付费，非纯文生图 |
| 智谱 BigModel 系列 | 智谱 | 收费状态不确定，按决策排除 |
| 全部 NVIDIA / 文本对话模型 | NVIDIA 等 | 无媒体生成能力 |
