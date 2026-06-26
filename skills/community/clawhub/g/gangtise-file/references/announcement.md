# 公司公告调用指导

## 简介

按证券、关键词、日期等条件检索公司公告，返回文件 ID、标题等元数据。主脚本：`scripts/announcement.py`。参数（关键词、证券等）**无枚举值接口**，由后端**智能匹配**。证券代码需传入标准格式（如 `000001.SZ`）。

重要说明：**试用账号只能查询一个月内的公告**（以接口权限校验为准）。

## 主脚本：执行检索

| 参数 | 必填 | 说明 |
|------|------|------|
| `-k` / `--keyword` | 否 | 检索关键词，可为空。 |
| `--securities` | 否 | 证券代码列表，逗号分隔；必须为标准证券代码，如 `000001.SZ`。 |
| `-sd` / `--start_date` | 否 | 开始日期，如 `2026-01-01`。 |
| `-ed` / `--end_date` | 否 | 结束日期，如 `2026-12-31`。 |
| `--category_list` | 否 | 公告分类列表，逗号分隔（可直接传 categoryId；或传分类名称并在 `utils.ANNOUNCEMENT_CATEGORY_MAP` 中配置映射）。 |
| `--search_type` | 否 | 搜索类型：1-标题搜索 2-全文搜索。 |
| `--rank_type` | 否 | 排序方式：1-综合排序 2-时间倒序。 |
| `-l` / `--limit` | 否 | 返回数量上限。 |
| `-d` / `--download` | 否 | 是否在检索后自动下载所有对应公司公告文件，默认不下载。 |
| `-od` / `--output_dir` | 否 | 所有下载文件保存的目录，建议使用绝对路径。默认保存在 gangtise 工作目录下的 `announcements` 目录。 |
| `-dt` / `--download-types` | 否 | 下载文件类型，逗号分隔。可选：pdf, markdown。 |

**无枚举值接口的参数**（如 `keyword`、`securities`）：直接传入用户意图相关文本，后端会**智能匹配**。

## 调用示例

**按证券 + 关键词 + 时间：**
```bash
python3 scripts/announcement.py --securities 000858.SZ -k 业绩 -sd 2026-01-01 -ed 2026-12-31
```

**按关键词：**
```bash
python3 scripts/announcement.py -k 分红
```

**检索并自动下载公司公告：**
```bash
python3 scripts/announcement.py --securities 000858.SZ -k 业绩 -sd 2026-01-01 -ed 2026-12-31 -d true
```

## 返回说明

- **成功**：返回文件列表（含 file_id、标题等），可通过`python3 scripts/get_file.py --file-id <file_id> --file-type "公司公告"`下载。
- **失败**：返回错误信息。
