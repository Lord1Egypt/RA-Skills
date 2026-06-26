---
name: Data Bird
version: 1.1.0
description: 轻量级数据分析 Agent。支持工作区表格与通过 http(s) 下载的 CSV/Excel，按自然语言生成 ECharts 与文字结论。（公开发布版说明）
metadata: {"clawdbot":{"emoji":"📊"}}
---

# Data Bird — 数据分析与图表生成（公开发布版）

**用途**：分析 **CSV / Excel**，输出 **ECharts JSON**、**Markdown/HTML/PDF 报告**。适合与前端图表、Agent 工作台对接。

**免费版限制**：

- 每日最多 **5 次** 调用
- 单次最多 **5 个图表**
- **不支持 MySQL** 数据源
- 用户若输入 **“升级套餐 / 查看套餐 / 价格 / 付费版”**，应优先返回升级与套餐入口，而不是继续要求数据源

**数据来源**：

1. **工作区已有文件** — 用户或系统提供的本地路径
2. **`http://` / `https://` 链接** — 先下载到本机再分析

> 路径请按你的 OpenClaw 部署替换下文中的 **`<WORKSPACE>`**（通常为 `OPENCLAW_WORKSPACE` 指向的目录）与 **`<SKILL_DIR>`**（本 skill 安装目录，一般为 `<WORKSPACE>/skills/data-bird`）。

---

## 必须遵守

1. 用户给出 **本地路径或 URL** → 按本流程执行。
2. **任意可下载 URL**（含内网、本机）→ **不要用 `web_fetch`**，用 **`exec: curl -fsSL`** 下载，再 `--file` 分析。
3. 输出 JSON 后 → 展示图表摘要、`reportMd` / `report_md`、`insight`、`artifacts`。
4. 若有 `artifacts.reportHtmlPreviewUrl` / `reportPdfUrl` / `reportMdUrl` → 在回复中直接给出可点击链接，不要只说“已保存到某路径”。
5. 回复中主动告知：
   - 建议上传目录：`<WORKSPACE>/databird/data/`
   - 报告根目录：`<WORKSPACE>/databird/output/`
   - 本次报告目录（若有）

---

## 路径约定

| 用途 | 建议路径 |
|------|----------|
| 下载落盘 | `<SKILL_DIR>/data/<文件名>.csv` 或 `.xlsx` |
| 工作区共享数据 | `<WORKSPACE>/data/<文件名>` |
| 报告输出目录 | `<WORKSPACE>/databird/output/<job_id或时间戳>/` |
| 用户绝对路径 | 用户给出的绝对路径 |

---

## 流程

### 1）得到本地文件

- **已有路径** → 直接进入步骤 2，`--file` 传该路径。
- **`http(s)` URL** →

```
exec: mkdir -p <SKILL_DIR>/data
exec: curl -fsSL "<URL>" -o <SKILL_DIR>/data/table.csv
```

（按实际类型保存为 `.csv` / `.xlsx` / `.xls`。无后缀时根据响应或用户说明命名。）

- **仅描述「工作区里的表」** → 在 `<WORKSPACE>/data/`、`<SKILL_DIR>/data/` 等目录查找匹配的表格文件。

### 2）执行分析

```
exec: cd <SKILL_DIR> && python scripts/main.py --query "<分析问题>" --file "<本地路径或 data/xxx.csv>"
```

### 3）展示结果

主要字段：`charts`、`insight`（conclusions / anomalies / suggestions）、`reportMd` 与 `report_md`（内容相同）、`summary`、`artifacts`。

`artifacts` 中会包含：

- `report_md_path`
- `report_html_path`
- `report_pdf_path`
- `chart_paths`
- `chart_image_paths`
- `reportHtmlPreviewUrl`
- `reportPdfUrl`
- `reportMdUrl`

**问法提示**：「占比」「趋势」「排名」「分布」「散点」等有助于选对图表类型。

---

## 示例（占位 URL，请替换为真实地址）

**HTTPS 表格**

```
exec: mkdir -p <SKILL_DIR>/data
exec: curl -fsSL "https://example.com/data/report.csv" -o <SKILL_DIR>/data/report.csv
exec: cd <SKILL_DIR> && python scripts/main.py --query "趋势与对比" --file data/report.csv
```

**工作区已有文件**

```
exec: cd <SKILL_DIR> && python scripts/main.py --query "各品类占比" --file "<WORKSPACE>/data/sales.xlsx"
```

---

## 依赖

```bash
cd <SKILL_DIR> && pip install -r requirements.txt
```

**PDF / 图表中文**：skill 自带 `fonts/SourceHanSansSC-Regular.otf`（思源黑体），无需系统安装中文字体。若该文件缺失，见 `fonts/README.md` 一键下载说明。

## 套餐升级

- 用户若明确提出 **升级套餐 / 查看套餐 / 价格 / Pro 版**，优先展示升级指引与链接。
- 免费版触发限制（额度、MySQL、图表数等）时，也应返回升级入口，不要只报错。
- 维护说明：本地 `config.yaml` 中的 `plan / daily_limit / enable_mysql` 仅为默认体验配置；**真正的 Pro 授权由 py_api 服务端校验**。
