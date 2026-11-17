# 各平台审计知识库

按厂商的「如何判定模型免费」策略、已知免费模型、排除项与能力标记。这是免费模型审计员依赖的隐性知识——
通用 `/v1/models` 调用无法获得。

> **安装即用 / 路径自动识别**：本技能不依赖任何写死的绝对路径。启动时由
> `references/resolve_paths.py` 自动探测两处路径——配置根（按 `WORKBUDDY_CONFIG_DIR` →
> `CODEBUDDY_CONFIG_DIR` → `~/.workbuddy` 回退，指向 `models.json`）与工作区根（agent 当前 cwd
> 或 `--workspace` 参数，指向审计报告 + 每日日志）。**接手的其他用户无需改动任何路径配置**即可
> 直接运行；仅当 `models.json` 探测不到时才会向你询问具体路径。

## 海外主机集合（触发 SKILL.md 中的 VPN 门禁）

| 主机 | 厂商 | 需 VPN/代理 |
|---|---|---|
| `generativelanguage.googleapis.com` | Google Gemini | **需要**（地域封锁） |
| `integrate.api.nvidia.com` | NVIDIA NIM | 受限网络下需要（经 `127.0.0.1:7897` 走代理） |

其余厂商均为国内（中国部署），无需 VPN。

---

## 1. Google Gemini

- **端点**：`https://generativelanguage.googleapis.com/v1beta/openai`（OpenAI 兼容）。
  ⚠️ 路径**必须**是 `/v1beta/openai`；只用 `/v1beta` 会让 WorkBuddy 拼出错误 URL。
- **海外**：是 → 适用 VPN 门禁。
- **免费判定**：无目录计费字段。免费模型为公开的 `gemini-*-flash` 档位与 `*-latest` 自动跟随别名。
  通过对已知 flash 集 + 任何新的 `gemini-<ver>-flash` / `gemini-*-latest` 别名做实测来发现。
- **已知免费（已注册 8 个）**：代表性 id —— `gemini-3.1-flash-lite`、
  `gemini-3.5-flash`、`gemini-3.7-flash`、`gemini-3-flash-preview`、`gemini-flash-latest`、
  `gemini-flash-lite-latest`（另有两种 flash 变体）。确切当前集合以实时 `models.json` 为准——
  不要在这些模式之外硬编码。
- **能力**：flash-vision 档位 `supportsImages: true`；`supportsReasoning: false`
  （Gemini flash 不输出 `reasoning_content`）。
- **注意**：(1) `/v1beta/openai/models` 返回 **400**——OpenAI 兼容端点不支持模型*枚举*，故 `catalog`
  无法列出 Google 模型；改用已知 flash 集 + 活体 `test` 发现。(2) 即使走代理，某些网络仍地域封锁
  （`400` "User location not supported"）——这是**地域产物；绝不可据此移除模型**；保留并在可接受的
  网络区域验证。(3) 沙箱可能拦截 `googleapis`；改用沙箱绕过或系统代理重试。
- **2026-09-04 实测环境诊断（重要）**：在 WorkBuddy 沙箱内，`generativelanguage.googleapis.com`
  **全协议不可达**，且与宿主机 VPN 无关：① 经内部代理 `127.0.0.1:62526` → 一律 `502 Bad Gateway`
  （代理层封禁）；② 清除 `HTTPS_PROXY`/`HTTP_PROXY` + `ProxyHandler({})` 直连 → TCP 黑洞（进程挂起，
  socket 超时不起作用，被工具 SIGTERM）；③ 沙箱外（`dangerouslyDisableSandbox`）+ 清代理仍黑洞；
  ④ 同进程 NVIDIA 直连正常 → 对照排除全局断网。结论：沙箱网络策略阻断 googleapis，agent 进程出口
  不覆盖宿主机 VPN。**此乃连通性限制，非模型缺陷——8 条 Gemini 原样保留，不移除不降级。**
- **429 窗口重试模式**：早前曾拿到真实 `429`（限流），其重置窗口可由错误体读取（形如
  `将在 <时间> UTC+8 重置`）。当前黑洞疑为该 `429` 触发的 IP 层封锁，配额窗口重置后或恢复直连
  （与早前曾短暂直连成功拿到 404/429 一致）。实操：用 `references/google_audit.py`（自包含、强制清代理
  走宿主机网络、只产出 JSON 不改动 models.json）做补审；可挂一次性定时任务越过 429 窗口自动重跑，
  而非原地阻塞数小时。

## 2. NVIDIA NIM

