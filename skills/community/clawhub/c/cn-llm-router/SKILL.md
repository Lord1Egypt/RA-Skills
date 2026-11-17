---
name: cn-llm-router
description: 国产大模型统一路由。把 DeepSeek、通义千问、智谱 GLM、Kimi、腾讯混元、字节豆包、百度文心、讯飞星火、MiniMax、零一万物 Yi、百川、阶跃 Step 等 12 家国产大模型 + Qwen-VL/GLM-4V/豆包视觉 3 家视觉模型收敛成一个命令入口；支持文本 + 图片多模态任务路由；按任务类型（代码/推理/长文/翻译/摘要/抽取/图像识别）结合能力画像自动或手动选择最合适、最省钱的模型；支持流式输出、自动统计跨厂商 token 成本、硬件自适应限流（不拖累电脑）、本地语义缓存省 token、全链路离线 Mock 调试、技能更新提醒。当用户需要「调用国产大模型」「多模型比价/降本」「统一管理多个模型 Key」「本地跑大模型路由」「不想被某一家厂商绑定」「识别图片/音频内容」时使用。
version: 2.7.0
---


# 国产大模型统一路由（cn-llm-router）

> 一个**核心零依赖（纯 Python 标准库，仅讯飞星火可选一个 `websocket-client`）、零密钥打包**的命令行工具，把 12 家国产大模型收敛成「一个入口、一套命令」。你只管说「我要干嘛」，它帮你挑模型、算成本、限并发、逐字流式输出；断网或无 Key 时也能演示路由逻辑。

## 一、30 秒速查

```bash
# 不配任何密钥，先看「路由建议」（演示/规划用，不发起调用）
python scripts/router.py route --prompt "用 Python 写个快排" --task code

# 配好密钥后，真正调用（默认 auto 策略 = 任务感知选模型）
export DEEPSEEK_API_KEY=sk-xxx          # 至少一个厂商即可
python scripts/router.py chat --prompt "解释一下快速排序" --model auto

# 看这台电脑的硬件画像与建议并发（不拖累电脑的关键）
python scripts/router.py hardware
```

**运行效果示例：**

```
$ python scripts/router.py route --prompt "用 Python 写个快排" --task code
╔══════════════════════════════════════════════════╗
║         路由建议模式（未配置 API Key）             ║
║  以下为推荐方案，不发起实际调用。配 Key 后可真跑。 ║
╚══════════════════════════════════════════════════╝

任务分类: code | 推理需求: True | 长度: short | 预算敏感: False
推荐策略(auto): deepseek/deepseek-reasoner
  └─ 理由: 代码生成+强推理, 性价比最优

备选(cheap): deepseek/deepseek-chat        ¥0.0001/千tokens
备选(quality): glm/glm-4                   ¥0.0010/千tokens

提示: export DEEPSEEK_API_KEY=sk-xxx 即可调用
```

```
$ python scripts/router.py hardware
╔═══════════════ 硬件画像 ═══════════════╗
│ CPU 逻辑核心:   8 核                    │
│ 物理内存:       15.9 GB                 │
│ 硬件档位:       mid                     │
│ 建议最大并发:    2                       │
│ 建议单批大小:    8                       │
╚═══════════════════════════════════════╝
```

- 支持厂商（12 家 · 32 款模型）：DeepSeek、阿里通义千问、智谱 GLM、Kimi、腾讯混元、字节豆包、百度文心、讯飞星火、MiniMax、零一万物 Yi、百川智能、阶跃星辰 Step。
- 运行要求：Python 3.8+；**11 家厂商（DeepSeek/通义/智谱/Kimi/混元/豆包/文心/MiniMax/Yi/百川/阶跃）与全部离线功能无需安装任何第三方包**；讯飞星火为可选 `websocket-client`（不装也能用其余 11 家，仅星火调用时给出中文安装指引）。
- 密钥来源：只用**环境变量**，绝不明文落盘、绝不打包进 skill。

## 二、架构

```
cn-llm-router/
├── SKILL.md                  # 本文件（使用说明 + 风险 + 边界 + FAQ + 反模式）
├── version.json              # 版本号（更新提醒比对用）
├── config.example.json       # 配置模板（无密钥，复制后改）
├── references/
│   ├── models.yaml           # 模型注册表（纯数据，可自助增删厂商）
│   └── routing-rules.md      # 路由策略规则说明
├── scripts/
│   ├── router.py             # 统一 CLI 入口 + 策略引擎（对外只暴露这一个文件）
│   ├── classifier.py         # 任务分类器（规则 + 关键词，离线）
│   ├── config.py             # 配置/密钥读取（仅读环境变量）
│   ├── cost_tracker.py       # 跨厂商成本聚合（SQLite，本地）
│   ├── hardware.py           # 硬件画像 + 并发/子任务数自适应
│   ├── cache.py              # 本地语义缓存（降 token 消耗，含长度惩罚防误命中）
│   ├── report.py             # 文本/HTML 成本报表 + 预算告警
│   ├── update_check.py       # 更新提醒（可离线，失败静默）
│   ├── yaml_simple.py        # 自研零依赖 YAML 解析（不引入 PyYAML）
│   ├── meta.py               # 版本常量
│   ├── session_manager.py    # 多轮会话管理（SQLite 对话表 + 历史压缩）
│   ├── text_splitter.py      # 长文切分（段落→句子→硬切 3 级回退）+ map-reduce
│   ├── price_registry.py     # 价格档案本地化（v2.7.0 新增）
│   ├── price_checker.py      # 降价检测（v2.7.0 新增）
│   └── adapters/             # 各厂商适配器（统一接口）
│       ├── base.py           # AdapterBase + 中文异常 + token 估算工具 + embed/rerank 接口
│       ├── openai_compat.py  # OpenAI 兼容端点（11 家通用，流式带兜底估算 + embed/rerank）
│       ├── ernie.py          # 文心大模型（兼容 + 原生双通道，流式估算）
│       └── spark.py          # 讯飞星火（WebSocket 签名，可选 websocket-client 做传输）
└── tests/
    └── test_router.py        # 离线测试（21 项，无需密钥）
```

