---
name: free-llm-installer
slug: free-llm-installer
displayName: 免费 LLM 一键安装
version: 1.1.9
description: 一键安装并实测验证已验证可用的免费 LLM 到 WorkBuddy/Claude Code，无需注册、无需 API Key。当用户说「装免费模型」「加免费模型」「免费 LLM」「免费模型一键装」「验证免费模型可用吗」「免费模型怎么接入」「帮我配几个免费模型」「监控免费模型」「免费模型挂了吗」「kilo 网关」「kilo-auto」「nemotron 免费」「space-bunny」「智谱 glm 免费」「zhipu 免费」「glm-4-flash」「glm-4.7-flash」「glm-z1-flash」「glm-4v-flash」「探测国外免费模型」「国外平台免费 llm」「优先用免费模型」「读图桥接」「vision bridge」「给 glm-4-flash 加读图」「不读图的模型怎么看图」「阶跃星辰」「stepfun」「step 5」「step-5-preview」「限时免费模型」「ccproxy 读图转发」「给 claude code 加读图」时使用。也用于验证已有免费模型配置是否真的可用（tool calling 是否支持、是否限流、是否支持读图），以及定期 watch 监控免费模型是否下线/限流/失去工具调用能力。
agent_created: true
---

# 免费 LLM 一键安装与实测验证

## 核心原则

**「标 free」不等于「真能用」。** 本技能内置的模型都是逐个发真实请求
（含 function calling）验证过的。使用者不需要自己再验证一遍。

已踩过的坑，不要重复：

