---
name: dx-data-baseline
description: 集团数据现状摸底/数据资产盘点。当用户要"数据现状摸底/数据资产盘点/数据普查/系统摸排/数据目录/成熟度评估/DCMM初评/我们有什么数据"时使用。
description_en: Data baseline survey and asset inventory for a group. Use when the user asks what data they have, wants a system survey, data catalog, DCMM maturity assessment, or full data census. Produces an asset inventory, data-flow diagram, and DCMM maturity score.
license: Apache-2.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
metadata:
  author: 大数据猎人
  version: "2.0"
  domain: 数据现状摸底·资产盘点
  fused_from: ["csv-data-wrangler", "duckdb/duckdb-skills"]
---

# 数据现状摸底（七道工序：汇 + 存）

## 何时使用
- "盘一下集团有什么数据""数据资产盘点""系统摸排""数据目录""做个 DCMM 成熟度评估"。
- 任何数字底座/数据治理/入表项目的**第一步**（也是 orchestrator 的第一道门禁）。
- 用户说"不知道我们到底有多少数据、在哪、能不能用"。

## 目标
把"**有什么数据、在哪、谁负责、质量如何、能不能用**"盘清楚，作为后续架构/质量/应用规划的地基。
**产出是"地基"，不是"装修"**——摸底阶段不做治理、不做架构，只做事实清点。

## 核心方法论：先盘系统，后盘数据

### 为什么顺序不可颠倒
系统是**数据源的真相**。没摸清系统边界就发问卷，收回来的答案是"业务侧以为的数据"，与实际存储对不上，必然返工。

```
第一遍：脚本扫机器        → 得到客观事实（有哪些库/表/字段/文件）
第二遍：问卷核语义        → 补业务含义（这字段什么意思、谁负责）
第三遍：交叉校验           → 机器画像 vs 业务回答，冲突处就是问题所在
```

## 四步法（可照做）

### Step 1｜系统摸排（1–2 天）
**目标**：列出集团**全部**数据产生与承载的系统。

操作：
1. 让 IT 提供系统清单（在建/在用/停用）——但**务必现场核对**，清单常缺"影子系统"和离线流程。
2. 按类型分类：核心业务系统 / 财务 / 人力 / 交易 / 物联网设备 / 采购的 SaaS / 自研 / **离线 Excel 流程**。
3. 每个系统记录：系统名、上线时间、厂商/自研、技术栈（DB 类型）、负责人（业务+技术）、主要数据、更新频率。
4. **重点盘"数据出口"**：哪些数据对外报送（监管/母公司/合作方）。

**产出**：系统清单表（系统 × 归属 × 负责人 × DB × 用途）。

### Step 2｜数据资产盘点（3–7 天，工作量最大）
**目标**：按"业务域 → 系统 → 库表 → 字段"四级建清单。

操作：
1. **先跑脚本**（见下节"脚本化盘点"）：扫描数据库/文件，得到客观的表名、字段名、行数。
2. **再发问卷**（`../_shared/assets/调研问卷模板.md`）：向业务侧核对字段**业务含义**、口径公式、权威源。
3. **交叉校验**：脚本扫出的字段 vs 业务回答的字段——对不上的就是"孤儿表"或"未登记数据"。
4. 按 `../_shared/assets/数据资产目录模板.md` 的 17 列格式填写。

**产出**：数据资产清单（xlsx，含业务域/系统/表/字段/业务含义/口径/权威源/负责人/敏感级别/在用状态）。

### Step 3｜数据流图（1–2 天）
**目标**：画出跨系统的数据流向。

操作：
1. 标记每个业务域的数据"从哪来、存哪、给谁用"。
2. 画出主要链路：业务系统 → 采集 → 存储 → 分析/报表 → 对外报送。
3. **标注断点**：手工传递环节、多份拷贝、口径冲突处（这些是后续治理重点）。

**产出**：`系统摸排与数据流图.md`（mermaid 或图片）。

### Step 4｜DCMM 成熟度评分（半天）
**目标**：给出 8 域量化画像，作为后续规划的基线。

操作：
1. 对照 `../_shared/references/DCMM-DMBOK对标.md` 的 8 域定义逐项打分（1–5 分）。
2. 运行脚本：
   ```bash
   python _shared/scripts/maturity_score.py scores.json
   ```
   输入 JSON：`{"数据战略":2,"数据治理":2,"数据架构":2,...}`
3. 输出加权总分 + 等级判定（初始/受管理/稳健/量化/优化）。

**产出**：`DCMM成熟度初评_<集团>.md`（8 域分数 + 等级 + 短板清单）。

## 脚本化盘点（融合 csv-data-wrangler / duckdb-skills）

**原则：能用脚本扫的，绝不手工问。**