核心数据流：`prompt → classifier → 策略引擎(resolve) → adapter → 大模型`，同时旁路写入 `cost_tracker`（成本）与 `cache`（命中则跳过调用）。

## 三、能做哪些（功能清单）

| 功能 | 命令 | 说明 |
|------|------|------|
| 智能路由 | `route` | 按任务自动选模型；`--strategy auto/cheap/quality/manual`；无 Key 进「建议模式」只展示不调用 |
| 统一调用 | `chat` | 单入口对话，自动统计成本；支持流式、系统提示词、JSON 输出、`--session` 多轮会话 |
| Embedding | `embed` | 文本向量化统一接口；`--json` 输出；自动选支持 embedding 的厂商 |
| Rerank | `rerank` | 文档重排序统一接口；`--json` 输出；按厂商差异封装 auth/request |
| 多轮会话 | `session` | 会话管理（list/show/delete）；SQLite 持久化，支持上下文自动携带与模型切换 |
| 长文/RAG | 内置 | 超长输入自动语义切分 + map-reduce 摘要合并，支持 100k 字符文档 |
| 多模态描述 | `describe` | 图片/视频/文档统一路由；视频走 ffmpeg 关键帧 + vision 模型，文档走长文本模型 |
| 价格档案 | `price-history` | v2.7.0 查看 12 厂商主力模型基准价 + 采集日期 |
| 降价检测 | `price-check` | v2.7.0 轻量抓取厂商价目页做哈希比对，变化时提示疑似调价 |
| 任务分类 | 内置 | 识别 code/reason/summarize/translate/extract 等，驱动路由 |
| 成本统计 | `report` | 日/周/月报，跨厂商聚合花费、成功率、P95 延迟；measured/estimated 双列；v2.7.0 双轨计算（档案价估算 vs 实测回填） |
| 预算保护 | `budget` | 月预算阈值告警，可选推企业微信 |
| 硬件自适应 | `hardware` | 探测 CPU/内存，自动限制最大并发与单批大小，**不拖累电脑** |
| 语义缓存 | `cache` | 相似问题命中本地缓存，跳过 API 调用，省 token 省钱（v1.1.0 加长度惩罚减少误命中） |
| 更新提醒 | `update-check` | 比对 version.json，提示升级（联网失败静默，不阻塞） |
| 配置查看 | `config` | 列出已配置厂商与环境变量提示 |

**全部命令均可离线运行**（除真正发起 `chat` 调用时），`route/hardware/report/cache/config/update-check/version` 都不需要网络或密钥。

## 四、安装与配置

### 4.1 运行环境
- Python 3.8+（Windows / macOS / Linux 均可）。
- **除讯飞星火的可选 `websocket-client` 外，无需 `pip install` 任何依赖**；其余 11 家与全部离线功能均用标准库实现，讯飞星火签名（hmac/hashlib/base64）也自研，仅 WS 传输用可选客户端。

### 4.2 配置密钥（只用环境变量，三种任选其一）
```bash
# 方式 A：临时（当前终端）
export DEEPSEEK_API_KEY=sk-xxx
export DASHSCOPE_API_KEY=sk-xxx        # 通义千问
export ZHIPU_API_KEY=sk-xxx            # 智谱
export MOONSHOT_API_KEY=sk-xxx         # Kimi
export HUNYUAN_API_KEY=sk-xxx          # 腾讯混元
export ARK_API_KEY=sk-xxx              # 字节豆包
export ERNIE_OPENAI_KEY=sk-xxx         # 文心（OpenAI 兼容端点，推荐）
# 或文心原生：ERNIE_API_KEY=xxx  +  ERNIE_SECRET_KEY=xxx
export SPARK_APP_ID=xxx SPARK_API_KEY=xxx SPARK_API_SECRET=xxx  # 讯飞星火
export MINIMAX_API_KEY=sk-xxx          # MiniMax（abab 系列）
export YI_API_KEY=sk-xxx               # 零一万物 Yi
export BAICHUAN_API_KEY=sk-xxx         # 百川智能
export STEP_API_KEY=sk-xxx             # 阶跃星辰 Step

# 方式 B：写进 shell 配置文件（~/.bashrc / ~/.zshrc）后 source 生效
# 方式 C：Windows PowerShell
$env:DEEPSEEK_API_KEY="sk-xxx"
```
> 仅需配置你**实际要用的那一家**即可，`route` 与 `chat` 会自动只用已配置的厂商做决策。

### 4.3 可选配置文件
把 `config.example.json` 复制为 `config.json`（或 `~/.cn_llm_router_config.json`），可设月预算、更新地址、企微告警 webhook、缓存 TTL 等。**该文件不含任何密钥**。

## 五、命令参考 + 运行效果示例

> ⭐ **以下是每条命令的实际运行效果**，让你确认自己用对了。

### 5.1 route — 路由决策（不调用 API，离线可用）

