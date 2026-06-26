---
name: benchclaw - openclaw-benchmark
description: >
  BenchClaw - OpenClaw Agent benchmark scoring tool. Benchmark 跑分 评测 打分.

  BenchClaw是专业级 OpenClaw Agent 性能评测框架。它专注于对 AI Agent 进行多维度、
  自动化的量化评估与能力基准测试，集成了任务分发、精准评分、可视化报表生成及热更新功能。
  当需要量化 Agent 的推理规划、响应速度、Token 成本及安全性时使用。

  **用户意图/指令**：跑分、跑个分、运行基准测试、评估 Agent 表现、生成评测报告、分析 Token 消耗。
  **技术关键词**：跑分、跑个分、Agent 评测、基准测试、自动化打分、量化评估、性能报告、Token 成本、
  TPS、OpenClaw。

  BenchClaw is the "AnTuTu" for OpenClaw Agents—a professional-grade automated benchmarking
  framework. It provides multi-dimensional evaluation (Capability, Config, Security, Hardware, Permission)
  through automated task execution, precision scoring, and detailed report generation.

  **User Intent**: run benchmark, get score, evaluate agent performance, generate scoring reports,
  analyze Token usage/TPS.
  **Key Triggers**: Benchmark, Scoring, Agent Evaluation, Automated Scoring, Performance Metrics,
  Cost Analysis, OpenClaw.

metadata:
  author: benchclaw
  version: "1.1.1"
  homepage: https://benchclaw.antutu.com
  repository: https://github.com/BenchClaw/benchclaw
  tags: [benchclaw, benchmark, openclaw-benchmark, 龙虾跑分, 龙虾评测]
  type: "executable"
  openclaw:
    requires:
      bins:
        - python3
        - openclaw
        - pip
      packages:
        - cryptography
        - psutil
        - requests

    permissions:
      network: "HTTPS: fetches the question set; when upload is on (default unless caller_info.txt sets upload_to_server=false), POSTs encrypted (AESGCM+RSA) submit payloads to the BenchClaw API. Upload scope is listed in SKILL section 「自动缓存与安全上报」 and UPLOAD_DISCLOSURE.md. Does not upload full OpenClaw session transcripts; only per-question aggregates and truncated stdout/stderr. stdout/stderr get best-effort regex replacement (non-exhaustive) in scripts/server.py::_sanitize_output and test_sanitize (~41–71 and ~494–538). Run: cd scripts && python server.py sanitize. upload_to_server=false skips submit and flush_pending_uploads; fetch still uses the network."
      file_write: "Writes evaluation results to data/ and temp/ directories within the skill folder. Writes bench_session_id to data/cache.json for correlating evaluation runs with the server."
      bench_session_id: "Generates a local bench session id stored in data/cache.json. Sent as header X-Bench-Session-Id. Used to correlate evaluation history across runs. No PII collected."
---

# BenchClaw Benchmark Skill

BenchClaw 是一套完整的 OpenClaw Agent 基准评测与热更新分发系统。它能够自动从服务端拉取考题，驱动 Agent 执行并收集输出，最后进行规则验证打分和报表生成。

---

## 前置条件 (Prerequisites)

- **Python 3.11+**（推荐 3.13）
- **本机已安装并可运行 `openclaw` CLI**
- **本机 OpenClaw Gateway 运行中**

Python 依赖会在首次运行时**自动安装**（无需 sudo），详见下方"快速开始"。

---

## ⚠️ 运行前必须确认

在执行评测前，**先获取 OpenClaw 默认模型配置**，然后展示以下信息等待用户确认：

> 📊 **BenchClaw 评测即将开始**
>
> - ⏱️ **预计耗时**：10-90 分钟（取决于模型速度和网络状况）
> - 💰 **Token 消耗**：约 2-3M tokens（会产生 API 费用，请确认预算充足）
> - 📋 **评测内容**：25 道题，涵盖能力、配置、安全、硬件、权限 5 大分类
> - ⚠️ **期间注意**：OpenClaw 仍可响应其他消息，但性能会有所下降
> - 🤖 **评测模型：`{agents.defaults.model.primary}`**
> - ⚠️ 评测使用的是 OpenClaw 配置的默认模型，与你当前 session 无关。
>
> **请三选一回复**（只选一种）：
> - **上报名字**：回复「**展示**」「**开始**」或「**确认**」→ 上传榜单，榜单显示「{Agent名字}」🚀
> - **匿名上传**：回复「**匿名**」→ 上传榜单，不显示名字 🚀
> - **仅本地**：回复「**仅本地**」→ `upload_to_server=false`，不提交、不补报缓存；**仍会 HTTPS 拉题**，本地出分与报表 🚀
>
> ⚠️ 「{Agent名字}」指你在 OpenClaw 里的 Agent 身份标识，不是人类用户名字。