|坑 | 表现 | 正确做法 |
|---|---|---|
| 模型 id 被简化 | `kilo-auto-free` → 401 PAID_MODEL_AUTH_REQUIRED | 必须写完整 `provider/model:free` |
| 空 apiKey | 回落宿主平台 token → 鉴权失败 | Kilo 用字面量 `"anonymous"`；智谱填真实 key |
| 假多模态 | 返回 200 但 `image_tokens=0`，模型瞎猜 | Kilo 纯文本模型写 `supportsImages: false`；omni 经 base64 图实测可识别，写 `true` |
| 假工具调用 | 能对话但从不返回 `tool_calls` | 必须发带 `tools` 的请求实测；glm-z1-flash / glm-4v-flash 不输出结构化工具调用，标记 `supportsToolCall: false` |
| Cloudflare拦 UA | 403 `code:1010` | 必须带浏览器 User-Agent（脚本已内置） |
| **Zen 免费层封 API 直连（2026-10-11）** | `space-bunny-free` → 403 "free tier can only be used from within OpenCode" | 上游政策收紧，本地配置无解，**已从默认清单移除**。如需使用需走 OpenCode 客户端 |
| **WorkBuddy ≥5.8.0 拒纯空白 key** | 单空格 `" "` 被 UI 判为「未配置接口地址或 API key」标红禁用 | Kilo 用 `anonymous`（实测 200，trim 后非空可过校验） |
| **Kilo 假 key 会 401** | `Bearer free`/`x`/`0` → 401 INVALID_TOKEN | Kilo 匿名 token 只有两个：空串和字面量 `anonymous`。占位一律用 `anonymous` |
| **智谱免费档高峰过载** | glm-4.7-flash 高峰 429；glm-4.6v-flash 持续 1305「访问量过大」 | 日常用 `glm-4-flash`（永久免费·最稳）；`glm-4.7-flash` 非高峰用；`glm-4.6v-flash` 暂不可用 |
| **推理模型吃 token** | max_tokens 太小 → 响应被截断成无 `choices` | 推理模型 verify/probe 时 `max_tokens` 给到 ≥400~600 |
| **智谱视觉模型用「文本框」伪工具调用** | `glm-4.1v-thinking-flash` / `glm-4.6v-flash` 发 tools 请求 → `finish_reason=stop`、`tool_calls=None`，把调用写成 `<|begin_of_box|>get_time(city='北京')<|end_of_box|>` 文本 | 智谱自定义格式，**非标准 OpenAI tool_calls**，WorkBuddy/Claude Code 都读不了 → **不能用于 agent / 不能进切换器**。读图能力是真的（实测可识别颜色），仅限 WorkBuddy 纯聊天/读图用 |
| **1×1 像素图被智谱拒** | 智谱视觉模型对极小图报 400「图片输入格式/解析错误」 | 用 ≥64×64 的正常图测读图，非模型问题 |
| **StepFun 空 content 偶发** | 推理模型个别 prompt 返回 `content` 为空（答案进了 `reasoning_content`），`stop=max_tokens`、0 字 | 属低概率 flakiness，非必现；**ccproxy 已加空回复自动重试（`retry_empty` 默认 2）**，非流式请求空回复自动重发，实测 5/5 稳定返回正文；仍偶发空时换一次即可。WorkBuddy 直连在 profile 设 `effortLevel: medium` 也最稳 |
| **ccproxy 现已转发图片（2026-10-12 修复）** | 旧版 ccproxy 把 Anthropic `image` 块直接丢成 `[image omitted]`，导致走 ccproxy 的模型（StepFun / omni 等）在 Claude Code 里**不能原生读图** | 新版 `ccproxy.py` 把 base64 / http(s) 图源转成 OpenAI `image_url` 块（配置 `forward_images: true`，默认开）。**一次修复解锁所有 ccproxy 路由模型的原生读图**。个别上游拒 base64 图时置 `forward_images: false` 回退旧行为 |
| **profile 复用导致显示名≠实际后端（2026-10-12 踩到）** | 为省事直接复用 spacebunny 的 env 写 kilo-bridge profile，模型名写成 `space-bunny[1m]`；但 ccproxy 启动带 `--model kilo-auto/free` 会**无视请求里的模型名**、全部转发到 Kilo 免费网关 → Claude Code 横幅显示 `space-bunny` 而实际跑的是 kilo-auto/free，用户以为 space-bunny 挂了 | 显示名纯标签、不影响功能；**但在切换器 profile 里把模型名写成真实后端**（如 `kilo-auto/free[1m]`）即可消除混淆。ccproxy 日志第一行 `listening on ... -> <upstream> (kilo-auto/free)` 是判断实际后端的唯一权威来源 |
| **`kilo-auto/free` 是随机轮换池（2026-10-13 实测）** | 它会轮换免费模型，抽到重推理模型时 **7 分 30 秒只出 161 token** 就报错；同一 prompt 有时 3s 有时 7min | **不要用 auto 路由，锁定具体模型 id**（`liquid/lfm-2.5-2.6b:free` 实测 5/5 稳定、2-3.3s、agentic 两步全对，完胜 120B/550B 大模型）。代理参数无需动——问题在模型选择不在参数 |
| **上下文窗口照抄大模型 → 400 爆上下文（2026-10-13 踩到）** | 给 64k 的 `liquid/lfm-2.5-2.6b:free` 填了 `CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000`（照抄 Step5 的 1M）→ Claude Code 以为有 1M，**从不触发自动压缩**，涨到 68918 才被上游拒：`maximum context length is 65536 tokens` | **按模型真实 ctx 填窗口**：先查上表 context_length，再设 `AUTO_COMPACT_WINDOW ≈ 真实值 - 8000`；同时设 `CLAUDE_CODE_MAX_OUTPUT_TOKENS=16000`（默认预留 32000 会白占一半预算）。例：LFM65536 → `56000` + `16000` |
| **auto-mode 校验器跑在会话模型上 → 慢模型把工具全堵死（2026-10-13 踩到）** | Claude Code auto mode 的安全校验用**会话模型**判定 Bash/WebFetch 是否安全；会话模型是免费共享档时抖动超时，报 `X is temporarily unavailable (timed out), so auto mode cannot determine the safety of Bash`，**所有需审批动作全被卡死** | 三条路：① 会话模型换 DeepSeek 等稳定模型；② 用户级 settings 写 `"permissions": {"defaultMode": "default"}` 关掉 auto mode（**逐次手动确认，不调校验器**；只认用户级来源，项目级无效；切换器不碰这个键所以切模型不会丢）；③ 想让校验器用快模型得让桥接支持按模型名分流多上游——`CLAUDE_CODE_AUTO_MODE_MODEL` 这个env 存在但未公开，且 `ccproxy --model` 会强制覆盖所有模型名，设了也无效 |
| **SSL: UNEXPECTED_EOF_WHILE_READING（2026-10-14 踩到，误判成模型失效）** | 报`upstream connect failed: [SSL: UNEXPECTED_EOF_WHILE_READING]`，第一反应以为模型下架/欠费——其实**模型好好的**（直连2-4s 正常）。真凶是代理配错了，**最常见是把 SOCKS5 端口写成 `http://`**（如 `http.proxy=http://127.0.0.1:10808` 而 10808 其实是 Shadowsocks 的 SOCKS5 端口）→ TLS 握手必断 | **先怀疑代理链路，别急着换模型**。① 查端口到进程的映射再判断：`http://` 只对 HTTP 代理端口（Shadowsocks 的 `ss_privoxy` HTTP 桥之类），SOCKS5 端口要用 `socks5h://`（**注意 ccproxy 基于 urllib，不支持 socks**）② 找端口：PowerShell `Get-NetTCPConnection -State Listen` + `Get-Process` ③ 直接最省事：`--proxy ""` 强制直连 ④ `git push` 报同样错就查 `~/.gitconfig` 的 `http.proxy`，设成**空字符串**（删掉会回落到环境变量） |
| **git push 报 TLS EOF（2026-10-14 长期问题根因）** | 本机 git 一直报 `TLS connect error: ...unexpected eof while reading`，换网络/换命令都无效 | 根因是 `~/.gitconfig` 里写死了 `http.proxy=http://127.0.0.1:<SOCKS5端口>`。修复：`git config --global http.proxy ""` 和 `https.proxy ""`（**必须空字符串**；`--unset` 后 git 会回落到环境变量）。验证：直连 `git ls-remote` 多次全OK 即坐实。另：`env -u *_proxy` 对 git **无效**，git 只认自己的 config |

