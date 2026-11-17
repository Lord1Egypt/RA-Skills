---
name: claude-code-third-party-model
slug: claude-code-third-party-model
displayName: Claude Code 接入第三方模型
version: 1.3.0
license: MIT
category: dev-programming
subCategories: [dev-script, dev-bug-fix]
platforms: [WorkBuddy, Claude Code, Codex]
description: 把本地 Claude Code 接到第三方端点——分两路：① 原生 Anthropic 兼容端点（DeepSeek / Kimi / GLM）直接改 ANTHROPIC_BASE_URL；② 只有 OpenAI 兼容端点的模型（Space Bunny / 各类 stealth 模型）必须加本地网关做 Anthropic→OpenAI 协议转换 —— **用自建零依赖 `ccproxy.py`**（claude-code-router 2.1.1 的流式 SSE 输出畸形、已弃用）。并诊断「模型名写对了却不生效」「配置被别处覆盖」「未知模型告警」「连第三方后变慢」「API Error: The response stream was malformed」五类问题。当用户说「给 claude code 配置 deepseek/别的模型」「claude code 换模型不生效」「ANTHROPIC_BASE_URL 怎么设」「unrecognized_model 警告」「claude code 连 deepseek 很慢」「effort 设多少」「要不要开 max」「把 OpenRouter 上的某某模型接进 claude code」「space bunny 怎么接」「响应流畸形/回答不完整/流式报错」「网关 502 / WinError 10054 刷屏」「error code 1010」「It may not exist or you may not have access to it」「卡住不动」「Bash 工具卡住」「auto mode cannot determine the safety of Bash」「大 payload 变慢」时使用。也覆盖**多 profile 一键切换**（`ccswitch.py`：「切 deepseek」「切 space bunny」「现在什么模型」）。含模型 ID 实测法、配置优先级判定法、Windows 注册表排查、用本地中继抓真实请求做性能归因、claude-code-router 的 config-router.json 文件名陷阱、自建网关的规范 SSE 生成法与客户端令牌鉴权。也覆盖**把模型配进 WorkBuddy 客户端**（`~/.workbuddy/models.json`）——含「`apiKey` 留空会被回落成平台 token 导致上游 401 / 错误码 3001」这一最易踩坑的诊断与修法。
agent_created: true
---

# Claude Code 接入第三方模型（Anthropic 兼容端点）

> 开源仓库：<https://github.com/oracis/claude-code-third-party-model>
> 本技能自带两个**零依赖**脚本（在 `scripts/` 目录下）：
> **`ccproxy.py`** —— Anthropic ↔ OpenAI 协议转换网关（纯标准库，约 1240 行）；
> **`ccswitch.py`** —— 多 profile 一键切换 + 网关启停协调（跨平台，约 430 行）。
> 另有 `examples/profiles/` 提供开箱可用的 `settings.json` 模板。

## 核心思路

**不要相信文档里的模型名，也不要猜哪份配置生效 —— 两件事都实测。**

第三方文档经常出现旧模型名 / 别名混写（例如 DeepSeek 官方两版文档分别写
`deepseek-flash` 和 `deepseek-v4-flash`）。以**服务端报错为准**。

---

## Step 1 · 实测真实模型 ID

先看账号可用清单：

```bash
curl -s https://api.deepseek.com/models -H "Authorization: Bearer $KEY"
```

再拿候选名逐个打 Anthropic 兼容端点（**这才是权威**，`/models` 常漏别名）：

```bash
KEY=$(python -c "import json;print(json.load(open(r'C:/Users/<u>/.claude/settings.json'))['env']['ANTHROPIC_AUTH_TOKEN'])")
for M in "deepseek-flash" "deepseek-flash[1m]" "deepseek-v4-flash" "deepseek-chat" "deepseek-v4.1-flash"; do
  printf '%-24s => ' "$M"
  curl -s -m 45 https://api.deepseek.com/anthropic/v1/messages \
    -H "x-api-key: $KEY" -H "anthropic-version: 2023-06-01" -H "content-type: application/json" \
    -d "{\"model\":\"$M\",\"max_tokens\":8,\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}]}" \
    | python -c "import sys,json;d=json.load(sys.stdin);print('OK ->',d['model'] if 'model' in d else 'ERR '+str(d.get('error',{}).get('message'))[:160])"
done
```

要点：
- 若本机设置了 HTTP 代理，curl 默认会经代理转发；给 curl 加 `--noproxy` 声明直连目标
  （如 `--noproxy api.deepseek.com`），或按第五部分把目标列入 `no_proxy` 环境变量。
- 失败时报错信息会**直接列出全部合法模型名**，这是最快的权威来源。
- 成功时回显的 `model` 字段是**服务端归一化后的真名**，能看出哪些是别名
  （如 `deepseek-chat` → 回 `deepseek-v4-flash`）。

> 已知别名关系（DeepSeek，2026-09 实测）：`deepseek-flash` = `deepseek-v4-flash`
> = `deepseek-chat`（同一模型，即 V4.1 Flash）；`deepseek-v4.1-flash` **不存在**。

## Step 2 · `[1m]` 后缀是什么

`[1m]` **不是模型名的一部分**，是 Claude Code 本地的「上下文窗口声明」后缀，服务端会剥离
（发 `deepseek-flash[1m]` 回体是 `"model":"deepseek-flash"`）。

- 不加：CC 按 **200k** 处理 auto-compact。
- 加：`modelUsage.contextWindow` 变 **1000000**。
- 模型不在 CC 内建目录时会打一行 `[claude-code:unrecognized_model]` 到 stderr，
  **无害、不影响功能**，`CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT=1` 也消不掉，
  别在这上面浪费时间。
- 更精细的控制用 `CLAUDE_CODE_AUTO_COMPACT_WINDOW`（DeepSeek 官方建议 `786432`）。

## Step 3 · 配置模板

`~/.claude/settings.json`（**用户级、跨项目**，是唯一真相源）：

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "<KEY>",
    "ANTHROPIC_MODEL": "deepseek-flash[1m]",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "deepseek-flash[1m]",
    "ANTHROPIC_DEFAULT_OPUS_MODEL_NAME": "deepseek-flash",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "deepseek-flash[1m]",
    "ANTHROPIC_DEFAULT_SONNET_MODEL_NAME": "deepseek-flash",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "deepseek-flash",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL_NAME": "deepseek-flash",
    "ANTHROPIC_DEFAULT_FABLE_MODEL": "deepseek-flash[1m]",
    "ANTHROPIC_DEFAULT_FABLE_MODEL_NAME": "deepseek-flash",
    "CLAUDE_CODE_SUBAGENT_MODEL": "deepseek-flash[1m]",
    "CLAUDE_CODE_EFFORT_LEVEL": "max",
    "CLAUDE_CODE_AUTO_COMPACT_WINDOW": "786432",
    "API_TIMEOUT_MS": "600000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
  },
  "model": "deepseek-flash[1m]",
  "tui": "fullscreen"
}
```

`_MODEL_NAME` 是**显示名**（不带 `[1m]`）；`_MODEL` 是**真正发给 API 的 ID**。
`DEFAULT_*_MODEL` 让 `/model opus|sonnet|haiku` 都落到同一个模型。

## Step 4 · 查真实支持的 env 变量名（别照抄博客）

Claude Code 现在是**单文件 native 二进制**（不是 js），直接从里面提取权威变量名：

```bash
B="$APPDATA/npm/node_modules/@anthropic-ai/claude-code/bin/claude.exe"
strings -n 6 "$B" | grep -ohE "ANTHROPIC_[A-Z_]+|CLAUDE_CODE_[A-Z0-9_]+|API_TIMEOUT_MS" | sort -u
```

（Windows 的 `$APPDATA` 在 Git Bash 下即 `C:/Users/<u>/AppData/Roaming`。）
值得注意的真实变量：`ANTHROPIC_DEFAULT_FABLE_MODEL`、
CLAUDE_CODE_{MAX_CONTEXT_TOKENS, AUTO_COMPACT_WINDOW, SUBAGENT_MODEL, EFFORT_LEVEL,
DISABLE_1M_CONTEXT, MODEL_CATALOG, MODEL_OVERRIDES...}。

## Step 5 · 判定「哪份配置生效」—— 必须实测

**优先级实测结论：`settings.json` 的 `env` 块 > 从 shell/系统继承的进程环境变量。**
（官方文档那句「shell 导出的 ANTHROPIC_MODEL 优先于文件里的 `model` **键**」说的是
`model` 键，不是 `env` 块，别被绕进去。）

**验证方法**（唯一可靠手段）：跑一次带 JSON 输出的查询，读 `modelUsage`。

```bash
cd <项目目录> && claude -p "hi" --output-format json < /dev/null 2>&1 \
  | tr -d '\r' | grep -o '"modelUsage":{.*' | head -c 600
```

看 `canonicalModel` 和 `contextWindow` 就知道真实生效的是什么。
验证子代理：提示里让它起一个 Agent，再 grep `"canonicalModel":"..."`。

## Step 6 · 排查其它覆盖源（Windows）

依次查这些地方，**任何一处都会造成「改了不生效」**：

```bash
# 1) 用户/系统级持久环境变量（用 Python winreg 读，最省事）
python -c "
import winreg
for root,lab in ((winreg.HKEY_CURRENT_USER,'HKCU'),(winreg.HKEY_LOCAL_MACHINE,'HKLM')):
    try:
        k=winreg.OpenKey(root,r'Environment'); n=winreg.QueryInfoKey(k)[1]
        for i in range(n):
            nm,v,_=winreg.EnumValue(k,i)
            if 'ANTHROPIC' in nm.upper() or 'CLAUDE' in nm.upper(): print(lab,nm,'=',v)
    except FileNotFoundError: pass
"
# 2) 项目级覆盖（优先级高于用户级）
cat .claude/settings.json .claude/settings.local.json 2>/dev/null
# 3) ~/.claude.json 里的 model / env 字段
python -c "import json;d=json.load(open(r'C:/Users/<u>/.claude.json'));print({k:d[k] for k in ('model','env','primaryApiKey') if k in d})"
```

改 HKCU 环境变量后**必须广播**，否则已开着的资源管理器/终端读不到新值：

```python
import ctypes
ctypes.windll.user32.SendMessageTimeoutW(0xFFFF, 0x1A, 0, ctypes.c_wchar_p('Environment'),
                                         0x0002, 5000, ctypes.byref(ctypes.c_ulong()))
