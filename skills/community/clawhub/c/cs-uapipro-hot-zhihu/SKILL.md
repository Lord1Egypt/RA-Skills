---
name: cs-uapipro-hot-zhihu
description: |
  抓取知乎热榜，使用 UAPIPRO API（https://uapis.cn）。当用户询问"知乎热榜"、"知乎热搜"、"知乎热门"时触发。
  需要环境变量 UAPIPRO_API_KEY。
---

# 知乎热榜 - UAPIPRO API

通过 UAPIPRO API 获取知乎热榜数据。

## 快速使用

直接通过 exec 调用脚本：

```bash
# 获取完整热榜
python3 scripts/zhihu_hot.py

# 获取前10条
python3 scripts/zhihu_hot.py 10

# JSON格式输出
python3 scripts/zhihu_hot.py --json
python3 scripts/zhihu_hot.py 10 --json
```

## API 信息

- **接口**: `GET https://uapis.cn/api/v1/misc/hotboard?type=zhihu`
- **认证**: `Authorization: Bearer <UAPIPRO_API_KEY>`
- **返回**: 知乎热榜列表，每条包含 index、title、url、hot_value、extra(可选 desc/image/label)
- **更新**: 约几分钟一次

## 脚本用法

```bash
python3 zhihu_hot.py [N] [--json|-j]
```

- `N` - 返回前N条（不传则返回全部，约50条）
- `--json` - 以 JSON 格式输出（用于程序调用）

## 返回字段说明

| 字段 | 说明 |
|------|------|
| index | 排名序号 |
| title | 问题标题 |
| url | 问题链接 |
| hot_value | 热度值，如"634 万热度" |
| extra.desc | 问题描述/摘要 |
| extra.image | 配图URL（相对路径） |
| extra.label | 标签，如"新" |

## Python 调用示例

```python
import subprocess
import json
import os

# 调用脚本获取JSON输出
result = subprocess.run(
    ["python3", "scripts/zhihu_hot.py", "10", "--json"],
    capture_output=True, text=True,
    env={**os.environ, "UAPIPRO_API_KEY": os.environ.get("UAPIPRO_API_KEY", "")}
)
data = json.loads(result.stdout)
for item in data["list"]:
    print(item["index"], item["title"])
```

## 老大输出格式偏好

标题：XXX（热度：XXX）
原文链接：XXX

每次回复知乎热榜时统一使用此格式。
