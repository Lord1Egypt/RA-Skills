# 首席观点调用指导

## 简介

按关键词、证券、券商、研究方向、首席分析师、概念、投研标签、来源类型等条件检索**首席观点**列表，返回观点 ID、标题、正文摘要及作者与关联标的等元数据。主脚本：`scripts/opinion.py`。券商提供枚举值接口（`scripts/get_institutions.py`）；研究方向提供枚举值接口（`scripts/get_industries.py`）；其余如无枚举接口的参数由用户传入 ID 或关键词，证券代码需标准格式（如 `000001.SZ`）。

## 主脚本：执行检索

| 参数 | 必填 | 说明 |
|------|------|------|
| `-k` / `--keyword` | 否 | 搜索关键词；可为空。 |
| `-sd` / `--start_date` | 否 | 开始日期，格式 `YYYY-MM-DD`。 |
| `-ed` / `--end_date` | 否 | 结束日期，格式 `YYYY-MM-DD`。 |
| `-l` / `--limit` | 否 | 返回数量上限。 |
| `--rank_type` | 否 | 排序：`1` 综合排序（默认），`2` 时间倒序。 |
| `--securities` | 否 | 证券代码列表，逗号分隔；标准格式如 `000001.SZ`。 |
| `--industries` | 否 | **研究方向**列表，逗号分隔；传入宏观/策略/固收/金工/海外等名称，脚本映射为 `researchAreaList`（**不使用** `industryList`）。 |
| `--institutions` | 否 | 发布机构（券商），逗号分隔；可选值见枚举脚本。 |
| `--chiefs` | 否 | 首席分析师 ID 列表，逗号分隔。暂不支持匹配。 |
| `--concepts` | 否 | 概念 ID 列表，逗号分隔。暂不支持匹配。 |
| `--llm_tags` | 否 | 投研业务标签，逗号分隔。可选：`strongRcmd`（强烈推荐）、`earningsReview`（业绩点评）、`topBroker`（头部券商）、`newFortune`（新财富团队）；也可传中文（强烈推荐/业绩点评/头部券商/新财富团队）。 |
| `--source_types` | 否 | 来源，逗号分隔。可选：`realTime`（实时）、`openSource`（开放来源）；也可传中文（实时/开放来源）。 |

**无枚举值接口的参数**（如 `keyword`、`chiefs`、`concepts`）：按用户意图直接传入；概念、首席等一般为**业务 ID**，请以平台侧数据为准。

## 枚举值脚本：获取参数可选值

- **券商（发布机构）**：执行 `scripts/get_institutions.py` 获取机构列表。

```bash
python3 scripts/get_institutions.py
```

## 调用示例

**按关键词 + 投研标签 + 来源：**

```bash
python3 scripts/opinion.py -k 半导体 --llm_tags strongRcmd --source_types realTime -l 20
```

**按券商 + 研究方向（宏观/策略/固收/金工/海外等）：**

```bash
python3 scripts/opinion.py --institutions 兴业证券 --industries 宏观,策略 -l 20
```

注意：参数名仍为 `--industries`，但本接口实际发往 `researchAreaList`（研究方向 ID），**不使用** `industryList`；与 `summary.py` 中「行业 + 研究方向混合解析」的用法不同。

**按时间范围 + 排序：**

```bash
python3 scripts/opinion.py -sd 2026-03-01 -ed 2026-03-30 --rank_type 2 -l 30
```

## 返回说明

- **成功**：返回观点列表（含观点 ID、标题、正文摘要、作者与券商、关联证券/行业/概念、标签等）。本接口为列表查询，**不包含**与 `get_file.py` 绑定的文件下载流程；若后续开放与文件中心一致的下载方式，以接口文档为准。
- **失败**：返回错误信息。