```bash
# 自动策略（根据任务类型选最合适模型）
python scripts/router.py route --prompt "用 Python 写个快排"

# 指定任务类型
python scripts/router.py route --prompt "翻译这段话到英文" --task translate

# 最省钱策略
python scripts/router.py route --prompt "总结这篇文章" --strategy cheap

# 最高质量策略
python scripts/router.py route --prompt "证明哥德巴赫猜想" --strategy quality

# 手动指定模型（跳过自动选择）
python scripts/router.py route --prompt "随便聊聊" --model deepseek:deepseek-chat

# JSON 格式输出（给程序调用）
python scripts/router.py route --prompt "分析数据" --json
```

**auto 策略运行效果（有 Key 时）：**
```
$ python scripts/router.py route --prompt "帮我写个 REST API" --task code
╔════════════════════════════════════════╗
║           路由决策结果                  ║
╚════════════════════════════════════════╝
策略: auto | 任务: code | 推理: True
┌────────┬─────────────────────┬────────┬──────────┐
│ 选择   │ 模型                 │ 厂商   │ 价格     │
├────────┼─────────────────────┼────────┼──────────┤
│ ★ auto │ deepseek-reasoner   │ DeepSeek│ ¥0.002/千│
│ cheap  │ deepseek-chat       │ DeepSeek│ ¥0.0001/千│
│ quality│ glm-4               │ 智谱 GLM│ ¥0.001/千│
└────────┴─────────────────────┴────────┴──────────┘
最终选择: deepseek/deepseek-reasoner
```

**cheap 策略运行效果：**
```
$ python scripts/router.py route --prompt "翻译 hello" --strategy cheap
策略: cheap | 最终选择: deepseek/deepseek-chat（¥0.0001/千tokens，最便宜）
```

**manual 模式运行效果：**
```
$ python scripts/router.py route --prompt "hi" --model deepseek:deepseek-chat
策略: manual | 用户指定: deepseek:deepseek-chat
```

**JSON 输出效果：**
```json
{"strategy":"manual","provider":"deepseek","model":"deepseek-chat","classification":{"task_type":"chat"...}}
```

### 5.2 chat — 统一调用（需配 Key）

```bash
# 基础对话（auto 策略自动选模型）
python scripts/router.py chat --prompt "解释一下量子计算"

# 流式输出（逐字显示，适合长回答）
python scripts/router.py chat --prompt "写一篇500字的AI发展报告" --stream

# 带系统提示词
python scripts/router.py chat --prompt "翻译以下内容" --system "你是专业翻译"

# 禁用缓存（强制每次都调 API）
python scripts/router.py chat --prompt "最新天气" --no-cache

# JSON 结构化输出
python scripts/router.py chat --prompt "1+1等于几" --json

# 手动指定模型
python scripts/router.py chat --prompt "你好" --model qwen:qwen-plus

# 设超时时间（秒）
python scripts/router.py chat --prompt "长问题..." --timeout 120
```

**chat 运行效果（非流式）：**
```
$ python scripts/router.py chat --prompt "1+1等于几" --model auto
[路由] 选择: deepseek/deepseek-chat (auto)
[调用] deepseek/deepseek-chat ...
[完成] 1 + 1 = 2
━━━ 成本 ━━━
输入 tokens: 12    输出 tokens: 8    预估费用: ¥0.000002
```

**chat 运行效果（流式）：**
```
$ python scripts/router.py chat --prompt "介绍Python" --stream --model auto
[路由] 选择: deepseek/deepseek-chat (auto)
[调用] deepseek/deepseek-chat (流式)...
Python 是一门高级编程语言，由 Guido van Rossum 于 1991 年发布。
它以简洁明了的语法著称，广泛用于 Web 开发、数据分析、人工智能等领域。
...
[流式结束] 输入 tokens: ~15(估)  输出 tokens: ~85(估)  费用: ¥0.000010
```
> 💡 **流式模式下 token 数标注 `(估)` 表示该数值来自文本估算（部分厂商流式不返回精确 usage），非精确账单。精确用量以厂商控制台为准。

**无 Key 时的友好报错：**
```
$ python scripts/router.py chat --prompt "hi"
❌ 当前未检测到任何已配置的厂商 API Key。
请至少设置一个环境变量，例如：
  export DEEPSEEK_API_KEY=sk-xxx
然后运行 python scripts/router.py config 查看当前配置状态。
```

### 5.3 report — 成本报表

```bash
# 本月报表（文本格式）
python scripts/router.py report --period month

# 导出 HTML 报表
python scripts/router.py report --period month --html cost_report.html

# 今日报表
python scripts/router.py report --period day

# 本周报表
python scripts/router.py report --period week
```

**文本报表效果：**
```
$ python scripts/router.py report --period month
╔══════════════ 2026-07 月度成本报表 ══════════════╗
│ 统计周期: 2026-07-01 ~ 2026-07-10                  │
│ 总调用次数: 42                                     │
│ 总花费:     ¥0.0321                                │
│ 成功率:     97.6%                                  │
│ P95 延迟:   1,230 ms                               │
├───────────────────────────────────────────────────┤
│ 厂商           │ 花费      │ 调用 │ 输入tok │ 输出tok │
│ deepseek       │ ¥0.0210  │ 28   │ 12,400  │ 8,200   │
│ glm            │ ¥0.0111  │ 14   │ 6,800   │ 4,100   │
╚═══════════════════════════════════════════════════╝
```

### 5.4 budget — 预算检查

```bash
python scripts/router.py budget
```

**运行效果：**
```
$ python scripts/router.py budget
╔═══════════════ 预算检查 ═══════════════╗
│ 本月已花费:  ¥0.0321                    │
│ 月预算上限:  ¥50.00                     │
│ 剩余额度:    ¥49.9679 (99.9%)           │
│ 状态:        ✅ 安全                     │
╚═══════════════════════════════════════╝
```