```

## 收尾清单

- [ ] 改前备份：`cp ~/.claude/settings.json ~/.claude/backups/settings.json.bak-$(date +%Y%m%d-%H%M%S)`；
      若要动 HKCU，先把变量导出一份 json 到同目录。
- [ ] 改后**必须**跑 Step 5 验证主模型 + 子代理模型，不能只看配置文件。
- [ ] 报告里**不要回显 API Key**，只说前缀 + 长度。
- [ ] 收尾时用 Step 9 检查是否留下了重复配置源。

## 常见坑速查

| 现象 | 根因 |
|---|---|
| 报 `invalid_request_error` 且列出支持名 | 模型名错/不存在，用报错里列的名字 |
| 每次启动一行 `[claude-code:unrecognized_model]` | 正常，第三方模型都不在 CC 目录里 |
| `contextWindow` 只有 200000 | 模型名忘了加 `[1m]` |
| 改了 settings.json 不生效 | 有 HKCU/项目级/`.claude.json` 覆盖，或没重启 CLI |
| 命令行读注册表不方便 | 直接用 Python `winreg`，无需外部程序 |
| PowerShell 有时 exit 0 但无输出 | 该环境下 stdout 未必回显，换 bash + python 排查更可靠 |
| `export ANTHROPIC_MODEL=...` 后没变化 | `settings.json` 的 env 块优先级更高，见 Step 7 |

---

# 第二部分：接入后「变慢」怎么定位

**不要猜。** 慢只有四个来源：启动开销 / 网络 / 模型推理 / 交互感知。按下面顺序逐层排掉。

## Step 7 · 先记住优先级铁律（决定了怎么切档）

```
claude --model / --effort 等命令行参数
      >  ~/.claude/settings.json 的 env 块
      >  shell / 系统 继承来的环境变量
```

**推论（最容易踩）**：`export ANTHROPIC_MODEL=xxx` 再启动 claude **不生效**，因为
settings.json 的 `env` 块会覆盖它。所以：
- **单次切换** → 用命令行参数：`claude --effort high --model deepseek-flash[1m] -p "..."`
- **会话内即时切换** → 交互模式里用 `/effort`、`/model` 斜杠命令
- **持久切换** → 改 settings.json（建议写个小工具，见下方 ccmode 思路）
- **千万不要顺手同步一份到 HKCU 环境变量**——见 Step 14「单一配置源」

> 判据校验：`claude --effort bogus -p hi` 会打印合法值清单，比翻文档快。
> 实测合法值：`low / medium / high / xhigh / max`。**`off` 不在其中**，会被静默忽略。

## Step 8 · 用本地中继抓真实请求体（唯一可靠手段）

搭一个 127.0.0.1 上的透明转发，把 `ANTHROPIC_BASE_URL` 指过去，
就能录到 Claude Code **真实发出的 JSON**（含 thinking 配置、工具数、body 大小）。

关键实现点：
- 用 `http.server.ThreadingHTTPServer` + `http.client.HTTPSConnection`，纯标准库。
- 上游响应必须**边收边发**（`transfer-encoding: chunked`），否则会破坏 SSE 流。
- 记录 `ttfb` / `first_chunk` / `total` / 请求体里的 `thinking` / 响应里的 `usage`。
- 用同目录 `tag.txt` 给每一轮实验打标签，避免多次运行串味。
- `ANTHROPIC_BASE_URL` 支持 `http://`，指向 127.0.0.1 时记得把 `NO_PROXY` 加上 `127.0.0.1`。

**⚠️ 最大坑**：在 Bash 工具里用 `nohup ... &` 起的中继会**随该次命令的进程组一起被杀**，
表现为「Claude Code 连不上 → 一直重试 → 看起来像卡死」，
而且因为 SIGTERM 打断管道，**连报错都看不到**。
必须用工具自带的后台运行能力（`run_in_background`）启动长驻进程。
改坏 settings.json 后要立刻还原，别让它停在指向死端口的状态。

## Step 9 · `CLAUDE_CODE_EFFORT_LEVEL` 对第三方模型通常是空操作

**实测（DeepSeek，2026-09 复核）**：在 low / medium / high / xhigh / max 五档下，
Claude Code 发出的请求体**完全一致**：

```json
"thinking": {"type": "adaptive", "display": "omitted"}
```

`body_bytes` 五档完全相同（66008）。因为 Claude Code 判定该模型走
**adaptive thinking**（模型自己决定想多久，不设 token 预算），
所以**根本没有 effort 这个旋钮可拧**。

跑出来的对照数据（同一道逻辑题，重复 3 次）：

| effort | wall 均值 | 输出 token 均值 |
|---|---|---|
| high | 15.3s | 829 |
| max  | 15.0s | 830 |

**差异 0.3s / 1 个 token，纯噪声。** 结论：对 DeepSeek 别在 effort 上调优，
它不改变任何东西。（`low` 更快的前提是模型真的收到小预算；adaptive 下不成立。）

判断某模型是否 adaptive：R 代码里 `CCn({runtimeOverride, resolvedModel, canonicalModel})==="adaptive"`
就读 `ANTHROPIC_DEFAULT_*_MODEL_SUPPORTED_CAPABILITIES` 里的能力声明。

## Step 10 · 把 wall time 拆成「API 耗时」和「Claude Code 开销」

有了中继记录（`total` = 纯 API 耗时）和 `claude -p` 的 wall time，一减就出来了：

```
Claude Code 开销 = wall_s − 中继记录的 total
```

**实测样例（本机）**：

| 项 | 数值 |
|---|---|
| 中继测得的纯 API 耗时 | 2.9–5.6s（**164–221 tok/s**） |
| 裸 curl 直连同一道题 | 3.1s（**181 tok/s**） |
| `claude -p` wall time | 13.4–17.8s |
| **`claude --version`（零模型调用）** | **4.9–5.5s** |

→ **API 侧完全正常，瓶颈是 Claude Code 每次进程启动约 5 秒。**
反过来说，如果 `claude --version` 都要好几秒，那「换模型/调 effort」全都白费。

**启动慢的常见原因与验证**：
```bash
for i in 1 2 3; do S=$(date +%s.%N); claude --version >/dev/null 2>&1; E=$(date +%s.%N); \
  python -c "print(f'{$E-$S:.2f}s')"; done      # 走 npm shim
EXE=<npm>/node_modules/@anthropic-ai/claude-code/bin/claude.exe
$EXE --version                                   # 直接调二进制 —— 关键对照！
cat <claude.exe> > /dev/null                     # 纯磁盘读 227MB 要多久
echo 'exit 0' > /tmp/n.sh; bash /tmp/n.sh        # 空 sh 脚本 —— 量 shell 层开销
```

### ⚠️ 先量 shim 层，再怪杀软（2026-09-23 实测推翻了旧结论）

**旧结论（错误）**：「`node -e ""` 也要 2s → 杀软实时扫描在拖后腿，加 Defender 排除项」。
**实测打脸**：加了排除项（路径 + 进程）后**毫无变化**，而真正的差异在别处：

| 路径 | 耗时 |
|---|---|
| **`claude.exe --version`（直接调二进制）** | **1.14–1.34s** |
| `claude --version`（经 npm 的 shim） | 4.06–5.66s |
| 空 sh 脚本（什么都不做） | 1.10–1.41s |
| 读 227MB 二进制 | 1.41s（**161 MB/s**，磁盘正常） |

→ **多出来的 3–4 秒是「多一层 shell 包装」的开销**（`claude` 实际是
`npm/claude` 这个 `#!/bin/sh` 脚本，`exec` 到真正的 exe；在 MSYS 等 POSIX 兼容层下每层 sh
启动约 1.2s）。**不是 Defender，不是磁盘，不是网络。**

判断方法：`bash /tmp/空脚本.sh` 就要 1.2s 的话，说明是**当前执行环境**的进程创建开销，
**用户在自己真实终端里不会有这个损耗** —— 别拿受限环境里的 wall time 当用户的真实体验。

**`node -e ""` 慢不等于杀软**：claude 是 native 二进制，根本不经 node 启动，
用 node 当对照组本身就是错的对照。

### ⚠️⚠️ 性能测量必须 A/B/A，本机噪声能吃掉一切结论

**2026-09-23 的惨痛教训**：先入为主地认为「慢 = 杀软」，加了一堆排除项，
最后 A/B/A 一测发现**全部是噪声**。具体数据：

| 项目 | ①无排除 | ②有排除 | ③撤销后 |
|---|---|---|---|
| 建 100 个文件 | 1391ms | 1432ms | **660ms**（最快！） |
| 建 60 个目录 | 652ms | 464ms | 761ms（最慢） |
| python 启动（同一状态连测 3 轮） | 790 / 730 / **1303** ms | | |

**同一状态下 python 启动能在 335–1303ms 间波动（4 倍！）**，
而排除项带来的差异只有几十毫秒 —— **完全淹没在噪声里**。

必守规则：
1. **任何性能改动都要 A/B/A**：改前 → 改后 → 撤销后再测。
   只做 A→B 会得出错误结论（顺序效应 = 缓存预热/系统负载）。
2. **每项至少重复 10–15 次取中位数，并看标准差**。
   差异小于 1 个标准差 = 不可信，直接判「无效果」。
3. **别拿单轮数据下结论**。第一次跑通常偏慢（冷），后面才稳定。
4. 大目录 `du -sh` 会超时被 SIGTERM，用 Python `os.walk` 加时间上限。
5. 单次超过 ~100s 的基准脚本会被前台超时杀掉，拆小或后台跑。

**最终结论**：Defender 排除项在这台机器上**无可测量收益**，代价却是
若干目录脱离实时扫描 → **不加**。
只有在「单个操作涉及成千上万小文件」（npm install / git clone / 解压大包）
且实测收益稳定 >30% 时，才值得针对那个具体目录临时加。

Defender 排除项若要加（**需管理员 + 必须先问用户**）：
`Add-MpPreference -ExclusionPath "<npm>\node_modules\@anthropic-ai\claude-code"`
（读排除项也要管理员：HKLM `...\Windows Defender\Exclusions\Paths` 普通权限 `PermissionError`）
**加完必须复测**；无改善就撤销（`Remove-MpPreference`），别留着白降防护。

## Step 11 · 缓存：默认是好的，别误判

会话内**上下文缓存是生效的**。同一 session 的第 2 个请求：
`cache_read_input_tokens: 16384`，`input_tokens` 从 16359 掉到 174。

**别被假象骗了**：每次 `claude -p` 都是全新会话（冷缓存），
单个请求的 `cache_read` 恒为 0 —— 这不代表缓存坏了。
要验证缓存，必须让**一次会话发出 ≥2 个请求**（例如给它一个需要调用工具的提示）。