### 工具选择（按数据规模，来自 csv-data-wrangler 决策树）
| 数据量 | 工具 | 理由 |
|---|---|---|
| < 1GB | pandas | 内存搞定，生态全 |
| 1–10GB | **Polars** 或 **DuckDB** | Polars 快，DuckDB 可直接查文件 |
| > 10GB | Spark / 分布式 | 单机内存不够 |

### DuckDB 直扫（推荐，零部署）
```sql
-- 直接查 CSV/Parquet，无需入库
SELECT * FROM 'data/*.parquet' LIMIT 10;
-- 表画像：行数 / 空值率 / 唯一值
SELECT COUNT(*) AS rows,
       COUNT(DISTINCT id) AS uniq,
       SUM(CASE WHEN name IS NULL THEN 1 ELSE 0 END) AS null_name
FROM 'data/*.parquet';
```

### 通用扫描脚本
`../_shared/scripts/scan_assets.py`（零依赖）：
```bash
python _shared/scripts/scan_assets.py <目录> --out assets.csv
```
自动枚举 CSV/Excel/Parquet/DB 等数据文件，输出路径/大小/修改时间/CSV表头，并给出工具选型建议。
**离线文件也算数据源**——Excel 目录必须纳入盘点。

### 元数据批量提取
- 数据库：查 `information_schema.tables/columns` 批量导出。
- Parquet：读 footer 拿 schema。
- 好处：避免人工录入遗漏，且与系统清单交叉验证。

## 输出物（门禁检查）
- [ ] `系统清单_<集团>_<日期>.md`
- [ ] `数据资产清单_<集团>_<日期>.xlsx`（17 列完整）
- [ ] `系统摸排与数据流图.md`（含断点标注）
- [ ] `DCMM成熟度初评_<集团>.md`（8 域分数 + 等级）

**门禁**：以上四项齐全方可进入 `dx-architecture-opt`。

## 访谈执行要点
- **分两轮**：第一轮 IT/系统管理员（系统与库表），第二轮业务负责人（字段语义与口径）。
- 每场访谈记录：受访人角色 / 时间 / 主题 / 关键论点 / 数据证据 / **待确认事项**。
- 业务回答必须技术侧复核（"看起来有"≠"实际在用"）。
- 优先访谈**数据出口密集**的部门（财务、监管报送、核心交易）。

## Gotchas
- **切勿先发问卷再盘系统**——没摸清系统边界，问卷填出来全是幻觉（返工的主因）。
- **主数据（客户/供应商/商品/组织）先定唯一标识再盘点**，否则跨系统对不上（同一客户在交易/会员/财务三套 ID 是常态）。
- 字段级必须记录**业务语义**，否则后续"金额""数量"等口径必然算错。
- 盘点要覆盖**离线文件/Excel/接口/物联网设备**等非数据库数据源，不止数据库。
- **"影子系统"和 Excel 流程**最容易被漏——它们常是真实业务的关键数据源。
- 摸底阶段**不要顺手做治理**：记录问题但不修，修是 dx-data-quality 的活。
- **敏感级别要在摸底时就标定**（公开/内部/敏感/重要数据），否则后续架构阶段无法做访问控制设计。
- 资产清单的"在用状态"（在用/沉睡/未用）必须标——沉睡表是后续治理的优先清理对象，但**删之前要下架公示，不能直接删**。
- **Windows 下脚本输入必须兼容 BOM**（2026-09-12 试跑踩坑）：PowerShell `Set-Content -Encoding utf8` 写的 JSON/CSV 带 BOM，`maturity_score.py` 曾因此 `json.load` 崩溃、`scan_assets.py` 表头被 BOM 污染首列名。**已修复**（统一 `utf-8-sig` 读取）；新增脚本或手工构造输入时沿用此约定。
- **DCMM 加权均值判定偏乐观**：8 域中 4 个 1 分也可能判"受管理级 2 级"（1.5 分落在 2 级区间）。看结果**必须对照短板域清单**，不能只报等级——对外材料建议同时给"总分 + 短板域数"。

## 复用与融合
- **融合来源**：`csv-data-wrangler`（按规模选工具决策树）、`duckdb/duckdb-skills`（DuckDB 直查做表画像）。
- 下游：dx-architecture-opt（门禁消费本技能产出）。
- 总控：dx-engagement-orchestrator。

## 参考
- 七道工序方法论：../_shared/references/七道工序方法论.md
- DCMM-DMBOK 对标：../_shared/references/DCMM-DMBOK对标.md
- 数据资产盘点模板：../_shared/references/数据资产盘点模板.md
- 调研问卷模板：../_shared/assets/调研问卷模板.md
- 资产目录模板：../_shared/assets/数据资产目录模板.md
- 评分脚本：../_shared/scripts/maturity_score.py
- 扫描脚本：../_shared/scripts/scan_assets.py