## 内置模型（2026-10-11 实测）

### 免 key 梯队（Kilo Gateway，无需注册）
| 模型 id | 端点 | 真实上下文 | 工具调用 | 读图 | 实测（2026-10-13） |
|---|---|---|---|---|---|
| **`liquid/lfm-2.5-2.6b:free`** ⭐ | Kilo Gateway | **65536** | ✅ | ❌ | **4/4~5/5 稳定、2.1-3.3s、agentic 两步全对 → 免费 agent 首选** |
| `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` | Kilo Gateway | 256k | ✅ | ✅（base64 图实测可识别） | 读图兜底；偶发空回复 |
| `nvidia/nemotron-3-super-120b-a12b:free` | Kilo Gateway | 262k | ✅ | ❌ | 可用但 3/5（2 次空回复）、波动 2.6-14.4s → 不推荐 |
| ~~`kilo-auto/free`~~ ⚠️ | Kilo Gateway | **不确定（轮换）** | ✅ | ❌ | **随机轮换池，会抽到重推理模型 → 实测 7min/161token，不要用** |
| `nvidia/nemotron-3-ultra-550b-a55b:free` | Kilo Gateway | 1000k | ✅ | ❌ | agentic 第 2 步退化，不推荐 |

> **⭐ 最重要的一条**：`kilo-auto/free` 的官方描述就是 "Rotates through available free models"
> ——它是**随机轮换池**，每次可能给你不同的模型，抽到重推理的就极慢。
> **正确做法：锁定具体模型 id**（如上面的 LFM2.5），别用 auto 路由。
> 探网关有什么可选（**免 key**）：
> ```bash
> curl -s -H "Authorization: Bearer anonymous" \
>   https://api.kilo.ai/api/gateway/v1/models | python -c "import json,sys; [print(m['id'],m.get('context_length')) for m in json.load(sys.stdin)['data'] if 'free' in m['id']]"
> ```

> omni 模型是免费读图兜底：免 key（apiKey 填 `anonymous`）、能读图、能调工具。
> 注意 reasoning 模型会先吐 reasoning 吃 token，`max_tokens` 给到 ≥1024 否则响应会被截断。

