---
name: daily-report-writer
description: 根据输入生成日报 Markdown 草稿并写入 reports 目录
user-invocable: true
metadata: {"openclaw":{"emoji":"📝"}}
---

# Daily Report Writer

## Use when
- 用户要求生成“日报/工作总结草稿”

## Inputs
- date（必填，YYYY-MM-DD）
- highlights（必填，数组）
- blockers（可选，数组）

## Steps
1. 校验参数是否齐全。
2. 读取（或创建）`reports/{{date}}-daily-report.md`。
3. 按固定模板写入内容。
4. 返回 `status/summary/data/nextAction`。

## Failure
- 缺参数：明确指出缺哪一项，并给示例输入。
- 写文件失败：返回目录权限检查建议。