- **端点**：`https://integrate.api.nvidia.com/v1`
- **海外**：是（受限网络下经代理走）。
- **免费判定**：目录（`/v1/models`，约 84 个模型）**不含计费字段**。通过**活体对话补全测试**判定：
  - `200` + 真实内容 → 免费 / 可用，**新增**。
  - `402` / `403` → 无免费额度 / 付费，**排除**。
  - `404` → 已列出但该免费端点未部署，**排除**。
  - **`410 Gone` → 已永久下线，且通常同时从 `/v1/models` 消失 → 移除**。2026-09-04 实测确认
    `openai/gpt-oss-120b`、`stepfun-ai/step-3.7-flash`、`nvidia/nemotron-3-nano-30b-a3b` 三条均为
    410，且已不在目录，已移除。
  - `000`（连接重置 / 读超时）→ 网络/VPN 产物，经代理重试；不做判定。
  - `5xx`（500/503）→ 服务端过载，**保留**；下一轮复查。
- **已知免费（已注册）**：`nvidia/nemotron-3-ultra-550b-a55b`（推理）、
  `nvidia/nemotron-3.5-lightning-30b-a3b`、`nvidia/nemotron-3-super-120b-a12b`、
  `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning`、`openai/gpt-oss-20b`、
  `deepseek-ai/deepseek-v4-flash-0731`、`minimaxai/minimax-m3`、`moonshotai/kimi-k3`、
  `meta/llama-3.2-11b-vision-instruct`（多模态）、`google/gemma-4-31b-it`、
  `mistralai/mistral-nemotron`、`meta/muse-glimmer-30b`、`poolside/laguna-xs-2.1`。
- **能力**：按模型设定；推理变体会输出 `reasoning_content`（`supportsReasoning: true`）。
- **注意**：
  - `kimi-k2.6`、`llama-3.1-nemotron-ultra-253b-v1`、`nemotron-4-340b-instruct`、
    `nemotron-nano-3-30b-a3b`、`mistral-nemo-minitron-8b-8k-instruct`、`phi-3.5-moe-instruct`
    等返回 `404`（账户未部署）。
  - 大体量模型（`deepseek-v4-flash-0731`、`deepseek-v4-pro-0813`、`llama-3.2-90b-vision-instruct`）
    常出现**读超时**，`TIMEOUT=120` 也可能不够；判定前至少重试 2–3 次（180s 超时）。
    2026-09-04 实测：`moonshotai/kimi-k3`、`google/gemma-4-31b-it`、
    `nvidia/nemotron-3-super-120b-a12b` 首轮超时/503、二轮即 200——**切勿据单轮超时移除**。
  - `mistralai/mistral-nemotron` 连续多轮 `500`：按规则保留，但在报告中标注「服务端持续错误」。
  - 目录里大量条目是 embedding / rerank / guardrail / 图像 / ASR / TTS（约 45 条），全部按
    「非对话接口」跳过；有效对话候选约 39 条。

## 3. SenseNova（商汤）

- **端点**：`https://token.sensenova.cn/v1/chat/completions`
- **海外**：否。
- **免费判定**：对 `GET https://token.sensenova.cn/v1/models` 返回的模型，当且仅当**所有计费值均为
  `"0"`** 时为免费。对**未出现在目录中**的模型（见目录说明，如 `kimi-k3` / `deepseek-v4-pro`），
  依官方 Token Plan 公告（0 元公测）+ 活体对话测试（200 + 内容 = 免费）判定。
- **目录**：`/v1/models` 端点历史上仅返回 **6 个「经典」模型**（4 个对话 + 2 个图像生成 `u1-fast` /
  `u1.5-lite`）。⚠️ **Token Plan 可能暴露不在 `/v1/models` 返回的额外对话模型**——截至 2026-08-28，
  `kimi-k3` 与 `deepseek-v4-pro` 可调用（0 元公测）但未出现在目录中。
  **2026-09-04 更新：目录已扩展为 8 条**（`sensenova-6.7-flash-lite`、`deepseek-v4-flash`、
  `glm-5.2`、`sensenova-u1-fast`、`sensenova-6.8-flash-lite`、`sensenova-u1.5-lite`、
  `deepseek-v4-pro`、`kimi-k3`），6 个对话模型 `pricing` 字段全为 `0`。
  仍应同时直接对文档给出的模型 id 做对话 `test`，**不要**只靠目录枚举。
- **已移除（2026-09-04）**：`sensenova-6.7-flash-lite` 连续 4 次 `404 model route not found`
  （跨约 20 分钟），目录仍标价 0 但 chat 路由已不存在，经用户确认移除。下轮若恢复可重新入库。