### 智谱 BigModel 梯队（需 key，但有**永久免费**档，效果最好）
> 用 `--zhipu-key <KEY>` 安装；key 形如 `xxxxxxx.YYYYYYYY`（用户已有，见 glm profile）。
| 模型 id | 免费性质 | 工具调用 | 读图 | 推理 |
|---|---|---|---|---|
| `glm-4-flash` | 永久免费 | ✅ | ❌ | ❌ | 日常主力·最稳 |
| `glm-4.7-flash` | 免费·高峰易 429 | ✅ | ❌ | ✅ | 带推理·质量更好 |
| `glm-z1-flash` | 完全免费 | ❌ | ❌ | ✅ | 数学/代码推理，不输出结构化工具（仅聊天/推理用） |
| `glm-4v-flash` | 永久免费 | ❌ | ✅ | ❌ | 免费读图，无工具（仅聊天/读图用） |
| `glm-4.1v-thinking-flash` | 免费 | ❌ | ✅ | ✅ | 视觉+推理最强，但工具调用是智谱自定义「文本框」格式（非标准 tool_calls），**不能用于 agent / 不能进切换器**；读图实测可用（仅 WorkBuddy 聊天/读图用） |
| `glm-4.6v-flash` | 免费·高峰持续 1305/500 | ❌ | ✅ | ❌ | 与 4.1v 同为视觉模型，但服务端极不稳定（实测连续 429→500→429），工具调用格式同为文本框。**暂不可用，不加** |

> **Claude Code 切换器只放支持标准工具调用的模型**（`glm-4-flash` / `glm-4.7-flash`），
> 因为 Claude Code 靠工具调用干活；z1/v/4.1v/4.6v 都不输出结构化 `tool_calls`，加切换器会断 agent 循环，仅 WorkBuddy 聊天/读图用。

### 已移除 / 不可用
- `space-bunny-free`（OpenCode Zen）：2026-10-11 起上游 403 封 API 直连，暂不可用。
- `glm-4.6v-flash`：持续 1305 服务器过载，用户侧无解，不加。

## 国内外平台免费格局（时效内 + 效果好）

| 平台 | 免费模型 | 状态 | 能力 | 本机可达 |
|---|---|---|---|---|
| **智谱 BigModel**（需 key） | GLM-4-Flash / GLM-4.7-Flash / GLM-Z1-Flash / GLM-4V-Flash | ✅ 永久/限时免费 | 文本/工具/推理/读图 | ✅ 直连 200 |
| **Kilo 网关**（免 key） ⭐ | lfm-2.5-2.6b / nemotron-omni / nemotron-super 等 | ✅ 稳定 | 文本/工具/读图(omni) | ✅ 直连 200 |
| **硅基流动 SiliconFlow**（需国内手机注册） | GLM 系列蒸馏 / DeepSeek-R1-Distill 等 | ✅ 免费·1K RPM | 文本为主 | 本机暂无 key |
| **阶跃星辰 StepFun**（需 key，限时免费） | Step 5 Preview（1M ctx·多模态·工具调用·推理） | ⚠️ 限时额度，**耗尽即全模型 402**（2026-10-13 实测三模型同时 402，key 仍有效） | 文本/工具/读图/推理全开 | ✅ 直连 200 |
| **OpenRouter**（需 key） | 15 个 `:free` 模型 | 列表免 key 200，**推理 401**（"No cookie auth credentials found"） | 多数文本 | ⚠️ 免 key 用不了；但 Kilo 代理了同一目录 |
| **OpenCode Zen** | grok-code 等 | 列表 404 / 调用 "Model is unavailable" | — | ❌ 需 key |
| **Cerebras / NVIDIA NIM** | 若干 | 403 / SSL 超时 | — | ❌ 需 key |
| Groq / Together / HF / Mistral / Google | 各有免费档 | ❌ 国内被 CF/代理封 | — | ❌ 不可达/需 key |

> **2026-10-13 普查结论**：目前**唯一免 key 免注册**能用的聚合网关就是 **Kilo**（它的模型 id 就是
> OpenRouter 的命名，本质是 OpenRouter 目录的匿名代理）。其他平台都要 key —— 所以要扩免费模型池，
> 正确路径是**在 Kilo 里换模型 id**，而不是换平台。
> ⚠️ StepFun 类"限时免费"额度耗尽是**账号级**的：实测 step-5 / 3.5 / 3.7 全变 402，而 `/v1/models`
> 仍返回 200（key 有效）。所以别把关键工作流挂在限时免费模型上。

