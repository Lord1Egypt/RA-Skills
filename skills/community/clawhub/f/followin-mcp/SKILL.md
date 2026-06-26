---
name: followin-mcp
description: Followin MCP 相关子 Skill 的索引与入口。在需要路由到情报/舆情/策略/宏观/美股等能力时，先读本文件再打开 references 下对应 *.SKILL.md。
metadata:
  {
    "openclaw":
      {
        "emoji": "🧩",
        "os": ["darwin", "linux", "win32"],
        "requires": { "bins": [] },
        "install": [],
        "version": "1.0.0"
      }
  }
---

# Followin MCP — 子 Skill 索引

本目录的 **`references/`** 下包含 **13** 个独立 Skill 文件（`*.SKILL.md`），每个文件自带 YAML `name` / `description`、`metadata`，以及 **「本 Skill 与 MCP 工具映射」**（含 `followin-mcp` / `premium-mcp` SSE 配置片段）。  
**实现具体任务时**：根据用户意图选中下表中的文件，**完整阅读该文件正文**，再按其中的工具名与路由规则调用 MCP。

打包与目录结构说明见 **`references/README.md`**。

---

## 按主题分组

### 情报与舆情（加密）

| 文件 | Skill 名 | 用途概要 |
|------|----------|----------|
| [references/01-followin-intel-center.SKILL.md](references/01-followin-intel-center.SKILL.md) | `followin-intel-center` | 代币解锁、宏观数据、上币下架、项目事件、量价异动、资金费率等「情报中心」聚合频道。 |
| [references/02-breaking-news.SKILL.md](references/02-breaking-news.SKILL.md) | `breaking-news` | 针对单条加密新闻/事件，分析受影响标的与多空倾向；正文以分析流程为主，**无固定 MCP 工具**。 |
| [references/03-trending-news-topics.SKILL.md](references/03-trending-news-topics.SKILL.md) | `trending-news-topics` | 「今天发生什么、什么最热」类热点舆情；关注事件与话题，非单币深度。 |
| [references/04-crypto-daily-brief.SKILL.md](references/04-crypto-daily-brief.SKILL.md) | `crypto-daily-brief` | 加密市场**日报/早报**（触发词如日报、加密日报）；**宏观/美股早报**不归本 Skill。 |
| [references/05-token-buzz-views.SKILL.md](references/05-token-buzz-views.SKILL.md) | `token-buzz-views` | **指定具体代币**后的新闻、深度、KOL、社群观点聚合。 |

### 交易与社群信号

| 文件 | Skill 名 | 用途概要 |
|------|----------|----------|
| [references/06-trading-strategy-signal.SKILL.md](references/06-trading-strategy-signal.SKILL.md) | `trading-strategy-signal` | 顶级交易员实盘、KOL 喊单等交叉验证；模糊「市场/KOL 怎么看」及**所有 KOL 喊单类**查询默认归本 Skill；**不含资金费率**。 |
| [references/07-tg-channel-intel.SKILL.md](references/07-tg-channel-intel.SKILL.md) | `tg-channel-intel` | Telegram 频道话题、共识与分歧；可按偏好筛选频道。 |

### 宏观看盘与早报

| 文件 | Skill 名 | 用途概要 |
|------|----------|----------|
| [references/08-btc-macro-dashboard.SKILL.md](references/08-btc-macro-dashboard.SKILL.md) | `btc-macro-dashboard` | BTC 宏观环境 **0–100 评分**与分层解读（如「BTC 宏观怎么样」）。 |
| [references/09-gold-macro-dashboard.SKILL.md](references/09-gold-macro-dashboard.SKILL.md) | `gold-macro-dashboard` | 黄金宏观环境 **0–100 评分**与分层解读。 |
| [references/10-macro-morning-brief.SKILL.md](references/10-macro-morning-brief.SKILL.md) | `macro-morning-brief` | **宏观/美股维度**晨间简报（触发词含宏观日报、美股早报、morning brief 等）；纯「加密日报」走 `crypto-daily-brief`。 |

### 美股与宏观分析

| 文件 | Skill 名 | 用途概要 |
|------|----------|----------|
| [references/11-us-stock-earnings-report.SKILL.md](references/11-us-stock-earnings-report.SKILL.md) | `us-stock-earnings-report` | **单股**财报三维分析（须指定代码或公司名）；泛问「今天有哪些财报」走情报中心。 |
| [references/12-macro-analyzer.SKILL.md](references/12-macro-analyzer.SKILL.md) | `macro-analyzer` | 宏观指标 **影响/解读**（须同时有指标名 + 影响类意图）；纯数据查询走情报中心，综合晨报走 `macro-morning-brief`，BTC/黄金盘面走对应 dashboard。 |
| [references/13-us-stock-divergence-scan.SKILL.md](references/13-us-stock-divergence-scan.SKILL.md) | `us-stock-divergence-scan` | 价格、媒体与内部人交易等**背离/静默异动**扫描；泛问异常走热点舆情，个股异动规则见各 Skill 边界说明。 |

---

## 快速路由（与其它 Skill 的边界）

- **「加密日报」** → `04-crypto-daily-brief`；**「宏观/美股早报、morning brief」** → `10-macro-morning-brief`。
- **「今天有什么热点/消息」** → `03-trending-news-topics`；**「某代币新闻/KOL 观点」** → `05-token-buzz-views`（须点名代币）。
- **「KOL 喊单 / 交易员实盘」** → `06-trading-strategy-signal`；**资金费率/解锁/上币等频道情报** → `01-followin-intel-center`。
- **「BTC 或黄金宏观打分」** → `08` / `09`；**「某宏观指标对市场的影响」** → `12-macro-analyzer`。
- 各文件 **description** 与正文中的 **不得路由到其它 Skill** 说明具有最高优先级；冲突时以**目标 Skill 全文**为准。

---

## 使用方式（给 Agent）

1. 根据用户问题在上表中定位 **一个** 主 Skill 文件。  
2. 打开对应 `references/*.SKILL.md`，遵循其 **MCP 配置**与 **工具映射表**。  
3. 需要并列能力时（例如情报中心 + 单币舆情），分别打开多个文件，注意各 Skill 声明的互斥路由。