## Step 12 · 交互模式「感觉卡住」大多是思考被隐藏了

`display: "omitted"` 时思考过程不渲染，用户盯着空白等 = 主观上「好慢」。
交互模式下让思考可见的设置键是 **`showThinkingSummaries: true`**
（源码：`showThinkingSummaries ?? false` → 为真则 `display: "summarized"`）。
合法 display 值：`summarized` / `omitted` / `highlights`。

## Step 13 · 换大模型前先量一下，pro 有可能更慢

同一道题的裸 API 对照（DeepSeek）：

| 模型 | 简单推理 | 多步推理 | 吞吐 |
|---|---|---|---|
| `deepseek-flash` | 2.7–3.5s ✅ | 4.6–10.6s ✅ | **164–204 tok/s** |
| `deepseek-v4-pro` | 24.9–32.9s ✅ | 67.6–74.0s ⚠️ | **41–52 tok/s** |

- pro 吞吐只有 flash 的 **约 1/4**；同样一道简单题它也要「想」1300–1565 token（flash 的 3 倍）。
- pro 在多步推理题上会**一路想到 max_tokens 上限仍不给结论** —— 提示词里要求「最后一行输出结论」
  时它会直接截断。
- 所以：**「换个更强的模型」在第三方端点上经常是先换来 4–10 倍的等待**。
  要换就明确告诉用户这个代价，别默认 pro 更好。

## 性能问题速查表

| 现象 | 先查什么 |
|---|---|
| 每次启动都慢 | `claude --version` 计时；杀软实时扫描；二进制大小 |
| `claude -p` 慢但交互不慢 | 每次调用都要付一次进程启动成本，用会话复用/`--continue` |
| 第一个字出来很慢 | 中继的 `ttfb` vs `first_chunk`；adaptive thinking 在想 |
| 每轮都慢 | 中继看 `total`；对比裸 curl 同题 |
| 换 pro 后更慢 | 正常，见 Step 13 |
| 调 effort 没变化 | 正常，见 Step 9 |

---

# 第三部分：收尾——只留一份配置源

## Step 14 · 单一配置源（Single Source of Truth）

**结论：配置只写在 `~/.claude/settings.json`，不要同时在 Windows 环境变量里放一份。**

理由（实测）：
1. **环境变量那份根本不起作用**。`settings.json` 的 `env` 块优先级更高（Step 5），
   两处同值时行为一致，两处不同值时以 `settings.json` 为准。
2. **它是麻烦的源头**。一旦 `settings.json` 被删、或 `CLAUDE_CONFIG_DIR` 变了，
   环境变量那份会**静默接管**并指向另一个模型（可能更贵）。
3. **环境变量会泄漏给所有子进程**。`ANTHROPIC_AUTH_TOKEN` 进了系统环境，
   任何 npm postinstall、构建脚本都能读到你的 API Key。`settings.json` 只有 CC 自己读。
4. 排查时要两处对照，纯粹增加心智负担。

**清理流程**（清理前先确认没有别的工具依赖这些变量）：

```python
import winreg, json, os, ctypes
# 1) 先备份
k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Environment', 0, winreg.KEY_QUERY_VALUE)
hits = {winreg.EnumValue(k,i)[0]: winreg.EnumValue(k,i)[1]
        for i in range(winreg.QueryInfoKey(k)[1])
        if 'ANTHROPIC' in winreg.EnumValue(k,i)[0].upper()
        or 'CLAUDE_CODE' in winreg.EnumValue(k,i)[0].upper()}
json.dump(hits, open(backup_path,'w',encoding='utf-8'), indent=2)
# 2) 删除
k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Environment', 0, winreg.KEY_SET_VALUE)
for name in hits: winreg.DeleteValue(k, name)
# 3) 广播，否则已开的终端仍持有旧值
ctypes.windll.user32.SendMessageTimeoutW(0xFFFF, 0x1A, 0,
    ctypes.c_wchar_p('Environment'), 0x0002, 5000, ctypes.byref(ctypes.c_ulong()))
```

**清理前必查**：有没有别的消费者（aider / codex / 自己写的 curl 脚本 / MCP 配置里的
`${ANTHROPIC_*}`）。查法：在用户目录里 grep `ANTHROPIC_AUTH_TOKEN|ANTHROPIC_BASE_URL`。

> ⚠️ grep 坑：WorkBuddy 工作区里若有名为 `nul` 的文件，ripgrep 会直接
> `os error 1` 崩掉退出码 2；大目录还会 30s 超时。改用 Python `os.walk`
> 自己过滤后缀和跳过大目录。

**验证删干净了没有**（关键：必须在干净环境里跑，否则当前 shell 还继承着旧值）：

```python
import os, subprocess, re
env = {k:v for k,v in os.environ.items()
       if not (k.upper().startswith("ANTHROPIC") or k.upper().startswith("CLAUDE_CODE"))}
p = subprocess.run([r"C:/Users/<u>/AppData/Roaming/npm/claude.cmd",
                    "-p", "hi", "--output-format", "json"],
                   capture_output=True, text=True, env=env, timeout=240,
                   stdin=subprocess.DEVNULL)
print(re.search(r'"canonicalModel"\s*:\s*"([^"]*)"', p.stdout).group(1))
```

能正常返回 `canonicalModel` 就证明 **settings.json 单独撑得住**。

> subprocess 坑：Windows 上传 `"claude"` 会 `FileNotFoundError`，必须给
> **`claude.cmd`** 的完整路径。

**配套要求**：如果你写了自己的切档工具，**它必须只写 settings.json**。
否则下次切档又把环境变量写回来，两份配置死灰复燃。

---

# 第四部分：Windows 环境注意点

## `ConnectionResetError: [WinError 10054]` 满屏 traceback（2026-10-06 实测根治）

**症状**：网关窗口刷出整块 traceback，源头是 `socketserver.py` 的
`process_request_thread`，栈底是 `handle_one_request` → `rfile.readline` →
`socket.recv_into`：

```
Exception occurred during processing of request from ('127.0.0.1', 10511)
  File "socketserver.py", line 766, in __init__ ... self.handle()
  File "http\server.py", line 415, in handle_one_request
ConnectionResetError: [WinError 10054] 远程主机强迫关闭了一个现有的连接。
```

**这本身不是故障** —— 客户端中途放弃请求就会这样。但**必须处理**，因为：

1. 一次中断刷一整块 traceback，几十行起步；
2. 它会把真正该看的日志（上游 400/5xx、`UNEXPECTED ERROR`）**淹没**；
3. 看起来像网关崩了，实际连接是好的。

**常见触发**（都是正常流量，不是 bug）：用户按 Esc / Ctrl+C 取消、
Claude Code 换掉不再需要的请求、keep-alive 空闲 socket 被对端回收、
流式响应读到一半客户端就关窗。

**修法（`ccproxy.py`，两处 + 一个常量）**：

```python
CLIENT_GONE = (ConnectionResetError, ConnectionAbortedError, BrokenPipeError)
```

1. `Handler.handle_one_request` 覆盖：包住基类调用，只捕获上面三个异常 →
   置 `close_connection = True`，打**一行**说明后正常返回。
2. 新增 `QuietThreadingHTTPServer(ThreadingHTTPServer)`，覆写 `handle_error`：
   - `CLIENT_GONE` → 一行日志（路由到 `log()`，可被 verbose 关闭）
   - `TimeoutError` → 一行日志（空闲 keep-alive 被回收也是这个形态）
   - **其他异常 → `log_always()` 打出 `UNEXPECTED ERROR handling request from ...`
     再调 `super().handle_error()` 保留原traceback**。
     绝不能静默吞掉真故障。
3. `main()` 里改用 `srv = QuietThreadingHTTPServer(...)`。
4. 新增 `log_always()`：不受 `--verbose` 影响的输出通道。
   桌面启动器默认**不加** `--verbose`，真实错误若走 `log()` 就永远看不见 ——
   这是排查问题时最容易踩的空。

`WinError 10053`（本地软件中止了已建立的连接，中文系统上对应 `ECONNABORTED`）
与 10054 同类，也要一并捕获；流式写回时它已被 `do_POST` 的 `except` 收尾。

**验证方法**：不能只测正常请求，要**主动制造中断**：

```python
# 1) 发一半 body 就 close
s.sendall(headers + body[:len(body)//2]); s.close()
# 2) 连上就 close，一个字节都不发
s.close()
# 3) 流式响应读一半就 close
r.read(120); c.close()
```

每种打 3 次，然后检查网关 stderr：**零 traceback**，且每个请求恰好一行日志。
实测 9 次中断 → 9 行简洁日志，功能回归（keep-alive 10/10、中断场景 4/4）全通过。

## `stream error 10054` 之后再无请求 → 会话静默卡死（2026-10-06 实测根治）

**症状**（与上一节的 traceback 刷屏**完全不同**，别混淆）：

```
[ccproxy] stream error: [WinError 10054] 远程主机强迫关闭了一个现有的连接。
[ccproxy] client disconnected before the response was sent (harmless - it cancelled the request)
[ccproxy] "GET /health HTTP/1.1" 200 -
<此后日志静默，客户端再也没有新请求发出>
```

`/health` 还能 200，说明**监听线程活着**；但真实推理请求一个都不再出现，
整个会话像卡死。**这不是客户端问题，是网关的 bug。**

**根因（两条独立缺陷，缺一不可）**：

1. **非流式路径的 `resp.read()` 会永久阻塞**。上游先回
   `Content-Length: N` 再发 RST（`SO_LINGER{1,0}`），`http.client` 会**一直等
   满 N 字节**，RST 只让 `recv` 抛一次、被重试后继续等 → 线程永久卡住，
   客户端既收不到响应也等不到连接关闭（实测 `http=000`，6/6 全挂）。
2. **流式路径用「假装成功」掩盖截断**。RST 后旧代码调 `tr.finish()`，
   照发 `message_delta(end_turn)` + `message_stop`。客户端看到的是
   **一个语法完全合法、内容却被截断的"完整"回答**，于是接受它、不重试、
   不再发新请求 —— 表现就是「然后就没有新请求被发出来了」。

**为什么"重启就好"骗人**：`ThreadingHTTPServer` 每请求一线程，卡死的线程
不会传染，**流式请求仍能 200**（实测 RST 后 stream 200 / health 200，
只有 `stream:false` 挂死）。所以看起来"时好时坏"，实则取决于
Claude Code 该轮是否发了非流式请求。

