# A 股涨停板龙虎榜深度研判 + 财富密码选股策略

面向 **OpenClaw（大龙虾）** / **QClaw（小龙虾）** / **MiMo Desktop / MiMoCode** 的**日更投研融合体系**：

1. **涨停板龙虎榜深度研判报告**（21 章 / 四层漏斗 v2）— 支持两种排版样式，见下表
2. **strategy 自动化选股包** — 公式、硬闸门、L2.5 可交易性、累计 α 预算、熔断、盘前检查
3. **westock MCP 取数** — 优先腾讯自选股 MCP，否则降级为本地 JSON 演示数据

> 当前版本：**v2.2.0**（口径 v2 · 2026-09-12 定稿｜v2.1 新增 BII 双栏范式｜v2.2 日更默认改出 BII 双栏 + 新增第 14 页「次日 5 条可证伪预判」· 2026-09-16）
> · **当前发行版本：v4.0.5**（2026-11-14 · 在 4.0.4 基础上做安全加固：§18.13 权限边界声明、安装脚本去 `rsync --delete`、示例数据快照化，见下节）
> · v4.0.4（2026-11-14）：统一深度投研报告四阶段流水线实跑基线，见 SKILL.md §18.12 与 docs/unified-deep-research-pipeline-20261113.md（服务端已发布，处于安全复核暂挂状态）
> · v4.0.3（2026-11-13）：跨会话长期实盘本金 ¥100,000 口径固化，见 SKILL.md §18.11 与 docs/capital-caliber-20261113.md
> · 测试覆盖：**107 条断言全绿**
>
> 成功是有预谋的精心策划。本仓库提供可执行流程与风控，**不构成投资建议**。

---

## 两种排版样式

| | 样式 A（classic） | 样式 B（bii，**日更默认**） |
|---|---|---|
| 版式 | 单栏 21 章铺排 | BlackRock 投资研究院「左文字栏 295px ‖ 右图表栏」双栏 |
| 纸张 | A4 纵向 | A4 横向 |
| 配色 | MS 深蓝 #002B5C + 金 #C5A572 | 黑 #000 + 品牌黄 #FFB500 |
| 图表 | ECharts（可选）· 6 张 | Chart.js 4.4.1（内联）· 8 张 |
| PDF 通道 | Playwright（浏览器缺失时自动回退系统 Chrome + CDP）| 系统 Chrome + CDP |
| 篇幅 | 26–38 页 | **20 页**（四态回滚 20 / 18 / 16 / 14；P14 恒为次日 5 条可证伪预判）|
| 附加产物 | PPTX（26 页）| — |
| 命令 | `--style classic` | `--style bii`（两套都出：`--style both`）|

两种样式**共用同一套口径与漏斗逻辑**（`strategy/`），只是版面与图表实现不同 ——
换样式不会改变结论，也不会多出一份需要同步维护的算法。涨跌配色两种样式都保持
A 股习惯（涨红 #C1272D / 跌绿 #1E8449）。

**日更默认只出样式 B**；样式 B 自带「次日 5 条可证伪预判」页，因此可独立成篇，
19:15 的核验任务直接读它即可。实现与六个必踩坑见 `SKILL.md` §12。

---

## 统一深度投研报告（v4.0.4 · 四阶段流水线）

原三条独立定时任务合并为**一次触发 → A 主研判 / B T−1 核验 / C 五大战法 / D 统一报告 → 一份主交付**。
A/B/C 仍是阶段、不再并列交付；主交付是单文件自包含 HTML + A4 PDF，2026-11-13 实跑为
**64 内联 SVG / 31 表 / 57 页**，0 外部依赖，全部图表内联生成。