- **排除**：图像生成模型**不兼容对话补全 → 跳过**（与其他厂商非对话接口规则一致）。
- **能力**：对话模型的 `supportsImages` 因模型而异。
  ⚠️ **目录的 `input_modalities` 字段不可靠，不要直接照抄**。2026-09-04 实测：`kimi-k3` 在目录中
  `input_modalities` 仅 `["text"]`，但实测传入 base64 图像**正常接受并返回内容**。验证方式：
  发送 `image_url`（data URI，1×1 PNG 即可）+ 文本提问，看是否 400/报错。
- **空内容 ≠ 失效**：`sensenova-6.8-flash-lite` 等推理模型在 `max_tokens` 偏小时，额度被
  `reasoning_content` 耗尽，表现为「200 但 content 为空」。判定时用 `max_tokens ≥ 200`，
  或检查 `reasoning_content` 是否非空，勿据此判定失效。
- **端点级限流（可用性判据，2026-09-24 新增）**：SenseNova 免费 `deepseek-flash` 为共享免费公共端点，
  实测返回 `429 EndpointTPMExceeded` / `rps exhausted`——秒级（rps）与分钟级（TPM/RPM）额度极低，
  在 WorkBuddy 多请求对话模式下第一句成功后即 429，**不可用**，已据此从可用集剔除。该判据已写入
  SKILL.md：确立「**免费 + 存活 ≠ 可用**」，新增候选须叠加 `test_harness.py burst` 连续多请求不崩验证。

## 4. BigModel（智谱 GLM）

- **端点**：`https://open.bigmodel.cn/api/paas/v4`
- **海外**：否。
- **免费判定**：以官方计费文档为准。免费 flash 档位：
  `glm-4.7-flash`、`glm-4.6v-flash`（多模态/视觉）、`glm-4-flash-250414`、
  `glm-z1-flash`（推理）、`glm-5.3-flash`、`glm-4.5-flash`。
- **付费 / 排除**：`glm-5.3`（旗舰，付费——此处 `200` **仍会扣费**，勿添加）。`glm-4.6-flash` 返回
  `403`「无权访问」（跳过）。`glm-5.2-flash` / `glm-5.1-flash` / `glm-5-flash` 返回 `400`（不存在，跳过）。
- **能力**：`glm-4.6v-flash` → `supportsImages: true`；`glm-z1-flash`、`glm-5.3-flash`、
  `glm-4.5-flash` → `supportsReasoning: true`。
- **注意**：`429` = 限流，模型仍有效（保留）。

## 5. Agnes

- **端点**：`https://api.agnes-ai.cn/v1`
- **海外**：否。
- **免费判定**：`GET https://api.agnes-ai.cn/v1/models` 列出候选；以活体对话补全测试
  （`200` + 内容 = 免费）确认。
- **已知免费（已注册）**：`agnes-2.0-flash`、`agnes-2.5-flash`、`agnes-2.5-pro`、`agnes-2.5-pro-alpha`。
- **排除**：图像/视频模型（`agnes-image-*`、`agnes-video-*`）为非对话（跳过）。
- **待观察**：`agnes-2.5-pro-beta` 结果**不稳定**——2026-09-04 首轮 `200` 有内容、二轮 `404` 返回 HTML
  错误页。按「不确定不入库」处理，下一轮复查；若两轮一致通过再入库。
- **能力**：flash → `supportsReasoning: false`；pro → 按响应而定。

## 6. SiliconFlow（硅基流动）

- **端点**：`https://api.siliconflow.cn/v1`
- **海外**：否（国内）。
- **免费判定 — 特殊情况 ⚠️**：`/v1/models` **无计费字段**；**无余额查询端点**；且**新账户会获赠欢迎额度**，
  因此付费模型也返回 `200`。故此处 **`200` 不能证明免费**。是否免费**只能**依据 SiliconFlow 官方「免费」标记：
  - 计费页（`siliconflow.cn/pricing`）将某模型标记为「免费」。
  - 社区 `free-model.com` 的 SiliconFlow 免费清单。
  - 已验证的「X 系列免费」公告（如「Qwen3 系列免费」）。
  活体测试**仅用于确认可达性 + 内容**，绝不据此推断免费状态。
- **已知免费对话/视觉（已注册 8 个，2026-09-04 核定）**：`deepseek-ai/DeepSeek-R1-0528-Qwen3-8B`（推理）、
  `Qwen/Qwen3-8B`、`Qwen/Qwen2.5-7B-Instruct`、`THUDM/GLM-Z1-9B-0414`（推理）、
  `THUDM/GLM-4-9B-0414`、`tencent/Hunyuan-MT-7B`（翻译）、`deepseek-ai/DeepSeek-OCR`（视觉）、
  `PaddlePaddle/PaddleOCR-VL-1.5`（视觉）。
  外部佐证：2026-07-07 定价快照列出上述前 6 条为「¥0 免费档」；2026-08-21 快照确认
  `GLM-Z1-9B-0414`、`GLM-4-9B-0414`、`Hunyuan-MT-7B`、`PaddleOCR-VL-1.5` 输入输出免费。