**修法（`ccproxy.py` 三处）**：

```python
def do_POST(self):
    self._responded = False      # ① 区分"还没回复"和"已回复"
    ...
    if not want_stream:
        try:
            raw_body = resp.read()
        except Exception as e:
            log_always("upstream body read failed mid-flight: %s: %s" % (...))
            self._send_error_anthropic(502, "api_error",
                                       "upstream response was truncated: %s" % e)
            return                                  # ② 绝不静默挂死
    ...
    except Exception as e:
        log_always("stream error: %s: %s" % (type(e).__name__, e))
        if want_stream:
            self._send_stream_error("api_error", ...)   # ③ error 事件，不补 message_stop
        elif not self._responded:
            self._send_error_anthropic(502, "api_error", ...)
    finally:
        self.close_connection = True                   # 不留半开 keep-alive
```

**③ 是关键**：流式失败必须发 `event: error`（Anthropic 规范里表示
"这次尝试失败"），**不能补 `message_stop`**。补了等于告诉客户端
"这条回答完整结束了"，客户端就不会重试。

**验证方法（必须造 RST，不能只测正常请求）**：
写一个假上游，`SO_LINGER{1,0}` 后 `close()` 制造真 RST：

```python
self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))
self.connection.close()
```

非流式要**谎报 Content-Length**（`len(body)+50` 但只发 `len(body)`）
才能复现永久阻塞。修复前：6/6 `http=000` 挂死；修复后：6/6 在 **44ms** 内
返回 502，流式路径发出 `event: error` 且带已输出字符数。

**排查这条坑时踩到的两个环境陷阱（都不是代码问题，别误判成 bug）**：

- **`nohup ... &` 启动的进程会随工具 shell 退出被回收**。日志停在最后一行、
  端口无监听、`/health` 返回 502 —— 看起来像"网关又挂了"。
  工具里必须用后台任务方式启动（`run_in_background`）才活得久。
- ~~上游 `User-Agent` 不是断流原因~~。实测无 UA / 浏览器 UA / 诚实 UA
  各 3 次全部干净收尾（9/9），**不要**在这上面浪费时间。
  ⚠️ **2026-10-07 更正**：这条只在**直连**时成立。**经代理出口时 UA 恰恰是致命项** ——
  见下节「Cloudflare 1010」，当时正是这条旧结论让人差点改错方向。

## 请求行带绝对 URL → 404（2026-10-07 实测根治）

**症状**：网关日志里请求行长这样，**混在正常请求中间**：

```
[ccproxy] "POST /v1/messages?beta=true HTTP/1.1" 200 -
[ccproxy] "POST http://127.0.0.1:3457/v1/messages?beta=true HTTP/1.1" 404 -
[ccproxy] "POST http://127.0.0.1:3457/v1/messages?beta=true HTTP/1.1" 404 -
```

Claude Code 侧表现为**跑到一半报**：
`There's an issue with the selected model (space-bunny[1m]). It may not exist
or you may not have access to it. Run --model to pick a different model.`
—— 这句提示**极具误导性**：模型明明是好的，上下文窗口也确实是 1M。

**根因**：经代理（PROXY / TUN）时，客户端发给代理的是**绝对形式**的请求目标
（RFC 7230 §5.3.2 允许代理把绝对 URI 发给下一跳）。网关原来用
`self.path.split("?")[0]` 取路径，于是得到
`http://127.0.0.1:3457/v1/messages` —— 带 scheme 和 host，
跟 `/v1/messages` 比对不上 → **404**。

**修法（两处，`do_POST` 与 `do_GET` 各一个）**：

```python
from urllib.parse import urlparse      # 确认已导入

# do_POST
path = urlparse(self.path).path         # 原：self.path.split("?")[0]
# do_GET
if urlparse(self.path).path in ("/health", "/", "/status"):
```

`urlparse().path` 对两种形式都只返回路径部分，是标准解法。

**验证（用裸 socket 发绝对 URL，别只测相对路径）**：

```python
s = socket.create_connection(("127.0.0.1", 3457), timeout=60)
req = (b"POST http://127.0.0.1:3457/v1/messages?beta=true HTTP/1.1\r\n"
       b"Host: 127.0.0.1:3457\r\nx-api-key: " + tok.encode() +
       b"\r\ncontent-type: application/json\r\nContent-Length: " +
       str(len(body)).encode() + b"\r\nConnection: close\r\n\r\n" + body)
```

实测修复后：相对路径 200、绝对 URL 200、绝对 URL 的 `count_tokens` 200，
真实 `claude.exe -p` 带 Bash 工具跑 **6 轮 `is_error=false`**。

**判据：日志里同时出现 `/path` 和 `http://host/path` 两种形式 → 就是这个坑。**
`http.client` 不会把绝对 URL 发给你，所以这类问题**只在本机直连的测试里复现不出来**，
必须真的经代理跑一次多轮工具调用才会暴露。

## `error code: 1010`：`User-Agent` 被 Cloudflare WAF 拦（2026-10-07 实测根治）

**症状**：网关窗口刷 502 / `WinError 10054`，failures jsonl 里清一色
`upstream_status 599` + `ConnectionResetError`，**看起来像"上游挂了/网络不通"**。
但模型其实好好挂着，配置一个字都没错。

**根因**：`ccproxy.py` 原来只发 `Content-Type` + `Accept`，**不发 User-Agent**。
Python 客户端栈（`urllib.request` 会自动加 `Python-urllib/3.x`；裸 `http.client` 则可能干脆不发）被 Cloudflare 的 WAF 识别成机器人 →
回 `403 error code: 1010`。**且仅在经代理出口 IP 时触发，直连不触发。**

**决定性 A/B 表（各2 次，6/6 稳定复现）**：

| 链路 | User-Agent | 结果 |
|---|---|---|
| 经代理 | Python 默认（不设） | **403 `error code: 1010`** |
| 经代理 | `ccproxy/1.0 (+local gateway)` | 200, 1.9s |
| 经代理 | 浏览器 UA | 200, 1.6s |
| **直连** | Python 默认 | **200 ✅** |
| 直连 | 诚实 UA | 200, 2.0s |

**修法（`ccproxy.py` 的 `_open_upstream()`，一行）**：

```python
headers = {
    "Content-Type": "application/json",
    "Accept": "text/event-stream" if oa_req.get("stream") else "application/json",
    # 不设 UA 会被 WAF 403 1010，且表象像"上游挂了"
    "User-Agent": "ccproxy/1.0 (+local gateway)",
}
```

诚实 UA 就够，**不必伪装浏览器**。顺带：直连时带 UA 反而快 6 倍
（12.5s → 2.0s，慢的那次是 WAF 排队）。

### ⚠️ 判据顺序：403/4xx 错误码 > 超时

**这才是本次最贵的教训**：第一轮我看到 `http=000` / 15s 超时 / `WinError 10054`
就断定"Zen 上游对本机不可达"，还据此建议改网关的代理策略 —— **方向完全错了**。
超时是最不可靠的信号，因为它**能由"拒绝"伪装出来**（WAF 断连 / RST / 静默丢弃）。

→ **见到超时应先设法拿到一个状态码**（直连绕过代理打一次、看 `failures` 里有没有
`upstream_status`、或换 `curl -v` 看 TLS 握手在哪一步断）。
**`upstream_status 599` 是网关自己的合成码，不是上游返回的真实码** ——
它只说明"连接没能完成"，不能推出"上游不可用"。
真实错误码出现了（`403` / `401` / `400`）才是有信息量的。

### 为什么模型清单能 200 而推理 403

`GET /zen/v1/models` 是公开只读端点，WAF 放行；`POST /zen/v1/chat/completions`
才走 WAF 规则。**所以"能拉到模型清单"不能证明"推理能通"** ——
别用它当健康判据（`/health` 只验网关自己，不打上游，同样不能证明上游可用）。

**教训**：`log_always` 打出的 `stream error` 不是"无害噪音"，它是
**上游链路已经断了**的唯一信号。下一条请求不来时，先查
`netstat -ano | findstr :3457` 看监听是否还在 —— 监听在但请求不来，
才是本节这个 bug。

**别把工具的进程回收当成崩溃**：用工具后台任务启动的长驻服务，会在
任务生命周期结束时收到 `status: failed` 通知，但那是**外壳被回收**，
不等于进程死了。以 `netstat` + `/health` 为准 —— 实测出现过
通知报 failed、PID 已从 12040 变成 2400（被重新拉起）、端口仍在监听、
流式与非流式请求依然 200 的情况。**判定标准只有一个：端口是否 LISTENING。**

**判据：看到 socketserver 的 traceback 先别查网关逻辑** ——
先确认异常类型。`CLIENT_GONE` / `TimeoutError` 是客户端行为，与网关无关；
其它类型才顺着 `log_always` 标记去查。

## `count_tokens` 404 连环污染：`Bad request syntax ('{"model"...` （2026-10-06 实测根治）

**症状**（日志里连着出现，顺序固定）：

```
"POST /v1/messages?beta=true" 200 -
"POST /v1/messages/count_tokens?beta=true" 404 -
code 400, message Bad request syntax ('{"model":"space-bunny","messages":[...}],"tools":[]}POST /v1/messages?beta=true HTTP/1.1')
"POST /v1/messages?beta=true" 200 -
```

那个 `code 400 ... Bad request syntax` **不是上游报错**，是 `BaseHTTPRequestHandler`
自己打出来的 —— 注意它在消息里**重复了整个请求体并紧跟下一条请求行**，这是决定性特征。
看起来像客户端发了畸形请求、或像 body 里带了奇怪字符，实际都不是。

**根因（两个叠加）**：

1. **缺 `/v1/messages/count_tokens` 端点**。Claude Code 每次请求前都调它算上下文预算，
   而 `do_POST` 只认 `/v1/messages`，其它路径直接 404。
2. **致命的那一半**：404 是**在读取请求体之前**返回的。HTTP/1.1 keep-alive 下，
   客户端已经把几十 KB 的 body 写进 socket 了，我们没读走 →
   下一个请求复用同一 socket 时，解析器从**残留 body 中间**开始读 →
   把 body 的 JSON 当成请求行 → `Bad request syntax`。
   **body 越大越容易触发**（本例 body 是整个 page.tsx）。

→ **判据：`BaseHTTPRequestHandler` 里任何 return 之前，都必须先把 body 读干净。**

**修法**（`ccproxy.py`，两处）：

- 新增 `_drain_request_body()`：按 64KB 分块读干净 `Content-Length`，
  再处理 chunked（de-chunk 到结束块并吃掉其后的 CRLF），
  **返回 body 字节**（供后续复用，别读第二次）。
