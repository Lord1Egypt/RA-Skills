---
title: "A股(机构主力)股指期货持仓统计-中金所"
summary: "从中金所官网下载并解析会员持仓排名 XML，按“中信期货(代客)”与“全市场前20名会员合并”两维度统计股指期货(IF/IH/IC/IM)绝对持仓与净增对比，生成 HTML 报告。固化了 datatypeid 的正确字段映射与官方的“比上交易日增减”净增口径，规避把套利当多单的经典错误。"
description: "当用户需要从中金所(cffex.com.cn)获取股指期货(IF/IH/IC/IM)席位持仓、统计机构净多空、计算净增对比、分析主力席位动向、或自动生成每日持仓统计报告/邮件时使用。关键修正：datatypeid=1 是持买单量(多单)、=2 是持卖单量(空单)、=0 是套利(不计入多空净持仓)；净增对比使用官方 varvolume(比上交易日增减)字段直接求和，而非“当日−前日”自行相减。"
version: "1.0.0"
author: "FangXing"
tags: ["A股", "股指期货", "中金所", "持仓排名", "机构主力", "中信期货", "量化", "金融数据"]
category: "finance"
license: "MIT"
homepage: ""
---

# A股(机构主力)股指期货持仓统计 · 中金所

从中金所官网解析会员持仓排名，自动下载当日数据并生成两维度（**中信期货(代客)** / **全市场前20名会员合并**）的绝对持仓与净增对比报告。

## 一、适用场景（触发条件）

- 想看某日股指期货主力席位（尤其中信期货）的多空持仓与净增变化
- 需要逐品种（IF/IH/IC/IM）统计机构净多空、分析主力意图
- 要生成每日持仓统计报告（HTML）或定时发邮件复盘
- 自然语言举例：「统计今日股指持仓」「跑一下中信期货(代客)净增对比」「对比 8/10 和 8/7 的股指持仓」

## 二、被调用时的执行流程

1. **运行统计脚本**（自动下载当日数据 + 对比前一交易日 + 正确口径出报告）：
   ```
   python3 ~/.workbuddy/skills/ashare-if-cffex-position/if_netchange.py
   ```
   - 指定日期对比：`...if_netchange.py 20260810 20260807`
   - 静默只出报告：`...if_netchange.py --quiet`
2. **校验关键数**：中信期货(代客) 中证500 多单净增须 = **−2,932**（IC2608 219 − IC2609 2,422 − IC2612 774 + IC2703 45）。若不符，说明 datatypeid 映射又搞反了，立即回头查第三节映射表，不要将就输出。
3. **呈现结果**：用 `present_files` 打开生成的 `股指期货持仓统计_YYYYMMDD.html`（自动预览 + 卡片）。
4. **不发邮件**：本 skill 只出报告。若要发邮件，需用户单独说明收件人，走 agent-mail（触发确认闸门，用户确认后重发）。

## 三、⚠️ 最关键：datatypeid 正确映射（极易搞反）

中金所持仓排名 XML 每个 `<data>` 条目含 `datatypeid` 字段，真实含义（已与用户逐笔核对验证）：

| datatypeid | 含义 | 是否计入多空净持仓 |
|---|---|---|
| **1** | 持买单量（**多单**） | ✅ 计入 |
| **2** | 持卖单量（**空单**） | ✅ 计入 |
| **0** | 套利 | ❌ 排除 |

> 历史上曾误把 `0` 当持买、`1` 当套利，导致“多单”栏取成套利数据（已因此发错邮件）。**务必遵守上表，这是本技能存在的核心价值。**

## 四、数据字段说明

每个 `<data>` 条目关键字段：
- `partyid`：会员席位码（中信期货 = 0018）
- `shortname`：席位名称（中信期货全部为“中信期货(代客)”，无自营行；**建议按 `shortname` 含“中信期货(代客)”精确过滤**，而非仅按 partyid）
- `instrumentid`：合约代码（如 IC2608 / 2609 / 2612 / 2703）
- `datatypeid`：见第三节映射表
- `volume`：当日持仓量（**绝对持仓**用此字段）
- `varvolume`：**比上交易日增减**（官方净增字段；**净增对比**用此字段直接求和，比“当日−前日”更准——因已计入合约上市/退市、会员进出前20名等边界）

## 五、下载地址与校验