- SOP 与九条跨阶段纪律：`SKILL.md` **§18.12**
- 同步记录：`docs/unified-deep-research-pipeline-20261113.md`
- 生成器与样本：[GitHub `templates/unified/`](https://github.com/yjkj999999/a-share-dragon-tiger-strategy/tree/main/templates/unified) · [`docs/unified-report-20261113.html`](https://github.com/yjkj999999/a-share-dragon-tiger-strategy/blob/main/docs/unified-report-20261113.html)

> 两套资金口径（7 亿机构容量 / ¥100,000 实盘）、两套闸门、三层只读旁路权限边界**不变**；
> 本流水线不改变任何冻结阈值与判定结论。**不构成投资建议**。

---

## 目录

```
a-share-dragon-tiger-strategy/
├── strategy/                  # 9 模块 + 测试 + demo（~1700 行）
├── templates/                 # 样式 A：HTML 模板 + Playwright 渲染 + python-pptx
│   └── bii/                   # 样式 B：双栏生成器 + Chart.js + CDP 导 PDF + 校验脚本
├── assets/echarts.min.js      # 离线 ECharts
├── scripts/generate_daily.py  # 日更入口（--style classic|bii|both）
├── framework/                 # 十五五 18 方向跟踪池（102 板块 + 12 SW1 + 70 股）+ 口径 v2 结论
├── reports/                   # 18 方向三层核验生成器（build_15th5_report.py + cache/）
├── docs/wealth-password-strategy.md  # 投资方法总纲
├── skill/                     # 本目录（SKILL.md + README.md + skill-card.md）
└── README.md
```

## 快速开始

```bash
# 1. 自检
python3 strategy/test_formulas.py    # → 通过 107 / 失败 0

# 2. 一键 demo
python3 strategy/run_demo.py

# 3. 生成一日报告（样式 A：HTML + PDF + PPTX）
python3 scripts/generate_daily.py --date 2026-09-16 --out out/dragon-tiger-20260916

# 3b. 日更默认：BII 双栏版式（样式 B：HTML + PDF，自带四重校验）
python3 scripts/generate_daily.py --style bii --date 2026-09-16 \
    --predict-file out/dragon-tiger-20260916/predictions.json   # 第 14 页次日预判

# 3c. 两套都出
python3 scripts/generate_daily.py --style both --date 2026-09-16

# 4. 生成十五五 18 方向三层核验报告（离线）
cd reports && python3 build_15th5_report.py
```

依赖：Python 3.10+、`python-pptx`、`lxml`、`Pillow`；**Node 22+**（样式 B 的校验与导 PDF 用，
无需 npm install）；**Chrome / Edge / Chromium** 或 Playwright chromium（导 PDF 需要其一）。

## 安装为 Skill（三平台）

```bash
R=/path/to/a-share-dragon-tiger-strategy   # 安装前人工确认指向可信目录
STAMP=$(date +%Y%m%d-%H%M%S)
for D in ~/.openclaw/workspace/skills/a-share-dragon-tiger-report \
         ~/.qclaw/skills/a-share-dragon-tiger-report \
         ~/.config/mimocode/skills/a-share-dragon-tiger-report ; do
  if [ -d "$D" ]; then
    cp -a "$D" "${D}.bak-${STAMP}"   # 先备份，保留目标目录独有文件
  else
    mkdir -p "$D"
  fi
  cp -R "$R/skill/." "$D/"           # 只覆盖同名文件
done
```

> **安全说明**：安装脚本**不使用 `rsync --delete` 或任何删除动作**，不会移除目标目录中已有但本包没有的文件；
> 覆盖前自动备份。请逐平台核对 `$D` 路径后再执行。安装属人工运维动作，
> **不是报告生成流水线的自动步骤**，也不会由 skill 自行触发。

技能触发词：生成龙虎榜研判、涨停深度报告、融合选股策略日更、四层漏斗核验、
做十五五方向核验、用双栏版式 / BlackRock 范式出报告。

## 六条已确认口径（v2 · 永久生效）

唯一来源：`strategy/calibers.py`。

| # | 口径 | v2 取值 |
|---|---|---|
| ① | 国企央企背景 | 偏好项（+6 分），不是门槛 |
| ② | 产业偏好 | 新兴科技成长优先（+8 分） |
| ③ | 净利润增长率 | **半年口径**（最新中报年内同比）|
| ④ | 单年亏损 | 减分项（−10 分）；连续两年年报亏损 = 否决 |
| ⑤ | 「链」形态主题 | 跳过 L1 否决权（行业层仅定性）|
| ⑥ | 基础可交易性 | L2.5 独立层（位于 L2 与 L3 之间）|

增速红线：中报同比 ≤ 0 → 排除；中报同比 < 上年度增速的 50% → 重大减分 −15 分。
口径变更须全量重算历史结论并报告 ±N 只敏感度。

## 十五五 18 方向跟踪池（v2.0 新增）

`framework/baseline_15th5_20260911.json` 内置十五五「6 张网 + 6 新兴支柱 + 6 未来产业」三层核验跟踪池：
**102 板块**（boards_unique=102）+ **12 SW1**（ind_layer=12）+ **70 股**（stocks_unique=70），
含每条记录的 `rank`/`pos`/`vr`/`lo`/`hi` 三层核验字段。配套 `framework/conclusions_v2_20260911.json`
给出六条口径 v2 + 增速红线 + L2/L2.5/L3 结论 + ±N 敏感度；`reports/build_15th5_report.py` 可离线
产出「十五五六张网与产业方向三层核验报告」HTML。

## 核心公式

| 公式 | 定义 |
|---|---|
| 综合分 S | `0.30·tech + 0.25·flow + 0.20·fund + 0.15·cycle + 0.10·fib` |
| α_max | I 40% / II 30% / III 15% / IV 5%（冰点 ×0.5）|
| 仓位 N | `floor(权益 × r ÷ (entry − stop))` |
| 累计 α | `Σ开仓名义 ≤ α_max × 权益` |
| 单票 / 单行业上限 | 10% / 30%（突破书面复盘）|
| 熔断 | 回撤 ≥15% 减仓；≥25% 停机 |
| 凯利（参考）| `min(p − (1−p)/b, 0.25) × 0.5` |

考核带：年化 12% – 25%，按年复利；看板：执行完整率 + 风控合规率。

## 推送到 GitHub

```bash
git init && git add . && git commit -m "feat: A-share dragon-tiger v2.1 (BII two-column variant + --style switch + CDP PDF fallback)"
git remote add origin git@github.com:yjkj999999/a-share-dragon-tiger-strategy.git
git push -u origin main
```

## 定时任务

| 时间 | 任务 | 要点 |
|---|---|---|
| 交易日 18:00 | 生成日更报告 | **默认只出样式 B（BII 双栏，14 页）**；先落盘 `data.json` + `predictions.json`，再跑 `--style bii` |
| 交易日 19:15 | 预判核验 | 读**上一交易日**报告的「9.1 次日（YYYY-MM-DD）5 条可证伪预判」，逐条判定 + 三层命中率 |

`predictions.json` 契约（5 条硬性数量，每条必须有 `claim` + `falsify`）见 `SKILL.md` §12.9；
缺该文件时生成器渲染「示例占位页」并明确标注，不会静默出错。

## 免责声明

本项目仅供教育与研究。数据可能为 T-1；任何收益数字为情景或历史，**不构成投资建议**。
市场有风险，投资需谨慎。

---

**Author**

本 Skill 由 **Wang Dongjie 王东杰** 创作

资深复合型战略财务专家 · 上市公司资本运作操盘手 · 集团化财务管控与风险治理高级工程师

Wdj_@163.com · 13952453499