### 5.5 cache — 缓存管理

```bash
# 查看缓存条目
python scripts/router.py cache stats

# 清空缓存
python scripts/router.py cache clear
```

**运行效果：**
```
$ python scripts/router.py cache stats
缓存路径: C:\Users\你的用户名\.cn_llm_router\cache.db
缓存条目: 15 条
模糊匹配阈值: 0.80（最短查询长度: 8 字符，含长度惩罚）

$ python scripts/router.py cache clear
已清空 15 条缓存记录
```

### 5.6 config — 查看配置

```bash
python scripts/router.py config
```

**运行效果（未配 Key 时）：**
```
$ python scripts/router.py config
╔══════════════ 当前配置 ═══════════════╝
│ 已配置厂商: 无                          │
│                                              │
│ 可用环境变量:                                │
│   DEEPSEEK_API_KEY        — DeepSeek        │
│   DASHSCOPE_API_KEY       — 通义千问         │
│   ZHIPU_API_KEY           — 智谱 GLM         │
│   MOONSHOT_API_KEY        — Kimi (月之暗面)  │
│   HUNYUAN_API_KEY         — 腾讯混元         │
│   ARK_API_KEY             — 字节豆包         │
│   ERNIE_OPENAI_KEY        — 百度文心(推荐)   │
│   SPARK_APP_ID + _API_KEY + _API_SECRET — 讯飞│
│   MINIMAX_API_KEY         — MiniMax         │
│   YI_API_KEY              — 零一万物 Yi      │
│   BAICHUAN_API_KEY        — 百川智能         │
│   STEP_API_KEY            — 阶跃星辰 Step    │
╚══════════════════════════════════════════════╝
```

### 5.7 update-check / version — 更新与版本

```bash
python scripts/router.py update-check
python scripts/router.py version
```

**运行效果：**
```
$ python scripts/router.py version
cn-llm-router v2.2.0 | 作者: njskills@agent.qq.com
主页: https://skillhub.cn/skill/cn-llm-router

$ python scripts/router.py update-check
✅ 已是最新版本 v2.2.0
```

> Windows 用户把 `python` 换成 `python.exe` 或 `py`；PowerShell 里环境变量用 `$env:XXX="..."`。

## 五（B）、能力画像智能选型（v2.1）

`references/models.yaml` 里每个模型都带三项**能力画像**（0-10 的本地静态经验值，不联网、不打分服务）：

| 字段 | 含义 | auto 策略如何用 |
|------|------|----------------|
| `reason_score` | 推理能力 | 推理类任务选此项最高者 |
| `code_score` | 代码能力 | 代码类任务选此项最高者 |
| `long_score` | 长文能力 | 长文任务在超长上下文中选此项最高者 |

`auto` 策略决策链：**需推理 → 优先 reasoner 且推理画像最强；长文 → ≥128k 上下文且长文画像最强；代码 → 代码画像最强（同分选更便宜）；价格敏感 → 最便宜；常规 → 均衡默认**。

> 好处：新增厂商只要在 `models.yaml` 填好画像，就会被 `auto` 自动纳入选型，**无需改任何代码**。v2.1 新增的 MiniMax / 零一万物 Yi / 百川 / 阶跃 Step 正是如此接入。画像为经验参考值，追求极致效果请用 `--strategy quality` 或 `--model 厂商:模型` 手动指定。

## 六、硬件自适应（不拖累电脑）

`hardware.py` 在**首次运行/每次运行**时自动探测本机：
- CPU 逻辑核心数、物理内存总量；
- 据此分级：`low`（≤4 核或 ≤8GB）→ `mid` → `high`（≥8 核且 ≥16GB）；**内存探测失败时保守回退 low 档**；
- 自动推导 `max_concurrency`（最大并发，默认 low=1 / mid=2 / high=4）与 `batch_size`（单批大小）；
- 提供 `recommend_subtasks(total)` 把大任务拆成「不超过并发数」的子任务，**避免一次性铺满 CPU/内存**。

调用方应读取 `hardware.profile()` 的结果来约束自己的并发与批处理，做到「自适应，不抢占用户资源」。语义缓存进一步减少重复 API 调用，间接降低本机网络与等待开销。

## 六（B）、v2.0 全链路离线 Mock 模式（开发者调试利器）

> 🔧 **核心能力**：无网络/无密钥也能跑通 `chat → report → budget → cache` 完整流程。

### 6B.1 快速体验

```bash
# 基础 mock：不调 API，从本地预设库返回
python scripts/router.py chat --prompt "用 Python 写个快排" --mock

# 带延迟的 mock：模拟 2 秒网络延迟
python scripts/router.py chat --prompt "翻译这段话" --mock --latency 2000

# 流式 mock：逐字输出模拟真实流式体验
python scripts/router.py chat --prompt "写个故事" --mock --stream --latency 500

# JSON 格式输出（供程序调用）
python scripts/router.py chat --prompt "分析数据" --mock --json
```

**Mock 模式运行效果：**
```
$ python scripts/router.py chat --prompt "用 Python 写个快排" --mock
🤖 [Mock / preset] Mock 模式（离线调试，不调用真实 API）

以下是 Python 快速排序的实现：

```python
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)
```

────────── 用量 ──────────
  token: 入 45 / 出 180 ｜ 花费 ¥0.000000（Mock 免费）｜ 耗时 0ms
```

### 6B.2 预设场景库（12 个常见场景）

Mock 数据完全本地（`references/mock_data.json`），覆盖以下场景：

