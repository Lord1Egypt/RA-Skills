# 归档元数据头模板

> 每份归档文件开头必须包含以下元数据头。
> 元数据头使用 YAML frontmatter 格式，方便检索和去重。

---

## 模板

```markdown
---
task_name: "<任务名>"
run_time: "<YYYY-MM-DD HH:MM:SS>"
data_source: "<数据源>"
status: "<success/partial/failed>"
error_count: <N>
archived_to: ["feishu_drive", "obsidian", "ima"]
---

# <简报标题>

<简报正文>
```

---

## 字段说明

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| task_name | string | 是 | 任务名称 | "ClawHub Daily" |
| run_time | string | 是 | 运行时间 (ISO 8601) | "2026-07-11 09:00:23" |
| data_source | string | 是 | 数据源（逗号分隔） | "ClawHub API, Convex" |
| status | string | 是 | 运行状态 | "success" / "partial" / "failed" |
| error_count | int | 是 | 错误数量 | 0 |
| archived_to | array | 是 | 已归档到的端 | ["obsidian", "ima"] |

---

## 状态定义

| status | 含义 | archived_to 预期 |
|--------|------|-----------------|
| success | 主任务成功，三端全部归档 | ["feishu_drive", "obsidian", "ima"] |
| partial | 主任务成功，部分端归档失败 | ["obsidian"] (缺失的端不列出) |
| failed | 主任务失败 | [] (无归档) |

---

## 生成代码

```python
import json
from datetime import datetime

def generate_metadata_header(task_name, data_source, status, error_count, archived_to):
    """Generate YAML frontmatter metadata header."""
    return f"""---
task_name: "{task_name}"
run_time: "{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
data_source: "{data_source}"
status: "{status}"
error_count: {error_count}
archived_to: {json.dumps(archived_to, ensure_ascii=False)}
---"""
```

---

## 完整示例

```markdown
---
task_name: "ClawHub Daily"
run_time: "2026-07-11 09:00:23"
data_source: "ClawHub Convex API"
status: "success"
error_count: 0
archived_to: ["feishu_drive", "obsidian", "ima"]
---

# ClawHub Daily 推荐 - 2026-07-11

## 今日推荐 Top 5

1. **skill-foo** - 自动化办公场景，安装量增长15%
2. **skill-bar** - 开发工具类，新增5星评价
...

## 数据统计
- 抓取总数: 200
- 推荐维度: D1 趋势
- 去重窗口: 7天
```
