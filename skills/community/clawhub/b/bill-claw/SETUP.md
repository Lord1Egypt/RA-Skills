# BillClaw 本地运行

## 环境

- Python 3.10+（建议）
- 依赖见 `requirements.txt`

## 安装

在项目根目录（与 `scripts/`、`requirements.txt` 同级）执行：

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

数据库文件默认路径为 `db/expenses.db`。若需自定义：

```bash
export BILLCLAW_DB_PATH=/绝对路径/自定义.db
```

## CLI（JSON 出参均在 stdout）

工作目录建议为项目根目录，以便相对路径一致。以下命令中的 `python scripts/main.py` 可替换为根目录的 `python main.py`（转发到同一入口）。

```bash
# 记一笔支出
python scripts/main.py add --json-string '{"date":"2026-03-21","type":"支出","category":"正餐","amount":35,"note":"拉面"}'

# 解析自然语言片段（辅助 Agent）
python scripts/main.py parse --json-string '{"text":"昨天打车18块"}'

# 条件查询
python scripts/main.py query --json-string '{"date_from":"2026-03-01","date_to":"2026-03-31","type":"支出"}'

# 删除预览 → 用户确认后再 delete-confirm
python scripts/main.py delete-preview --json-string '{"date_from":"2026-03-20","keyword_in_note":"打车"}'
python scripts/main.py delete-confirm --json-string '{"ids":[1,2]}'

# 分类归并预览 → merge-confirm
python scripts/main.py merge-preview --json-string '{"keyword_in_note":"约会","type":"支出"}'
python scripts/main.py merge-confirm --json-string '{"ids":[3,4],"new_category":"恋爱"}'

# 用户自定义分类（记账时 category 可直接填该名称）
python scripts/main.py category-add --json-string '{"name":"恋爱","kind":"支出"}'
python scripts/main.py category-list --json-string '{}'

# 报表（生成 PNG + highlights）
python scripts/main.py report --json-string '{"date_from":"2026-03-01","date_to":"2026-03-31","output_dir":"./billclaw_output"}'
# 输出目录内主要文件：report_dashboard.png（合图）、expense_by_category.png、income_by_category.png、daily_trend.png、monthly_bar.png

# 导出 CSV
python scripts/main.py export-csv --json-string '{"path":"./export.csv","date_from":"2026-01-01"}'

# Web 看板（阻塞进程，按 Ctrl+C 结束）
python scripts/main.py serve --json-string '{"host":"127.0.0.1","port":8000}'
```

也可将 JSON 写入文件后用 `--json params.json`；或在管道中传入 stdin（非 TTY 时）。

## 报表图表中的中文

`scripts/report.py` 会自动选用系统里常见的中文字体（如 macOS 的 PingFang SC、Windows 的微软雅黑、Linux 的 Noto CJK 等）。若饼图/标题仍显示为方框，请在系统安装一款 CJK 字体，例如 Debian/Ubuntu：`sudo apt install fonts-noto-cjk`，安装后删除 matplotlib 字体缓存再试：`rm -rf ~/.cache/matplotlib`。

## Web 看板静态资源

Chart.js、Hammer、chartjs-plugin-zoom 已置于 `scripts/static/vendor/`，由 Flask 以 `/static/...` 提供，**无需外网**。升级依赖时参见 [scripts/static/vendor/README.md](scripts/static/vendor/README.md)。

## Agent 集成

完整意图、确认策略与字段说明见同目录下的 [SKILL.md](SKILL.md)。
