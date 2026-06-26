---
name: A-stock-report
description: "A股数据驱动型报告自动生成与推送系统，支持晨报 / 收盘小结 / 晚报 / 盘中预警 / IPO周报 / 财经周末版。内置投资者情绪打分（6维度，满分100）与AI后市展望。"
version: 3.5.4
---

# A股报告系统

>A股数据驱动型报告自动生成与推送系统，支持晨报 / 收盘小结 / 晚报 / 盘中预警 / IPO周报 / 财经周末版

---

## 目录结构（v3.2.3+1 起明示，v3.5.0 简化）

`clawhub publish` 按 `.clawhubignore` 排除 `knowledge/` + `*.bak`（v3.4.4 立），其他整目录上传。装好后 `~/.hermes/skills/A-stock-report/` 结构：

```
A-stock-report/
├── SKILL.md                      ← 本文件（含完整执行流程 + 14 段护栏 + changelog 索引）
├── _meta.json
├── .clawhubignore                ← v3.4.4 立：排除 knowledge/ + *.bak
│
├── 🐍 scripts/                  ← 12 个 Python 脚本 + 3 个 JSON prompt 模板
│   ├── _lock.py / _send_lib.py  ← 共用库
│   ├── check_consistency.py     ← 14 段一致性护栏（A~H 段）
│   ├── skill_dispatcher.py      ← LLM 驱动型任务的 5d 数据抽取 + prompt 注入
│   ├── collect_{morning,evening}_data.py / send_{morning,close,evening,intraday,weekend,ipo}.py
│   ├── templates/{morning,evening,weekend}.json
│   ├── cron_jobs/{cron_mirror.json, README.md}
│   └── references/{config.json, fallback-chain-validation.md, weekend-4kb-budget.md}
│
└── 📚 knowledge/                ← changelog + 决策主题（**按需 skill_view 加载，不进默认 context**）
    ├── changelog/                ← 按版本号组织
    │   ├── README.md             ← 35 条 changelog 索引
    │   └── vX.Y.Z.md             ← 单版完整细节（v3.5.0 立，19 条新加）
    └── decisions/                ← 跨版本决策中心（按主题）
        ├── README.md
        ├── architecture.md       ← 架构演进
        ├── data-pitfalls.md      ← 数据源踩坑集
        ├── lessons-learned.md    ← 核心教训
        ├── guardrails.md         ← 护栏规则
        └── dispatcher-patterns.md
```

