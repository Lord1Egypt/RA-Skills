---
name: cn-model-gateway
description: "国产大模型统一 MCP 服务器，通过标准 JSON-RPC 2.0 协议为 Claude Code / Cursor / Cline 等 Agent 框架提供 DeepSeek、通义千问、智谱 GLM、Kimi、腾讯混元、火山豆包、MiniMax、零一万物、百川智能、阶跃星辰十家模型的统一调用接口。11 个 MCP 工具（ask_model/describe_image/embed_text/rerank/audio_transcribe/video_understand/batch_submit/batch_result/list_providers/health_check/health_report）+ 单一网关状态资源 + 2 个 prompt 模板。内置统一错误映射（v1.9.0 新增 429/451/余额不足/内容审查四类错误 + 中文处置建议）、流式 SSE 输出+心跳保活+断线重连、每日健康晨报 + 厂商变更雷达（3σ 异常检测）、使用量统计、硬件感知并发控制、SQLite WAL 批量任务队列、自动故障转移、环境变量优先读取 API key。支持 Function Calling、多模态视觉、5 个非 MCP 框架适配器（LangChain/AutoGPT/CrewAI/Coze/Dify）、性能基准测试和 Token 价格追踪。config.json 填写 api_key 即可启动，无需 GPU、不做微调、不做私有部署，只做标准 MCP 协议网关。"
version: 1.9.0
---


# 国产模型 MCP 服务器

CN Model Gateway 是一个**纯 Python、零运行时依赖**的国产大模型统一 MCP 服务器。它启动后通过 stdio 暴露标准 JSON-RPC 2.0 接口，让任何兼容 MCP 的 Agent 框架（Claude Code、Cursor、Cline、n8n、Claude Desktop 等）一站式调用 DeepSeek、通义千问、智谱 GLM、Kimi、腾讯混元、火山豆包、MiniMax、零一万物、百川智能、阶跃星辰十家模型。

**核心定位：只做 MCP 协议网关。**

- ❌ 不做本地模型推理 / GPU 部署
- ❌ 不做模型微调 / 训练
- ❌ 不做私有部署版 SaaS
- ✅ 只做标准 MCP 协议接口，把各家模型统一封装成 MCP tools/resources/prompts

---

## 适用场景

| 场景 | 说明 |
|------|------|
| 你想在 Claude Code / Cursor / Cline 里一键切换 DeepSeek / 通义 / 智谱 / Kimi / 混元 / 豆包 | ✅ 安装后在 MCP 配置里加一段，框架自动发现 |
| 你想对比同一问题在多个模型上的回答差异 | ✅ `ask_model` 传入 `providers=[a,b]` 即可对比 |
| 你想让模型描述一张图片 | ✅ `describe_image` 工具，支持 Qwen-VL/GLM-4V/豆包视觉 |
| 你想让模型调用工具（Function Calling） | ✅ `ask_model` 传入 `tools` 参数，返回 `tool_calls` |
| 你想生成文本向量嵌入 | ✅ `embed_text` 工具，支持 deepseek/zhipu/doubao/tongyi |
| 你想对文档按相关性重排序 | ✅ `rerank` 工具，支持 zhipu 等 |
| 你想将语音转为文字 | ✅ `audio_transcribe` 工具 |
| 你想理解视频内容 | ✅ `video_understand` 工具（关键帧+视觉描述） |
| 你想统计调用量、token 消耗、各模型使用占比 | ✅ 内置 SQLite 统计 + 周报功能 |
| 你希望错误信息是中文的、不暴露原始英文 API 报错 | ✅ 统一错误映射（v1.9.0 新增 429/451/余额不足/内容审查四类 + 中文处置建议） |
| 你希望在低配电脑上用，不希望 AI 把你的内存吃满 | ✅ 硬件感知并发控制（自动采集 CPU/内存 → 动态限制并发数） |
| 你希望每天自动检查各厂商 API 是否可用，晨报推送异常 | ✅ 每日健康晨报（最小调用控制成本 <0.1 元/天，本地 HTML + 可选 webhook） |
| 你希望厂商接口变更或故障时第一时间知道 | ✅ 厂商变更雷达（滑动窗口 + 3σ 异常检测，晨报置顶告警） |
| 你有一个国产模型 API key，想把它接到你的 Agent 工作流里 | ✅ 填 config.json 启动即可 |