- `do_POST` **第一行**就 `raw = self._drain_request_body()`，
  然后 404 / 401 / bad json 等所有早退分支都在 body 已读走之后才返回。
- 实现 `/v1/messages/count_tokens`：本地估算即可（复用 `estimate_tokens`
  的 `字符数/3.5`），返回 `{"input_tokens": N}`。它本来就只是给 auto-compact
  做阈值比较，不需要真 tokenizer。**别再 404** —— 404 本身就是 bug 的来源。
- 401 分支也要排空：未授权请求同样带 body。

**三个连带坑**：

1. `_drain_request_body` **必须返回 body**。若它丢弃，调用方还得再读一次
   `self.rfile.read()` → 拿到空 → `_count_tokens` 恒返回 0。
2. 分块读取要用 `min(remaining, 65536)` 循环，别一次 `read(n)`；
   大 body（实测 300KB）容易短读。
3. chunked 传输要**读到 size=0 的结束块**并吃掉其后的 CRLF，否则边界仍不对齐。

**验证方法（必须测 keep-alive，不能只测单请求）**：

用一个 `http.client.HTTPConnection` 复用同一连接，先打 `count_tokens`，
再在同一连接上打 `/v1/messages`，第二次必须是 200。

实测覆盖：count_tokens→messages 同连接 200；未知路径 404→messages 同连接 200；
同一连接交替 10 次 10/10 全 200；401 路径后同连接 200；300KB body 200 且
`message_stop` 恰好 1 次；真实 `claude.exe` 多轮全 200。

> 顺带说明：日志里 `401` 出现在 count_tokens 上是**正常**的 —— 那是本节测试
> 故意不带 token 打的，目的是确认 401 路径也不会污染连接。

## 间歇性 upstream 400 `invalid request`：tool_result 前插了 user 消息（2026-10-06 实测根治）

**症状**：用 ccproxy + Space Bunny 时，会话中途**间歇性** 400，日志只有一句
`upstream 400 {"error":{"type":"invalid_request_error","message":"... [invalid_request_error] invalid request"}}`，
**完全不说哪条消息有问题**。有的请求 200、下一条就 400，CC 会自动重试所以有时能过去，
表现为"卡一下"。看起来像限流、像内容太长、像模型名错，**都不是**。

**根因**：Claude Code 会在 assistant 的 `tool_use` 和它的 `tool_result` **之间**
插入 user 消息（`AskUserQuestion` 的回答、hook 输出、中断式输入）。转成 OpenAI 格式后
就变成：

```
assistant(tool_calls) -> user -> tool      ← tool 脱离了它的 assistant
```

严格的 OpenAI 兼容网关拒绝这个形状。实测确认：
- `M[:38]`（结尾是 user）→ **200**
- `M[:39]`（结尾是 tool）→ **400**
- 把那条 tool 的 `content` 换成完全合法的 user 消息 → **200**
- 连 `tool_call_id` 是假值的孤儿 tool 消息 → **400**
- `max_tokens` 从 32000 降到 2048 → 仍 **400**（排除 token 预算）

→ **判据：tool 消息前面紧邻的必须是声明它的那个 assistant（含 tool_calls），
中间不能夹 user/system。**

**修法**（`ccproxy.py` 的 `_repair_message_sequence`，已内置）：把夹在
assistant 与其 tool 结果之间的 user/system 消息**移到 tool 结果之后**，
并把它们的文本**前置合并进第一个 tool 结果的 content** —— 不丢任何信息。
函数返回新列表，单趟扫描，幂等，不修改入参。

### 排查这类"上游说 valid 但没说是哪个"的 400 的通用手法

1. **先抓真实请求体**：网关在 upstream != 200 时把 `oa_req` 落到
   `~/.claude-code-proxy-failures.jsonl`（含 summary + 完整 body，>256KB 自动截断）。
   设为 `CCPROXY_DUMP_FAILED=0` 可关闭。**没有这步就只能猜。**
2. **前缀扫描找临界点**：`for k in range(30,41): post(M[:k])` —— 精确定位
   「加哪一条开始 400」。本例 `first 38 -> 200 / first 39 -> 400`，一步锁定。
3. **对照实验排除干扰**：同一条消息换 role / 换 content / 改 max_tokens / 删一半，
   看 400 是否消失。别只试一个变量。
4. **别被"1 个字符也 400"误导**：单独发一条 `{"role":"system","content":"x"}` 也 400，
   看起来像"system 消息不被支持"，其实是**该消息后面没有 user**。
   → 任何"最小用例也失败"都要怀疑**结构约束**，不要怀疑内容。

### 修完必须做的回归

- 离线单测 13 个用例覆盖：正常配对、单/多 user 插入、user+system 插入、
  多 tool 中途插入、连续 3 次插入、空 tool content、幂等性、入参不被修改。
  **断言三件事**：无 `user/system -> tool` 相邻、无内容丢失、无孤儿 `tool_call_id`。
- 用**抓到的真实失败 body** 回放 → 必须 200。
- 真实 `claude.exe -p` 多轮带工具 → 失败日志必须为空。

## Windows `.cmd` 启动器：编码与换行是头号坑（2026-10-05 实测）

给用户写 Windows 批处理启动器，**必须 GBK 编码 + CRLF 换行**，否则整段脚本会被
cmd.exe 拆成碎片：

| 症状 | 根因 |
|---|---|
| `'nny' is not recognized...` | 文件是 UTF-8 + **LF**，cmd.exe 把 `Bunny` 之类行截断（LF 不算行尾） |
| `'--verbose' is not recognized...` | 同上，某行被拆成独立命令行 |
| `'任意键关闭窗口。' is not...` | 同上 + GBK 解码 UTF-8 产生乱码 |
| `The system cannot find the path specified.` | 上一行的乱码把路径写坏了 |

**正确写法**：用 Python 显式控制编码，别用 Write 工具直接写（默认 UTF-8 + LF）：

```python
open(path, "wb").write(("\r\n".join(lines) + "\r\n").encode("gbk"))
```

中文提示语配合 `chcp 936`；若必须 UTF-8 中文，则 `chcp 65001` **且**文件存 UTF-8 + CRLF。
中文文件名本身没问题，坏的是**内容编码**。

### 批处理里三个必须避开的坑

1. **`timeout` 会被 Git Bash / MSYS 的 coreutils 抢占** → 报
   `timeout: invalid time interval '/t'`。延时改用 `ping -n 2 127.0.0.1 >nul`。
2. **用了 `!VAR!` 就必须 `setlocal EnableDelayedExpansion`**，否则取到空值，
   清理/条件分支静默失效（`if defined OLD` 那套同理）。
3. **`for /f` 取 netstat 的 PID**：`netstat -ano | findstr LISTENING | findstr ":PORT "`
   取第 5 个 token；注意排除 `TIME_WAIT`（它不是 LISTENING）。

### 端口占用的静默卡死

端口已被另一个网关实例占用时，`ccproxy.py` **不会报错退出，而是继续挂着**，
表现为「双击启动器 → 窗口有输出 → 但 claude 连不上」。启动器必须先清理：

```
for /f "tokens=5" %%P in ('netstat -ano ^| findstr LISTENING ^| findstr ":3457 "') do set "OLD=%%P"
if defined OLD taskkill /F /PID !OLD!
# kill 后必须复检一次，仍占用则报错退出，别让用户干等
```

`ccswitch.py` 自带的网关拉起有同样问题（见上「本机坑」表）。
**验证启动器时务必先手动清空端口**，否则测的是「旧实例还活着」，
会误判成新启动器正常。

## 其它本机坑

| 现象 | 说明 |
|---|---|
| `subprocess.run(["claude", ...])` → `FileNotFoundError` | Windows 上必须给 **`claude.cmd`** 的完整路径 |
| ripgrep/Grep 工具全目录搜索失败 | 工作区里若有名为 `nul` 的文件会 `os error 1`（退出码 2）；大目录 30s 超时。改用 Python `os.walk` 过滤后缀 |
| 需要跑管理员权限的命令 | 用标准的 UAC 提权方式（`Start-Process -Verb RunAs` 或 ShellExecuteEx+`runas`），**执行前先向用户说明并征得同意** |

---

# 附录 A · 智谱 GLM 已知可用配置（2026-09 实测）

智谱官方**原生支持 Anthropic 协议**，文档里直接给了 Claude Code 配置，接入最省心。

## 端点与模型名（权威，无需猜）

- Anthropic 协议 Base URL（Claude Code 用这个）：`https://open.bigmodel.cn/api/anthropic`
  - ⚠️ 末尾**不要加 `/v1`**——Claude Code 会自动拼 `/v1/messages`，拼成
    `https://open.bigmodel.cn/api/anthropic/v1/messages`（这正是智谱的正确路径）。
  - 国际站 z.ai 同协议：`https://api.z.ai/api/anthropic`（Key 用 z.ai 平台发的）。
- API Key：`https://open.bigmodel.cn/usercenter/apikeys` 创建。
  填进 `ANTHROPIC_AUTH_TOKEN`（即 Key 本身，CC 会带 `x-api-key` 头，别加 `Bearer `）。
- 模型 ID（小写，OpenAI/Anthropic 端点通用）：
  - 免费视觉：`glm-4.6v-flash`（128K，9B 轻量，**免费档仅 1 并发**）
  - 免费文本：`glm-4.7-flash` / `glm-4.5-flash`
  - 便宜强档：`glm-5.3-flash`（1M 上下文，约 ¥1.07/¥3.55）、`glm-5.2`
  - 旗舰：`glm-5`

