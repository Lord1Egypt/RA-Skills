# Chapter Parsing Reference

## 合并脚本使用说明

所有章节切分和拼接逻辑由 `scripts/merge.py` 完成，AI 只需按 SKILL.md 流程调用脚本。

## Part 标题匹配正则（merge.py 内部使用）

```python
import re

# 能匹配的格式：
# # **Part1：【AI优先：本周核心工作复盘总结】**
# # Part1：【AI优先：本周核心工作复盘总结】
# # **Part 1: xxx**
# # Part 1: xxx

pattern = r'^#\s*\*?Part\s*(\d)\s*【(.+?)】\s*$'
```

## 人员姓名提取

来源优先级：
1. 从 `feishu_fetch_doc` 返回的 `title` 字段提取中括号内姓名，如 `[AIO]-[通信行业中心]-[阿拉法特]-2026-04-06` → `阿拉法特`
2. 从 URL 路径中无规律时，使用消息中的列出顺序 + 序号作为标识（如「文档1」「文档2」）
3. 实在无法判断时，用 `doc_id` 前6位作为临时标识

## 错误处理

| 场景 | 处理方式 |
|------|---------|
| 某文档某 Part 缺失 | 该 Part 下跳过该员工，不留空占位 |
| `feishu_fetch_doc` 返回 forBidden | 跳过该文档，继续处理其他文档 |
| `feishu_fetch_doc` 触发频率限制 | 等 3 秒重试一次 |
| fetch 失败超过 2 次 | 跳过该文档 |
| 文档内容为空 | 跳过该文档 |

## 合并顺序

严格按照用户在消息中列出的文档顺序（URL 出现顺序）依次拼接，不做字母序或部门排序。

## 新文档标题命名

```python
from datetime import datetime

names = ["阿拉法特", "陈功彬", "丁丁"]
current_month = datetime.now().strftime("%Y-%m")  # "2026-04"

title = f"[AIO]-[{'/'.join(names)}]-周报合并-{current_month}"
# → "[AIO]-[阿拉法特/陈功彬/丁丁]-周报合并-2026-04"
```

## 临时文件清理

合并完成后，AI 应清理临时文件：
```bash
rm -f /tmp/merge_doc_*.md
```
