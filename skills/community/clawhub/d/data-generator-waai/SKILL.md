---
name: data_generator
description: "Data Generator / 数据生成器 - Generate training data from user instructions. Input: tool name + command list. Output: JSONL. / 根据用户指令生成训练数据。"
metadata:
  author: "WaaiOn"
  version: "1.0"
  openclaw:
    emoji: "📝"
    requires:
      bins: ["python3"]
---

# 📝 Data Generator / 数据生成器

Generate training data from Excel user instructions.

## When to Use / 使用场景

| EN | CN |
|----|----|
| Generate training data from instructions | 从用户指令生成训练数据 |
| Batch produce AI training samples | 批量生成AI训练样本 |
| Build dataset from Excel | 从Excel构建数据集 |

## Features / 功能

| Feature | EN | CN |
|---------|----|----|
| Excel input | Excel file support | Excel文件输入 |
| JSONL output | JSONL output | JSONL格式输出 |
| Multi-tool support | Multi-tool support | 支持多种工具 |
| Customizable prompt | Customizable prompt | 可自定义提示词 |

## Usage / 使用

```python
from data_generator import Generator

# Simple / 简单
gen = Generator()
result = gen.generate(
    tool_name="dev_control",
    commands=["打开空调", "关闭窗帘"],
    excel_file="data.xlsx"
)

# With prompt / 自定义提示词
result = gen.generate(
    tool_name="alarm_remind",
    commands=["提醒我起床"],
    prompt_template="自定义提示词模板"
)
```

## Parameters / 参数

| Parameter | Type | EN | CN |
|-----------|------|----|----|
| tool_name | str | Tool name | 工具名称 |
| commands | list | Command list | 命令列表 |
| excel_file | str | Excel file path | Excel文件路径 |
| prompt_template | str | Custom prompt | 自定义提示词(可选) |

## Output / 输出

```jsonl
{"conversations": [...], "system": "..."}
{"conversations": [...], "system": "..."}
```

## Installation / 安装

```bash
npx clawhub install data-generator-waai
```

## Author / 作者

- WaaiOn