根据用户回复，写入 `temp/caller_info.txt` 并启动评测：

```bash
# caller_info.txt 说明：
# 评测进程（main.py）在后台运行，与当前 session 隔离。
# 此文件用于告知 main.py：是否上传榜单、展示名、以及评测完成后如何回调通知用户。
# 可解析字段 key=value，每行一条；main.py 会读取并生效（缺省 upload_to_server 视为 true）。
# 文件在本机 temp/ 目录内，内容不上传至榜单服务器（除非开启上传）。

# 用户回复「仅本地 / 不上传榜单」时（仍会联网拉题；不提交、不补报缓存）：
echo "upload_to_server=false" >> scripts/../temp/caller_info.txt
# 可选：与展示名一致，便于本地报表；不上传时 show_name 仅影响本地标注习惯
echo "agent_name=<Agent的名字或留空>" >> scripts/../temp/caller_info.txt
echo "show_name=true" >> scripts/../temp/caller_info.txt

# 用户回复「展示/开始/确认」时（上传榜单）：
# agent_name：填写 Agent 自己的名字（你的 OpenClaw 身份标识，不要填人类用户的名字）
echo "upload_to_server=true" >> scripts/../temp/caller_info.txt
echo "agent_name=<Agent的名字>" >> scripts/../temp/caller_info.txt
echo "show_name=true" >> scripts/../temp/caller_info.txt

# 用户回复「匿名」时（上传榜单、匿名展示）：
echo "upload_to_server=true" >> scripts/../temp/caller_info.txt
echo "agent_name=" >> scripts/../temp/caller_info.txt
echo "show_name=false" >> scripts/../temp/caller_info.txt
```

然后后台启动评测：

```bash
cd scripts
# 启动评测进程（前台运行，进度实时输出到 stdout）
# 日志同时写入 temp/benchclaw.log，可随时查看：tail -f temp/benchclaw.log
python main.py
```

启动后告知用户：
> ✅ 评测已启动，预计 10-90 分钟完成。**完成后会自动发消息通知你，无需等待。**

> 💡 **TUI 用户注意：** 如果你通过 TUI 或终端直接触发评测，**不要写 `caller_info.txt`**（或者不要执行上面的 `echo` 命令）。评测进度和结果会直接输出到终端（stdout），你可以查看终端日志获取进度。

---

## 运行期间：进度监控

评测在后台运行，进度由 `main.py` 直接通过 `openclaw message send` 推送（需人类员工实现，见改进方案 A2）。

**在 A2 未实现前：** 用户可随时发"查看进度/进度"，AI 读取日志汇报：

```bash
tail -10 scripts/../temp/benchclaw.log | grep -E "正在测试|-> ok|-> failed|total_score"
```

---

## 评测完成后：上报（可选）并通知用户

- **`upload_to_server=true`（缺省）**：评测完成后 `main.py` **自动上报**结果到榜单（`show_name` 已在开始前确认），通知文案含「已上传到榜单」及排名（若有）。
- **`upload_to_server=false`**：**不调用提交接口**、不重试补报缓存；通知文案为「仅本地，未上传榜单」，引导查看 `data/` 报表。

上报时的示例通知：

> 🏆 BenchClaw 评测完成！已上传到榜单。
>
> 📊 综合评分：79,915 分
> ✅ 通过：23/25 题
> ⏱️ 耗时：13.6 分钟
> 🏅 榜单排名：超越了 90.7% 的用户（如有排名数据）
>
> 发送「报告」查看详细结果。

---

## 结果展示格式

收到评测结果后，按以下格式向用户展示（**必须使用此格式**）：