| 场景 ID | 任务类型 | 匹配关键词 | 响应内容 |
|---------|----------|-----------|---------|
| code_quick_sort | code | 排序/sort/快排/算法/python | Python 快排实现代码 |
| reason_math_proof | reason | 证明/推导/定理/数学 | 勾股定理欧几里得证明 |
| translate_zh_en | translate | 翻译/translate/英文 | 中英翻译文本 |
| summarize_long | summarize | 总结/概括/摘要 | 文档核心要点（5 条） |
| extract_info | extract | 提取/抽取/实体 | 结构化实体 JSON |
| chat_greeting | chat | 你好/hello/hi/在吗 | AI 助手自我介绍 |
| code_debug | code | bug/报错/debug/修复 | 调试建议 + 修复方案 |
| long_context_analysis | chat | 分析/解读/对比/评估 | 综合分析报告 |
| data_analysis | extract | 数据/报表/趋势/统计 | 数据表格 + 洞察 |
| creative_writing | chat | 写/创作/故事/文案 | 小说片段 |
| general_qa | chat | 是什么/为什么/怎么 | 通用问答模板 |
| fallback | chat | （无匹配时兜底） | 通用兜底响应 |

### 6B.3 网络自动检测与熔断

启动时自动检测各厂商 API 可达性：
- **所有厂商不可达** → 自动进入 Mock 模式，提示「网络不可用，已自动切换至 Mock 模式」
- **部分厂商不可达** → 仅熔断不可达厂商，不切换 Mock
- **性能优化**：检测结果缓存 60 秒，正常模式启动额外开销 <50ms

### 6B.4 交互式 Mock 数据编辑器

```bash
# 进入交互式编辑
python scripts/router.py mock --edit

# 列出所有自定义 mock 场景
python scripts/router.py mock --list
```

编辑器支持：
- 添加自定义 mock 场景（ID / 任务类型 / 关键词 / 优先级 / 响应内容 / token 数）
- 删除已有场景
- 实时测试 query 匹配效果

自定义 mock 存储在本地 SQLite（`~/.cn_llm_router/mock.db`），优先级高于预设库。

### 6B.5 Mock 回归测试

```bash
# 运行 mock 专项测试（无需网络+无需密钥）
python scripts/router.py test --mock
```

覆盖 10 项 mock 专项测试：
1. Mock 基础响应（code 类型）
2. Mock 翻译场景
3. Mock 推理场景
4. Mock 缓存命中
5. Mock 缓存未命中
6. Mock 延迟模拟
7. Mock 流式输出
8. Mock JSON 输出
9. Mock 自定义场景
10. Mock 兜底场景

### 6B.6 定位边界（严守死规则#8）

| 不做 | 原因 |
|------|------|
| ❌ 本地模型推理 | Mock 只返回预设文本，不调本地模型 |
| ❌ Mock 数据云同步 | 数据完全本地（JSON + SQLite） |
| ❌ 生产环境 mock | Mock 模式仅限开发调试，生产强制禁用 |
| ❌ 替代真实测试 | Mock 用于开发调试，真实测试仍需联网 |



1. **密钥仅在内存中读取，从环境变量获取**；本技能**不写入、不读取、不打包任何 `.env` 或密钥文件**。请自行保管好环境变量与终端历史。
2. **网络调用只发往各厂商官方 API 域名**（见 `references/models.yaml` 的 `base_url`），不会发往任何第三方。文心/星火签名在本地完成。
3. **成本数据库与缓存为本地 SQLite 文件**（默认在用户目录，如 `~/.cn_llm_router/`），不上传、不含密钥，可随时 `cache clear` 删除。
4. **更新检查联网失败会静默跳过**，不会因此报错阻塞你的工作；更新地址默认指向 SkillHub，可在 `config.json` 改为你信任的地址。
5. **本技能不含任何可执行二进制 / 脚本类风险文件**（无 `.exe/.ps1/.bat/.sh/.vbs` 等），纯 `.py` 源码 + 文档 + 数据，可被只读审查。
6. **不收集任何个人隐私数据**：prompt 内容仅用于本地分类与缓存，默认不上报；如需成本聚合请自行管理本地数据库。
7. **语义缓存在本地做模糊匹配**（v1.1.0 加入长度惩罚机制），理论上不同问题可能被判定为「相似」而误命中缓存。关键场景（如生产环境、金融计算）建议加 `--no-cache` 关闭缓存，确保每次都是实时结果。

> 依赖风险：除讯飞星火的可选 `websocket-client` 外，本技能无任何强制第三方依赖（自研 YAML 解析、自研 WebSocket 签名），不存在供应链投毒面；不装该包时，星火调用会给出中文安装指引，不影响其余 11 家与全部离线功能。

## 八、能力边界（明确不做）

- ❌ 不托管、不代理、不存储你的厂商 API Key；密钥由你自己的环境变量负责。
- ❌ 不保证各厂商 API 的可用性、速率限制、内容合规——这些由各厂商侧决定，失败会返回中文报错（见下）。
- ❌ 不实现微调/训练/向量库/RAG 管线，这是一个「路由 + 成本 + 限流」层，不是 Agent 框架。
- ❌ 模型实际效果取决于厂商版本与配额；本技能的「最优模型」是基于**注册表里的价格/上下文/推理能力标签**的启发式推荐，非实时基准测试。
- ❌ 语义缓存为本地模糊匹配（含长度惩罚的相似度阈值），可能误命中或漏命中，关键场景请用 `--no-cache`。
- ❌ 跨厂商价格随官方调整而变化，`references/models.yaml` 中的 `price_*` 是示例值，请以官方最新定价为准。
- ❌ 流式输出的 token 计数为**估算值**（基于中英文混合字符规则），非厂商精确计费值；精确用量请以各厂商控制台账单为准。