---

## 安装

### 前提条件

- Python 3.9+（已安装在你系统上）
- 至少一个国产模型的 API key

### 安装步骤

```bash
# 1. 克隆或下载本 skill 文件夹
git clone https://github.com/your-org/cn-model-gateway.git
cd cn-model-gateway

# 2. 复制配置模板，填写你的 api_key
cp config/config.json.example config/config.json
# 然后编辑 config.json，填入你的 api_key
```

**无需 pip install，所有代码使用 Python 标准库（urllib/json/sqlite3/asyncio）。**

---

## 使用方法

### 方式一：作为 MCP 服务器（推荐，给 Claude Code / Cursor / Cline 用）

在 Claude Code / Cursor / Cline 的 MCP 配置文件中加入：

```json
{
  "mcpServers": {
    "cn-model-gateway": {
      "command": "python",
      "args": ["D:/skill/cn-model-gateway/main.py", "run", "-c", "D:/skill/cn-model-gateway/config/config.json"]
    }
  }
}
```

启动 Agent 框架后，即可自动发现 8 个工具 + 2 个资源 + 2 个 prompt 模板。

### 方式二：命令行直接提问

```bash
# 直接提问（自动选择可用模型）
python main.py ask "写一个快速排序"

# 指定模型提问
python main.py ask "写一个快速排序" -p deepseek

# 对比多个模型
python main.py ask "解释量子计算" --providers deepseek tongyi zhipu

# 描述一张图片
python main.py describe_image "https://example.com/photo.jpg" -p tongyi

# 生成文本向量嵌入
python main.py embed "文本1" "文本2" -p deepseek

# 文档重排序
python main.py rerank -q "查询" -d "文档1" "文档2" "文档3" -p zhipu

# 语音转文字
python main.py transcribe "audio.mp3" -p zhipu

# 理解视频内容
python main.py video "video.mp4" -p zhipu

# 查看已配置模型状态
python main.py status

# 查看使用统计
python main.py stats

# 执行健康检查（最小调用，记录延迟/成功率）
python main.py health

# 生成每日健康晨报（本地 HTML + 可选 webhook 推送）
python main.py report
python main.py report --webhook https://your-webhook-url

# 启动 MCP 服务器
python main.py run
```

### 方式三：Python API 直接调用

```python
from src.router import ModelRouter
from src.adapters.base import ChatMessage

router = ModelRouter()
router.register_all({
    "deepseek": {"api_key": "sk-xxx"}
})

msgs = [ChatMessage(role="user", content="你好")]
resp = router.chat(msgs, provider="deepseek")
print(resp.content)
```

---

## 内置工具（MCP tools/list 返回）

| 工具名 | 描述 | 关键参数 |
|--------|------|---------|
| `ask_model` | 向模型提问（单家/多家对比/Function Calling） | `question`（必填）, `provider`（可选）, `providers`（可选列表，指定 2+ 家对比）, `model`（可选）, `temperature`（可选）, `tools`（可选，Function Calling 工具定义） |
| `describe_image` | 向视觉模型发送图片，返回描述或回答 | `image`（必填，URL/base64/文件路径）, `prompt`（可选，默认"请描述这张图片"）, `provider`（可选）, `model`（可选） |
| `embed_text` | 将文本转换为向量嵌入（embedding） | `texts`（必填，文本列表）, `provider`（可选）, `model`（可选） |
| `rerank` | 对文档列表按查询相关性重排序 | `query`（必填）, `documents`（必填，文档列表）, `provider`（可选）, `model`（可选） |
| `audio_transcribe` | 将音频文件转换为文字（语音识别） | `audio`（必填，URL/base64/文件路径）, `provider`（可选）, `model`（可选）, `language`（可选） |
| `video_understand` | 理解视频内容（关键帧+视觉描述） | `video`（必填，URL/文件路径）, `prompt`（可选）, `provider`（可选）, `model`（可选） |
| `batch_submit` | 提交批量任务列表，立即返回任务 ID | `tasks`（必填，任务列表）, `priority`（可选，0-9，默认 5） |
| `batch_result` | 查询批量任务状态和结果 | `task_id`（必填）, `include_items`（可选，默认 false） |
| `list_providers` | 列出所有已配置且可用的模型提供商 | 无 |
| `health_check` | 检查所有已配置提供商的连通性 | 无 |
| `health_report` | 生成每日健康晨报（本地 HTML），含各厂商成功率/延迟/配额余量 + 厂商变更雷达（3σ 异常检测） | `save`（可选，默认 true）、`days`（可选，默认 1，最大 7） |