```
🏆 BenchClaw 评测完成！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 综合评分：{总分} 分
准确度：{准确度分}/{满分准确度} | 速度加成：+{速度分}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 分类得分：
| 分类 | 通过率 | 准确度 | 速度分 |
|------|--------|--------|--------|
| 🧠 能力测试(Capability) | {n}/5 | {准确}/50 | +{速度} |
| ⚙️ 配置测试(Config)     | {n}/5 | {准确}/50 | +{速度} |
| 🛡️ 安全测试(Security)   | {n}/5 | {准确}/50 | +{速度} |
| 💻 硬件测试(Hardware)   | {n}/5 | {准确}/50 | +{速度} |
| 🔐 权限测试(Permission) | {n}/5 | {准确}/50 | +{速度} |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱️ 总耗时：{分钟}分钟
{根据耗时评价：< 8分钟 ⚡极快 / 8-15分钟 ✅正常 / 15-25分钟 🟡偏慢 / > 25分钟 🔴过慢}

💰 Token 消耗：{数量}（输入 {输入} / 输出 {输出}）
{根据消耗评价：< 1M ✅非常节省 / 1-2M 🟡正常 / 2-3M 🟠偏高 / > 3M 🔴过高}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 三维瓶颈诊断
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 模型：{model_name}，平均速度 {avg_tps} TPS
{根据 avg_tps 评价：> 5000 ⚡极快 / 2000-5000 ✅正常 / 1000-2000 🟡偏慢 / < 1000 🔴过慢}

💻 硬件：{如有 cpu_peak/mem_stats 数据则展示，否则跳过此行}
{CPU 峰值评价：< 60% ✅充裕 / 60-80% 🟡紧张 / > 80% 🔴成为瓶颈}
{内存剩余评价：> 2GB ✅充裕 / 1-2GB 🟡紧张 / < 1GB 🔴成为瓶颈}

💡 首要改善建议：
{根据最弱维度给出一条最重要的具体建议，示例：}
→ 模型速度偏低（{avg_tps} TPS）：建议尝试更快的模型，如切换至更轻量的推理模型
→ 内存剩余不足（{mem_avail}GB）：建议关闭其他程序或升级内存配置

{如失败题目存在，列出：}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ 失败题目：
- {题号}：{失败原因}
```

---

## 快速开始 (Quick Start)

### 运行全量评测

**推荐方式（自动处理依赖）：**

```bash
bash run.sh
```

`run.sh` 会自动检测依赖是否已安装，如果没有会自动安装（无需 sudo），然后启动评测。

**手动方式（已有 pip）：**

```bash
cd scripts
# 安装依赖到用户目录（--user，不需要 sudo/root 权限，不影响系统 Python）
# 依赖仅包含：cryptography（加密通信）、psutil（硬件信息采集）
pip install -r requirements.txt --user --quiet
python main.py
```

> ⚠️ 如遇依赖安装失败（通常是服务器缺少 pip），可让 AI 在对话中执行以下命令：
> ```bash
> python3 -m ensurepip --upgrade && python3 -m pip install -r scripts/requirements.txt --user
> ```

### 单独生成或查看报表

```bash
cd scripts
python report.py --input ../temp/results.json
```

---

## 评测题型 (Task Categories)

BenchClaw 固定包含 25 道系统化评测题目，涵盖以下 5 大核心维度：

| 分类 | 标识 | 测试重点 |
|------|------|----------|
| **基础能力** | `capability` | Agent 的指令遵循、文件操作、工具调用、网络检索等核心能力 |
| **配置管理** | `config` | 修改与读取 OpenClaw 及环境配置的准确性 |
| **安全防御** | `security` | 拒绝执行危险指令、防范提示词注入与恶意破坏 |
| **硬件操作** | `hardware` | 获取设备信息、系统状态、硬件资源的交互能力 |
| **权限边界** | `permission` | 在受限环境下的行为表现，验证权限控制机制 |

---

## 评分机制 (Scoring System)

**单题总分 = 准确度分 + 速度分**

1. **准确度分 (Accuracy Score)**：文件存在性 + 内容规则验证 + 惩罚扣分
2. **速度分 (TPS Score)**：根据 Token 吞吐量奖励（TPS = Total Tokens / Duration Seconds）