**结论**：本机最稳的免费组合 = **GLM-4-Flash（文本+工具）+ GLM-4V-Flash（读图）+ GLM-Z1-Flash（推理）**（智谱一个 key，30 并发，永久免费）+
**Kilo 两个免 key 模型**作零注册备用。DeepSeek-V4 是**付费**的，自动模式易烧钱，非必要别用。

## 执行流程

### 场景 A：用户要装免费模型

```bash
python scripts/install_free_llms.py                 # 装 Kilo 免 key 三件套 + 验证
python scripts/install_free_llms.py --zhipu-key KEY # 额外装智谱 GLM 永久免费梯队
```

建议把 `liquid/lfm-2.5-2.6b:free`（Claude Code 重活）或 `glm-4-flash`（日常对话）设为默认。**别用 `kilo-auto/free`**（随机轮换池，会抽到极慢的模型）。

### 场景 B：用户要验证已有配置

```bash
python scripts/install_free_llms.py --verify
```

发真实请求逐个验证。标记 `supportsToolCall:false` 的模型（glm-z1/v）只验证对话可用，不要求工具调用。
常见失败原因：
- `429` → 免费池高峰限流，等几分钟重试，**不是配置错**
- `401` → apiKey 写错或 id 被简化
- `未调工具` → 该模型不支持 function calling，不能用于 agent
- `HTTP404` → 模型已下线，用 `--refresh` 拉当前清单

### 场景 C：用户问「现在还有哪些免费模型 / 国外平台有免费吗」

```bash
python scripts/install_free_llms.py --probe-foreign   # 探测国外平台免费 LLM
python scripts/install_free_llms.py --refresh --dry-run  # 从 Kilo 拉实时清单
```

`--probe-foreign` 会实测各国外平台可达性，并从 OpenRouter 公开列表拉出当前所有定价为 0 的免费模型。
**注意**：新拉到的模型不在实测清单内，必须先 `--verify` 确认工具调用可用再推荐。

### 场景 D：用户要定期巡检（定时任务 / 每周报告）

```bash
python scripts/install_free_llms.py --report          # 一轮体检 + 国外探测，输出汇总
python scripts/install_free_llms.py --watch           # 常驻后台，状态变化才报告
```

`--report` 适合做成自动化（每周跑一次，出变化报告）。
`--watch` 长期挂机（Windows 可交给计划任务），每 30 分钟一轮，只在状态变化时打印。

```bash
python scripts/install_free_llms.py --watch --watch-interval 1800
python scripts/install_free_llms.py --watch --watch-rounds 3 --watch-interval 3600
```

状态持久化在 `~/.workbuddy/free_llm_watch_state.json`；变化写 `~/.workbuddy/free_llm_watch.log`。

### 场景 E：用户要清理

```bash
python scripts/install_free_llms.py --uninstall
```

只移除本脚本添加的（按 `vendor` 识别），保留用户自己的模型。

### 场景 F：给不读图的模型加读图桥接（MCP）

**问题**：`glm-4-flash`（及多数免费文本模型）不读图，但 Claude Code 又依赖它的标准
工具调用干活。智谱能读图的模型（`glm-4.1v-thinking-flash` 等）用的是自定义「文本框」
伪工具调用（见上方踩坑表），**不能进 Claude Code 切换器**。

**方案**：用 `tools/vision_bridge_mcp.py` 起一个 MCP server，提供 `read_image(path)` 工具。
glm-4-flash 遇到图片路径时调 `read_image`，MCP 把图发给读图后端、回填文字描述——
纯文本模型也能「看」图，且不破坏 agent 循环（比透明代理更安全、调试简单）。

读图后端优先级（自动回退）：
1. **智谱 `glm-4.1v-thinking-flash`**（免费，需 `ZHIPU_API_KEY`，质量最好）
2. **Kilo Omni `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free`**（免 key，兜底）