## 配置模板（settings.json 的 env 块）

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://open.bigmodel.cn/api/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "你的智谱API Key",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "glm-4.7-flash",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "glm-5.3-flash[1m]",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "glm-5.3-flash[1m]",
    "CLAUDE_CODE_AUTO_COMPACT_WINDOW": "1000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
    "API_TIMEOUT_MS": "600000"
  }
}
```

## GLM 接 CC 的三个坑

1. **`glm-4.6v-flash` 免费档只有 1 并发请求**（ayautomate 实测）。Claude Code 会并行发
   子代理/工具调用请求，极易触发限流排队 → 实际体验卡顿。**当主模型不推荐**，更适合走
   「视觉理解 MCP Server」(`glm-4.6v`) 或 lobehub 的 `glm-4.6v-flash-mcp` 只处理图片/视频任务。
2. **上下文 128K 的模型别加 `[1m]` 后缀**（如 `glm-4.6v-flash` 就别加）。`[1m]` 只给真有
   1M 窗口的模型用（如 `glm-5.3-flash[1m]`），否则 `contextWindow` 会虚标导致 auto-compact 错乱。
3. **免费模型商用条款未明确**（ayautomate 标注 "Commercial use: Unclear"）。个人使用无妨；
   要进生产先查智谱当前条款。复杂编码优先用 `glm-5.3-flash` 或 `glm-4.7-flash`（免费文本），
   比视觉 Flash 更能扛多步任务。

---

# 第五部分：只有 OpenAI 兼容端点的模型 → 必须加本地网关

**适用**：模型只在 OpenAI 兼容网关上提供，没有 Anthropic 原生端点。
典型是 Space Bunny（2026-09 匿名免费预览，1M 上下文，强制推理、五档 reasoning effort，$0）。

> ⚠️ **2026-09-29 重大更正：`claude-code-router` 的流式转换是坏的，不要再拿它做方案。**
> 实测 v2.1.1（npm 上只有 2.1.0/2.1.1，**没有修复版**）输出的 Anthropic SSE：
> **每个事件都写两遍**（两个不同的 `message_start`）、**从不发 `message_stop`**、
> `message_delta.delta` 是空 `{}`。Claude Code 因此报
> **`API Error: The response stream was malformed. The response above may be incomplete.`**
>
> 定位手法（可复用）：把它指向一个**标准得不能再标准**的假上游——自己起个 Python HTTP 服务
> 返回教科书式 OpenAI SSE（`data: {...}\n\n` + `finish_reason` + `data: [DONE]`）——
> **照样畸形**，说明是路由器自身 bug，与上游无关；再查假上游的请求日志确认**上游只被请求 1 次**，
> 即重复输出是它自己写了两遍。
>
> **替代方案：自建 `ccproxy.py`（见第七部分）**，零依赖、事件序列严格合规。
> 下面的路由器配置留作历史参考，新搭建请直接走第七部分。

**同一个 stealth 模型往往有多个上游，优先选免 key 的那个**：

| 上游 | 端点 | 模型名 | 认证 |
|---|---|---|---|
| **OpenCode Zen** | `https://opencode.ai/zen/v1/chat/completions` | `space-bunny-free` | **免 key（匿名）可用** |
| OpenRouter | `https://openrouter.ai/api/v1/chat/completions` | `stealth/space-bunny-alpha` | 需 key（注意：整段 `:free` 后缀会 404） |
| AI/ML API | `https://api.aimlapi.com/v1/chat/completions` | `stealth/space-bunny-alpha` | 需 key |

- **OpenCode Zen 免 key 实测（2026-09-29）**：不带任何 `Authorization` 头直接 POST
  `space-bunny-free` 即返回真实结果、`cost:"0"`。**账号被封也不用怕，直接换 Zen。**
  （限时免费，约 ~2026-09-30 到期；`@namzu/zen` 也称 keyless 走 `space-bunny-free`，
  但「网关准入随时可能变」。）
- 两条通道 **模型 ID 不同**：Zen 带 `-free` 后缀，OpenRouter 不带 `:free` 后缀。

## 为什么必须过网关

Claude Code 只发 **Anthropic Messages** 协议，这类模型只吃 **OpenAI Chat Completions**。
协议不同，`ANTHROPIC_BASE_URL` 直接指过去必炸。用 **`claude-code-router`** 在本地
做协议转换（含流式 + 工具调用 + 推理参数翻译）。

架构：`Claude Code → http://127.0.0.1:3456 → claude-code-router → OpenRouter`

## ⚠️ 最大坑：配置文件名是 `config-router.json`，**不是** `config.json`

这是「配置明明写了却不生效」的头号原因，静默失败，极难查：

```
DEFAULT_CONFIG_PATH = path.join(homedir(), ".claude-code-router", "config-router.json")
```

- README / 网上教程普遍写 `config.json` —— **错的**。
- 写错文件名后路由器**不会报错**，而是加载内置 `DEFAULT_CONFIG`，
  里面塞着 `codewhisperer-primary`（AWS）和 `shuaihong-openai` 两个陌生 provider。
- **识别方法**：跑 `ccr health`，若出现你不认识的 provider 名，就是没读到你的配置。

## ⚠️⚠️ 同等大坑：系统代理环境变量接管网关请求

网关内部用 **axios**，而 axios **会读取 `http_proxy`/`https_proxy`/`HTTP_PROXY`/`HTTPS_PROXY`
环境变量**。本机（或任何开了代理的机器）若设了这些变量，网关会**把所有上游请求都交给代理转发**，
症状极具迷惑性：

| 现象 | 说明 |
|---|---|
| 打上游得 **400**，但用 `curl` 直连同一上游是 200/401 | 代理层引入的假错误 |
| 打本地 `http://127.0.0.1:xxxx` 得 **502** | 代理无法回环（连 localhost 也被转发） |
| 不同上游表现不一致、模型名明明正确却失败 | 别怀疑模型名，先查代理 |

**定位法（决定性）**：架一个**本地回显 HTTP 服务器**（Python stdlib），把网关 endpoint 临时
指到 `http://127.0.0.1:3999/v1/chat/completions`，再经网关发一次请求：
- 回显服务器**收到**请求 → 网关没有经代理转发（可继续查别的）。
- 回显服务器**收不到**、网关报 502 → **请求被代理接管了**（本地地址也被代理吞掉）。

**修复**：按 HTTP 客户端通用的 `no_proxy` 约定，**把本地回环地址与直连可达的上游域名列入
`no_proxy`，即声明这些目标不走代理**（其余流量仍按系统代理设置走）：

```bash
# bash：只为回环地址声明直连，其余保持系统代理设置
NO_PROXY='127.0.0.1,localhost' no_proxy='127.0.0.1,localhost' <node.exe> <cli.js> start
```
```cmd
REM Windows 启动器里
set NO_PROXY=127.0.0.1,localhost
set no_proxy=127.0.0.1,localhost
<node.exe> <cli.js> start
```

> 若确实需要「这个进程完全不使用任何代理」（例如上游必须直连、而系统代理不通），
> 再显式覆盖这几个变量——**先确认该上游直连可达**（不带代理参数 `curl` 能返回 200），
> 且只对单个进程生效，不要写成全局永久环境变量。

注意：**这一条对所有「本地网关转上游」的场景都适用**（不只 claude-code-router）。
Claude Code 自己连 `127.0.0.1:3456` 时同样可能被代理接管 → 在 `no_proxy` 里加上 `127.0.0.1`。

## 安装（装进 managed node workspace，别 `npm install -g`）

```bash
mkdir -p "C:/Users/<u>/.workbuddy/binaries/node/workspace"
cd "C:/Users/<u>/.workbuddy/binaries/node/workspace"
"<node.exe>" "<版本根目录>/node_modules/npm/bin/npm-cli.js" install claude-code-router
```

> npm-cli.js 在**版本根目录** `.../node/versions/22.22.2-3/node_modules/npm/bin/npm-cli.js`，
> **不在** workspace 里（踩过）。

## 配置模板：`~/.claude-code-router/config-router.json`

```json
{
  "server": { "port": 3456, "host": "127.0.0.1" },
  "routing": {
    "rules": {
      "default":     { "provider": "opencode-zen", "model": "space-bunny-free" },
      "background":  { "provider": "opencode-zen", "model": "space-bunny-free" },
      "thinking":    { "provider": "opencode-zen", "model": "space-bunny-free" },
      "longcontext": { "provider": "opencode-zen", "model": "space-bunny-free" },
      "search":      { "provider": "opencode-zen", "model": "space-bunny-free" }
    },
    "defaultProvider": "opencode-zen",
    "providers": {
      "opencode-zen": {
        "type": "openai",
        "endpoint": "https://opencode.ai/zen/v1/chat/completions",
        "authentication": { "type": "bearer", "credentials": { "apiKey": "" } },
        "settings": {
          "categoryMappings": { "default": true, "background": true, "thinking": true,
                                "longcontext": true, "search": true },
          "models": ["space-bunny-free"],
          "defaultModel": "space-bunny-free"
        }
      }
    }
  },
  "debug": { "enabled": true, "logLevel": "info", "traceRequests": false,
             "saveRequests": false, "logDir": "C:/Users/<u>/.claude-code-router/logs" }
}
```

要点：
- `endpoint` 要写**完整** `/v1/chat/completions` 路径（不是 base URL）。
- 路由器**按 category 路由**，**忽略** Claude Code 请求里带的 model 名，
  真正生效的是 rule 里的 `model`。所以 settings.json 里写 `space-bunny` 也无所谓。
- 五个 category 全部指向同一 provider，否则子代理 / 长上下文请求会漏到别处。
- 路由器会**合并**内置默认 provider，`ccr health` 长期显示
  `System degraded` + `codewhisperer-primary ❌` —— **无害**，别去修。
  （`opencode-zen ❌` 也可能出现，因为 health 探活方式与实际 messages 调用不同；
  只要经 `/v1/messages` 能拿到真实回包，就是通的，别被 health 误导。）
- **免 key 上游**：`"apiKey": ""` 即可，路由器会**省略** Authorization 头 → Zen 视为匿名。
  填**任何非空假 key** 反而会被 Zen 拒（`AuthError: Invalid API key.`）。
- 强制推理模型（Space Bunny）**`max_tokens` 要给足**，否则推理 token 吃光预算、
  返回 `content: []`（表现为"空回复"，不是坏了）。

## Claude Code 侧 settings.json

```json
"env": {
  "ANTHROPIC_AUTH_TOKEN": "<本地网关令牌>",
  "ANTHROPIC_BASE_URL": "http://127.0.0.1:3456",
  "ANTHROPIC_MODEL": "space-bunny[1m]",
  "ANTHROPIC_DEFAULT_OPUS_MODEL": "space-bunny[1m]",
  "ANTHROPIC_DEFAULT_SONNET_MODEL": "space-bunny[1m]",
  "ANTHROPIC_DEFAULT_HAIKU_MODEL": "space-bunny[1m]",
  "ANTHROPIC_DEFAULT_FABLE_MODEL": "space-bunny[1m]",
  "CLAUDE_CODE_SUBAGENT_MODEL": "space-bunny[1m]",
  "CLAUDE_CODE_AUTO_COMPACT_WINDOW": "1000000",
  "API_TIMEOUT_MS": "600000"
}
```

