---
name: batch-convert-zh
description: >
  批量格式转换 / 文档批处理 / 多格式一键互转 / batch convert。支持PDF、Word、PPT、Markdown等格式批量互转，HR批量处理简历、财务批量归档报表、运营批量整理素材、开发批量导出技术文档。一次选择多个文件，自动完成格式转换，避免逐个手动操作的低效率。适用于合同报告转Word、多份文档统一导出PDF、演示文稿批量转PDF防止格式错乱等场景。搜索触发词：批量转换文件、PDF批量转Word、文档格式互转、多个文件一键转换、PPT批量转PDF、自动格式转换、文件批处理工具、办公文件转换。
tags: [批量转换, 格式转换, batch-convert, 文档处理, PDF转Word, Word转PDF, PPT转PDF, 办公自动化, 文件批处理, 批量导出]
---

# 批量文档格式转换

支持一次性将大量文件在 PDF、Word（DOCX）、Markdown、HTML、Excel、PPT 等格式之间批量互转，自动检测格式、并行处理，统一输出设置，大幅提升文档处理效率。

## Tools Required
- office-mcp / batch_convert

## Usage
- "把这个文件夹里所有的PDF合同批量转换成Word文档，方便我们编辑修改"
- "将这些Markdown格式的技术文档全部转成PDF，统一发给客户"
- "我有一百多份Word周报，帮我批量导出成PDF存档"

## Examples
输入：把 `/reports/2024/` 目录下所有 DOCX 文件批量转为 PDF，保存到 `/reports/2024/pdf/`
输出：已检测到 47 个 DOCX 文件，并行转换完成：
- 成功：47 个
- 失败：0 个
- 输出目录：`/reports/2024/pdf/`
- 耗时：23 秒