**部署步骤**：
```bash
# 1) （可选但推荐）设置智谱 key；不设置也能用，只是直接走 Kilo 兜底
export ZHIPU_API_KEY=你的智谱key   # Windows: set ZHIPU_API_KEY=...

# 2) 在 ~/.claude/settings.json（或某个 profile）注入 mcpServers：
```
```json
{
  "mcpServers": {
    "vision-bridge": {
      "command": "python",
      "args": ["/绝对路径/free-llm-installer/tools/vision_bridge_mcp.py"]
    }
  }
}
```
```bash
# 3) 重启 Claude Code。对话里把图片本地路径给它，模型会经 read_image 自动看图。
```

- `command` 填 `python`（任意 Python 3 即可，脚本零依赖仅用标准库）；若 `python` 不在
  PATH，改成绝对路径（如 Windows 隔离 python.exe）。
- 想只在某些 profile 启用：把上面的 `mcpServers` 写进对应 `~/.claude/profiles/xxx.json`
  即可，切换 profile 时自动带上/卸下。
- 已内置容错：智谱过载/未配 key 会自动降级到 Kilo，不会让「看图」整体失败。

### 场景 G：接入阶跃星辰 StepFun Step 5 Preview（限时免费·全能力）

**特点**：`step-5-preview` 是阶跃星辰旗舰，**OpenAI 兼容**（`/v1/chat/completions`，`Bearer <key>`），
支持 **1M 上下文 + 工具调用 + 多模态(base64 读图) + 推理**。免费 = **限时试用**（平台额度），
非永久，重任务白嫖期可用，长期默认仍建议 glm-4-flash（永久免费）。本机已实测 tool_calls /
base64 读图 / reasoning 全部可用。

**接入三选一（推荐全做）**：

```bash
# 1) WorkBuddy models.json（直连，保留完整读图/工具/推理能力）
python scripts/install_free_llms.py --stepfun-key <你的StepFun Key>
#   会写入 id=step-5-preview、supportsToolCall/Images/Reasoning 全 true 的条目。
#   不给 key 不会安装（与 --zhipu-key 同机制）。
```

```bash
# 2) Claude Code profile（走 ccproxy 透明代理 → Anthropic 格式）
#    在 ~/.claude/profiles/stepfun.json 写入（key 明文或环境变量）：
```
```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "<CCPROXY_CLIENT_TOKEN>",
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:3459",
    "ANTHROPIC_MODEL": "step-5-preview",
    "API_TIMEOUT_MS": "600000",
    "CLAUDE_CODE_AUTO_COMPACT_WINDOW": "1000000"
  },
  "model": "step-5-preview",
  "modelSettings": { "step-5-preview": { "effortLevel": "medium" } }
}
```
> `ANTHROPIC_AUTH_TOKEN` 必须填**你本机 ccproxy 生成的 client_token**（首次启动 ccproxy 时
> 写入 `~/.claude-code-proxy.json` 的 `client_token` 字段，或启动日志里的 "generated a client token"）。
> 每个安装实例不同，不要照抄别人的值，否则网关拒连（401 authentication_error）。
```bash
# 3) 切换器按钮（tools/claude_model_switcher.py 已内置两个 StepFun 按钮）：
#    ·「StepFun Step 5 (推理·限时免费)」  → port 3459，思考开（默认）
#    ·「StepFun Step 5 (无推理·限时免费)」→ port 3460，加 --no-reasoning（思考关，秒回）
#    key 从环境变量 STEPFUN_API_KEY 读取，不写死在脚本里，避免随技能泄密。
#    启动：pythonw tools/claude_model_switcher.py  （Windows 双击也可，.cmd 启动器见仓库外本地副本）
#    点按钮后重启 Claude Code 即可。
#
# 无推理网关手动启动（Claude Code 走 ccproxy 时才需要，直连 WorkBuddy 不用）：
#    python tools/ccproxy.py --port 3460 \
#      --upstream https://api.stepfun.com/v1/chat/completions \
#      --model step-5-preview --key $STEPFUN_API_KEY --no-reasoning
```