- `ANTHROPIC_AUTH_TOKEN` 这里是**本地网关的令牌**，不是上游真 key —— 真 key 只存在网关 config
  一处，不随 `settings.json` 扩散。网关会校验这个令牌：不带或带错直接 401，其它本地进程
  无法白用你的上游额度。
- 令牌在网关**首次启动时自动生成**并写进 `~/.claude-code-proxy.json`；`ccswitch.py` 会把它
  同步到 `settings.json` 与各网关 profile，两端始终一致（手工写 `router-local` 之类的占位值
  也能跑，会被自动替换为真令牌）。
- 1M 上下文的模型用 `[1m]` 后缀 + `AUTO_COMPACT_WINDOW=1000000`。

## 配进 WorkBuddy 客户端（`~/.workbuddy/models.json`）

GUI 里「配置自定义模型」写的就是这个文件（顶层数组或 `{ "models": [ ... ] }` 都合法）。
除了 Claude Code，也可以让 WorkBuddy 本体直接选第三方模型：

```json
{
  "id": "space-bunny-free",
  "name": "Space Bunny",
  "vendor": "OpenCode Zen",
  "url": "https://opencode.ai/zen/v1/chat/completions",
  "apiKey": " ",
  "supportsToolCall": true,
  "supportsReasoning": true
}
```

> ⚠️ **`apiKey` 不能留空字符串**（这是最容易踩的坑）。运行时（`codebuddy-headless.js`）
> 取 key 的逻辑是：
> ```js
> ei = settings.env.CODEBUDDY_API_KEY || process.env.CODEBUDDY_API_KEY;  // 默认 = 平台 token
> if (model.apiKey) ei = model.apiKey;                                   // 有值才覆盖
> if (ei) headers['x-api-key'] = ei, headers['Authorization'] = `Bearer ${ei}`;
> ```
> 空串是**假值** → 不覆盖 → 客户端把自己的 **WorkBuddy 平台 token** 当 Bearer 发给上游，
> 症状是上游回 `401 AuthError: Invalid API key.`（错误码 3001、`category: custom_model_auth`），
> 报错信息会指向「请检查模型配置（API Key、模型 ID、接口地址）」——**全是误导**，
> 配置一个字都没错。Claude Code 侧没有这个问题（网关自己管上游鉴权）。
>
> **修法：把 `apiKey` 填成单个空格 `" "`**。上游只会看到 `Authorization: Bearer  `，
> 而**匿名型端点会先 trim 再判空**，所以照常放行。
> 实测（`http.client` 直发，不经 curl，避免尾随空格被裁掉）：
> `Bearer  `（token=1 空格）→ **200**；`Bearer   `→ 200；`Bearer \t` → 200；
> **`Bearer \xa0`（非断行空格）→ 401** —— 所以必须是 ASCII 空格/Tab，别用全角或不换行空格。
> 反例：任何**非空可见值**（含 `undefined`/`null`/`EMPTY`/`sk-`）一律 401。
>
> 相关环境变量（排查用）：`CODEBUDDY_API_KEY`（key 本体）、
> `CODEBUDDY_API_KEY_DISABLED=1`（**设了则整套 key 逻辑短路、完全不发 Authorization 头** ——
> 这是最"干净"的关掉方式，但它会同时影响 WorkBuddy 自己的内置模型，慎用）；
> `CODEBUDDY_CUSTOM_HEADERS`（附加自定义头）、`CODEBUDDY_DISABLE_CUSTOM_MODELS_FILE=1`（不读 models.json）。
>
> `models.json` 的用户级文件**有 watcher（1s 去抖）+ 每次请求重新读 config**，
> 改完通常**不必重启客户端**，直接重发即可；不行再重启。用户级 `apiKey` 还可能在
> 保存时被凭据编解码加密（`WBEF1` 前缀），读到明文不受影响。

## 诊断：怎么拿完整出站请求体（关键）

网关会把上游错误**包装**掉，只留一句 `openrouter request failed: Request failed with
status code 400`，看不出是 auth 还是 body 格式问题。拿真实 body 的方法：

1. config 里开 `"traceRequests": true`（配合 `saveRequests`），重启网关；
2. 发一次测试请求；
3. 从日志里**用 node 解析** axios 的 `config.data`（日志里该字段会被截断，别直接肉眼看）：

```bash
node -e "
const fs=require('fs');
fs.readFileSync('<logDir>/ccr-2026-09-29.log','utf8').split('\n').filter(Boolean).forEach(l=>{
  const o=JSON.parse(l);
  if(o.level==='error'&&o.data?.config) console.log(o.data.config.data, JSON.stringify(o.data.config.headers));
});"
```

**A/B 判据**：同一个无效 key，直连 OpenRouter 返回 **401** `Missing Authentication header`，
而经网关返回 **400** —— 两者都是 auth 被拒，只是 OpenRouter 对网关来源的错误码不同。
**拿到合法 OpenAI 格式 body 且模型名正确 = 链路已通**，剩下只是换真 key。
（判断 body 是否合法：形状应是
`{"model":"stealth/space-bunny-alpha","messages":[...],"max_tokens":N,"stream":false}`）

## 启动

网关必须常驻，且**不能用 `nohup ... &`**（会随命令进程组被杀，见 Step 8）。
用工具自带的后台运行能力起，或给用户建启动器（本机已固化，见第六 / 七部分）：

```bash
# 前台起网关（窗口可见，保持开着）
python scripts/ccproxy.py --port 3457 --verbose
# 或让切换器代劳（推荐）：它判定是否真需要网关、避免重复启动
python scripts/ccswitch.py gateway
```

> **脚本随本技能提供，位于 `scripts/` 目录下** —— `ccproxy.py`（网关）+ `ccswitch.py`（切换器）。
> 纯 Python 标准库、零第三方依赖，拷到任意位置都能跑。
> Windows 用户想双击即用，可自建 `.cmd` 启动器（内部先 `chcp 65001` 防中文乱码），
> 内容就是上面那两行命令。
> 注意 CC 2.1.278 起 `bin` 指向原生 `claude.exe`（不再有 `cli.js`）；`claude.cmd` 只是批处理包装。

## 已知限制

- Space Bunny 是**强制推理**模型，默认 effort 较高（偏慢）。想提速要调 reasoning effort，
  但 Claude Code 的 `CLAUDE_CODE_EFFORT_LEVEL` 经网关**未必能传下去**（同 Step 9，
  很可能是空操作），需要实测确认。
- 匿名 stealth 模型规格/数据政策未公开（提供方可能保留 prompt，不用于训练），
  别用于高敏感或强合规场景。

---

# 第六部分：多 profile 一键切换（ccswitch）

**目标**：用户说一句「切 deepseek」/「切 space bunny」就完成切换，不再手工改配置。

## 用法

```bash
python scripts/ccswitch.py deepseek          # 切到 DeepSeek 原生端点
python scripts/ccswitch.py spacebunny        # 切到 Space Bunny（自动拉起网关）
python scripts/ccswitch.py status            # 当前 profile + 网关状态
python scripts/ccswitch.py list              # 列出所有 profile
python scripts/ccswitch.py gateway           # 只确保网关在跑
python scripts/ccswitch.py <p> --no-gateway  # 只改 settings，不动网关
```

别名：`ds`→deepseek，`bunny`/`sb`/`zen`→spacebunny。

## 设计（可直接照搬到别的工具）

1. **profile 即模板**：`~/.claude/profiles/<name>.json` 存一份完整的 Claude Code
   `settings.json`；切换 = 复制覆盖 `~/.claude/settings.json`。
2. **切前必备份**：旧文件存 `~/.claude/backups/settings.json.bak-<时间戳>`；
   与目标内容相同则跳过（不刷屏）。
3. **是否需要网关由配置自身推出**，不靠额外元数据：
   `ANTHROPIC_BASE_URL` 含 `127.0.0.1:3457` → 需网关（切过去自动拉起、切走自动停）；
   其它（如 `api.deepseek.com/anthropic`）→ 原生端点，不需要网关。
4. **网关本体是 `ccproxy.py`（第七部分），不是 claude-code-router**；
   **停网关**：`netstat -ano` 找 `:3457 LISTENING` → `taskkill /F /PID`。
5. 新增模型 = 丢一个 profile json 进去，脚本自动出现在 `list` 里。
6. **令牌自动对齐**：网关的 `client_token` 与 `settings.json` 的 `ANTHROPIC_AUTH_TOKEN`
   由切换器统一同步（仅在空值/占位值时生成新令牌），用户不用手抄令牌，两边也不会漂移。

## 关键提醒

- **切换后必须重启 Claude Code**（已开会话仍持旧 settings）—— 脚本会打印这句。
- 脚本在 `scripts/` 下，**跨平台**：Windows 走 `netstat` + `taskkill`，
  macOS / Linux 走 pidfile + `SIGTERM`。
- 想让 Windows 用户双击即用，自建 `.cmd` 启动器即可（内部 `chcp 65001` 防中文乱码），
  内容就是 `python <技能目录>\scripts\ccswitch.py <profile>`。

## 本机坑（2026-09-29）

| 现象 | 真相 |
|---|---|
| `Popen` 起的网关**活不过本次调用** | 以后台方式启动（Bash 的 `run_in_background`），或让用户用 `.cmd` 启动器双击运行 |
| `/tmp/sb.json` 写得出、Python 打不开 | Git Bash 的 `/tmp` 是虚拟路径，原生 Python 看不见。落盘要写 Windows 真实路径，或直接走管道 |

→ 结论：**验证链路优先「直连端点」**，别依赖拉起完整 CC；网关的常驻方式见第七部分。

---

# 第七部分：ccproxy —— 自建零依赖 Anthropic↔OpenAI 网关（2026-09-29）

**为什么自建**：见第五部分的更正。`claude-code-router` 的 SSE 转换是坏的，
且它只有 2 个版本、无新版可升，2MB 压缩产物 + 超长行无法可靠打补丁 —— 与其修，不如替换。

## 文件清单

| 路径 | 作用 |
|---|---|
| `scripts/ccproxy.py` | 网关本体（Python 3 **stdlib**，零第三方依赖，约 740 行） |
| `scripts/ccswitch.py` | profile 切换器 + 网关启停协调（跨平台，约 515 行） |
| `~/.claude-code-proxy.json` | 配置：`host` / `port` / `upstream{url,model,api_key}` / `timeout` / `verbose` / `client_token` |
| `examples/profiles/*.json` | 开箱可用的 `settings.json` 模板，拷到 `~/.claude/profiles/` |

