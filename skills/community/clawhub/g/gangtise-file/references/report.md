# 研究报告调用指导

## 简介

按关键词、证券、日期、机构、行业、来源类型、荣誉类型等条件检索研究报告，返回文件 ID、标题、摘要等元数据。主脚本：`scripts/report.py`。行业、机构提供枚举值接口（`scripts/get_industries.py`、`scripts/get_institutions.py`）；其余参数**无枚举值接口**，由后端**智能匹配**用户传入的文本。证券代码需传入标准格式（如 `000001.SZ`）。

## 主脚本：执行检索

| 参数 | 必填 | 说明 |
|------|------|------|
| `-k` / `--keyword` | 否 | 检索关键词，可为空。 |
| `-sd` / `--start_date` | 否 | 开始日期，如 `2026-01-01`。 |
| `-ed` / `--end_date` | 否 | 结束日期，如 `2026-12-31`。 |
| `-l` / `--limit` | 否 | 返回数量上限，默认由系统配置。 |
| `--securities` | 否 | 证券代码列表，逗号分隔；必须为标准证券代码，如 `000001.SZ`。 |
| `--institutions` | 否 | 机构名称，逗号分隔；可选值见枚举脚本。 |
| `--industries` | 否 | 行业名称，逗号分隔；可选值见枚举脚本。 |
| `--source_types` | 否 | 来源类型，逗号分隔；可选值：`研报`、`公众号`。 |
| `--honor_types` | 否 | 荣誉类型，逗号分隔；可选值：`新财富`、`金牛`、`水晶球`。 |
| `--deep` | 否 | 是否仅限深度报告（flag 参数，传入即启用）。 |
| `-d` / `--download` | 否 | 是否在检索后自动下载所有对应研究报告文件，默认不下载。 |
| `-od` / `--output_dir` | 否 | 所有下载文件保存的目录，建议使用绝对路径。默认保存在 gangtise 工作目录下的 `report` 目录。 |
| `-dt` / `--download-types` | 否 | 下载文件类型，逗号分隔。可选：pdf, markdown。 |

**无枚举值接口的参数**（如 `keyword`、`securities` 等）：直接传入用户意图相关文本，后端会**智能匹配**，无需先查枚举。

## 枚举值脚本：获取参数可选值

- **行业**：执行 `scripts/get_industries.py` 获取行业列表。
- **机构**：执行 `scripts/get_institutions.py` 获取机构列表。

```bash
python3 scripts/get_industries.py
python3 scripts/get_institutions.py
```

## 调用示例

**按关键词 + 时间 + 数量：**
```bash
python3 scripts/report.py -k 比亚迪 -sd 2026-01-01 -ed 2026-12-31 -l 20
```

**按关键词 + 来源 + 行业 + 荣誉类型：**
```bash
python3 scripts/report.py -k 新能源 --source_types 研报 --industries 电力设备 --honor_types 新财富
```

**按证券 + 关键词：**
```bash
python3 scripts/report.py -k 业绩 --securities 300750.SZ,002594.SZ
```

**仅深度报告：**
```bash
python3 scripts/report.py -k 锂电 --deep
```

**检索并自动下载研究报告：**
```bash
python3 scripts/report.py -k 新能源 --industries 电力设备 -sd 2026-01-01 -ed 2026-12-31 -d true
```

## 返回说明

- **成功**：返回文件列表（含 file_id、标题、摘要等），可通过`python3 scripts/get_file.py --file-id <file_id> --file-type "研究报告"`下载。
- **失败**：返回错误信息。