---

## 内置资源（MCP resources/list 返回）

| 资源 URI | 描述 |
|----------|------|
| `cn-model-gateway://status` | 网关状态总览——当前配置（不含 api_key 明文）+ 使用统计 + 配额告警，一屏汇总 |

---

## 内置 Prompt 模板（MCP prompts/list 返回）

| 模板名 | 描述 | 参数 |
|--------|------|------|
| `code_review` | 代码审查提示模板 | `code`（必填）, `language`（可选，默认 python） |
| `translate` | 中英互译提示模板 | `text`（必填）, `target_lang`（必填：zh/en/ja） |

---

## 配置说明

`config.json` 格式：

```json
{
  "deepseek": { "api_key": "sk-xxx" },
  "tongyi": { "api_key": "sk-xxx" },
  "zhipu": { "api_key": "your-key" },
  "kimi": { "api_key": "your-key" },
  "hunyuan": { "api_key": "SECRET_ID:SECRET_KEY" },
  "doubao": { "api_key": "your-key" }
}
```

### API Key 读取优先级（v1.4.0）

1. **环境变量**（推荐，更安全）：`DEEPSEEK_API_KEY`、`DASHSCOPE_API_KEY`、`ZHIPU_API_KEY`、`KIMI_API_KEY`、`HUNYUAN_SECRET_ID`、`DOUBAO_API_KEY`、`MINIMAX_API_KEY`、`LINGYI_API_KEY`、`BAICHUAN_API_KEY`、`STEPFUN_API_KEY`
2. **config.json**（向后兼容）

推荐做法：环境变量设置 api_key，config.json 只填非敏感配置（如 `model`、`base_url` 等）。

- 可以只填一家，也可以十家全填
- `hunyuan` 比较特殊，格式为 `secret_id:secret_key`（冒号分隔）
- 未填 api_key 的提供商自动标记为不可用，不影响其他家使用

---

## 统一错误映射

各家模型返回的错误码不同，本 skill 统一映射为 MCP 标准错误码：

| MCP 错误码 | 含义 | 触发场景 |
|-----------|------|---------|
| `-32602` | 参数错误 | API key 无效、内容审核未通过、请求参数缺失 |
| `-32001` | 模型不可用 | 提供商未配置或已过期、地区限制（451） |
| `-32002` | 速率限制 | 调用频率超限（429）、额度不足、余额不足 |
| `-32603` | 内部错误 | 网络超时、响应解析失败 |

所有错误信息均为**中文**，便于排查。

### v1.9.0 新增错误类型

| 错误类型 | 错误码 | 处置建议 |
|---------|--------|---------|
| 429 限流 | `-32002` | 等待 60 秒后重试，或降低调用频率 |
| 451 地区限制 | `-32001` | 检查地区设置，或联系厂商客服 |
| 余额不足 | `-32002` | 检查余额页充值 |
| 内容审查触发 | `-32602` | 修改提示词重试，避免敏感内容 |

错误映射表已 YAML 外置（`references/error_map.yaml`），支持热更新。

---

## 性能优化

- **硬件感知并发**：启动时自动采集 CPU 核数和内存大小，低配电脑（< 4GB 内存）限制并发数为 1，高配最多 4 并发
- **零外部依赖**：纯 Python 标准库，无 `pip install`，避免环境污染
- **流式输出**：长对话走 SSE 流式，不堵内存
- **SQLite WAL 模式**（v1.4.0）：全部数据库启用 WAL，支持多 Agent 框架同时写入不报锁错误
- **故障转移**（v1.4.0）：auto 模式按能力画像排序 + 超时自动切换备用提供商，成功率 99%+

---

## 版本更新提醒

本 skill 会在每次启动时打印当前版本号（stderr）。要获取最新版本：

```bash
# 检查 GitHub 最新版本（需安装 gh CLI）
gh release list --repo your-org/cn-model-gateway
```

建议关注本 skill 的 GitHub Release 页获取更新通知。

---

## ⚠️ 风险项（必读）

