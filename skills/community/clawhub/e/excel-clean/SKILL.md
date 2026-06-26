---
name: Excel Cleaner
description: Clean Excel data — deduplication, fill missing values, format conversion.
---

# Excel Cleaner（Excel数据清洗）

> 去重 / 空值填充 / 格式转换 | Pandas驱动

## 功能 | Features

- ✅ **批量去重** — 按指定列组合去重
- ✅ **空值填充** — 支持填充固定值、前值、后值
- ✅ **格式转换** — 数值/文本/日期格式互转
- ✅ **保留原文件** — 输出为 `_cleaned.xlsx`，原文件不变

## 使用场景 | Use Cases

| 场景 | 说明 |
|---|---|
| 名单去重 | 删除重复客户/订单记录 |
| 数据补全 | 用"未知"或0填充空值 |
| 格式标准化 | 日期统一为 YYYY-MM-DD |

## 使用方式 | Usage

```
输入参数:
  file_path       Excel文件路径
  dedup_cols      去重列名列表（可选）
  fill_value      空值填充内容（可选）
  convert_type    格式类型转换（可选）

输出:
  success         是否成功
  output          输出文件路径
  rows            处理后行数
```

## 示例 | Example

```python
result = excel_clean(
    file_path="/data/orders.xlsx",
    dedup_cols=["订单号", "手机号"],
    fill_value="未知",
    convert_type="日期:YYYY-MM-DD"
)
```

## 依赖 | Dependencies

```
pandas >= 1.3.0
openpyxl >= 3.0.0
```

*版本 v1.0*
