---
name: filesystem-access-greaterpeter
description: 安全的本地文件读/写/列表能力，默认只在 OpenClaw workspace 目录内工作。
---

## 使用建议

- 当你需要查看、编辑或列出工作区内的文件时使用本技能。
- 仅访问相对路径或工作区子目录，避免越权访问用户其他目录。
- 典型场景：查看日志、生成 Markdown 报告、保存脚本或配置文件。

## 安全约束

- 禁止在 workspace 之外执行写入操作。
- 避免删除用户重要文件，如配置、源码或系统文件。