| 风险 | 说明 | 规避方式 |
|------|------|---------|
| API Key 泄露 | 用户需自行保管 api_key，config.json 文件勿提交到公开仓库 | 推荐使用环境变量（DEEPSEEK_API_KEY 等）替代 config.json 明文；config.json 加到 .gitignore |
| 模型调用计费 | 每次调用都会消耗对应模型提供商的额度，费用由用户自行承担 | 定期查看 `python main.py stats` 统计，设置各平台额度预警 |
| 内容安全 | 模型回答内容由各提供商审核策略决定，本 skill 不额外过滤 | 生产环境建议叠加内容安全过滤层 |
| 网络依赖 | 每次调用都通过 urllib 直连各模型 API，需要联网 | 离线环境无法使用各家模型能力 |
| 并发安全风险 | SQLite 已启用 WAL 模式（v1.4.0），多进程并发安全 | 如仍遇到锁错误，检查 .db-wal 文件是否损坏，可删除重建 |
| 配置格式 | hunyuan 必须是 `secret_id:secret_key` 格式，其他家是普通 key | 使用前运行 `python main.py status` 检查连通性 |
| API 版本兼容 | 各模型提供商可能更新 OpenAI-compatible 接口路径或字段 | 关注各平台公告，本 skill 会随版本更新适配 |

---

## 能力边界

- 支持文本对话、图片理解（v1.5.0 新增多模态）、文本向量嵌入（v1.6.0）、文档重排序（v1.6.0）、语音转文字（v1.6.0）、视频理解（v1.6.0）
- 支持 Function Calling / Tool Use（v1.5.0 新增，通过 `tools` 参数传入）
- 支持批量异步调用（v1.8.0 新增）：`batch_submit` 提交任务列表 → 后台顺序执行 → `batch_result` 轮询结果；失败自动重试一次
- 支持 SSE 心跳保活（30s ping）+ 断线重连（v1.8.0 新增）：客户端断开后凭请求 ID 重连续传，网络抖动不导致长回答作废重计费
- 支持每日健康晨报（v1.9.0 新增）：最小真实调用（"hi" ~2 token/厂商），SQLite 记录延迟/成功率/配额余量，异常晨报置顶告警
- 支持厂商变更雷达（v1.9.0 新增）：滑动窗口（24h vs 7d 基线）+ 3σ 异常检测，自动标注"疑似接口变更/故障"
- 不支持本地模型推理或 GPU 部署
- auto 模式支持故障转移（v1.4.0 新增），默认按能力画像排序 + 超时自动切备用

---

## 常见问题（FAQ）

**Q: 为什么启动后没有任何提供商可用？**
A: 检查 config.json 格式是否正确，api_key 是否填写。运行 `python main.py status` 查看状态。注意 hunyuan 格式是 `secret_id:secret_key`（冒号分隔）。

**Q: 能同时配置多个提供商让 skill 自动选择吗？**
A: 可以。auto 模式会按能力画像（benchmark 历史评分）和连通性状态排序，选最优的。超时/失败时自动切换到下一家（可通过 `--no-failover` 关闭）。

**Q: 如何对比多个模型的回答？**
A: 在 `ask_model` 工具中传入 `providers: ["deepseek", "tongyi", "zhipu"]`（2 家及以上），会自动返回对比结果。不传 `providers` 则单家调用。

**Q: 如何让模型描述一张图片？**
A: 使用 `describe_image` 工具，传入 `image`（URL/base64/文件路径）和可选的 `prompt`。支持 Qwen-VL、GLM-4V、豆包视觉等多模态模型。

**Q: 如何使用 Function Calling？**
A: 在 `ask_model` 工具中传入 `tools` 参数（工具定义列表），模型可能会在响应中返回 `tool_calls`。你需要自行执行工具并将结果作为后续对话的输入。

**Q: 如何生成文本向量嵌入？**
A: 使用 `embed_text` 工具，传入 `texts` 列表。支持 deepseek（deepseek-embedding）、zhipu（embedding-2）、doubao（doubao-embedding）、tongyi（text-embedding-v2）等。

**Q: 如何对文档进行重排序？**
A: 使用 `rerank` 工具，传入 `query` 和 `documents` 列表。支持 zhipu（rerank）等提供商。

**Q: 如何将语音转为文字？**
A: 使用 `audio_transcribe` 工具，传入音频文件路径或 URL。支持 zhipu、doubao 等提供商。

