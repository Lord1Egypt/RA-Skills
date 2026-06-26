---
name: crc-bank-statement-converter
description: "将不同银行导出的流水 Excel / CSV 批量转换为监管报送标准格式（9 列）。Use when: 用户需要转换银行流水格式、汇总多银行多账户流水、整理监管报送数据。NOT for: 非银行流水文件处理、加密/损坏文件修复。需要 Python3 + openpyxl + xlrd。"
metadata: { "openclaw": { "emoji": "🏦", "requires": { "bins": ["python3", "pip"] } } }
---

# 银行流水格式批量转换

将不同银行导出的流水 Excel / CSV 文件批量转换为监管流水导入模板格式（9 列标准格式）。

## When to Use

✅ **USE this skill when:**

- "帮我把这些银行流水转成标准格式"
- "把这个月所有子公司的流水汇总到一份 Excel"
- "把各银行导出的流水统一整理成报送格式"
- "批量转换流水文件，要汇总表和分项表"
- 监管报送需要统一格式的银行流水
- 多个公司/多个银行的流水文件需要汇总
- 每月重复性的流水格式整理工作

## When NOT to Use

❌ **DON'T use this skill when:**

- 非 Excel / CSV 格式的文件（PDF、Word 等）→ 用对应的文件转换工具
- 需要修改流水内容或金额 → 这是格式转换工具，不改变数据
- 需要分析流水数据（趋势、统计）→ 转换后用数据分析技能
- 加密的银行文件 → 需先解密再转换
- 非银行流水类 Excel（如发票、合同）→ 不适用

## 支持的银行格式

自动识别以下格式，无需手动选择：

- **标准 .xlsx**（openpyxl 解析）
- **旧版 .xls 二进制**（xlrd 解析）
- **HTML 表格 .xls**（银行网页导出的 .xls 实际是 HTML）
- **XML Spreadsheet .xls**（工行电子回单等）
- **伪 .xls 实为 .xlsx**（扩展名不匹配的 ZIP 格式）
- **标准 .csv**（自动识别 UTF-8 BOM、GB18030/GBK、UTF-16 等常见编码；支持中国银行等“中文[英文]”表头导出）

## Commands

### 首次使用 — 环境初始化

```bash
pip install openpyxl xlrd
```

验证环境：

```bash
python3 -c "import openpyxl, xlrd; print('OK')"
```

### 转换流水文件

```bash
# 基本用法（自动输出 zip 到输入文件夹同级的"输出"目录）
python3 /home/node/agents/skills/crc-bank-statement-converter/converter.py "<输入文件夹路径>"

# 指定输出 zip 路径
python3 /home/node/agents/skills/crc-bank-statement-converter/converter.py "<输入文件夹路径>" "<输出 zip 路径>"
```

**参数说明：**

- **输入文件夹路径**（必填）：包含 `.xls` / `.xlsx` / `.csv` 流水文件的文件夹，支持子文件夹递归扫描
- **输出 zip 路径**（可选）：不提供时自动生成到输入文件夹同级的 `输出` 目录下，文件名 `监管流水_<时间戳>.zip`

## Quick Responses

**"帮我把这批银行流水转成标准格式"**

1. 确认用户提供了文件夹路径
2. 检查 Python 环境和脚本是否就绪
3. 执行转换（推荐输出到 workspace 方便用户下载）：
```bash
python3 /home/node/agents/skills/crc-bank-statement-converter/converter.py "/home/node/workspace/流水数据" "/home/node/workspace/监管流水.zip"
```
4. 报告转换结果（成功/失败数量）+ 提示用户去 workspace 下载 zip

**"把本月所有子公司的银行流水统一转换"**

```bash
python3 /home/node/agents/skills/crc-bank-statement-converter/converter.py "/home/node/workspace/本月流水" "/home/node/workspace/本月监管流水.zip"
```

**"检查转换后的文件是否与原始流水金额一致"**

转换完成后解压 zip，读取「汇总.xlsx」或某家公司单独的 Excel，抽查几行与原始文件对比金额列。

## 输出格式

输出一个 **zip 压缩包**，结构如下：

```
监管流水_<时间戳>.zip
├── 汇总.xlsx             # 所有公司流水合并到一张表，含 _来源公司 列
├── <原文件名 1>.xlsx     # 每个源文件对应一份独立 Excel（9 列）
├── <原文件名 2>.xlsx
└── ...
```

模板 9 列：`日期 | 收入 | 支出 | 余额 | 摘要 | 对方户名 | 对方银行 | 对方账号 | 备注`

- `日期` 固定输出为 `YYYY-MM-DD` 文本格式，例如 `2026-04-14`，不会保留时分秒。
- `对方户名`、`对方银行`、`对方账号` 会兼容常见的“对方/交易对方/交易对手/付款人/收款人/付方/收方/借方/贷方”等银行导出表头叫法。

zip 输出到 workspace 后，普通用户可直接从文件管理面板下载。

## Notes

- 输出按交易日期时间**正序**（旧→新）排列；银行导出的倒序流水（含同一日期/时间戳内的倒序）会自动检测并反转
- 自动跳过以 `~` 开头的临时文件和含 `说明` 的文件
- 自动过滤汇总行（含"合计"、"小计"、"累计"、"笔数"的行）
- CSV 支持逗号、Tab、分号分隔；如果银行导出文件前几行是查询摘要，会自动定位真正表头行
- 电子回单格式（无余额列）的余额字段为空
- 如果转换失败，检查文件是否为加密或非标准格式
- 脚本位置：`/home/node/agents/skills/crc-bank-statement-converter/`
