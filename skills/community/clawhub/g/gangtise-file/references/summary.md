# 会议纪要调用指导

## 简介

按关键词、证券、机构、行业、来源类型、会议类别/市场/参会人角色等条件检索会议纪要，返回文件 ID、标题、摘要等元数据。主脚本：`scripts/summary.py`。行业、机构提供枚举值接口（`scripts/get_industries.py`、`scripts/get_institutions.py`）；其余参数（关键词、证券等）**无枚举值接口**，由后端**智能匹配**。证券代码需传入标准格式（如 `000001.SZ`）。

## 主脚本：执行检索

| 参数 | 必填 | 说明 |
|------|------|------|
| `-k` / `--keyword` | 否 | 检索关键词；可为空。 |
| `-sd` / `--start_date` | 否 | 开始日期，格式 `YYYY-MM-DD`。 |
| `-ed` / `--end_date` | 否 | 结束日期，格式 `YYYY-MM-DD`。 |
| `-l` / `--limit` | 否 | 返回数量上限。 |
| `--securities` | 否 | 证券代码列表，逗号分隔；必须为标准证券代码，如 `000001.SZ`。 |
| `--institutions` | 否 | 机构，逗号分隔；可选值见枚举脚本。 |
| `--industries` | 否 | 行业，逗号分隔；可选值见枚举脚本。 |
| `--source_types` | 否 | 来源类型，逗号分隔；可选值：`会议平台`、`网络资源`、`公司公告`。 |
| `--category_list` | 否 | 会议类别，逗号分隔。可选值：`earningsCall`、`strategyMeeting`、`fundRoadshow`、`shareholdersMeeting`、`maMeeting`、`specialMeeting`、`companyAnalysis`、`industryAnalysis`、`other`（也支持中文：`业绩会`、`策略会`、`基金路演`、`股东大会`、`并购会议`、`特别会议`、`公司分析`、`行业分析`、`其他`）。 |
| `--market_list` | 否 | 纪要所属市场类别，逗号分隔。可选值：`aShares`、`hkStocks`、`usChinaConcept`、`usStocks`（也支持中文：`A股`、`港股`、`美股中概`、`美股`）。 |
| `--participant_role_list` | 否 | 特殊参会人标识，逗号分隔。可选值：`management`、`expert`（也支持中文：`高管`、`专家`）。 |
| `-d` / `--download` | 否 | 是否下载文件。 |
| `-od` / `--output_dir` | 否 | 下载文件保存路径。 |
| `-dt` / `--download-types` | 否 | 下载文件类型，逗号分隔。可选：pdf, markdown。 |

**无枚举值接口的参数**（如 `keyword`、`securities`）：直接传入用户意图相关文本，后端会**智能匹配**。

## 枚举值脚本：获取参数可选值

- **行业**：执行 `scripts/get_industries.py` 获取行业列表。
- **机构**：执行 `scripts/get_institutions.py` 获取机构列表。

```bash
python3 scripts/get_industries.py
python3 scripts/get_institutions.py
```

## 调用示例

**按关键词 + 会议类别：**
```bash
python3 scripts/summary.py -k 锂电 --category_list earningsCall -l 20
```

**按证券 + 行业：**
```bash
python3 scripts/summary.py --securities 002594.SZ --industries 汽车
```

**按时间范围 + 来源：**
```bash
python3 scripts/summary.py -k 储能 -sd 2026-01-01 -ed 2026-06-30 --source_types 会议平台
```

**按市场 + 参会人角色：**
```bash
python3 scripts/summary.py -k AI --market_list aShares --participant_role_list management -l 20
```

## 返回说明

- **成功**：返回文件列表（含 file_id、标题、摘要等），可通过`python3 scripts/get_file.py --file-id <file_id> --file-type "会议纪要"`下载。
- **失败**：返回错误信息。
