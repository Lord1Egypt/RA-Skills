# Csv To Task

[English](./README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![版本](https://img.shields.io/badge/version-1.0-blue)

> 将 CSV 行转换为结构化的、可追踪的任务对象 — 支持 Jira 工单、Markdown 清单、JSON 数组

## 解决什么问题

用户有电子表格或 CSV 导出数据，需要将每一行转换成可以实际追踪的任务——分配负责人、设优先级、定截止日期。这个技能将 CSV 列映射到任务字段（标题、负责人、优先级、截止日期），并按用户需要的格式输出。

**触发条件：** CSV 数据 + 任务/待办/工单创建意图。

## 功能特性

- **自动字段映射** — 检测列名并映射到任务属性（标题从第一个文本列取，负责人从姓名列取，优先级从 P0-P3 或高/中/低识别）
- **多格式输出** — Markdown 清单、Jira 风格工单、JSON 数组或带新列的 CSV
- **处理残缺数据** — 缺失负责人标记为"未分配"，缺失优先级标记为"普通"
- **保留所有原始数据** — 每行精确转为一个任务，无静默丢弃

## 快速开始

```bash
# 通过 ClawHub 安装
clawhub install csv-to-task

# 或手动复制
cp -r csv-to-task ~/.openclaw/skills/
```

### 使用方法

```
/csv-to-task
```

粘贴 CSV 并要求"转换为任务"——指定格式（Jira、Markdown、JSON）。

```
/csv-to-task/estimate
```

为每个任务添加时间/复杂度估算，用于冲刺计划。

## 工作模式

| 模式 | 说明 |
|------|------|
| `/csv-to-task` | 默认——将 CSV 行转换为指定格式的任务对象 |
| `/csv-to-task/estimate` | 为每个任务添加时间/复杂度估算 |

## 示例

| 场景 | 输出 |
|------|------|
| 10 行，无状态列 | 所有任务标记为"待办"，附注"未发现状态列" |
| 优先级为 P0-P3 格式 | 正确映射到任务优先级 |
| 标题列 200 个字符 | 完整标题保留，在描述字段做摘要 |
| 3 行无负责人 | 每行标记"未分配"，不虚构姓名 |

## 目录结构

```
csv-to-task/
├── SKILL.md          # 技能入口
├── LICENSE
├── README.md
├── README_zh.md
├── CONTRIBUTING.md
├── .gitignore
├── references/       # 字段映射模板、格式示例
└── tests/
```

## 许可证

MIT 许可证 — 详见 [LICENSE](LICENSE)。