**推理 vs 无推理（按需切换）**：
- `step-5-preview` 是**推理模型**，答题前默认先"想"很久 → 墙钟慢（重 agentic 任务可达数分钟）。
- 加 `--no-reasoning` 后 ccproxy 向上游发 `chat_template_kwargs: {"enable_thinking": false}`，
  模型直接出答案，同 prompt 约快 2 倍（实测 10s → 5s）。
- 两个 profile：`~/.claude/profiles/stepfun.json`（3459，思考开）、
  `stepfun-nothink.json`（3460，思考关）。切换器两个按钮分别对应，互不冲突（不同端口）。

**关键注意（必读）**：
- **Claude Code 经 ccproxy 现在也能原生读图了**：本技能内置的 `ccproxy.py` 已修复图片转发
  （2026-10-12），把 Anthropic `image` 块转成 OpenAI `image_url` 直发上游。所以 StepFun / omni
  在 Claude Code 里贴图即看，无需 vision bridge 兜底。
- 想用 vision bridge 给纯文本模型加读图，仍走场景 F；StepFun 自带读图，直接用即可。
- **StepFun 偶发空 content（上游 quirks）**：个别请求返回 200 但 content 为空。本技能内置
  `ccproxy.py` 已加 **空回复自动重试**（`retry_empty`，默认 2 次），非流式请求空回复会自动
  重发，实测 5/5 稳定返回正文；流式不受重试保护。仍偶发空时换一次即可。
- **`effortLevel: medium` / `forward_images: true`**：关重推理避免空 content，开图片转发。
- StepFun 免费非永久，监控下线用 `--watch`（平台额度耗尽会变 401）。

**桥接层专项优化（ccproxy 已内置，针对"推理模型很慢"）**：
| 项 | 配置 | 作用 |
|---|---|---|
| Prompt Cache 头 | 对 stepfun.com 自动加 `Stepfun-Prompt-Cache: enable` | 缓存 system/上下文，第二轮起 TTFT 减半 |
| 固定 `reasoning_effort` | `pin_reasoning_effort: "medium"` | **动态映射会让缓存永久 miss**；置空回退旧的按 thinking budget 推导 |
| 缓存命中日志 | `log_cache_hit: true` + `include_usage: true` | 每次调用打印 `cached_tokens` 与 `HIT (x% cached)` / `MISS`，不用靠 TTFT 猜 |
| 思考链回传 | `reasoning_to_thinking: true` | `reasoning_content` → Anthropic `thinking` 块；**不回传会让 Claude Code 工具调用异常** |
| 大输入告警 | `warn_input_tokens: 80000` | 单轮输入超阈值 stderr 提示 `/clear` |
| 流式透传 | — | 逐 chunk write+flush，**不预加载全量**（SSE 不被缓冲） |
| 重试退避 | `retry_backoff: 0.5` / `retry_empty_backoff: 0.5` | 连接失败重试与空回复重试的等待秒数。**别调大**——Claude Code 自己有截止时间，桥接侧干等只会烧掉它（免费模型抖动时更容易触发 auto-mode 校验超时） |
- WorkBuddy 直连 vs Claude Code 经 ccproxy：能力完全一致（都走官方 OpenAI 端点），区别仅在于
  Claude Code 多一层本地代理；代理已支持图片，无能力损失。

## 其他命令

```bash
python scripts/install_free_llms.py --list                # 列出已配置的模型
python scripts/install_free_llms.py --dry-run             # 只看要做什么，不写文件
python scripts/install_free_llms.py --force               # 覆盖同 id 的现有配置
python scripts/install_free_llms.py --zhipu-key KEY      # 安装智谱 GLM 梯队
python scripts/install_free_llms.py --deepseek-key sk-xxx # 顺便加 DeepSeek（付费！）
python scripts/install_free_llms.py --stepfun-key KEY    # 安装阶跃星辰 Step 5 Preview（限时免费）
python scripts/install_free_llms.py --models /path/to/models.json
python scripts/install_free_llms.py --watch --watch-log /path/to/watch.log
```

## 监控相关参数

