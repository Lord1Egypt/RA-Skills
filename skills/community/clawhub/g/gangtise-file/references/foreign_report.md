# 外资研报调用指导

## 简介

按关键词、证券、日期、券商、行业、研报类别、区域、语义标签、评级/评级变动、页数范围等条件检索**外资研报列表**，返回研报 ID、标题、摘要等元数据。主脚本：`scripts/foreign_report.py`。行业、券商、区域提供枚举值接口（`scripts/get_industries.py`、`scripts/get_institutions.py`、`scripts/get_regions.py`）；其余参数**无枚举值接口**时由后端**智能匹配**用户传入的文本。境外证券代码格式如 `UBER.N`（见平台「境外股票代码格式规范」）。

## 主脚本：执行检索

| 参数 | 必填 | 说明 |
|------|------|------|
| `-k` / `--keyword` | 否 | 检索关键词，可为空。 |
| `-sd` / `--start_date` | 否 | 开始日期，如 `2026-01-01`。 |
| `-ed` / `--end_date` | 否 | 结束日期，如 `2026-12-31`。 |
| `-l` / `--limit` | 否 | 返回数量上限，默认由系统配置（单页最大 50 条，脚本内分页拉取）。 |
| `--securities` | 否 | 证券代码列表，逗号分隔；境外格式如 `UBER.N`；填股票代码时**主要对公司研究**生效。 |
| `--institutions` | 否 | 券商名称，逗号分隔；可选值见枚举脚本。 |
| `--industries` | 否 | 行业名称，逗号分隔；可选值见枚举脚本。 |
| `--region_list` | 否 | 区域名称，逗号分隔；可选值见枚举脚本。 |
| `--category_list` | 否 | 研报类别，逗号分隔：`macro` / `strategy` / `industry` / `company` / `bond` / `quant` / `morningNotes` / `fund` / `forex` / `futures` / `options` / `warrants` / `market` / `wealthManagement` / `other`。 |
| `--llm_tag_list` | 否 | 语义标签，逗号分隔：`inDepth` / `earningsReview` / `industryStrategy`。 |
| `--rating_list` | 否 | 评级：`buy` / `overweight` / `neutral` / `underweight` / `sell`。 |
| `--rating_change_list` | 否 | 评级变动：`upgrade` / `maintain` / `downgrade` / `initiate`。 |
| `--min_report_pages` | 否 | 研报最小页数。 |
| `--max_report_pages` | 否 | 研报最大页数。 |
| `--search_type` | 否 | `1` 标题搜索，`2` 全文搜索（默认 `1`）。 |
| `--rank_type` | 否 | `1` 综合排序，`2` 时间倒序（默认 `1`）。 |
| `-d` / `--download` | 否 | 是否在检索后自动下载对应外资研报文件，默认不下载。 |
| `-od` / `--output_dir` | 否 | 下载保存目录，建议绝对路径；默认在 gangtise 工作目录下 `foreign_report`。 |
| `-dt` / `--download-types` | 否 | 下载类型，逗号分隔：`pdf`、`markdown`。 |

## 枚举值脚本

- **行业**：`python3 scripts/get_industries.py`
- **券商**：`python3 scripts/get_institutions.py`
- **区域**：`python3 scripts/get_regions.py`

## 调用示例

**关键词 + 时间 + 数量：**

```bash
python3 scripts/foreign_report.py -k 自动驾驶 -sd 2026-02-01 -ed 2026-03-30 -l 20
```

**类别 + 券商 + 语义标签：**

```bash
python3 scripts/foreign_report.py -k 新能源 --category_list industry,company --institutions 摩根大通 --llm_tag_list inDepth -l 15
```

**境外证券代码：**

```bash
python3 scripts/foreign_report.py --securities UBER.N -l 10
```

**检索并下载：**

```bash
python3 scripts/foreign_report.py -k 半导体 -sd 2026-01-01 -ed 2026-03-30 -d true
```

## 返回与下载

- **成功**：返回列表字段含 `类型` 为「外资研报」、`类型中ID` 为 `reportId` 等；下载完整文件使用：

```bash
python3 scripts/get_file.py --file-id <reportId> --file-type "外资研报"
```

- **失败**：返回错误信息；试用账号若超出一个月范围可能被接口拒绝。
