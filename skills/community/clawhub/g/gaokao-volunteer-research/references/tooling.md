# 工具层说明

`scripts/gaokao_toolkit.py` 是本 skill 的确定性工具入口。它不替代官方系统，也不保证所有省份页面格式都能自动解析；它负责把可查证资料保存、结构化和校验，失败时输出可定位的错误。

## 1. 官方入口索引

查询省份官方入口：

```bash
python3 scripts/gaokao_toolkit.py index lookup --province 广东
```

校验索引里的 URL 是否可访问：

```bash
python3 scripts/gaokao_toolkit.py index verify --province 广东
```

索引文件：`data/official-source-index.json`。省级 URL 是入口种子，使用前仍要进入当年高考专题或省考试院发布页核验。

## 2. 页面和章程快照

保存官方页面、PDF、招生章程或政策文档：

```bash
python3 scripts/gaokao_toolkit.py snapshot \
  --url "https://example.edu.cn/admission/2026-charter.html" \
  --out "/tmp/gaokao-research/raw" \
  --source-name "示例大学 2026 年招生章程" \
  --source-type charter \
  --province 广东 \
  --year 2026
```

输出：

- 原始文件快照。
- 同名 `.meta.json`，包含 URL、抓取时间、content-type、sha256、来源名称、年份、省份和类型。

## 3. 一分一段和批次线解析

解析 CSV、TSV、Markdown 表格或简单 HTML 表格：

```bash
python3 scripts/gaokao_toolkit.py parse-table \
  --input tests/fixtures/guangdong-score-table.md \
  --out /tmp/score-table.json \
  --kind score \
  --province 广东 \
  --year 2026 \
  --category 物理类
```

批次线同样使用 `parse-table`，把 `--kind` 改成 `cutoff`。输出 JSON 会保留原始列名，并尽量标准化出 `score`、`rank`、`batch`、`cutoff_score` 等字段。

## 4. 研究包一致性校验

校验研究包是否缺关键文件、缺 URL、口径不一致或出现禁止表达：

```bash
python3 scripts/gaokao_toolkit.py validate-package \
  --dir tests/fixtures/sample-package \
  --province 广东 \
  --year 2026 \
  --category 物理类
```

输出 JSON：`ok`、`errors`、`warnings`。

## 5. 回归测试样例

运行真实省份行为样例的静态检查：

```bash
python3 scripts/gaokao_toolkit.py regression --cases tests/regression-cases.json
```

这些样例检查 skill 文档是否继续覆盖必要触发词、禁止表达和文件交付要求。它不验证真实录取结果。
