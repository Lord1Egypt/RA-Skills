---
secrets:
  - name: ODDS_API_KEY
    description: "用户自行申请的 The-Odds-API 免费密钥"
permissions:
  network:
    - host: "api.the-odds-api.com"
      ports: [443]
      reason: "拉取实时赔率数据（The Odds API v4）"
---

---
name: footyclaw
description: >
  FootyClaw — 足球投注全流程助手。覆盖赛事信息抓取、足彩玩法规则、赔率获取（通过环境变量
  ODDS_API_KEY 读取密钥）、基本面分析、EV期望值计算、Kelly公式仓位管理、最终下注方案推荐、
  账本记账与资金曲线生成。
  触发词：分析今晚比赛、查赔率、找投注机会、今天有什么场、EV分析、Kelly仓位、
  下注推荐、记账、更新账本、出账本图表、足彩、亚盘、大小球、欧盘。
---

# ⚽ FootyClaw — 足球投注全流程 Skill

## 0. 快速开始

用户首次使用时询问：
1. **初始资金池金额**（本金）
2. **股东结构**（若多人合伙，记录各人出资比例）

> **密钥安全规范**：API 密钥通过环境变量 `ODDS_API_KEY` 获取，由 Skill
> 平台 secrets 机制自动注入。**不要在对话中询问、打印或以任何方式暴露用户的
> 明文密钥。** 若环境变量缺失，提示用户到 Skill 设置页面配置 `ODDS_API_KEY`
>（免费注册：https://the-odds-api.com）。

---

## 1. 标准分析流程

### Step 1 — 读取资金池
从会话记忆中获取当前资金池余额（首次使用时由用户提供初始金额）

### Step 2 — 拉取赔率
python3 scripts/daily_scanner.py \
  --bankroll <资金池> --min-ev 1.0 --hours-ahead 36
（脚本自动从环境变量 `ODDS_API_KEY` 读取密钥，无需手动传入）

扫描覆盖：英超/西甲/德甲/意甲/法甲/欧冠/欧联/欧协联

### Step 3 — EV 计算（核心规则）
必须用 Pinnacle 公平概率 vs 其他 bookmaker 赔率：
1. 提取 Pinnacle 对同一市场的两个结果配对去 vig
2. 公平概率 fp = (1/o1) / (1/o1 + 1/o2)
3. EV% = fp×(odds-1) - (1-fp)
4. 绝不用 Pinnacle 对 Pinnacle 算 EV（会得到虚假 100%+）
5. 排除：matchbook/betfair_ex/williamhill/betonlineag

EV 阈值：<1% 不投 | 1-3% 可投 | 3-5% 好机会 | >5% 需核实

### Step 4 — 基本面核查
详见 references/fundamental-analysis.md：
- xG/xGA 数据趋势
- 近期主客场分开统计
- 伤病/停赛情况
- 轮换风险（国际赛周/欧战密集期）
- 赔率移动方向（跟随 sharp money）

### Step 5 — 仓位计算
Kelly = (fp×(odds-1) - (1-fp)) / (odds-1)
推荐注额 = Kelly × fraction × 资金池
- fraction 默认 1/4 Kelly，可按用户风险偏好调整
- 正 EV 机会不足时不强行凑负 EV 注
- 单注上限：资金池 20%（风控硬性上限）
- 连续亏损 3 日：建议降低仓位直至盈利

### Step 6 — 输出下注方案
企业微信不渲染 Markdown 表格，必须用纯文本格式：

📅 周X（MM-DD）｜总注 ¥X,000

🏴 主队 vs 客队 | HH:MM
投注项 @赔率 | EV +X.X% | ¥X,000 | 赢 +¥X,000

三天总注 ¥X,000 | 期望 +¥XXX | 全中 +¥X,000

---

## 2. 盘口规则速查

亚盘让球：
- X.0：赢全赢，平退款，输全输
- X.25：赢全赢，平=半输，输全输
- X.5：赢全赢，平/输全输（无退款）
- X.75：赢1球=半赢，赢2球+=全赢，平/输全输

大小球 Under 方向：
- U2.25：2球半赢，3球+全输
- U2.5：2球以下全赢，3球+全输
- U2.75：3球半赢，4球+全输
- U3.0：3球退款，4球+全输
Over 方向完全相反。

盈利计算：
- 全赢：注额 × (赔率 - 1)
- 半赢：注额 × (赔率 - 1) × 0.5
- BTTS/DNB：见 references/betting-rules.md

---

## 3. 账本记账（纯对话，零文件写入）

账本数据由大模型会话记忆维护，每次记账直接在对话框打印 Markdown 表格：
| Day | 日期  | 注数 | 中/总 | 盈亏   | 期末资金 | 备注 |
用户可随时说"出账本"查看完整表格。

盈利计算规则：
- 欧盘独赢盈利 = 注额 × (欧赔 - 1)
- 亚盘盈利 = 注额 × HK赔率（HK赔率 = 欧赔 - 1）
- 股东权益按出资比例分配

资金曲线图：`python3 scripts/chart_generator.py`
脚本从 stdin 读取账本 Markdown 表格，在内存中生成 SVG，输出 Base64 编码的
`<img>` 标签到 stdout，可直接嵌入对话框显示，不写任何本地文件。

---

## 4. 联赛特性速查

英超 soccer_epl：~2.7球，平局率26%，主场优势弱
西甲 soccer_spain_la_liga：~2.5球，技术流，强队让球有价值
德甲 soccer_germany_bundesliga：~3.2球，高进球，大球多
意甲 soccer_italy_serie_a：~2.5球，防守为主，BTTS No多
法甲 soccer_france_ligue_one：~2.4球，PSG碾压，非PSG小球多
欧冠 soccer_uefa_champs_league：~2.9球，首回合保守

---

## 5. 参考文件索引

- references/betting-rules.md — 完整盘口规则
- references/fundamental-analysis.md — 基本面分析框架
- scripts/daily_scanner.py — 全联赛 EV 扫描
- scripts/ev_calculator.py — EV + Kelly 计算
- scripts/fetch_odds.py — 单联赛赔率拉取
- scripts/chart_generator.py — 账本图表生成（stdin→Base64 img，零文件写入）
