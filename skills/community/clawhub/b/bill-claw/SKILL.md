---
name: billclaw
description: Drives the BillClaw local bookkeeping CLI against SQLite (db/expenses.db) via scripts/main.py JSON subcommands—add/query transactions, delete and category-merge with preview+confirm, user-defined categories, reports with chart PNGs, CSV export, and a local Flask dashboard. Use when the user tracks 记账/收支/账本, manages 分类, asks for 报表 or charts, wants to open the Web 看板, exports CSV, or mentions BillClaw or running main.py (root shim) / scripts/main.py.
---

# BillClaw 记账 Skill（OpenClaw / Agent 使用说明）

本 Skill 通过本地 **Python CLI** 操作 **SQLite** 账本（`db/expenses.db`），实现记账、分类管理、报表图表与 Web 看板。Agent 负责自然语言理解与**二次确认**；脚本负责结构化读写与一致性。

---

## 1. 功能概览

- 记账（结构化字段；可选 `parse_text` 辅助从片段补全字段）
- 条件查询（日期范围、类型、分类、备注关键词等）
- 删除（**先 preview 列候选，用户确认后再 confirm**）
- 分类归并（**先 preview，用户确认后再批量改 category**）
- 用户自定义分类（`user_categories` 表；记账时 `category` 可直接用自定义名）
- 报表：深色主题多图 PNG（**合图** `report_dashboard.png`：KPI + 支出/收入环形图 + 每日趋势 + 按月柱图；另有单图 `expense_by_category.png`、`income_by_category.png`、`daily_trend.png`、`monthly_bar.png`）+ 结构化 `highlights`（供你生成有温度的中文总结）；`data.agent_json` 中含 `primary_chart` 指向合图路径
- Web 看板：本地 Flask + `scripts/dashboard.html` + `scripts/static/vendor` 内 Chart.js，支持时间筛选、按月柱状图、分页明细与图表交互（缩放/平移等），离线可开页
- 导出 CSV（可选）

**环境变量**：`BILLCLAW_DB_PATH` 可覆盖默认数据库路径。

**调用方式**：在项目根目录执行 `python scripts/main.py <子命令> --json-string '<JSON>'` 或 `--json 文件.json`；亦可使用根目录 `python main.py ...`（转发到同一入口）。**标准输出为一行 JSON**：`{"ok": bool, "error": str|null, "data": {...}}`。

---

## 2. 用户意图（Intent）与处理流程

### Intent A：记一笔账

1. 从用户话中提取：`date`（YYYY-MM-DD）、`type`（`收入`|`支出`）、`category`、`amount`（元）、`note`。
2. 若字段不全，可调用 `parse` 子命令辅助：  
   `python scripts/main.py parse --json-string '{"text":"<用户原句或片段>"}'`  
   使用返回的 `time.date`、`amount.value`、`type_hint`、`category_hint` 补全（仍需你判断是否ambiguous）。
3. **时间模糊**：若 `parse` 或你的理解中 `ambiguous: true`，**先问用户确认日期/时刻**，再 `add`。
4. **金额异常**：若 `add` 的 `data` 中含 `suspicious: true`，**先向用户确认是否输错**，再决定是否重新 `add` 或取消。
5. 写入：  
   `python scripts/main.py add --json-string '{"date":"...","type":"支出","category":"正餐","amount":35,"note":"..."}'`  
   可选：`"parse_text":"昨天午饭38"` 与上述字段合并（缺省字段由解析补全）。

**默认支出分类**：正餐、零食饮料、出行、购物、日常开销、娱乐、居住、医疗健康、家人、社交、其他。  
**默认收入分类**：工资、奖金、投资、家人、其他收入。  
用户自定义分类可先走 Intent D，之后记账 `category` 填该名称即可。

---

### Intent B：查账 / 列表

`python scripts/main.py query --json-string '{...}'`

常用字段：

- `date_from`, `date_to`（含边界，格式建议 `YYYY-MM-DD`）
- `type`：`收入` / `支出`
- `category`：精确匹配
- `category_like`：SQL LIKE 子串
- `note_like`：备注 LIKE
- `keyword_in_note`：备注或分类中包含关键词
- `limit`：默认 500

将 `data.rows` 用简洁表格或列表回复用户。

---

### Intent C：删除记录

**禁止直接删除。** 必须两步：

1. `delete-preview`：与 `query` 相同过滤字段，返回 `data.preview_rows` 与 `data.ids`。  
2. 向用户展示将删除的记录，**得到明确确认**后：  
   `delete-confirm`：`{"ids":[...]}`

---

### Intent D：新增自定义分类

`python scripts/main.py category-add --json-string '{"name":"恋爱","kind":"支出"}'`  
`kind` 只能是 `收入` 或 `支出`。  
可用 `category-list` 查看已有用户分类。

---

### Intent E：分类归并（把一批记录改到新类）

1. `merge-preview`：用 `keyword_in_note`、`old_category`、`old_category_like`、`date_from`/`date_to`、`type`（默认可筛支出）等缩小范围。  
2. 展示 `preview_rows`，**用户确认**后：  
   `merge-confirm`：`{"ids":[...],"new_category":"恋爱"}`

---

### Intent F：报表（图表 + 口语化总结）

`python scripts/main.py report --json-string '{"date_from":"2026-03-01","date_to":"2026-03-31","output_dir":"./billclaw_output"}'`

- `data.charts`：各 PNG 绝对路径；**优先向用户展示** `report_dashboard`（或 `data.agent_json` 里的 `primary_chart`）。兼容旧键名：`expense_pie`≈支出分类图，`trend`≈每日趋势。
- `data.highlights`：总收支、TOP 支出类、占比等。
- `data.narrative_hints`：简短提示句；**你应在此基础上**用朋友/恋人语气写 1～3 句中文总结（可轻微幽默），避免机械罗列数字。
- 图表文件落在 `output_dir`（见下方「output 目录与定时清理」）；多次 `report` 会累积 PNG，需按需或定期清理。