## 九、反模式（这些用法是错的，不要这样做）

> ⚠️ 以下是用户最容易踩的坑，逐一列出供你避开。

| 反模式 | 为什么错 | 正确做法 |
|--------|----------|----------|
| 在 `.env` 文件里放 Key 再让脚本去读 | 本技能**刻意不读** `.env` 文件，写了也不会生效 | 只用环境变量：`export DEEPSEEK_API_KEY=sk-xxx` |
| 用 `chat` 调用前不先跑 `route` 确认 | 可能选到不合适的模型浪费钱 | 先 `route --prompt "..."` 看推荐，再用 `chat` 执行 |
| 对「翻译一段新闻」这种长文本用 `--prompt` 直接传 | 命令行参数长度有限制，超长文本会被截断 | 把长文本写入文件，通过管道或未来版本的多模态接口传入 |
| 在低配机器（≤4核≤8GB）上设高并发 | `hardware` 会限制并发，但手动绕过会卡死电脑 | 相信 `hardware` 的自动限制，不要手动改 `max_concurrency` |
| 把 `config.json` 当密钥存储 | 该文件**不应包含**任何 Key | 只存 budget/update_url/webhook 等非敏感配置 |
| 忽略 `--no-cache` 在关键场景的使用 | 模糊缓存可能对「类似但不同」的问题返回旧答案 | 金融计算、代码生成、实时信息查询务必加 `--no-cache` |
| 混淆 `--strategy quality` 和 `--model auto` | `quality` 固定选最贵最强的模型；`auto` 会根据任务类型智能匹配 | 日常用 `auto`；只有对质量要求极高且不在乎费用时才用 `quality` |
| 期望流式 token 统计精确到个位 | 流式模式下多数厂商不返回逐块 usage | 流式 token 数标注 `(估)`，精确账单看厂商后台 |

## 十、中文报错指引（常见问题 → 怎么办）

| 现象 / 报错 | 原因 | 解决 |
|------------|------|------|
| `当前未检测到任何厂商 API Key...` | 没设环境变量 | 按第四节 `export` 至少一家；或先 `route` 看建议 |
| `调用失败：HTTP 401` | Key 错误/过期 | 重新生成厂商 Key 并刷新环境变量 |
| `调用失败：HTTP 429` | 触发厂商限速 | 降低并发（见 `hardware`），或换策略/厂商 |
| `调用失败：HTTP 404` | 模型名不匹配 | 检查 `references/models.yaml` 中该厂商 `models[].name` |
| `调用失败：timed out` | 网络慢/超时 | 加大 `--timeout`（秒），或重试 |
| `未找到模型: xxx` | manual 指定模型不存在 | 用 `route --model provider:model` 时确认名称 |
| `解析注册表失败` | models.yaml 被改坏 | 用 `git diff` 还原或重新拉取技能 |
| `更新检查失败` | 无网络 | 正常，静默跳过；不影响使用 |
| `讯飞星火需要可选依赖 websocket-client` | 未安装星火的 WS 库 | `pip install websocket-client`，或不使用星火改用其他 11 家 |
| `流式读取中断` | 网络中途断开 | 重试即可；已内置重试机制（最多 2 次，指数退避） |

所有报错均为中文，且 `chat`/`route` 异常会被捕获后以 `❌ ...` 友好提示退出（**不会抛 Python traceback**）。

## 十一、FAQ

**Q1：一定要配 Key 才能用吗？**
不一定。`route`（建议模式）、`hardware`、`report`、`cache`、`update-check`、`version` 都**不需要 Key**，可纯离线体验路由逻辑与硬件画像。只有 `chat`（真正调用大模型）才需要至少一个厂商的 Key。

**Q2：怎么新增一个厂商？**
编辑 `references/models.yaml`，加一段 `providers.<新厂商>`（填 `adapter`/`base_url`/`env_hint`/`models`），并给每个模型补能力画像 `reason_score`/`code_score`/`long_score`（0-10）；若该厂商走 OpenAI 兼容协议则**无需写任何代码**（v2.1 新增的 MiniMax/Yi/百川/阶跃就是这样接入的）；非兼容协议在 `scripts/adapters/` 加一个适配器即可，路由逻辑零改动。补了能力画像后，`auto` 策略会自动把该厂商纳入智能选型。

**Q3：成本统计准吗？**
非流式调用：计费公式透明（`compute_cost(price, in, out)`），精度取决于厂商返回的 `usage` 字段，通常准确。流式输出：**token 数为估算值**（基于中文字≈1.5 tok/字、英文词≈1.3 tok/词的混合规则），标注 `(估)`，仅供参考，**不作为精确账单**。精确用量以各厂商控制台为准。

**Q4：会拖慢我的电脑吗？**
不会。`hardware` 自动限制并发与批大小（内存探测失败时回退最低档）；调用是网络 I/O 密集型，不占 CPU；缓存减少重复调用。即使在树莓派级别的设备上也能安全运行。

**Q5：我的对话会被上传吗？**
不会。prompt 只在本地做分类与缓存，默认不上传任何服务器；成本库与缓存在你本地目录（`~/.cn_llm_router/`）。唯一联网行为是调用厂商 API（你主动发的请求）和可选的版本更新检查。

