# 📊 商业数据洞察 (biz-data-insight)

> 连接你的业务数据，AI自动生成分析报告和看板

---

## 功能亮点

- 🔌 **多数据源接入** — 支持 MySQL、PostgreSQL 数据库及 CSV / Excel / JSON 文件，一次配置长期使用
- 📈 **自动生成报告** — 每日、每周、每月报告自动产出，包含关键指标、趋势分析和可视化图表
- 🧠 **AI 智能洞察** — 自动识别数据异常、计算同比环比、提炼业务结论，不只是展示数字
- 💬 **交互式提问** — 用自然语言向数据提问，秒级返回分析结果和图表
- 📊 **Mermaid 可视化** — 报告内嵌饼图、折线图、柱状图，无需额外工具即可在 Markdown 中查看
- 🔒 **数据安全** — 所有查询在本地执行，数据不离开你的环境

---

## 版本对比

| 功能 | 免费版 | 付费版 ¥99/月 |
|------|:------:|:------------:|
| 数据源数量 | 1个 | 最多5个 |
| 数据库类型 | MySQL | MySQL + PostgreSQL |
| 文档类型 | CSV | CSV + Excel + JSON |
| 日报/周报 | 基础表格 | 表格 + Mermaid图表 + 洞察 |
| 月报 | ❌ | ✅ 完整多维度分析 |
| 交互式提问 | 5次/天 | 无限 |
| 异常检测 | ❌ | ✅ |
| 同比/环比 | ❌ | ✅ |
| 查询行数限制 | 100行 | 10,000行 |

---

## 快速开始

### 1. 安装 Skill

在 ClawHub 中搜索 `biz-data-insight`，点击安装，或使用命令行：

```bash
openclaw skill install biz-data-insight
```

### 2. 配置数据源

在项目根目录创建 `datasource.yaml` 文件：

```yaml
# 数据库连接示例
datasources:
  - name: 业务主库
    type: mysql
    host: localhost
    port: 3306
    database: my_business_db
    username: reader
    password: ${DB_PASSWORD}    # 支持环境变量

  # CSV 文件示例
  - name: 销售数据
    type: csv
    path: ./data/sales_2026.csv
    encoding: utf-8
```

### 3. 生成报告

```bash
# 生成日报
/biz-data-insight daily

# 生成周报
/biz-data-insight weekly

# 生成月报（付费版）
/biz-data-insight monthly

# 交互式提问
/biz-data-insight ask "上周销售额最高的产品是什么？"
```

### 4. 查看产出

报告自动保存到 `output/reports/` 目录，格式为 Markdown 文件，可直接在编辑器或 Git 仓库中查看。

---

## 报告示例

以下是一份自动生成的日报样例：

```markdown
# 📊 业务日报 — 2026-03-19（周四）

数据源：业务主库 | 统计周期：2026-03-19 00:00 ~ 23:59

## 核心指标

| 指标 | 今日 | 昨日 | 日环比 |
|------|-----:|-----:|-------:|
| 订单数 | 1,283 | 1,195 | +7.4% |
| 销售额 | ¥328,450 | ¥301,200 | +9.0% |
| 客单价 | ¥256 | ¥252 | +1.6% |
| 退货率 | 2.1% | 2.3% | -0.2pp |

## 分类销售占比

｜饼图将在此处渲染｜

## 今日摘要

- 订单数和销售额均高于昨日，主要受"春季促销"活动拉动
- 电子产品类目贡献了 42% 的销售额，为当日最大品类
- 退货率小幅下降，处于正常区间

---
*报告由 biz-data-insight 自动生成*
```

---

## 常见问题

### Q1: 支持哪些数据库版本？

MySQL 5.7+ 和 MySQL 8.x 均已测试通过。付费版额外支持 PostgreSQL 12+。

### Q2: 数据会上传到云端吗？

不会。所有数据查询和报告生成均在本地完成，数据不会离开你的运行环境。AI 分析基于查询结果的聚合数据进行，不会传输原始数据。

### Q3: 免费版可以同时连接多个数据源吗？

免费版限制为 1 个数据源。如果你需要同时分析多个库表或文件，请升级到付费版（支持最多 5 个数据源）。

### Q4: 如何自定义报告中的指标？

在 `datasource.yaml` 中为每个数据源添加 `metrics` 配置项，指定需要统计的字段、聚合方式和显示名称。详见 `references/report-templates.md`。

### Q5: Mermaid 图表在哪些工具中可以渲染？

Mermaid 图表在以下环境可直接渲染：GitHub / GitLab 的 Markdown 预览、VS Code（安装 Mermaid 插件）、Typora、Obsidian 等。大多数现代 Markdown 查看器均已支持。

### Q6: 报告生成速度如何？

取决于数据量和查询复杂度。通常情况下，日报在 5-15 秒内生成，周报约 15-30 秒，月报约 30-60 秒。

---

## 技术支持

- 📖 **文档**：查看 `references/` 目录获取模板和图表语法参考
- 🐛 **问题反馈**：在 ClawHub 的 Skill 页面提交 Issue
- 💬 **社区讨论**：加入 ClawHub 社区频道 `#biz-data-insight`
- 📧 **邮件**：skill-support@clawhub.dev

---

*biz-data-insight v1.0 | 兼容 OpenClaw 0.5+*
