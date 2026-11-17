---
name: ai-media-kit-pro
version: "1.0.0"
display_name: AI 音视频图片智能处理
display_name_en: AI Media Processing Toolkit
description: "音视频与图片的 AI 智能处理工具包：字幕擦除、视频画质增强、语音转字幕(ASR)、视频 OCR、人脸打码、语义切片、人声背景音分离、图像画质增强、图像擦除去水印，共 9 个能力。按次计费、按能力与素材时长/张数动态定价，通过支付宝扫码付款。"
description_zh: "音视频与图片的 AI 智能处理工具包：字幕擦除、视频画质增强、语音转字幕(ASR)、视频 OCR、人脸打码、语义切片、人声背景音分离、图像画质增强、图像擦除去水印，共 9 个能力。按次计费、按素材规格动态定价，支付宝扫码即用。"
description_en: "AI toolkit for audio, video and image processing: subtitle erasure, video quality enhancement, ASR subtitles, video OCR, face blurring, semantic segmentation, vocal separation, image enhancement and watermark erasure — 9 capabilities with per-use dynamic pricing via Alipay."
permissions:
  - shell
metadata:
  requires:
    bins: ["curl", "openssl"]
  product: amk-gateway
  domain: media
  capability_count: 9
---

# AI MediaKit 音视频/图片智能处理

网关 `${GW}` = `https://amk.pidiyun.com`。一次请求处理一个素材。共 9 个能力，按能力类型与素材规格**动态计价**（时长按分钟、图片按张），通过支付宝扫码付款。多素材分别建立任务并说明各自费用，等待用户授权后逐一处理。

## 能力清单与计价

| 能力 | `tool` | 类型 | 素材 | 计价口径 |
|---|---|---|---|---|
| 字幕擦除 | `erase-subtitle` | 视频·异步 | 视频 | 按擦除时长 |
| 视频画质增强（极速） | `enhance-video-fast` | 视频·异步 | 视频 | 按输出时长 |
| 语音转字幕 ASR | `asr-subtitles` | 视频·异步 | 视频 | 按输入时长 |
| 视频 OCR（识别硬字幕） | `video-ocr` | 视频·异步 | 视频 | 按输入时长 |
| 视频人脸打码 | `face-blur-video` | 视频·异步 | 视频 | 按输入时长 |
| 智能语义切片 | `semantic-segment` | 视频·异步 | 视频（≥30 秒） | 按输入时长 |
| 人声背景音分离 | `separate-voice` | 音频·异步 | 视频（含画面，纯音频暂不支持） | 按输入时长 |
| 图像画质增强 | `enhance-image` | 图像·**同步** | 图片 | 按张 |
| 图像擦除去水印 | `erase-image` | 图像·**同步** | 图片 | 按张 |

- **异步能力**：提交返回 `task_id`，需轮询查询，完成后交付结果 URL。
- **同步能力**（图像）：提交即返回结果，直接交付 `result_url`，无 `task_id`。
- **动态计价**：每个能力的实际金额由网关按其成本模型算出（视频/音频按时长，图像按张），下单后以网关返回的 `amount` 为准，**不要**按本清单或任何固定数字向用户报死价；向用户说明「按素材规格计价」，并以 402 账单里的金额为最终价格。

## 调用前

说明素材会上传对象存储并交由火山引擎处理，不承诺固定时间删除。

支付依赖支付宝官方买家组件 `alipay-bot`（来自 `@alipay/agent-payment`），以及官方 `alipay-payment-skill` 和 `alipay-authenticate-wallet`。调用前确认 CLI 可用、客户端能够加载这两个 Skill；执行支付时遵循 `alipay-payment-skill`，仅在支付流程明确返回需要开通或授权钱包时，才切换到 `alipay-authenticate-wallet`，不要主动用钱包检查拦截支付，不凭工具名称猜测付款协议。

这些组件属于买家运行环境的依赖，无需每个任务重复安装。若缺少依赖，停止上传与下单，提示由环境维护者或具备安装权限的 Agent 按官方说明安装（官方安装入口：`npx -y @alipay/agent-payment@latest install`），不擅自安装。客户端无法执行安装命令或加载官方 Skill 时，应明确说明当前环境尚不具备支付条件，不承诺自动完成安装。

首次使用时，官方支付组件会自动把「开通钱包 + 付款」合并为一次扫码（「授权并支付」），无需也不应手动拆分「先开通钱包、再付款」两步。买家与卖家使用不同的支付宝账号，避免同一账号付款被拒绝。

每个任务生成并保存请求 ID 与访问令牌：

```bash
REQUEST_ID="$(openssl rand -hex 16)"
REQUEST_TOKEN="$(openssl rand -hex 32)"
```

