# 已知免费媒体模型目录（free-media-gen）

本清单是审计与首装引导的权威参考，与 `config.json` 保持同步。
最后实测日期：**2026-09-04**（含活体生成复检 + 官方定价页核对）

## 一、纳入（免费可用）

| 模型 | 平台 | 模态 | 免费 | 需 VPN | 状态 | 特点 | 二级命令 |
|---|---|---|---|---|---|---|---|
| `agnes-image-2.1-flash` | Agnes | 图 | ✅ | 否 | **verified** | 官方定价页 Current price = $0；09-04 复检 HTTP 200 | 用 Agnes 生图 |
| `agnes-image-2.5-flash` | Agnes | 图 | ✅ | 否 | **verified** | 09-04 新增；官方 Current price = $0；活体实测 200 | 用 Agnes 生图 |
| `agnes-video-v2.0` | Agnes | 视频 | ✅ | 否 | **verified** | 官方「currently free」；异步两步取片；旧版 `/video/generations` 端点 | 用 Agnes 生视频 |
| `agnes-video-2.5-flash` | Agnes | 视频 | 限时免费 | 否 | verified | 仅 720P、≤5 参考图；新版 `/v1/videos`（必填 mode/size/seconds/aspect_ratio）。⚠ 09-04 提交遇 429 限流（非失效） | 用 Agnes 生视频 |
| `sensenova-u1.5-lite` | 商汤 | 图 | ✅ | 否 | **verified** | 目录 `pricing.image=0` 确认免费；可 `watermark=false` 去水印；返回 b64_json | 用商汤生图 |
| `sensenova-u1-fast` | 商汤 | 图 | ✅ | 否 | **verified** | 目录 `pricing.image=0` 确认免费；返回 URL；size 有白名单（1024x1024 会 400，默认 2048x2048） | 用商汤生图 |
| `Kwai-Kolors/Kolors` | 硅基流动 | 图 | ✅ | 否 | verified（账户受限） | 官方定价「免费」。⚠ 09-04 复检 HTTP 402 `account balance is insufficient`（账户余额不足，非模型失效），充值后可用 | 用 Kolors 生图 |

## 二、当前不可用 / 已转付费（不列入主清单）

| 模型 | 平台 | 原因（核实依据） |
|---|---|---|
| `gemini-3.1-flash-image-preview` | Google | 已整体移除：免费配额为 0（`429 RESOURCE_EXHAUSTED, limit: 0`，原生端点 `401 API_KEY_SERVICE_BLOCKED`）；09-04 在 VPN 下复测仍 429，按用户指令从技能整体删除 |
| `Tongyi-MAI/Z-Image-Turbo` | 硅基流动 | **付费 ¥0.10/张**（官方定价页）。09-04 审计发现并剔除 |
| `Tongyi-MAI/Z-Image` | 硅基流动 | **付费 ¥0.30/张**（官方定价页）。09-04 审计发现并剔除 |
| `baidu/ERNIE-Image-Turbo` | 硅基流动 | **付费 ¥0.11/张（≈$0.015）**（官方定价页）。09-04 审计发现并剔除 |
| `agnes-image-2.0-flash` | Agnes | 平台 `/v1/models` 目录中已不存在（09-04 复核仍无此模型） |
| `agnes-video-2.5`（非 Flash） | Agnes | 付费，按分辨率 $0.025–0.055/秒 |
| `Qwen/Qwen-Image` | 硅基流动 | 付费，¥0.3/张 |
| `Qwen/Qwen-Image-Edit(-2509)` | 硅基流动 | 图像编辑类且付费，非纯文生图 |
| 智谱 BigModel 系列 | 智谱 | 收费状态不确定，按决策排除 |

## 三、首装引导：免费 API 申请地址

当用户无任何可服务媒体模型的平台密钥时，输出以下引导：

| 提供商 | 免费媒体能力 | 申请地址 |
|---|---|---|
| Agnes | 图 + 视频 | https://agnes-ai.cn （国内版） |
| 商汤 SenseNova | 图（U1.5 Lite / U1 Fast） | https://www.sensenova.cn |
| 硅基流动 SiliconFlow | 图（Kolors 免费） | https://cloud.siliconflow.cn |

## 四、实测要点（避坑）

1. **活体测试 ≠ 免费**（最重要）。`media_auditor.py` 的活体测试只证明"能调用出图"，不证明免费。09-04 教训：脚本据此把 3 个 SiliconFlow 付费模型（¥0.10–0.30/张）误标为 `free:true`。已修复——自动新增一律 `free:false / status:unverified`，须人工核对官方定价页后手动转正。
2. **硅基流动目录不含定价字段**。其 `/v1/models` 仅返回 `id/object/created/owned_by`，无法据此判断免费；必须查官方定价页 https://www.siliconflow.cn/pricing 。
3. **商汤目录含 `pricing` 字段**。`pricing.image="0"` 即免费，可自动判定。
4. **Agnes 定价以官方页为准**。image 2.0/2.1/2.5-flash 全系 Current price = $0；video v2.0 currently free；video 2.5-flash 列 $0.025/秒（list price），实测仍走免费额度（429 提示 "free users"）。
5. **账户余额不足会让免费模型也 402**。SiliconFlow 账户余额为 0 时，连官方标"免费"的 Kolors 也返回 `402 account balance is insufficient`——这是账户级问题，不要据此判定模型失效或删除条目。
6. **429 是限流不是失效**。Agnes 免费额度限流返回 429 并提示升级 Token Plan，退避重试即可，切勿删除条目。
7. **Agnes 视频取片必须两步**：`GET /v1/videos/<task_id>` 取 `video_id`（≠ task_id），再 `GET /agnesapi?video_id=<vid>&model_name=<model>` 取 `metadata.url`；**必须带 `model_name`**，否则不返回直链。
8. **Agnes 视频两套接口**：v2.0 走旧版 `{base}/video/generations`；2.5-flash 走新版 `{base}/videos`（必填 `mode`/`size`/`seconds`/`aspect_ratio`）。
9. **目录端点须保留 `/v1` 前缀**。Agnes 剥离 `/v1` 会 403，SiliconFlow 会 404。
10. **商汤返回体**：U1.5 Lite 返回 `b64_json`（非 URL），脚本需处理两种形态。
11. **瞬态 503**：Agnes 中国站繁忙时会 503，脚本内置指数退避，必要时加大重试。