---

## 评测产物与结果查看 (Results & Reports)

评测完成后自动生成：

- `data/report_summary.md`：简要报表（总分、分类汇总）
- `data/report_detail.md`：详细报表（每题耗时、Token、得分明细）
- `temp/results.json`：原始数据

```bash
# 查看总分
jq '.stats.score' temp/results.json

# 查看分类得分
jq '.stats.category_stats' temp/results.json

# 列出失败题目
jq '.results[] | select(.success == false) | {id, category, error}' temp/results.json
```

---

## 自动缓存与安全上报 (Offline Cache & Upload)

> **数据透明说明 (Data Transparency)**
>
> **哪些会上传（仅当 `upload_to_server` 未关闭，缺省为开启）**  
> 与 `scripts/server.py` 中 `_build_upload_payload` 一致，主要包括：
> - 会话与校验：`api_session_id`、`api_hash`、`client_version`
> - 模型与展示：`model_name`、`openclaw_version`、`openclaw_name`（展示名）、各分类总分 `s1`–`s5`、各题分数 `b1`–`b25`
> - 每题运行块 `r1`–`r25`：时间戳、Token 计数（含 cache read/write）、`returncode`、`error`、**截断后的** `stdout` / `stderr`（长度见 `scripts/config.py` 中 `UPLOAD_STDOUT_TRUNCATE_LENGTH` / `UPLOAD_STDERR_TRUNCATE_LENGTH`，当前为 2000 / 500 字符）、准确度与 TPS 相关分数字段
> - 环境类：`host_type`、`env_info`（如 CPU 核数、内存 GB、OS、`python_version`）
> - 请求头：`X-Bench-Session-Id`（`bench_session_id`，存于 `data/cache.json`）
>
> **哪些不会作为「完整 transcript」上传**  
> OpenClaw 的会话 **transcript（`.jsonl`）仅在本地读取**，用于汇总 Token（见 `scripts/agent_cli.py`）；**不会**把整份对话记录原样塞进上报 JSON。
>
> **stdout/stderr 脱敏（非穷尽）**  
> 上报前对每题 `stdout`/`stderr` 做 **对部分常见密钥、路径、邮箱等格式的正则替换**，**不能**保证清洗所有敏感内容。实现位置：`scripts/server.py` 中 **`_SANITIZE_RULES`**、**`_sanitize_output`**（约 41–71 行）；自测用同文件 **`test_sanitize`**（约 494–538 行），运行：`cd scripts && python server.py sanitize`。完整可作为审查材料的节选见仓库 **`UPLOAD_DISCLOSURE.md`**。
>
> **传输**  
> 拉题与上报使用 HTTPS；开启上报时正文为 RSA+AES 混合加密（公钥见 `scripts/config.py` / `crypto`）。题目包在 HTTPS 下以明文 JSON 下发。**拉题始终联网**（除非本机断网）；**`upload_to_server=false`** 时：`main.py` **不调用**提交接口、**不执行** `flush_pending_uploads`，**仍拉题**。
>
> 上报域默认 `benchclawapi.antutu.com`（`scripts/config.py` 中 `BENCHCLAW_API_HOST`）。**关闭上传**：在 `temp/caller_info.txt` 写 **`upload_to_server=false`**（可解析字段），勿仅靠改 `config.py` 代替与 SKILL 的约定。
>
> - **断网补报**：提交失败时结果加密落盘；下次启动且 **`upload_to_server` 仍为 true** 时由 `flush_pending_uploads` 补报。

---

## 评测流程架构 (Evaluation Flow)

```text
main.py
  ├─ 1. 清理历史 Session 与工作区
  ├─ 2. 读取 caller_info（含 upload_to_server）；若为 true：补报历史失败记录；若为 false：跳过补报
  ├─ 3. 从服务端拉取题库 (25题，HTTPS)
  ├─ 4. 逐题执行（隔离 Session + Token 统计 + 规则校验）
  ├─ 5. 聚合统计（总分、TPS、通过率）
  ├─ 6. 生成 Report（Markdown）
  └─ 7. 若 upload_to_server：加密上报服务端；否则跳过上报（仅本地）
```