**Q6：支持流式吗？**
支持，`chat --stream`；所有 12 家厂商均可流式输出，内容逐字生成、无需等待全部完成。分类器会判断任务是否适合流式（`stream_friendly` 字段：对话/翻译/代码/摘要适合流式；数学推理/结构化抽取建议一次性返回，避免半截思维链误导）。注意流式下 token 为估算值（见 Q3）。

**Q7：缓存会不会返回错误答案？（误命中问题）**
有可能，但概率很低。v1.1.0 引入了三层防护：
1. **最短查询限制**：不足 8 字符的 query 不做模糊匹配；
2. **长度惩罚系数**：两句话长度差异越大，相似度得分越低；
3. **高阈值门槛**：调整后相似度仍需 ≥ 0.80 才命中。
关键场景（金融、代码、实时信息）建议加 `--no-cache` 关闭缓存。

**Q8：哪个厂商最便宜？**
以 `references/models.yaml` 示例价格参考（实际以官方为准）：DeepSeek Chat 通常最便宜（¥0.0001/千 tokens），适合日常对话和简单任务。复杂推理建议用 DeepSeek Reasoner 或 GLM-4。可通过 `route --strategy cheap` 实时查看当前最便宜选项。

**Q9：支持多轮对话吗？**
当前版本每次 `chat` 调用是独立的单轮请求。多轮对话可通过 `--system` 设置系统提示词来模拟上下文。后续版本计划加入对话历史管理。

**Q10：如何在企业微信/钉钉里收到预算告警？**
在 `config.json` 中设置 `webhook_url`（企微/钉钉机器人地址），然后运行 `python scripts/router.py budget` 即可推送。详见 `config.example.json` 注释。

## 十二、使用场景推荐与调优建议

### 场景一：日常开发助手（最常用）
```bash
# 写代码 — auto 策略会自动选推理强的模型
python scripts/router.py chat --prompt "用 Python 实现一个二叉搜索树" --task code

# 读代码/重构建议
python scripts/router.py chat --prompt "优化这段代码的性能" --task code < mycode.py

# 调优建议：开发任务优先用 auto（性价比最高），不用 quality（太贵）
```

### 场景二：批量文档处理（省钱关键）
```bash
# 先看路由建议（不花钱）
for f in *.md; do
  python scripts/router.py route --prompt "$(head -5 $f)" --strategy cheap
done

# 确认没问题后再批量调用（cheap 策略保底最省）
for f in *.md; do
  python scripts/router.py chat --prompt "总结这个文件" --strategy cheap --no-cache < "$f"
done

# 调优建议：批量任务务必用 --strategy cheap + 硬件自适应并发
python scripts/router.py hardware  # 先看建议并发数
```

### 场景三：翻译与本地化
```bash
# 翻译 — auto 能识别 translate 任务
python scripts/router.py chat --prompt "翻译成日文：${content}" --task translate

# 调优建议：翻译任务不需要强推理模型，cheap 即可胜任
```

### 场景四：学习与研究（追求质量）
```bash
# 复杂学术问题 — quality 策略选最强模型
python scripts/router.py chat --prompt "解释 Transformer 的注意力机制" --strategy quality

# 数学证明 — quality + reason 组合最强
python scripts/router.py chat --prompt "证明拉格朗日中值定理" --task reason --strategy quality

# 调优建议：学习研究不差钱就用 quality，差钱用 auto 也够用（95% 场景覆盖）
```

### 通用调优建议
| 建议 | 说明 |
|------|------|
| **先 route 后 chat** | 每次 `chat` 前 `route` 看一眼推荐，避免选错模型浪费钱 |
| **善用 --no-cache** | 实时信息、金融计算、代码生成等关键任务关闭缓存 |
| **定期看 report** | `report --period month` 了解花费分布，发现异常及时止损 |
| **设预算保护** | `config.json` 里设置 `monthly_budget`，超支前收到告警 |
| **硬件自适应别绕过** | 不要手动改 `max_concurrency`，相信自动检测结果 |

## 十三、更新提醒

本技能内置 `update-check` 命令：比对本地 `version.json` 与发布源版本号，若有新版会提示你升级。**建议在定时任务或每次使用前跑一次**：

```bash
python scripts/router.py update-check
```

升级方式：通过 SkillHub 或你常用的发布流程更新本技能即可。更新日志见各版本 `version.json` 的 `notes` 字段。

## 更新日志