---

### Intent G：打开 Web 看板

`python scripts/main.py serve --json-string '{"host":"127.0.0.1","port":8000}'`  
（进程会占用终端，需告知用户浏览器访问 `http://127.0.0.1:8000`。）

页面含：日期范围筛选与快捷预设（全部/本年至今/近三月/近一月）、总收支 KPI、**支出与收入分类**环形图、每日折线（滚轮缩放/拖拽平移，可重置）、按月收支柱状图、可排序分页交易表（可选仅收入/仅支出）。前端为 `scripts/dashboard.html`，JS 库在 `scripts/static/vendor/`（离线可用，见该目录 `README.md`）；中文字体使用系统字体栈。

---

### Intent H：导出 CSV（可选）

`python scripts/main.py export-csv --json-string '{"path":"./bills.csv","date_from":"2026-01-01"}'`

---

## 3. 子命令一览

| 子命令 | 作用 |
|--------|------|
| `add` | 插入一条交易 |
| `query` | 条件查询 |
| `delete-preview` / `delete-confirm` | 删除预览 / 执行删除 |
| `merge-preview` / `merge-confirm` | 改类预览 / 执行批量更新 category |
| `category-add` / `category-list` | 自定义分类 |
| `report` | 统计 + 出图 |
| `export-csv` | 导出 |
| `parse` | 从文本抽取时间/金额/类型/分类提示 |
| `serve` | 启动 Flask 看板 |

---

## 4. 输入 / 输出约定

- **成功**：`ok: true`，`data` 为有效负载。
- **失败**：`ok: false`，`error` 为可读说明。
- `add` 在写入成功后仍可能在 `data` 中带 `suspicious`（金额超参考阈值），**不代表未写入**；若你希望「先确认再记」，应在调用 `add` 前用规则判断或先问用户（推荐流程：先展示将记入的字段与异常提示，确认后再 `add`）。

---

## 5. 示例对话（覆盖常见场景）

### 5.1 正常记账

- 用户：「今天中午吃饭花了 42」  
- 你：解析为日期今天、支出、正餐 42 元 → `add`。回复简短确认。

### 5.2 模糊时间

- 用户：「晚上看电影 80」  
- 你：`parse` 若带 `ambiguous` 或 note 提示晚上默认 20:00 → **问用户是否指今晚/哪一天的晚上** → 确认后再 `add`。

### 5.3 金额异常

- 用户：「零食 10000」  
- 你：先警告可能多打一个 0，`add` 后若返回 `suspicious` 同样要口头确认；用户确认无误再保留。

### 5.4 新增分类

- 用户：「加个恋爱分类，支出用的」  
- 你：`category-add`，再说明以后可直接说「恋爱」类消费。

### 5.5 删除记录

- 用户：「删掉昨天所有打车」  
- 你：`delete-preview`（`date_from`/`date_to` 卡昨天 + `keyword_in_note` 或分类/备注）→ 列出 → 用户说「确认删」→ `delete-confirm`。

### 5.6 报表

- 用户：「看下这个月花销」  
- 你：`report` 传本月日期范围 → 发图路径 + 个性化短评。

### 5.7 Web 看板

- 用户：「打开账本网页」  
- 你：启动 `serve`，给出本机 URL，并说明需在本机浏览器打开。

---

## 6. 异常与用户确认策略（必须遵守）

1. **删除、批量改分类**：必须 preview → 用户明确确认 → confirm。  
2. **时间不确定**：追问具体日期。  
3. **金额与场景明显不符**：追问是否输错。  
4. **类型不明**：问清收入还是支出。  
5. **输出风格**：简洁、有温度；避免生硬系统提示腔。

---

## 7. 文件与依赖

- 脚本：`scripts/main.py`、`scripts/parser.py`、`scripts/db.py`、`scripts/report.py`、`scripts/web.py`、`scripts/utils.py`、`scripts/dashboard.html`、`scripts/static/vendor/`（看板 JS 依赖）
- 安装与命令示例：[SETUP.md](SETUP.md)

若 `serve` 或 `report` 报错缺依赖，提示用户执行 `pip install -r requirements.txt`。

---

## 8. output 目录与定时清理

- **目录含义**：`report` 将合图与单图 PNG 写入 `output_dir`。未传时默认为**当前工作目录**下的 `billclaw_output/`（与显式传 `./billclaw_output` 等价，取决于执行 `main.py` 时的 cwd）。这些文件仅为报表缓存/附件，**不替代** SQLite 账本（`db/expenses.db`）。
- **为何要清理**：同一目录下反复生成会堆积同名或带时间戳的文件，长期占用磁盘；对话中若用户关心空间、目录杂乱、或希望「整理报表文件」，应说明该目录用途与可清理性。
- **Agent 行为**：**删除磁盘文件前须征得用户明确同意**；同意后可删除该 `output_dir` 下过期的 PNG（或按用户指定的保留策略，例如只保留最近 N 天/最近一次生成）。删除前用一两句话说明将删的是报表图片、不涉及账本数据。
- **系统级定时清理（可选）**：若用户希望在无人值守时自动清理，可建议用本机 **cron**（Linux/macOS）或 **launchd**（macOS）定期删除指定 `output_dir` 下的 `*.png`（或整目录内旧文件），具体路径与保留天数由用户自行配置；Agent 不擅自替用户配置系统定时任务，除非用户明确要求协助编写命令或 plist 片段。