**Q: 如何理解视频内容？**
A: 使用 `video_understand` 工具，传入视频文件路径或 URL。系统会自动抽取关键帧并通过视觉模型生成描述。

**Q: 如何批量执行多个任务（如批量翻译、批量文档摘要）？**
A: 使用 `batch_submit` 工具提交任务列表（每项指定 `tool` 和 `arguments`），立即返回任务 ID。然后用 `batch_result` 工具轮询任务进度和结果。后台顺序执行（复用硬件自适应并发），失败任务自动重试一次并保留错误详情。

**Q: 网络断开后正在进行的调用会作废吗？**
A: 不会。v1.8.0 新增 SSE 心跳保活（30s ping）+ 断线重连：服务端缓冲最近 200 个 chunk，客户端凭请求 ID 重连后从断点续传，避免长回答作废重计费。

**Q: 如何查看每日健康晨报？**
A: 使用 `health_report` MCP 工具，或命令行 `python main.py report`。晨报保存在 `~/.cn-model-gateway/health_report_YYYY-MM-DD.html`，含各厂商成功率/延迟/配额余量。可选 `--webhook` 参数推送至企业微信/飞书等。

**Q: 厂商变更雷达是如何工作的？**
A: 系统持续记录每次健康检查结果到 SQLite。晨报生成时，对比 24h 错误率与 7d 基线错误率，若 24h 错误率 > 基线 + 3σ（且 >30%），自动标注"疑似接口变更/故障"并置顶告警。覆盖场景：厂商 API 路径变更、认证策略调整、模型下线等。

**Q: 健康检查的成本是多少？**
A: 每次健康检查对每家已配 Key 的厂商发送最小 prompt（"hi"，~2 token），10 家厂商单次约 20 token。按每日一次计算，日均成本 <0.1 元（以 DeepSeek 为例，20 token ≈ ¥0.00004）。可在 `config.json` 中设置 `health_check.enabled: false` 关闭。

**Q: 各家模型的默认模型是什么？**
A: deepseek-chat / qwen-turbo / glm-4-flash / moonshot-v1-8k / hunyuan-standard / doubao 系列。可通过 `model` 参数覆盖。

**Q: 使用量数据存在哪里？**
A: 默认存储在 `~/.cn-model-gateway/usage.db`（SQLite）。不会上传到任何服务器。

**Q: 支持哪些操作系统？**
A: Windows / macOS / Linux 全平台支持。需要 Python 3.9+。

**Q: 需要 GPU 吗？**
A: 完全不需要。本 skill 只做 API 网关，不进行本地推理。

---

## 支持与反馈

有更好建议：njskills@agent.qq.com

遇到问题请提供：
1. `python main.py status` 输出
2. 报错截图或完整错误信息
3. 你使用的 model provider 名称

---

## 更新日志