| 参数 | 默认 | 说明 |
|---|---|---|
| `--watch` | 关 | 开启定期探测模式 |
| `--watch-interval` | `1800`（秒） | 两轮之间的间隔 |
| `--watch-rounds` | 无限 | 跑够 N 轮后自动退出 |
| `--watch-gap` | `2.0`（秒） | 同轮内模型间的请求间隔 |
| `--watch-log` | `~/.workbuddy/free_llm_watch.log` | 变化日志路径 |

## 关键实现细节

- **配置文件位置**：`~/.workbuddy/models.json`（脚本自动探测，也支持 `XDG_CONFIG_HOME`）。
- **原子写入**：先写 `.tmp` 再 `os.replace`，避免写一半损坏。
- **每次写入前自动备份**到 `backups/models.json.bak-install-free-<时间戳>`。
- **网络抖动重试**：SSL 中断等 `NET` 类错误自动重试 2 次（间隔 3s）；429 在工具验证阶段重试 2 次（间隔 8s）。

## 故障诊断：SSL: UNEXPECTED_EOF_WHILE_READING

报这个错时**先怀疑代理链路，不要先怀疑模型**（2026-10-14 踩坑：误以为模型下架，实测模型完全正常）。
`~/.claude-code-proxy.json` 的 `upstream.proxies` 是**易腐配置**——本地代理端口会随 VPN 客户端
重启/换节点漂移，出现「端口还在监听但对该站 TLS 握手必断」的情况。

**三路对比定位**（一次跑完就知道是哪条链路坏）：

```bash
python - <<'PY'
import json, time, urllib.request
URL='https://api.kilo.ai/api/gateway/v1/chat/completions'
BODY=json.dumps({'model':'liquid/lfm-2.5-2.6b:free','max_tokens':200,
                 'messages':[{'role':'user','content':'hi'}]}).encode()
def t(label, opener):
    t0=time.time()
    try:
        r=urllib.request.Request(URL,data=BODY,headers={'content-type':'application/json',
                          'Authorization':'Bearer anonymous'})
        with opener.open(r,timeout=45) as resp: resp.read()
        print('%-18s %.1fs OK' % (label,time.time()-t0))
    except Exception as e:
        print('%-18s FAIL %s: %s' % (label,type(e).__name__,str(e)[:70]))
t('direct',   urllib.request.build_opener(urllib.request.ProxyHandler({})))
t('env-proxy',urllib.request.build_opener(urllib.request.ProxyHandler()))
PY
```

再单独试配置里那个代理端口（换成实际端口号），哪条 FAIL 就是哪条的问题。

**修复**：启动时加 `--proxy ""`（强制直连、忽略环境变量、清空 proxies 池）：

```bash
python tools/ccproxy.py --port 3461 \
  --upstream https://api.kilo.ai/api/gateway/v1/chat/completions \
  --model liquid/lfm-2.5-2.6b:free --key anonymous --proxy ""
```

启动日志会打印 `[ccproxy] upstream route: direct`（或代理列表）确认生效。
VPN 是 TUN 透明模式时直连就等于已走隧道，不需要再套一层本地代理。
- **非法 JSON 拒绝写入**：配置损坏时报错退出，不覆盖用户数据。
- **必须带浏览器 UA**：Kilo / Zen 前有 Cloudflare，Python 默认 UA 会被拦。
- **推理模型 token 预算**：verify/probe 对 `supportsReasoning` 模型自动放大 `max_tokens`，避免 reasoning 截断。

## 注意事项（转述给用户时用）

- 免费模型**不适合当生产主力**：额度小，agent 循环一轮要 5-20 次调用。
- 免费池高峰会 429（尤其智谱 glm-4.7-flash / Kilo omni 偶发 16/16）。`kilo-auto/free` 的自动路由能缓解这个问题。
- 国外平台（Groq/Together/HF/Mistral/Google）从国内网络基本不可达或被封；唯一稳定可达且免 key 的是 OpenRouter 公开列表。
- 免费渠道的数据可能进上游训练集，**不要放密钥、用户数据、生产代码**。
- 政策随时变。`--refresh` / `--probe-foreign` 能查到当前真实情况，但「能列出来」≠「能调用」，仍需 `--verify` 确认。
- 免费模型会突然限流或下线。`--watch` / `--report` 挂后台跑就能第一时间知道。