```
http://www.cffex.com.cn/sj/ccpm/YYYYMM/DD/PRODUCT.xml
```
- PRODUCT ∈ {IF, IH, IC, IM}
- 需带 `User-Agent` + `Referer`(`http://www.cffex.com.cn/cn/ccpm.html`)，URL 加随机 `?id=` 防缓存
- 校验：返回内容前 600 字节含 `<positionRank` 才为有效持仓 XML（否则可能 404/空）

## 六、算法（用户确认口径，已固化在脚本中）

```
多单净增   = Σ_各品种 (该品种持买单量 dt1 的 varvolume)   # 各合约“比上交易日增减”直接相加
空单净增   = Σ_各品种 (该品种持卖单量 dt2 的 varvolume)
净多空     = 多单净增 − 空单净增
绝对持仓   = Σ_各合约 (volume)，其中 dt1=多单、dt2=空单、dt0=套利排除
中信维度   = 仅 shortname 含“中信期货(代客)”的条目（精确匹配）
```

## 七、内置脚本（自包含、可携带、零依赖）

技能目录下已内置 **`if_netchange.py`**（与 SKILL.md 同级），纯 Python 标准库、无第三方依赖；下载缓存自动建在脚本同级 `cache/` 下，可随处拷贝运行。

```
# 本机（WorkBuddy 托管 Python，推荐）
python3 ~/.workbuddy/skills/ashare-if-cffex-position/if_netchange.py

# 任意机器（只要有 Python 3）
python3 ~/.workbuddy/skills/ashare-if-cffex-position/if_netchange.py
```
- 指定日期：`...if_netchange.py 20260810 20260807`
- 静默只出报告：`...if_netchange.py --quiet`
- 输出报告 `股指期货持仓统计_YYYYMMDD.html` 写入**当前工作目录**

> 工区 `if_stats_automation.py` 为每日 16:00 自动化版（下载+计算+生成报告+经 agent-mail 确认后发邮件至用户指定收件人），口径与本脚本一致。

## 八、输出约定

- 涨跌颜色（A股习惯）：涨 = 红、跌 = 绿
- 净多空为正标红（净多）、为负标绿（净空）
- 报告中必须标注口径说明与免责声明（仅供参考，不构成投资建议）

## 九、校验口诀

中信期货(代客) 中证500 多单净增应 = **−2,932**（IC2608 219 − IC2609 2,422 − IC2612 774 + IC2703 45）。若跑出来不是这个数，说明 datatypeid 映射又搞反了，回头检查第三节。

## 十、收藏、分享与发布

**① 给自己收藏（已自动完成，跨项目持久）**
技能位于用户级目录 `~/.workbuddy/skills/ashare-if-cffex-position/`，WorkBuddy 每次启动加载。调用方式：
- 斜杠命令：`/ashare-if-cffex-position`
- 自然语言：说“统计今日股指持仓”等，自动识别调用

**② 分享给他人（把整个 skill 文件夹给他即可）**
分享单元 = 文件夹 `ashare-if-cffex-position/`（含 `SKILL.md` + `if_netchange.py` + `cache/`）。对方放到 `~/.workbuddy/skills/ashare-if-cffex-position/`（Windows：`C:\Users\<用户名>\.workbuddy\skills\ashare-if-cffex-position\`），重启 WorkBuddy 即可用。脚本纯标准库、缓存自跟随，**对方零配置开箱即用**。

**③ 发布到 WorkBuddy 内置市场（官方审核上架制）**
> 内置市场（BuiltinMarket）为 WorkBuddy **官方审核制上架**，agent 侧市场工具仅支持 `search` / `install`，无法直接 push 发布。需经官方开发者/创作者平台提交 → 审核 → 收录。

本技能已满足提交材料标准，提交前自检清单：
- [x] 标题/摘要/描述无歧义，含完整 frontmatter（title/summary/description/version/author/tags/category）
- [x] 不依赖任何第三方包（纯标准库）
- [x] 数据字段口径与免责声明齐全
- [x] 含防错校验口诀（−2,932 校验锚点）

## 十一、免责声明

本技能基于中金所公开数据自动生成，仅供研究参考，**不构成任何投资建议**。市场有风险，投资需谨慎。报告中的“全市场前20名会员合并”为中金所公开的前20名会员持仓加总（官网仅披露前20名），非严格全市场；席位持仓含套保盘与代客业务，不代表自营方向。