首次提交、支付后重试、查询均复用原 ID、令牌和请求体；令牌不向无关人员展示。改变素材或能力必须新建任务。

## 上传素材

已有公网 HTTP/HTTPS 素材 URL 可直接使用。本地文件请求：

```http
POST /api/upload-url
Content-Type: application/json

{"request_id":"原请求ID","ext":"png"}
```

`ext` 使用真实文件扩展名（视频用 mp4/mov 等，图片用 png/jpg 等，音频用 mp3/wav 等）。返回 `put_url`、`tos_url` 和 `headers`；用 PUT 上传原素材，带上返回的全部 headers（包括 `x-tos-forbid-overwrite: true`）。上传后使用 `tos_url`。上传链接有效期不是文件删除期限。

## 提交与支付

```http
POST /api/jobs
Content-Type: application/json
X-Request-Token: <原访问令牌>

{"request_id":"原请求ID","tool":"<能力名>","video_url":"<素材URL>"}
```

- `tool` 从「能力清单」中选择。
- `video_url` 是现有网关的通用素材字段，视频/图片/音频都放这里。
- `resolution`（如 `1080p`）仅 `enhance-video-fast` 可选传，其他能力不要传；第一版不接受额外 `params`。

- **402**：保存订单号与完整 `Payment-Needed` 账单。核对 `amount` 币种为 CNY；金额异常（与素材规格明显不符、或为负/超范围）则停止付款并说明配置异常。把账单、原始请求方式、URL、请求体及 `X-Request-Token` 交给官方支付能力，展示价格并等待用户授权。
- 支付后由官方支付能力携带完整 `Payment-Proof` 重试原请求。保留其中的支付凭证、交易号和客户端会话信息，不自行编造、裁剪或重新签名。
- **200**：检查业务状态，只有 `completed` 才交付结果；不能把已提交或处理中视为完成。同步图像能力返回即 `completed`。
- **409**：参数不一致时恢复原参数；任务忙时等待至少 5 秒再查询。
- **422**：素材不满足所选能力的处理条件（如语义切片要求视频不短于 30 秒）。未产生订单、未收款，向用户说明原因，换素材或换能力后新建任务。
- **503 / 网络超时**：保留原任务标识，先查询或重试；不另建订单，不断言已退款。
- **404**：核对原请求 ID 和令牌，无法恢复时联系服务方，不重复付款。

已付款但结果不明时优先查原订单。账单失效须先由官方支付能力确认原订单状态；确认未支付后再获取新账单，防止重复扣款。成功路径不另行追加买家回执。

遇到 `PROXY_TARGET_BLOCKED`、`request expired`、“请勿重复绑定”或支付查询失败时，按 [支付异常排查](reference/payment-troubleshooting.md) 处理；具体支付宝命令与停止条件仍遵循当前安装的官方支付 Skill。

## 查询与交付

用户表示“支付成功”“已支付”或要求继续待确认支付时，先交由官方支付 Skill 查询当前支付单，并携带原请求方式、URL、请求体和业务 headers 恢复资源请求。用户口述付款成功或网关返回 `pending` 都不能代替支付宝支付状态。只有商户业务状态为 `completed` 才交付结果。

```http
GET /api/jobs/<原请求ID>
X-Request-Token: <原访问令牌>
```

需要等待时每 5–10 秒查询一次：

- `completed`：展示结果 `result_url` 及可用 `outputs`，提供下载链接并提醒及时保存，链接有时效。异步能力如字幕、切片、分离可能返回多个文件（如人声/背景音两路、多个片段），逐一列出。
- `submitted/queued/running/processing`：继续等待。
- `failed/canceled/cancelled`：查看 `order_status`；仅 `refunded` 可告知退款完成。
- `refund_pending/refund_processing`：退款尚未完成，可继续查询。
- `manual_review/refund_failed`：停止自动操作，保留订单号联系服务方。

服务器负责验付、履约与退款恢复；用户退出对话不等于取消订单。

## 素材规格与限制

- 视频：常见 mp4/mov/mkv 等，单文件大小与时长上限以上游实际返回为准，超限时如实说明，不承诺必然处理成功。**语义切片要求视频时长不短于 30 秒**，过短视频会被网关直接拒绝（422，不产生订单）。
- 图片：PNG、JPG、JPEG、WebP 等，单张不超过 10 MB；图像增强为固定 2 倍放大，宽高放大后不超过上游像素上限。
- 音频：人声背景音分离当前**仅支持视频类素材（含画面）**，纯音频文件（mp3/wav/m4a 等）暂不支持，收到纯音频请求时如实说明并建议改用带画面的视频；分离结果返回人声与背景音两路音频。
- 尺寸、格式、时长无法确认时如实说明，不承诺必然成功；结果保留上游输出格式。