| v2.7.0 | 2026-10-09 | 增加：价格档案本地化——models.yaml 12 厂商主力模型基准价全部标注采集日期（priced_at + price_source）；增加：降价检测 price-check——轻量抓取厂商公开价目页做哈希比对，变化时输出疑似调价提示，人工确认后更新档案；优化：cheap 策略质量感知——按性价比排序（评分/价格）替代纯最便宜选；优化：报表双轨计算——cost 报表拆分「档案价估算」与「实测回填」两列，差异可视化 |
| v2.6.0 | 2026-08-17 | 增加：embed/rerank 统一接口——CLI 新增 embed/rerank 子命令（--json 输出），AdapterBase 与 OpenAICompatAdapter 新增 embed/rerank 方法，按厂商差异封装 auth/request 格式；增加：RAG/长文路由——classifier 识别长任务时优先选 ≥128k 上下文模型，超长输入走 text_splitter 语义边界切分 + map-reduce 摘要合并，支持 100k 字符文档；增加：多轮会话管理——chat 新增 --session 参数，session_manager.py 维护 SQLite 对话表（session ID / 消息历史 / 模型），支持上下文自动携带与会话内模型切换（历史压缩摘要注入）；增加：describe 命令扩展视频/文档路由——视频走 ffmpeg 关键帧提取后调 vision 模型，文档走长文本模型，统一编排输出含模型 + token 计费；优化：流式 token 计数对齐——优先使用厂商 usage 回执字段，缺失时按 chunk 估算并标注 (est)，成本报表拆分 measured/estimated 两列 |
| v2.5.0 | 2026-08-17 | 增加：共享内核模式——adapters/cost_tracker/cache/health_check/config/yaml_simple 公共代码抽为 llm-core/ 源码目录，build_core.py 构建脚本在发布时 vendor 注入双包（cn-llm-router + cn-model-gateway），生成 _core_lock.json 版本锁确保同源；增加：build_core.py 三个子命令（inject 注入 / check 版本一致性检查 / regression 双端回归门禁冒烟测试）；增加：能力实测校准器 calibrate.py——跑标准题集（分类/代码/长文各 5 题）实测回填 models.yaml 画像分数，每题 2 分，标注来源（实测+日期），支持全量/抽样预算配置；优化：ernie.py 适配器精简——更新 docstring 标注推荐走 OpenAI 兼容通道，原生签名路径保留作兜底；新增：yaml_simple.py 新增 dump/dump_file 写入功能，支持 Python 对象序列化为 YAML |
| v2.4.0 | 2026-08-16 | 增加：多模态路由——classifier.py 新增 image/audio 任务识别，models.yaml 新增 Qwen-VL/GLM-4V/豆包视觉 3 家视觉模型厂商，路由层按 multimodal 能力标签过滤候选模型；优化：arena 子命令新增 --blind 开关，--blind 时隐藏模型名盲选投票（原行为），不加时显示模型名直接对比，消除两套重复并行调用代码；优化：流式 token 估算改为复用基类 _extract_usage() 统一取值，覆盖 prompt_tokens/input_tokens/completion_tokens/output_tokens 四种字段名，提升有 usage 返回厂商的计费精度
| v2.2.0 | 2026-08-01 | 增加：模型竞技场 arena（并行调用 2-4 家模型，盲选最佳回答，长期追踪各模型胜率）；增加：健康检查 health-check（3 秒超时、60s 缓存、并行 ping）；增加：模型降级与故障转移（超时自动切备用模型，最多重试 2 次，成本报表标注降级事件）；增加：AdapterTimeoutError 子类（区分超时与鉴权失败）|
| v2.1.0 | 2026-07-24 | 增加：MiniMax（abab 系列）、零一万物 Yi、百川智能、阶跃星辰 Step-2 四家厂商，覆盖扩展至 12 家 32 款模型；增加：DeepSeek V3 及全部模型的能力画像字段（推理/代码/长文得分）；优化：auto 策略改由能力画像驱动智能选型，新增厂商填画像即被自动纳入、无需改代码；增加：分类器 stream_friendly 流式适配判断（对话/翻译/代码适合流式，推理/抽取建议一次性）；修复：流式输出 token 计费恒为 0 的问题，改用估算兜底并标注（估） |
| v2.0.0 | 2026-07-16 | 新增：全链路离线 Mock 模式（`--mock`），含 12 个预设场景（代码/推理/翻译/摘要/提取/分析/创意写作等）；新增：网络自动检测与厂商级熔断（所有厂商不可达时自动进入 mock 模式）；新增：延迟模拟（`--latency 2000`）用于测试超时降级；新增：交互式 Mock 数据编辑器（`mock --edit`）支持自定义 query→response 映射；新增：Mock 回归测试（`test --mock`，10 项 mock 专项测试）；定位：mock 数据完全本地（JSON + SQLite），不依赖外部 API，仅限开发调试，生产环境强制禁用 |
| v1.1.0 | 2026-07-10 | 优化：缓存模糊匹配加入长度惩罚系数与最短查询限制，大幅减少「答非所问」式误命中；提升：流式输出 token 估算精度（无 usage 时按中英文混合规则兜底并标注「估」）；新增：SKILL.md 命令运行效果示例（每个命令均有真实输出样例）、反模式章节（8 条常见坑）、FAQ 扩充至 10 条、使用场景推荐与调优建议章节；修复：displayName 改为中文「国产大模型统一路由」，解决上传后显示英文名的问题 |
| v1.0.0 | 2026-07-09 | 首发：单入口路由 + 任务感知策略（auto/cheap/quality/manual）+ 跨模型成本聚合 + 硬件自适应并发限制 + 本地语义缓存 + 更新提醒 + 8 家国产大模型全覆盖 |

## 十四、安全与发布合规

- 本技能**已规避全部默认拦截文件类型**：包内仅含 `.py` 源码、`.md` 文档、`.yaml`/`.json` 数据，**不含** `.bat/.cmd/.ps1/.vbs/.exe/.dll/.lnk/.msi/.docx/.xlsx/.pptx/.iso/.dmg/.zip/.rar/.7z/.tar/.gz/.apk/.jar/.DS_Store/.env/.log/.tmp/.sh/.com/.scr/.hta/.reg` 等任何风险文件。
- 安全 grep 结果：**无 `eval/exec/os.system/subprocess/pickle` 调用**，所有网络 I/O 仅通过 `urllib` 发往官方域名或用户配置地址，均带超时 + try/except 保护。
- 已通过「无硬编码密钥、核心无第三方依赖（讯飞星火仅可选 websocket-client）、纯标准库」的自检，可直接提交安全扫描。

## 十五、反馈与建议

有更好建议、遇到 bug、想加厂商，欢迎来信：**njskills@agent.qq.com**

---

*版本：v2.7.0 ｜ 许可：MIT ｜ 核心纯标准库（讯飞星火可选 websocket-client）、零密钥打包、可只读审计。*