- **已移除（2026-09-04，用户裁决）**：`Qwen/Qwen3-14B`、`Qwen/Qwen3-32B`、
  `Qwen/Qwen3-30B-A3B-Instruct-2507`。三者实测均 `200` 可用，但**无任何官方免费标记**；外部定价快照
  显示 `Qwen/Qwen3-32B` 为付费（输入 ¥1 / 输出 ¥4，每百万 token）。
  ⚠️ 今后**不得**仅凭「Qwen3 系列免费」这类宽泛来源重新入库这三条——必须找到逐条 ¥0 标记。
- **排除（非对话）**：`BAAI/bge-*`（embedding/reranker）、`Qwen3-Embedding/Reranker`、`Qwen-Image`、
  `Kolors`、`Wan`、`CosyVoice`、`SenseVoice`（图像/语音）——不兼容对话 schema，即便免费也跳过。
- **排除（付费/前沿）**：`DeepSeek-V4-Flash/Pro`、`LongCat-2.0`、`GLM-5.2`、`Kimi-K2.7-Code`、
  `MiniMax-M2.5`、`Qwen3.5*/Qwen3.6*`、`Step-3.5-Flash`、`Seed-OSS-36B`（计费，需充值）→ 跳过。

## 7. AMD Radeon Cloud（Token Factory）

- **端点**：`https://developer.amd.com.cn/radeon/api/v1`（OpenAI 兼容；亦支持 Anthropic `/v1/messages`，但本注册表仅用 OpenAI chat 形态）。
- **海外**：否（中国区部署，国内直连，**无需 VPN**）。
- **免费判定**：AMD Radeon Cloud 的「Public Free Model APIs」为官方免费档。判定依据：① 官方 Token Factory 控制台对模型标注的 `FREE` 标记；② 活体认证——返回 `200`/`429`（限流）而非 `401`（鉴权失败）即视为 Key 有效、模型可达，可入库。`/v1/models` 目录枚举正常，但免费档清单以控制台 `FREE` 标记为准。
- **已知免费（2026-09-11 核定，5 个；全部 OpenAI 兼容、同一把全局共享 Key 通吃）**：
  - `DeepSeek-V4-Flash`（LLM，**1M 上下文**）
  - `DeepSeek-V4-Flash-0731`（LLM，DeepSeek V4 Flash 0731 版本）
  - `DeepSeek-V4-Flash-Vision-Exp`（**VLM，支持图像输入** `supportsImages: true`）
  - `Qwen3.8-Flash-Next`（**VLM，256K 上下文**，支持图像输入）
  - `MiniCPM5-1B`（LLM，轻量）
  - 以上官方声明均支持 Streaming / Tool Calling / Thinking（思维链）→ `supportsToolCall: true`。
- **排除（无图像/视频生成）**：AMD 免费档**不含任何 text-to-image / text-to-video 模型**；VLM 仅做图像*理解*（输入），不产出图像或视频。因此**不接入** free-media-gen 的生图/生视频端点；如用户问及，明确告知免费档无此类入口。
- **限流（实测重要）**：单 IP 120 RPM、单 Key 30 RPM、账户网关 **20 RPM**（平均每 ≥3s 一次）。调用/审计务必降速；遇 `429`（`ip_rate_limit_exceeded`）→ **保留模型、退避后重试**，绝不据此判定失效。免费额度按 token 计数（账户每日约等值 $10，次日凌晨重置），高并发会触发限流。
- **能力标记约定**：推理 `supportsReasoning` 依模型而定——DeepSeek 家族设 `true`，Qwen/MiniCPM 视实测；视觉模型 `supportsImages: true`。`maxInputTokens`：DeepSeek 系列 1,048,576；Vision-Exp 128,000；Qwen3.8 262,144；MiniCPM5 32,768。
- **Key 形态**：每账户一把全局共享 Key（Token Factory 控制台一键复制），所有免费模型共用同一 `apiKey`——新增同厂商模型时复用即可。

## 跨厂商通用规则

- **始终排除非对话接口**：embedding / reranker / image-generation / ASR / TTS。
- **`429` 保留**（限流，仍有效）。
- **`000` 绝不移除**（网络/VPN 产物）。
- **推理模型**：活体测试分配 `max_tokens ≥ 80`，否则输出空白。
- **新增同厂商模型时**，复用注册表中已有条目的厂商 `apiKey`。
