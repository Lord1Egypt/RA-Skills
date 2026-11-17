# Excel 处理技能（excel-skills）

> 版本：v1.0 | 整理日期：2026-09-12

## 定位

从 workspace/skills 149个技能中提炼整合的Excel全栈处理技能，覆盖本地Excel文件处理完整链路及飞书云端表格操作，并固化2026-07-24的openpyxl类型陷阱实战经验。

## 能力清单

- 工作簿创建/读取/编辑（openpyxl）
- 样式与格式化（表头样式、冻结、列宽自适应、数字格式）
- pandas数据通道（xlsx/csv/json互转、数据清洗、多Sheet写出）
- 多Sheet管理（新建/遍历/删除/合并）
- PDF表格转Excel（pdfplumber）
- 爬虫数据导出
- 飞书云端电子表格读写（feishu_sheets）

## 文件结构

```
excel-skills/
  SKILL.md              技能定义与完整用法
  README.md             本文件
  scripts/
    excel_toolkit.py    一站式命令行工具（info/convert/report/pdf2xlsx/merge）
    test_toolkit.py     回归测试（端到端验证report/merge/convert）
```

## 快速上手

```powershell
# 查看文件概况
python scripts/excel_toolkit.py info 数据.xlsx

# 生成规范样式报表
python scripts/excel_toolkit.py report 原始.xlsx 报表.xlsx

# 合并多Sheet
python scripts/excel_toolkit.py merge 数据.xlsx 合并.xlsx

# PDF表格转Excel
python scripts/excel_toolkit.py pdf2xlsx 文件.pdf 输出.xlsx

# 回归测试
python scripts/test_toolkit.py
```

## 依赖

Python 3.8+，pandas、openpyxl、pdfplumber（PDF转换用）。国内镜像安装：

```powershell
python -m pip install pandas openpyxl pdfplumber -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
```

## 核心铁律（实战教训）

1. openpyxl样式每种独立构造、独立赋值，禁止混合类型封装，禁止跨单元格共享后修改
2. skill脚本永久保留，清理临时文件时不得触碰 scripts/ 目录
3. CSV导出用 utf-8-sig，保证Excel直接打开不乱码