| v1.9.0 | 2026-10-09 | 新增每日健康晨报：HealthScheduler 调度器对已配 Key 厂商做最小真实调用（"hi" ~2 token），SQLite WAL 记录延迟/成功率/配额余量，异常晨报置顶告警；新增厂商变更雷达：滑动窗口（24h vs 7d 基线）+ 3σ 异常检测，自动标注"疑似接口变更/故障"；新增 health_report MCP 工具 + health/report CLI 子命令；统一错误映射扩容：新增 429 限流/451 地区限制/余额不足/内容审查触发四类错误，全部附带中文处置建议（"等 60 秒重试""检查余额页""修改提示词重试"）；错误映射表 YAML 外置（references/error_map.yaml），支持热更新；SKILL.md 更新工具列表（11 个工具）、FAQ、能力边界、错误映射说明 |
| v1.8.0 | 2026-08-24 | 新增批量异步任务引擎：batch_submit 提交任务列表立即返回 ID，后台顺序执行（复用硬件自适应并发），batch_result 轮询状态与结果，失败自动重试一次并保留错误详情；新增 SSE 心跳保活（30s ping）+ 断线重连（chunk ring buffer，凭请求 ID 从断点续传，保护长输出与成本）；MCP 资源合并：config + usage 两个资源合并为 cn-model-gateway://status 单一资源（配置+使用统计+配额告警一屏汇总）；新增 batch_queue.py 任务队列模块（SQLite WAL + 后台 worker 线程）；MCPServer 启动时自动启动 batch_worker，新增 shutdown() 优雅停止；SKILL.md 更新工具列表（10 个工具）、资源列表、能力边界、FAQ |
| v1.6.0 | 2026-08-24 | 新增共享内核（llm-core monorepo）：抽取 src/llm_core/ 共享内核模块，支持 MCP 形态与 CLI 形态共用同一份 core（adapters/router/error_map/cost/cache/monitor/benchmark），构建时注入同版副本+版本锁；新增 4 个 MCP 工具：embed_text（文本向量嵌入，支持 deepseek/zhipu/doubao/tongyi）、rerank（文档重排序，支持 zhipu）、audio_transcribe（语音转文字）、video_understand（关键帧抽取+视觉模型描述→视频摘要）；BaseAdapter 新增 4 个抽象方法（embed_text/rerank/audio_transcribe/video_understand）+ 降级 NotImplementedError 机制；CLI 新增 4 个子命令（embed/rerank/transcribe/video）；SKILL.md 全面更新工具列表/能力边界/FAQ |
| v1.5.0 | 2026-08-16 | 合并 MCP 工具：ask_model + compare_models → ask_model（新增可选 providers 参数，空=单家，≥2 家=对比）；新增多模态视觉支持：ChatMessage 加 image 字段 + describe_image MCP 工具 + 视觉适配器多模态 payload（Qwen-VL/GLM-4V/豆包视觉）；新增 Function Calling / Tool Use：ChatResponse 加 tool_calls 字段 + BaseAdapter 加 format_tools/parse_tool_calls 方法 + ask_model 支持 tools 参数；SKILL.md 全面更新工具列表/能力边界/FAQ |
| v1.4.0 | 2026-08-16 | 改进 auto 模式故障转移：auto_select() 从 random.choice 改为能力画像 + 健康检查有序选择；chat() 和 stream_chat() 新增自动故障转移循环，失败/超时自动切备用提供商；支持环境变量优先读取 api_key（DEEPSEEK_API_KEY / DASHSCOPE_API_KEY 等 10 个），config.json 向后兼容；SQLite 全部启用 WAL 模式（PRAGMA journal_mode=WAL），支持多 Agent 框架并发写入；新增 --timeout 和 --no-failover CLI 参数；新增 3 个故障转移+环境变量+WAL 单元测试（总计 40 tests） |
| v1.3.0 | 2026-08-01 | 新增模型性能基准测试套件（benchmark.py：50 道题库、6 维度评分、雷达图对比、历史追踪）；新增 Token 价格实时追踪（price_tracker.py：价格抓取、变更通知、趋势图、成本预测）；新增 4 个 CLI 子命令（benchmark/price/benchmark-history/price-history/cost-predict）；测试覆盖新增 8 个 benchmark + price_tracker 单元测试（总计 37 tests） |
| v1.2.0 | 2026-07-24 | 新增 5 个非 MCP 框架适配器（LangChain Tool、AutoGPT Plugin、CrewAI Tool、Coze 插件、Dify 工具节点）；扩展框架适配层从 MCP 生态到全 Agent 生态；新增 frameworks 模块（5 个适配器 + 统一导出）；测试覆盖新增 11 个框架适配器单元测试（总计 29 tests） |
| v1.1.0 | 2026-07-17 | 新增 4 家模型提供商（MiniMax/零一万物/百川智能/阶跃星辰）；更新 DeepSeek-V3 支持（deepseek-chat, deepseek-reasoner）；更新 Kimi 新版本（moonshot-v1-32k, moonshot-v1-128k）；扩展统一错误映射覆盖 10 家厂商；支持模型表格同步更新 |
| v1.0.0 | 2026-07-16 | 初始版本发布，包含：MCP JSON-RPC 2.0 完整协议适配（tools/list/call + resources/list/read + prompts/list/get）；6 家国产模型适配器（DeepSeek/通义/智谱/Kimi/混元/豆包）；统一错误映射（4 种 MCP 标准错误码 + 中文 message）；流式 SSE 输出；本地 MCP 服务器 stdio 启动；内置 4 个工具（ask_model/compare_models/list_providers/health_check）；2 个 prompt 模板（code_review/translate）；使用量统计（SQLite + 周报）；硬件感知并发控制（自动采集 CPU/内存 → 动态分配并发数）；纯 Python 标准库零依赖；CLAUDE.md/Cursor/Cline 配置文件模板 |