**knowledge/ 为什么保留在 publish 包但不进默认 context** (v3.4.4 改): `.clawhubignore` 排除后, **装上后无 knowledge/** — 用户需主动 `skill_view` 加载；本机开发保留完整 knowledge/ 不影响发布包大小。

---

## 版本历史（Changelog）

> **精简规则（v3.5.0 立）**：每条 ≤ 1 行索引，详细实战/根因/修法折到 `knowledge/changelog/vX.Y.Z.md`。完整 35 条索引见 [`knowledge/changelog/README.md`](knowledge/changelog/README.md)。
>
> **未发版段识别**：标题含 `(未发版)` 的是当前 v3.5.0 待 bump 的小改集合。

### v3.3.0 ~ v3.4.4（19 条，SKILL.md 主体）— 2026-06-11 晚 ~ 2026-06-16

- [v3.5.1 — send_evening_report.py 加 5 项内容质量硬校验](knowledge/changelog/v3.5.1.md) — 2026-06-18 晚（未发版）
- [v3.4.4 — 异常周（周二 cron）周末要闻端到端验证](knowledge/changelog/v3.4.4.md) — 2026-06-16（未发版）
- [v3.3.5+5 — fallback 链选 URL 原则：主题聚合页 > 单篇头条](knowledge/changelog/v3.3.5+5.md) — 2026-06-15 20:00 晚报（未发版）
- [v3.3.5+4 — web_search MCP 重试加固：覆盖 {"error": ...} 分支](knowledge/changelog/v3.3.5+4.md) — 2026-06-15 16:35（未发版）
- [v3.3.5+3 — 周末要闻 4 KB 截断修复 + 防幻觉 + 表格化 + H 段护栏](knowledge/changelog/v3.3.5+3.md) — 2026-06-15 下午（未发版）
- [v3.3.5+2 — 3 层 fallback 链 + 要闻段反例前置](knowledge/changelog/v3.3.5+2.md) — 2026-06-15 晨报（未发版）
- [v3.3.5+1 — 3 templates 加 batch_web_search 失败 fallback 机制](knowledge/changelog/v3.3.5+1.md) — 2026-06-13 晚（未发版）
- [v3.3.5 — 晨报渲染细节对齐 6/12 周五样本 + 删 v3.3.4 过头加固](knowledge/changelog/v3.3.5.md) — 2026-06-13 下午
- [v3.3.4 — 晨报过头加固（已废）](knowledge/changelog/v3.3.4.md) — 2026-06-13 凌晨
- [v3.3.3 — 尝试加固晨报，未生效，无代码变更](knowledge/changelog/v3.3.3.md) — 2026-06-12 晚
- [v3.3.2 — 模板约束一体化 + check 段 H 护栏](knowledge/changelog/v3.3.2.md) — 2026-06-12 晚
- [v3.3.1 — 晚报可读性修复：财经要闻 1 空行 + 依据 ≤ 50 字符](knowledge/changelog/v3.3.1.md) — 2026-06-11 深夜
- [v3.3.0 — 财经要闻段"任务定位"协议：防"盘面数据"冒充"要闻"](knowledge/changelog/v3.3.0.md) — 2026-06-11 晚
- [v3.2.9 — 3 个 dispatcher 任务 skills 字段清理](knowledge/changelog/v3.2.9.md) — 2026-06-11 下午
- [v3.2.8 — 收盘小结格式对齐：4 处拼接 bug](knowledge/changelog/v3.2.8.md) — 2026-06-11
- [v3.2.7 — .env 路径根除：8 脚本多路径回退](knowledge/changelog/v3.2.7.md) — 2026-06-10 下午
- [v3.2.6 — 双副本根除 + jobs.json 隐藏运行时副本修复](knowledge/changelog/v3.2.6.md) — 2026-06-10 上午
- [v3.2.5 — 盘中预警 cron prompt 纯 bash 化](knowledge/changelog/v3.2.5.md) — 2026-06-09 深夜
- [v3.2.4 — 文档补全：明示 knowledge/ 被 clawhub publish 上传](knowledge/changelog/v3.2.4.md) — 2026-06-09 晚
- [v3.2.3 — send_ipo_report.py 迁移到 _send_lib 共用库](knowledge/changelog/v3.2.3.md) — 2026-06-09 晚

### 历史版本（v3.2.2 ~ v3.0.0，11 条 + v2.0.0 ~ v2.0.10，11 条 = 22 条已折叠）

完整索引见 [`knowledge/changelog/README.md`](knowledge/changelog/README.md) —— `vX.Y.Z.md` 22 个详情文件保留。

### v3.5.0 改动（本版本 = SKILL.md 精简 + 14 段护栏加严，2026-06-16）

**触发**: SKILL.md 50665 字节 / 778 行 / 15 个 skill 排名第 1, 是第 2 名 ima-skill (16KB) 的 3.2 倍. Changelog 段 13KB 占 26.3%, 违反 v3.2.0 立"≤ 3 行 / 25 行硬上限"规矩.

**改法** (3 处):
1. Changelog 段 19 条 v3.3.0+ ~ v3.4.4 全部折到 `knowledge/changelog/vX.Y.Z.md` 详情文件, SKILL.md 留 1 行 / 条索引
2. `## 数据来源` (2.6KB) + `## IPO周报数据来源` (541B) 合并去重
3. `## 目录结构` (1.7KB) 简化, 标 knowledge/ 索引外置
4. frontmatter `version: 3.4.4` → `3.5.0` (按 MEMORY #12 "结构变更触发 v 大版本号讨论" 例外)

**未发版小改一并 bump 到 v3.5.0** (10 条): v3.3.5+1 ~ v3.3.5+5 + v3.4.4. 教训: "小改不刷 vX.Y.Z" 规则容易被滥用 (10 条小改 ≥ 2 个月), v3.5.0 立硬上限 — **未发版累积 ≥ 5 条必须下个结构变更 bump 走, 不许再攒**.

**MEMORY #12 立新约束**: 任何 skill 的 SKILL.md 单文件 > 30KB 必须先瘦身再发版.

## 安全配置（必读）

所有外部密钥均通过环境变量注入，**禁止硬编码**。路径可通过 `ENV_FILE` / `ENV_FILE_FALLBACK` 环境变量覆盖（默认从脚本自带 + 项目级 `_DEFAULT_ENV_PATH` 加载）。

### 密钥白名单原则

每个脚本**仅加载本任务实际需要的变量**，不得全量注入 `_DEFAULT_ENV_PATH` 所有密钥。

| 脚本 | 必需密钥（与 `_REQUIRED_KEYS` 同源，v3.2.7 修复）|
|------|---------|
| `collect_morning_data.py` | `IWENCAI_API_KEY`（A50 期货问财查询用）|
| `send_close_summary.py` | `WECOM_WEBHOOK_KEY`, `IWENCAI_API_KEY` |
| `collect_evening_data.py` | `WECOM_WEBHOOK_KEY` |
| `send_evening_report.py` | `WECOM_WEBHOOK_KEY`, `IWENCAI_API_KEY` |
| `send_morning_report.py` | `WECOM_WEBHOOK_KEY`, `IWENCAI_API_KEY` |
| `send_intraday_alert.py` | `WECOM_WEBHOOK_KEY` |
| `send_ipo_report.py` | `WECOM_WEBHOOK_KEY`, `IWENCAI_API_KEY` |
| `send_weekend_news.py` | `WECOM_WEBHOOK_KEY`, `IWENCAI_API_KEY` |

**问财 API 直连约定**（细节见 `## 数据来源` 段）：所有问财查询统一进程内直连 OpenAPI，**不使用 subprocess 外部调用**（避免通过 `IENV` 泄露环境变量给子进程）；消费侧必须兼容多字段名（同义词 nlp 翻译可能返回 `炸板家数` ↔ `涨停开板家数`）。

### 自动推送说明

配置 `WECOM_WEBHOOK_KEY` 即表示授权自动推送报告至企业微信。推送是自动化报告系统的组成部分，非人工干预。

| 密钥 | 环境变量 | 最小权限 | 来源 |
|------|---------|---------|------|
| 企业微信 Webhook | `WECOM_WEBHOOK_KEY` | 仅发送（只写） | 微信企业版 → 应用 → Webhook |
| 同花顺问财 API Key | `IWENCAI_API_KEY` | 只读查询 | 同花顺 i问财 SkillHub |

`.env` 文件格式示例：
```bash
WECOM_WEBHOOK_KEY=c4a1cd60-254e-4612-b365-c701482ae98c
IWENCAI_API_KEY=***
```

> **注意**：本 skill **只用 2 个 key**（WECOM + IWENCAI）。妙想 `MX_APIKEY` / Tushare `TUSHARE_TOKEN` 等由其他 skill（mx-data / mx-xuangu 等）使用，**不要加进 A-stock-report 的 `.env`**。

---

##快速开始

**手动跑一个报告（运维/补跑/测试用）：**

所有 6 个任务的完整命令（`source .env` + `python3 脚本路径` + 可选参数）都集中在 **`cron_jobs/cron_mirror.json` 的 `tasks.<name>.prompt` 字段**。

- LLM 驱动型（晨报/晚报/财经周末版）→ `templates/<task>.json` 的 prompt 模板 + `cron_jobs/cron_mirror.json`（无对应节点，由 jobs.json 直接调 dispatcher 注入）
- 独立脚本型（收盘小结/盘中预警/IPO 周报）→ `cron_jobs/cron_mirror.json#<task>` 节点

**手动跑通用模式：**

```bash
# 1. 读 cron_mirror.json 看 prompt 字段拿到完整命令
python3 -c "import json; print(json.load(open('/root/.hermes/skills/A-stock-report/cron_jobs/cron_mirror.json'))['tasks']['close_summary']['prompt'])"

# 2. 复制粘贴该命令到终端跑（已含 source .env + python3 路径 + 默认参数）
```

**历史命令备查（v3.1.5 清理前）：** 见 git log / 备份 `/workspace/archive/SKILL_md_pre_4segs_clean_*`

---

## 执行模式

**收盘小结、晚报、晨报** 采用不同模式：

- **收盘小结**：单一 Python 脚本，内置全部逻辑（取数 → 打分 → 生成报告 → 推送），cron 直接触发，无需 LLM 生成内容。
**晨报、晚报、周末要闻** 采用**两段式**：
- **第一段**（cron prompt）：调用 dispatcher 生成带真实日期的 prompt，写入约定路径
- **第二段**（同一 session）：读取 prompt 文件 → LLM 执行 → 写入内容文件 → 调用推送脚本

这样 SKILL.md 中的 prompt 模板只含通用占位符，日期在运行时由 dispatcher 动态注入。

---

## 数据来源

**总则**（v3.0+ 架构）：3 类数据源 + 4 端真相。

**3 类数据源**（按密钥需求划分）：
- **零密钥**：腾讯实时 API（`qt.gtimg.cn`） · 新浪 hq 数据（`hq.sinajs.cn`） · akshare 开源接口
- **IWENCAI_API_KEY**：同花顺 i 问财 OpenAPI（进程内直连，无 subprocess）
- 历史报告 MD（仅财经周末版用）：`/workspace/projects/A股报告系统/reports/`

**4 端真相**（防漂移，详见 `## 定时任务` 段）：`templates/` · `cron_jobs/cron_mirror.json` · `~/.hermes/cron/jobs.json` · `SKILL.md`

### 晨报数据来源（`collect_morning_data.py` + LLM 生成）

| 数据 | 来源 | 接口 / 字段 | 备注 |
|------|------|------------|------|
| 隔夜美股 3 大指数 | 腾讯实时 API | `qt.gtimg.cn/q=usDJI,usINX,usIXIC` | 字段含 name/price/pct |
| VIX 恐慌指数 | 新浪 hq 数据 | `hq.sinajs.cn/list=znb_VIX` | paperCode=znb_VIX，CBOE VIX 指数本身（13 字段：现价/涨跌/52 周范围）⚠️ 2026-06 新浪反爬升级：`User-Agent: Mozilla/5.0` 太短被识别为爬虫 → 403；**必须用完整浏览器 UA 字符串**（详见 `~/.hermes/skills/devops/sina-hq-sinajs-403-ua/SKILL.md`）|
| 富时 A50 期货 | 新浪 hq 数据 | `hq.sinajs.cn/list=...A50ETF`（512550） | 偶发 HTTP 403（同 UA 原因），失败回退华夏 A50ETF；缺失按 v3.1.3 协议 `❌ 数据缺失` 占位 |
| 港股恒生指数 | 腾讯实时 API | `qt.gtimg.cn/q=hkHSI` | 复用 get_us_indices 模式 |
| WTI 原油 + 现货黄金 | akshare 全球期货现货 | `ak.futures.futures_hf_em.futures_global_spot_em()` | GC00Y=COMEX 黄金 / CL00Y=WTI |

### 收盘小结数据来源（`send_close_summary.py` 独立脚本）

| 数据 | 来源 | 接口 |
|------|------|------|
| 6 大指数 + 成交额 | 腾讯实时 + akshare | `qt.gtimg.cn` + `stock_zh_a_spot_em()` |
| 涨跌停家数 / 炸板率 | 同花顺问财 | 1 次查询（`今日涨停家数 跌停家数 炸板家数`） |
| 全市场主力净流入 | 东方财富 RPT_MARKET_CAPITALFLOW | `INDEX_CODE="800000.EI"`，`BONDTYPE="A股"` |
| 行业板块涨跌 / 主力资金 | hithink-sector-selector | `今日行业板块涨幅前10` / `近5日主力净流入前10行业板块` |
| IF 期货基差 | 新浪 nf_IF0（今日优先）+ akshare `futures_main_sina` 兜底 | `hq.sinajs.cn` |

### 晚报数据来源（`collect_evening_data.py` + LLM 生成）

| 数据 | 来源 | 接口 |
|------|------|------|
| 6 大指数 + 成交额 | 同收盘小结 | 同上 |
| 亚太股市（日经/韩国综合） | 腾讯实时 | `qt.gtimg.cn` |
| 两融余额 / 两融交易额 | AKShare | `macro_china_market_margin_sh/sz` |
| 沪深300 PE / 股市风险溢价 | 同花顺问财 | 单次查询多字段 |
| 涨跌停家数 | 同花顺问财 | 复用收盘小结模式 |

### IPO 周报数据来源（`send_ipo_report.py`）

| 报告模块 | 接口 | 来源 |
|---------|------|------|
| 一、排队情况 | `ak.stock_register_kcb/cyb/bj/sh/sz` | 东方财富注册制审核公示 |
| 二、本周期上会 | `ak.stock_ipo_review_em` | 东方财富 IPO 审核动态 |
| 三、本周期获批 + 四、终止撤回 | `ak.stock_ipo_declare_em` | 证监会公示 |
| 五、下周期上会 | `ak.stock_ipo_review_em` | 东方财富 IPO 审核动态 |
| 六、新股上市 | `ak.stock_xgsr_ths` | **同花顺**（一次调用含上市信息/发行价/首日涨跌幅） |

### 财经周末版数据来源

**仅复用历史报告 MD**（无新数据采集）：`/workspace/projects/A股报告系统/reports/收盘小结_YYYYMMDD.md`（情绪打分/涨停家数）+ `晚报_YYYYMMDD.md`（两融/PE/ERP）。两套以交易日 key 对齐合并，详见下表：

| 指标 | 来源 MD | key 取法 |
|------|--------|---------|
| 涨停家数 / 情绪打分 | `收盘小结_YYYYMMDD.md` | 文件名 `YYYYMMDD` |
| 两融余额 / 两融比例 | `晚报_YYYYMMDD.md` | 报告内两融余额行日期 |

### 问财 API 兼容性约定

**坑 1 — 字段名同义词（2026-06-01 经验）**：问财 OpenAPI 在 query 含同义词时 nlp 翻译可能返回**不同字段名**（如 `炸板家数` ↔ `涨停开板家数`）。**消费侧必须兼容多字段名**，避免单一字段名失效导致数据缺失。已修复 `send_close_summary.py:167`（兼容 `炸板家数` / `涨停开板家数`）。未来遇到新同义词：在所有调用问财的脚本里加兼容分支，记到此节。

**坑 2 — 返回值类型不稳定（2026-06-16 经验，send_close_summary.py:78）**：

问财同一字段可能**不同时刻返回不同类型**——同一 query，今天返 `float`、明天返 `str`、后天返 `int`（nlp 翻译后端不稳定）。直接 `v > 0` 比较会在 str/int/str 互换时炸：

```python
# ❌ 错误写法 — TypeError: '>' not supported between instances of 'str' and 'int'
if "成交额" in k and v and v > 0:
    val_yi = float(v) / 1e8
```

**正确写法** — 三重防御：

```python
if "成交额" in k and v not in (None, "", 0, "0", "0.0"):
    try:
        v_num = float(v)        # 统一强转
    except (TypeError, ValueError):
        continue                # 转换失败跳过，不让一个坏字段拖垮整次查询
    if v_num > 0:               # 数值化后再比较
        val_yi = v_num / 1e8
        return v_num
```

**症状**：脚本异常分支 `'>' not supported between instances of 'str' and 'int'` → fallthrough 到兜底 → 兜底值 0 → 报告显示 `全市场成交额：0亿`。

**检测套路**（写消费代码时）：
- 任何 iwencai 字段的 `if v > 0` / `if v < x` / `if v == y` 都视为**潜在 bug**
- 修法模板：`v not in (None, "", 0) → try float(v) → 转换失败 continue → 数值比较`

**已修样本**：`send_close_summary.py:78` (commit `pre_20260616_turnover_typecompare.bak`)

---

## 文件名日期规则

| 报告 | 文件名日期取值 |
|------|--------------|
| 收盘小结 | `--date` 参数值；无参数则取当天 |
| 晚报 | `--date` 参数值；无参数则取当天 |
| 晨报 | 生成当天 |
| 财经周末要闻 | 生成当天 |

> **注意**：晚报内容里的两融余额标注日期（如"两融余额（04月13日）"）是数据对应的上一交易日，与文件名日期可能差1天。

---

## 周末要闻情绪轨迹数据来源

一周情绪轨迹从历史报告MD文件中提取，合并规则：

| 指标 | 来源 | key取法 |
|------|------|--------|
| 涨停家数/情绪打分 | 收盘小结 `收盘小结_YYYYMMDD.md` | 从文件名提取 `YYYYMMDD` |
| 两融余额/两融比例 | 晚报 `晚报_YYYYMMDD.md` | 从**报告内容**里两融余额行提取日期作为 key |

两套数据以交易日 key 对齐合并，保证周一到周五趋势线一致。

---

## 防并发锁

各脚本使用独立的锁文件，同时运行互不干扰：

| 脚本 | 锁文件 |
|------|--------|
| `send_close_summary.py` | `/tmp/a_stock_close_summary.lock` |
| `send_evening_report.py` | `/tmp/a_stock_evening.lock` |
| `send_morning_report.py` | `/tmp/a_stock_morning.lock` |
| `send_weekend_news.py` | `/tmp/a_stock_weekend.lock` |
| `send_ipo_report.py` | `/tmp/a_stock_ipo.lock` |
| `send_intraday_alert.py` | `/tmp/a_stock_intraday.lock` |

**锁残留检测（v2.0.1 起）：** 脚本有 `finally: _unlock()` 兜底，正常退出一定会释放。**若锁文件残留**：
1. 排查推送阶段异常日志（`wx()` 返回非 0 / 信号中断 / 网络超时）
2. 确认无进程在跑（`ps -ef | grep send_close`）后，手动 `rm /tmp/a_stock_close_summary.lock`
3. 残留超过 1 小时不重跑需要介入，避免重复推送

---

## 报告模板

### 晨报

```
📰 【股市晨报】YYYY年MM月DD日（周X）

━━━ 隔夜全球市场 ━━━
【美股收盘】
▪ 道琼斯：XXXXX.XX点，+X.XX%（精确数字，不得用"约"）
▪ 标普500：XXXXX.XX点，+X.XX%
▪ 纳斯达克：XXXXX.XX点，+X.XX%（可附"X连涨/连跌X日"）
▪ VIX恐慌指数：XX.XX（+X.XX%），恐慌等级：【低位(<20)/中位(20-30)/高位(>30)】

【港股及A50】
▪ 恒生指数：XXXXX.XX点，+X.XX%（附简要背景）
▪ 富时A50期货：XXXXX点，+X.XX%，偏强/偏弱运行【预判A股明日开盘】

【大宗商品】
▪ WTI原油：XXX.XX美元/桶，+X.XX%（精确数字，不得用"约"）
▪ 现货黄金：XXXX.XX美元/盎司，+X.XX%（精确数字）

━━━ 财经要闻 ━━━
【1】（标题）｜✅利好/❌利空/⚠️中性 对A股影响
  点评：（简洁分析，≤50字）
【2】（标题）｜✅利好/❌利空/⚠️中性 对A股影响
  点评：（≤50字）
（**≤7条**，顺序编号，每条格式固定：
  【编号】（标题）｜✅/❌/⚠️标签 对A股影响
  点评：（事件+分析，≤50字））

━━━ 今日操作建议 ━━━
【大盘研判】
（综合外围市场、宏观政策、量能等因素，给出2-3句综合判断）

【操作建议】
1. 【板块/策略】（期限）：具体建议+附标的
2. 【板块/策略】（期限）：...

【风险提示】
⚠️ （1-3条，最重要的风险）

⚠️ 仅供参考，不构成投资建议。股市有风险，投资需谨慎。
```

### 收盘小结

> **模板由 `send_close_summary.py` 脚本内置拼装**（`build_report()` 函数 f-string，L562+）—— SKILL.md 不再重复维护。改格式请直接改脚本。
>
> **协议说明**：
> - 6 段固定框架：①主要股指表现 ②板块行情 ③全市场主力资金 ④行业主力资金流 ⑤量化情绪打分 ⑥后市展望 + 数据来源落款
> - 量化情绪打分（满分 100，6 因子等权平均）：
>   - 涨停家数（10~100 家映射）
>   - 涨跌停比（对数插值）
>   - 炸板率（40%~10% 映射，越低越好）
>   - 主力净流入占比（-5%~+5% 映射）
>   - 全市场换手率（1%~4% 映射）
>   - IF 基差（-300~+150 点映射）
> - 后市展望默认文本（脚本 L560）："市场震荡调整，风格偏向题材与成长，建议控制仓位、关注轮动节奏。"

### 晚报

```
📋 【A股晚报】YYYY年MM月DD日

━━━ A股收盘 ━━━
• 上证指数：XXXX.X，↑/↓X.XX%
• 深证成指：XXXX.X，↑/↓X.XX%
• 创业板指：XXXX.X，↑/↓X.XX%
• 科创50：XXXX.X，↑/↓X.XX%
• 沪深300：XXXX.X，↑/↓X.XX%
• 中证500：XXXX.X，↑/↓X.XX%
• 成交额：X.XX万亿元

━━━ 亚太股市 ━━━
• 恒生指数：XXXX，↑/↓X.XX%
• 日经225：XXXXX，↑/↓X.XX%
• 韩国综合：XXXX，↑/↓X.XX%

━━━ 市场风险偏好 ━━━
• 两融余额（MM月DD日）：XXXXX亿，较前日+/-XXXX亿
• 两融余额/A股流通市值（MM月DD日）= X.XX%
  阈值：<3%安全 | 3-3.5%预警 | ≥3.5%高危
• 两融交易额/A股成交额（MM月DD日）= X.X%
  阈值：<7%保守 | 7-11%中性 | >11%过热
• 股市风险溢价（MM月DD日）= X.XX%
  阈值：<3%高估 | 3-6%中性 |>6%低估
• 沪深300 PE = XX.XX，近5年分位点 XX.X%

━━━ 财经要闻 ━━━
【1】（标题）｜✅利好/❌利空/⚠️中性 对A股影响
  点评：（≤50字）
【2】...（**≤7条**，每条格式固定，点评≤50字）

━━━ 今日操作建议 ━━━
【大盘研判】（2-3句）
【操作建议】
1. 【板块/策略】（期限）：具体建议
2. 【板块/策略】（期限）：...
【风险提示】（1-3条）

⚠️ 仅供参考，不构成投资建议。股市有风险，投资需谨慎。
```

### 财经周末版（cron 触发后 LLM 生成）

```
📰 【财经周末版】{周六日期} + {周日日期}

━━━ 一周情绪轨迹（5 个交易日，来源：收盘小结 + 晚报）━━━

【1. 市场短期情绪】
• 量化情绪打分：周一XX → 周二XX → 周三XX → 周四XX → 周五XX

【2. 杠杆率】
• 两融余额（亿元）：周一X → 周二X → ... → 周五X
• 两融余额占流通市值比例：周一X.XX% → ... → 周五X.XX%

【3. 估值水平】
• 沪深300PE：周一X.XX → ... → 周五X.XX
• 近5年分位点：周一X.X% → ... → 周五X.X%
• 股市风险溢价（ERP）：周一X.XX% → ... → 周五X.XX%

【4. 市场预期】
• IF基差：周一X.XX → ... → 周五X.XX

【5. 一周市场解读】
{不超过50字，综合市场情绪/杠杆/估值/预期 4 个维度的一句话总结}

━━━ 数据规则（防错）━━━
数据源 + ❌/⚠️ 硬约束在模板顶部"2. 数据源"段统一定义（v3.3.0 + v3.1.3 合并版），不在此处重复

━━━ 整体市场情绪研判 ━━━
情绪指标总结 | 核心驱动因素 | 当前风险点 | 下周操作参考

⚠️ 仅供参考，不构成投资建议。
```

---

## 定时任务（cron）

7 个 cron 任务（A 股 6 任务 + 每周 Skill 复盘 1 任务）的完整 schedule / repeat / deliver / prompt 字段集中在以下两处真相源：

- **生产配置（OpenClaw 读）**：`~/.hermes/cron/jobs.json`
- **人类可读镜像（git track）**：`cron_jobs/cron_mirror.json`

**SKILL.md 不再重复列 cron 表达式**（v3.1.5 清理）—— 一处变→多处忘改是 v3.0 之前的痛点。

**快速概览：**

| 任务 | 调度 | 类型 |
|------|------|------|
| A股晨报生成并推送 | 周一至五 08:00 | LLM 驱动型（template: `templates/morning.json`） |
| A股晚报生成并推送 | 周一至五 20:00 | LLM 驱动型（template: `templates/evening.json`） |
| A股收盘小结 | 周一至五 15:30 | 独立脚本（mirror: `close_summary`） |
| A股盘中预警 | 周一至五 09:00-14:55 每 5 分钟 | 独立脚本（mirror: `intraday`） |
| A股周末要闻生成并推送 | 周日 20:00 | LLM 驱动型（template: `templates/weekend.json`） |
| 每周 Skill 复盘 | 周日 18:00 | skill 自审 |
| A股IPO周报 | 周六 10:00 | 独立脚本（mirror: `ipo_report`） |

---


## 安装与验证

配置完 cron 后，按以下顺序逐一检查：

### Step 1：密钥检查

权威密钥白名单表在 `## 密钥白名单原则` 段（每个脚本需哪些 env 变量）。

**快速检查 2 个 env 变量是否就位：**

```bash
# 应输出 2 行非空（本 skill 只需 2 个 key）
for key in WECOM_WEBHOOK_KEY IWENCAI_API_KEY; do
  grep "^${key}=" /workspace/.env && echo "  ✅ $key"
done
```

**未配齐会怎样：** 脚本在 except 块内捕获缺失，会 `notify_failure()` 发预警 + exit 1（v3.1.0 修复链），不会静默继续。

> **注意**：`send_evening_report.py` 的"财经要闻"和"明日操作建议"两个区块**依赖 cron 中的 LLM 步骤生成**，不是脚本自己能产出的。若未配置对应 cron task，这两个区块**永远为空**，这是设计预期，不是 bug。

### Step 2：依赖检查

```bash
# 检查 akshare
python3 -c "import akshare; print('akshare', akshare.__version__)"

# 检查 tushare（IPO周报需要）
python3 -c "import tushare; print('tushare OK')"

# 检查 hithink-sector-selector CLI
python3 /workspace/skills/hithink-sector-selector/scripts/cli.py --help | head -3
```

### Step 3：Cron 任务检查

跑护栏脚本一次性验证 4 端一致性（templates ↔ cron_mirror ↔ jobs.json ↔ SKILL.md）：

```bash
python3 /root/.hermes/skills/A-stock-report/scripts/check_consistency.py
# 预期：✅ 全部 4/4 项通过，exit=0
```

**不要再用"❌手对表"逐行核对**——v3.1.5 之前 SKILL.md 这里有 7 行"应存在 ✅"表，靠人记得跑 1 个命令 + 7 行眼睛对——v3.1.5 改用护栏脚本机械检查，杜绝漂移。


---

## Cron 任务配置指引

6 个任务分两类：

- **LLM 驱动型（3 个）**：晨报 / 晚报 / 财经周末版 — prompt 外置于 `templates/`，由 `scripts/skill_dispatcher.py` 读取注入 LLM，LLM 解读后调脚本落地推送。
- **独立脚本型（3 个）**：收盘小结 / **盘中预警** / IPO 周报 — 无需 LLM，调度配置外置于 `cron_jobs/`，由 OpenClaw gateway 直接 `source .env && python3 ...` 跑脚本。盘中预警为每 5 分钟一次高频任务（必须无 LLM 介入）。

> **为什么用文件中转（LLM 型）？** cron prompt 在独立 session 运行，无法直接将变量传给后续脚本。通过写入约定路径的文件，脚本读取后注入报告模板，实现解耦。

> **🛡️ 4 端一致性护栏（v3.1.5+）**：本 skill 有 4 端真相 — `templates/`（LLM 调度模板，机器读） / `cron_jobs/cron_mirror.json`（生产 cron 镜像，人读） / `~/.hermes/cron/jobs.json`（生产 cron 真实配置，OpenClaw 读） / `SKILL.md`（文档）。改任何一端都可能造成幽灵模板（v3.1.3 的教训）。**修改以下任一文件后必须跑 `python3 scripts/check_consistency.py`**（exit 0=全过，exit 1=有错误）：
> - `templates/*.json`（3 个 LLM 任务 prompt）
> - `cron_jobs/cron_mirror.json`（3 个独立脚本任务）
> - `~/.hermes/cron/jobs.json` 中 3 个独立脚本任务的 prompt
> - SKILL.md 任务清单段（`### N. 任务名（详见 ...）` 格式）
>
| 报错时用 `--fix-hint` 看修复建议。脚本会检查 A) templates ↔ dispatcher 任务集、B) cron_mirror ↔ jobs.json prompt 字字一致、C) SKILL.md 引用真实存在、D) dispatcher 任务不在 mirror 出现、E) SKILL.md 主体无硬编码 cron 表达式 / .env 路径 / source+send 一行命令（v3.1.6+ E 段）。

### 1. 晨报（详见 templates/morning.json）

> Prompt 模板外置于 `templates/morning.json`（v3.0 架构），由 `scripts/skill_dispatcher.py` 读取并注入。

### 2. 收盘小结（详见 cron_jobs/cron_mirror.json#close_summary）

> 独立脚本模式 —— 无需 LLM，调度配置外置于 `cron_jobs/cron_mirror.json`（v3.0 架构；v3.1.4 起 3 任务合为单文件，close_summary 为 `tasks.close_summary` 节点），由 OpenClaw gateway 直接读取。脚本路径见 json 内 `prompt` 字段。

### 3. 晚报（详见 templates/evening.json）

> Prompt 模板外置于 `templates/evening.json`（v3.0 架构），由 `scripts/skill_dispatcher.py` 读取并注入。

### 4. 盘中预警（详见 cron_jobs/cron_mirror.json#intraday）

> 独立脚本模式 —— 无需 LLM，调度配置外置于 `cron_jobs/cron_mirror.json`（v3.0 架构；v3.1.4 起 3 任务合为单文件，intraday 为 `tasks.intraday` 节点），由 OpenClaw gateway 直接读取。脚本路径见 json 内 `prompt` 字段。**v3.1.3 之前该任务的模板曾错误地放在 `templates/intraday.json`（LLM 驱动型设计），但实际 cron 早已是独立脚本模式**；v3.1.3 已删除幽灵模板、归档到 cron_jobs/。

### 5. 财经周末版（详见 templates/weekend.json）

> Prompt 模板外置于 `templates/weekend.json`（v3.0 架构），由 `scripts/skill_dispatcher.py` 读取并注入。

### 6. IPO周报（详见 cron_jobs/cron_mirror.json#ipo_report）

> 独立脚本模式 —— 无需 LLM，调度配置外置于 `cron_jobs/cron_mirror.json`（v3.0 架构；v3.1.4 起 3 任务合为单文件，ipo_report 为 `tasks.ipo_report` 节点），由 OpenClaw gateway 直接读取。脚本路径见 json 内 `prompt` 字段。

### 验证 3：端到端 cron 验证

实际 cron 跑过后，检查：
1. 推送消息中"财经要闻"和"明日操作建议"区块是否有内容
2. 内容日期是否与当天日期一致
3. 报告文件名是否为当天日期

若发现为空，回到"验证 2"确认内容文件是否成功写入。

## 常见问题

**Q1：生成后如何做质量检查？**
A：生成报告后必须检查以下四项：
1. **日期检查**：报告第一行日期 == 文件名日期 == 当天实际日期（三者必须一致）
2. **星期检查**：报告中的日期字符串（`YYYY年MM月DD日（周X）`）与文件名中的日期 `weekday()` 对应周一～周五正确
3. **数据完整性**：
   - 收盘小结：指数行情、情绪打分、板块资金流、风险偏好、操作建议五段落齐全
   - 晨报/晚报：涨跌停统计、风险偏好、操作建议三段落齐全
4. **时效性**：数据陈旧（>2个交易日）时在报告内注明

**Q2：如何判断涨停情绪？**
A：涨停情绪由第4节打分函数统一评分（满仓风险系数 × 涨停家数权重 + 涨跌停比 × 炸板率综合得出 0-100 分），不再单独使用 emoji 分级。报告生成后通过"质量检查第3项"确认段落齐全即可。
- 参考：情绪总分 ≥ 70 → 🟢做多；≥ 55 → 🟡偏多；≥ 40 → ⚪分歧；≥ 25 → 🟠偏空；< 25 → 🔴冰点

**Q3：炸板率如何评分？**
A：炸板率由第4节打分函数中的 `_sc(exp_rate, 40, 10)` 公式映射到 0-100 分，阈值区间 [40%, 10%]，炸板率越低得分越高。
- 参考：情绪总分 ≥ 70 → 🟢做多；≥ 55 → 🟡偏多；≥ 40 → ⚪分歧；≥ 25 → 🟠偏空；< 25 → 🔴冰点

**Q4：两融数据比当天少一天？**
A：正常现象。两融数据在当天收盘后约 1～2 小时后更新，晚报/收盘小结取到的是上一交易日数据。

**Q5：主力净流入 > 500亿时显示什么？**
A：打印预警信息 `⚠️ 主力净流出-XXX亿，超大单+大单砸盘XXX亿，异常大额出逃，注意风险`，但保留真实数值（不重置为0）。

**Q6：定时任务重复推送？**
A：已内置文件锁机制的脚本会拒绝并发执行。当前各脚本锁机制如下：
- 晚报：`send_evening_report.py` → `/tmp/a_stock_evening.lock`（exists 检测 + sys.exit(0)，finally 解锁）
- 盘中预警：`send_intraday_alert.py` → `/tmp/a_stock_intraday.lock`（同上）
- 周末要闻：`send_weekend_news.py` → `/tmp/a_stock_weekend.lock`（同上）
- IPO周报：`send_ipo_report.py` → `/tmp/a_stock_ipo.lock`（原子 os.O_EXCL 创建，更严格，finally 解锁）
- 晨报：`send_morning_report.py` → `/root/.hermes/skills/A-stock-report/scripts/.morning_report_lock.json`（JSON 文件，内容含 `date` 和 `status`，检查当日是否已成功推送后才允许重复执行）

**Q7：报告内容日期和文件名不对应？**
A：收盘小结文件名=报告日期；晚报文件名=生成当天日期，内容日期=上一交易日；周末要闻以内容里两融余额标注的日期为 key，与收盘小结文件名日期对齐合并。

**Q8：如何使用 `--date` 指定历史日期？**
A：收盘小结和晚报均支持 `--date YYYY-MM-DD`，如 `python3 send_close_summary.py --date 2026-04-13`。晨报不支持指定历史日期。
