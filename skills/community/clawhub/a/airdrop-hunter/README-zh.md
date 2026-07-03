# Airdrop Hunter

🇺🇸 [English](README.md) · 🇨🇳 [中文](#airdrop-hunter)

**Web3 空投猎人 — 从小白到杀手**

[![Skill Version](https://img.shields.io/badge/version-3.0.0-blue.svg)](https://github.com/AntalphaAI/airdrop-hunter)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

> **MCP Server 版本**（NestJS）已迁移至 [antalpha-com/antalpha-skills](https://github.com/antalpha-com/antalpha-skills)，可通过 Antalpha MCP Server 作为 MCP 工具调用。

---

## 概述

Airdrop Hunter 不仅仅是找空投。它把你变成猎人。

我们过滤掉 90% 的垃圾空投信息，提供**引导式工作流**：发现 → 验证 → 策略。每次回复都包含**下一步建议**，让你永远不会迷茫"接下来该干嘛？"

**你将获得：**
- S/A/B 分级机会 — 不再挖垃圾
- 骗局防护 — 连钱包前先验证
- 零成本入门包 — 没 ETH？没问题
- 引导式狩猎 — 每个工具都告诉你下一步该做什么

---

## 功能特性

### 1. 数据驱动扫描（MCP 版本）
MCP Server 版本直接从以下来源获取结构化数据：
- **DefiLlama API** - 协议 TVL、类别、链信息
- **硬编码融资数据库** - VC 背书、融资金额
- **空投监控列表** - 精选 S/A 级项目

### 2. 项目评级系统

| 等级 | 标准 | 行动 |
|------|------|------|
| **S** | Tier-1 VC 背书（a16z、Paradigm），融资 $50M+ | 必做 |
| **A** | 知名 VC，融资 $10M+，已确认代币 | 高优先 |
| **B** | 测试网阶段，零成本，早期潜力 | 投机 |

### 3. 极简输出
没有废话。直接给你：
```
[项目] + [操作] + [成本/水龙头链接]
```

### 4. 安全扫描
- 域名验证（对比已知官方域名）
- 钓鱼模式检测（连字符仿冒、子域名钓鱼）
- 虚假申领网站检测

---

## MCP Server 版本（推荐）

最新版 Airdrop Hunter 以 MCP 工具形式运行在 Antalpha MCP Server 上。

**仓库地址**：[antalpha-com/antalpha-skills](https://github.com/antalpha-com/antalpha-skills)（`feat/airdrop-hunter` 分支）

**无需插件或 API Key。** 所有数据从公共 API（DefiLlama）获取。

### 你的武器库 — 5 个工具，3 大战术分类

| 分类 | 工具 | 代号 | 功能 | 使用场景 |
|------|------|------|------|----------|
| **情报** | `airdrop-scan` | 雷达 | 扫描市场上 S/A/B 分级的空投机会（含 TVL、融资、VC 数据） | 想看看现在有什么热点 |
| **情报** | `airdrop-daily-report` | 每日简报 | 4 板块晨报：高优先级项目、零成本机会、截止日期、骗局警报 | 规划一天、出差回来补课 |
| **尽调** | `airdrop-check-project` | 嗅探器 | 即时评级任意项目（S/A/B/C），检测已完成空投 | 有人提到某个项目，想知道值不值得花时间 |
| **尽调** | `airdrop-scam-check` | 护盾 | 验证 URL/项目是否存在钓鱼、仿冒、可疑域名 | 在 Twitter/Telegram 上看到空投链接，感觉不对劲 |
| **入门** | `airdrop-zero-cost` | 白嫖之路 | 查找 $0 成本的测试网和免费主网机会 | 新手入场、预算有限、想要零风险起步 |

### 工作流 — 发现、验证、策略

```
步骤 1：发现            步骤 2：验证              步骤 3：策略
┌──────────────┐     ┌───────────────────┐     ┌───────────────────┐
│ airdrop-scan │────>│ airdrop-check-    │────>│ airdrop-zero-cost │
│   雷达       │     │   project         │     │   白嫖之路        │
│              │     │   嗅探器          │     │                   │
│ airdrop-     │     │                   │     │ 找到免费方式      │
│ daily-report │     │ airdrop-scam-     │     │ 参与你刚验证过    │
│ 每日简报     │     │   check           │     │ 的空投项目        │
│              │     │   护盾            │     │                   │
└──────────────┘     └───────────────────┘     └───────────────────┘
```

**每个工具的返回结果都包含 `next_step` 建议**，告诉你下一步该用哪个工具以及为什么 — 让你永远不会再想"接下来该干嘛？"

### 下一步建议示例

| 你刚做完... | 猎人建议 |
|-------------|----------|
| 扫描发现 S 级项目 | "运行 `airdrop-check-project` 深度分析后再交互" |
| 查到一个 C 级项目（已完成） | "别浪费时间了。运行 `airdrop-scan` 找新机会" |
| 发现一个有官网的 A 级项目 | "在连钱包前先运行 `airdrop-scam-check` 验证 URL" |
| 查到一个高危骗局 URL | "远离！运行 `airdrop-check-project` 找正规官网" |
| 获得零成本机会列表 | "运行 `airdrop-scam-check` 验证官网 URL 是否安全" |
| 日报显示骗局警报 | "如果你看到过可疑链接，运行 `airdrop-scam-check` 验证" |

---

### 安装

1. 下载 `airdrop-hunter.skill`
2. 上传到 Skill 库
3. 测试命令：`daily report`

### 快捷命令

| 命令 | 操作 |
|------|------|
| `daily report` | 获取最新 24 小时空投清单 |
| `any zero-cost?` | 筛选免费测试网机会 |
| `check [项目名]` | 查询特定项目空投状态 |
| `S-grade tasks` | 只显示 S 级高优先级任务 |

---

## 输出示例

```
空投扫描结果 (2026-04-13)

高优先级（S 级）
1. Monad：测试网交互 | $0 | 无截止日期
   原因：Paradigm + Electric Capital（$444M 融资），Tier-1 VC
   链接：https://monad.xyz

2. Abstract：桥接 + Swap 任务 | $1-5 | 进行中
   原因：Founders Fund + Paradigm（$107M 融资）
   链接：https://abstract.xyz

零成本（B 级）
1. Initia：测试网参与 | 免费 | 进行中
   原因：Binance Labs 背书，测试网已上线
   链接：https://initia.xyz

骗局警报
- 钓鱼："scroll-airdrop-claim.xyz" 不是官方网址
- 官方：scroll.io
```

---

## 场景演示

### 场景 1：日常空投扫描

**用户**："现在有什么空投机会？"

**工具**：`airdrop-scan`

**渲染输出**：
```
空投扫描 (2026-04-13) — 发现 18 个机会

[S] Monad | 链 | $0 | monad.xyz
    Paradigm + Electric Capital ($444M) | 暂无代币

[S] Abstract | 链 | $1-5 | abstract.xyz
    Founders Fund + Paradigm ($107M) | TVL $52M

[A] Initia | DEX | $0 | initia.xyz
    Binance Labs ($7.5M) | 测试网已上线

... 还有 15 个
```

---

### 场景 2：每日报告

**用户**："给我今天的空投日报"

**工具**：`airdrop-daily-report`

**渲染输出**：
```
空投日报 — 2026-04-13

高优先级（S/A 级）
 1. Monad [S] | 测试网 | $0 | Paradigm + Electric Capital ($444M)
 2. Abstract [S] | 桥接+Swap | $1-5 | Founders Fund + Paradigm ($107M)

零成本机会
 1. Initia — 测试网参与（免费）
 2. MegaETH — 测试网交互（免费）

即将到期
 1. Berachain [A] — BGT 质押活跃，代币即将发布

骗局警报
 ! 连字符仿冒域名（如 project-airdrop.io）— 务必验证
 ! 官方项目绝不会通过私信发送申领链接
```

---

### 场景 3：查询特定项目

**用户**："Scroll 还值得做吗？"

**工具**：`airdrop-check-project`，参数 `project_name: "Scroll"`

**渲染输出**：
```
Scroll — C 级 | 空投已完成

代币：$SCR（已在交易）
TVL：$620M | 融资：$80M（Polychain、Sequoia）

状态：空投已分发。SCR 已上线。
警告：当心虚假"Scroll 空投"网站 — 官方是 scroll.io

建议：跳过 — 已无空投机会
```

---

### 场景 4：零成本机会

**用户**："有没有不用花 gas 的免费空投？"

**工具**：`airdrop-zero-cost`

**渲染输出**：
```
零成本空投 — 发现 3 个

1. Monad（测试网）| monad.xyz
   与测试网 dApp 交互 — 不需要真 ETH

2. Initia（测试网）| initia.xyz
   测试网 Swap + LP — 从水龙头免费领取测试币

3. MegaETH（测试网）| megaeth.com
   早期测试网参与 — 免费加入
```

---

### 场景 5：骗局检测

**用户**："scroll-airdrop-claim.xyz 是真的吗？"

**工具**：`airdrop-scam-check`，参数 `url: "https://scroll-airdrop-claim.xyz"`

**渲染输出**：
```
骗局警报 — 风险等级：极其危险

URL：scroll-airdrop-claim.xyz

警告：
 [极其危险] 连字符仿冒域名 — 检测到"scroll-airdrop"模式
 [极其危险] 使用了"scroll"名称但不是官方项目

安全替代：scroll.io

绝对不要连接你的钱包。这是钓鱼网站。
```

---

### 场景 6：骗局检测（安全 URL）

**用户**："berachain.com 是真的官网吗？"

**工具**：`airdrop-scam-check`，参数 `url: "https://berachain.com"`, `project_name: "Berachain"`

**渲染输出**：
```
安全 — berachain.com 是 Berachain 的验证官方域名。

未检测到警告。你可以谨慎操作。
连接钱包前始终独立验证 URL。
```

---

## 项目结构

### MCP Server 版本
```
libs/skills/airdrop-hunter/
├── src/
│   ├── airdrop-hunter.config.ts     # 配置
│   ├── airdrop-hunter.module.ts     # NestJS 模块
│   ├── constants/
│   │   ├── prohibited-tokens.ts     # 已完成空投（精确匹配）
│   │   ├── funding-database.ts      # 硬编码 VC/融资数据
│   │   ├── airdrop-watchlist.ts     # 精选 S/A 级项目
│   │   ├── vc-tiers.ts             # VC 等级分类
│   │   └── scam-patterns.ts        # 钓鱼检测模式
│   ├── model/
│   │   └── airdrop-project.model.ts # 数据接口
│   ├── service/
│   │   ├── defillama.service.ts     # DefiLlama API 客户端
│   │   ├── grading.service.ts       # S/A/B/C 评级引擎
│   │   ├── scam-detector.service.ts # 骗局检测
│   │   └── airdrop-scanner.service.ts # 扫描编排器
│   └── tools/
│       └── airdrop-hunter.tools.ts  # 5 个 MCP 工具注册
└── test/
    └── aird-hunter.test.ts          # 35 个单元测试
```

---

## 免责声明

**本工具仅供信息参考，不构成投资建议。**

- 始终自行研究（DYOR）
- 不要投入超过你能承受的损失
- 交互前验证所有信息
- 使用独立钱包进行空投猎取
- 绝不分享私钥或助记词

---

## 许可证

MIT 许可证
维护者：AntalphaAI 团队