```bash
python ccproxy.py --port 3457 --verbose                      # 前台带日志
python ccproxy.py --upstream <url> --model <name> --key <k>  # 临时换上游
curl -s -H "x-api-key: $TOKEN" http://127.0.0.1:3457/health  # {"ok":true,"service":"ccproxy",...}
```

CLI 参数优先于配置文件（且**不会**被写回配置文件）。当前上游：
`https://opencode.ai/zen/v1/chat/completions` + `space-bunny-free` + **空 api_key**
（Zen 免 key；填任何占位值都会被 `AuthError: Invalid API key` 拒）。

## 安全设计（默认即如此，不用额外配置）

网关是本机进程与「你的上游额度」之间唯一的关口，所以默认做了这几件事：

| 机制 | 做法 | 作用 |
|---|---|---|
| **客户端令牌鉴权** | `client_token` 首次启动自动生成（`secrets.token_urlsafe(24)`）；`/v1/messages` 与 `/health` 都校验，不符返回 401 | 其它本地进程无法把它当免费中转、白用你的上游凭证 |
| **只监听回环地址** | 默认 `host=127.0.0.1`；若被改成非回环地址，启动时打印显式警告 | 不把网关暴露到局域网 |
| **对端身份校验** | `ccswitch` 的健康检查要求响应里 `service == "ccproxy"`，否则判定「端口被其它进程占用」并报错，不再盲信端口 | 防止端口被别的程序占住后冒充网关、截走 prompt |
| **不读代理环境变量** | 上游走 `http.client` | 不受系统代理影响（见第五部分） |
| **改动有痕迹** | 令牌只写回配置文件的单个键（CLI 参数不落盘）；切档前自动备份 `settings.json` 到 `~/.claude/backups/` | 可回溯，不静默改你的环境 |

边界说明：令牌存放在本机配置文件里，**同一用户下的其它进程本就能读到该文件**。它挡的是
「本机程序顺手把网关当免费通道」，不是同用户内的强隔离；需要强隔离就用独立系统账号跑网关。

## 实现要点（照着抄，别重蹈覆辙）

1. **上游用 `http.client` 直连，不用 requests/axios** → 不读取 `HTTP_PROXY`/`HTTPS_PROXY`
   这类代理环境变量，从根上避免第五部分那类「请求被系统代理接管」的问题。
2. **事件序列严格合规**（这正是路由器翻车处）：
   `message_start`(恰 1 次) → `content_block_start` → `content_block_delta`* → `content_block_stop`
   → （下个块同理）→ `message_delta`（**带真实 `stop_reason`**）→ `message_stop`(恰 1 次)。
3. **异常也必须收尾**：上游中途断开 / 报错 / 返回空内容时，仍要补发
   `message_delta` + `message_stop`（必要时补一个空 text block），**绝不裸断** ——
   这是 `stream was malformed` 的根治手段。
4. **工具调用**：多个 tool_call 的 `arguments` 增量会**交错**到达，因此
   **不要在某个 tool 块出现时就关闭前一个块**；让所有块保持 open，**结束前按 index 顺序统一 close**。
   `arguments` 片段直接映射为 `input_json_delta.partial_json`（CC 自己拼接）。
5. `finish_reason` → `stop_reason`：`stop`→`end_turn`、`length`→`max_tokens`、
   `tool_calls`/`function_call`→`tool_use`。
6. **`reasoning_content` 直接丢弃**：Anthropic 的 thinking block 需要 `signature`，伪造易炸。
   （想要思考过程再加开关。）
7. 上游常不给 token 数 → 用 `字符数 / 3.5` 估算 `input_tokens`/`output_tokens`，
   够 CC 显示成本与 auto-compact 用。
8. 请求侧映射：`system`→role=system；user 里的 `tool_result` 块要**拆成独立的
   `{"role":"tool","tool_call_id":...}`**；assistant 的 `tool_use` → OpenAI `tool_calls`；
   `tools[].input_schema` → `function.parameters`；`tool_choice`：`any`→`required`、
   `tool`→`{type:function,function:{name}}`；`thinking.budget_tokens` → `reasoning_effort`。
9. **入站先鉴权**：`do_POST` / `do_GET` 开头部用 `hmac.compare_digest` 比对 `x-api-key`
   （或 `Authorization: Bearer`）与 `client_token`，不符返回 401 的 Anthropic 错误体。
   少了这一步，本机任何进程都能把你的上游额度当免费 API 用。
10. **健康检查要能证明身份**：`/health` 返回 `{"service":"ccproxy","pid":...}` 且要求令牌；
    调用方校验 `service` 字段，端口被别人占住时报错，而不是当成「网关已就绪」。
11. **只把令牌写回配置文件的那一个键**：CLI 覆盖项（`--port` / `--verbose` / …）不能落盘，
    否则调试用的临时参数会污染用户配置。

## 验证方法（必做，别凭感觉）

```bash
TOKEN=$(python -c "import json;print(json.load(open(r'C:/Users/<u>/.claude-code-proxy.json'))['client_token'])")
curl -sN http://127.0.0.1:3457/v1/messages \
  -H "x-api-key: $TOKEN" \
  -H 'content-type: application/json' -H 'anthropic-version: 2023-06-01' \
  -d '{"model":"x","max_tokens":300,"stream":true,"messages":[{"role":"user","content":"回答两个字:你好"}]}' > out.txt
```

逐块解析 `event:`/`data:` 后检查（实测通过的样子）：

| 检查项 | 期望 |
|---|---|
| 不带令牌打 `/health` 或 `/v1/messages` | **401**（鉴权生效，实测如此） |
| `/health` 带令牌 | `{"ok":true,"service":"ccproxy","pid":...}` |
| `message_start` / `message_delta` / `message_stop` 计数 | **各 1** |
| `content_block_stop` 计数 | = `content_block_start` 计数 |
| 首 / 末事件 | `message_start` / `message_stop` |
| text 拼接 | 等于完整回答（实测 `'你好'`） |
| 带 tools 时 | 出现 `content_block_start(type=tool_use)` + `input_json_delta`，args 能 `json.loads` 成功（实测 `{"city": "北京"}`），`stop_reason=tool_use` |
| 真实 CC | `claude.exe -p "7*8=?" --output-format json` → `result:"56"`、`stop_reason:"end_turn"`、`is_error:false` |

## 本机坑（与网关相关）

- **验证 CC 时优先用原生二进制入口**（比 `claude.cmd` 这层批处理包装更稳）：
  `~/AppData/Roaming/npm/node_modules/@anthropic-ai/claude-code/bin/claude.exe`
  （CC 2.1.278：`package.json` 的 `bin` = `bin/claude.exe`，**不再有 `cli.js`**，别再按老路径找）。
- 该 exe 体积约 237MB，首次 `ls` 会略慢，正常。


## 大 payload 才是真凶（2026-10-07 实测，v1.3.0）

前面两节修的是「持续性故障」。这一节是**残余的间歇故障**，机制完全不同。

### 决定性数据

同一网关、同一时刻、同一 payload，只改变一个变量：

| 场景 | 结果 | 耗时 |
|---|---|---|
| 16B token 小请求（顺序·直连） | 10/10 | **4.0s** |
| **183KB 真实 payload**（顺序·非流式） | 3/3 | **34-47s** |
| 183KB（顺序·流式） | 2/2 | 24-36s |
| 183KB（**并发 4**·流式） | 4/4 | 35-37s |
| 183KB（**并发 4**·非流式） | 4/4 | **44-45s** |
| 183KB（并发 4·流式·**经代理**） | 4/4 | **15-33s** |

两个关键推论：

1. **并发不叠加**（4 并发仍 45s，不是 180s）→ 排除客户端压力/连接池问题。
2. **经代理反而快约 40%** → 直连走的不是最优路由。

### 10054 的真实机制

**不是断连，是超时。** 183KB 请求让免费端点的轻量模型算 40 秒左右，
Cloudflare 边缘节点在这个时长附近会**掐掉仍在处理中的连接**，
网关侧看到的就是 `ConnectionResetError`。

26 次重放里**一次 RST 都没复现**——所以别再指望抓到它。

### 哪些请求是「大 payload」

挖`failures.jsonl` 的 `openai_body` 就能认出来，特征很硬：

| 特征 | 分类器请求 | 正常对话 |
|---|---|---|
| body 体积 | **178-183 KB** | 小 |
| system prompt | **140 KB** | 小 |
| `max_tokens` | 2112 / 10240 / 32000 | 正常 |
| `stop_sequences` | `['</block>']` | 无 |
| 结尾 | `MUST begin with <block>` | 无 |

这是 **Claude Code 的 Bash 安全分类器**，不是用户对话。
所以报错是 `auto mode cannot determine the safety of Bash`，
表现为「Bash 工具卡住不动」。

### 修法B：自动重试（`retries` / `retry_backoff`）

```python
def open_upstream_with_retry(oa_req):
    # 只重试传输层故障，绝不重试上游给出的 4xx/5xx —— 那是答案不是意外
```

**流式中途失败只在「一个字节都没吐给客户端」时才重试**，
用 `emitted` 高水位追踪：已吐内容就重放会导致重复输出，
这时失败比重复更诚实。

新增配置（默认值已写进 `DEFAULT_CONFIG`）：

```json
{ "retries": 2, "retry_backoff": 1.5 }
```

退避是 `backoff * 2**i`（1.5s → 3s）。

### 修法 C：走代理（`resolve_upstream_proxy`）

优先级：`upstream.proxy` 显式配置 > `HTTPS_PROXY`/`HTTP_PROXY` 环境变量 > 直连。
**配置里不写 `proxy` 键**就是「自动跟随环境变量」，
VPN 换端口时无需改配置。

实现用 **CONNECT 隧道**（`conn.set_tunnel`），
不是绝对形式请求目标 —— 这样 TLS 端到端，request-target 保持 origin form，
流式才能正常工作。实测快 40%。

### 验收结果（v1.3.0）

- `/health` 200、非流式 200、流式 SSE 六事件齐全
- **178KB 真实分类器 payload → 200**
- 真实 `claude.exe` 多轮工具调用全200，含绝对 URI 形式
- **failures.jsonl 停在 29 条，新版本零新增**

### 诊断顺序（补充）

1. 先看 `failures.jsonl` 里 `openai_body` 的**体积和 `max_tokens`**，
   别一上来就查网络连通性 —— 小请求能通不代表大请求能通。
2. 用**捕获的真实 payload 重放**，小请求测不出这个问题。
3. 网关启动时打印 `upstream route:` 和 `upstream retries:`。
   没有这两行，代理是否生效完全不可见 —— 排查时先确认它们。
