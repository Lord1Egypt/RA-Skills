---
name: cn-excel-formula
version: "1.2.0"
description: "Excel公式助手。自然语言描述需求，自动生成Excel公式。支持VLOOKUP、条件统计、日期计算、文本处理等200+常用公式。附带公式解释和示例数据。"
metadata:
  openclaw:
    emoji: 📊
    category: productivity
    tags:
      - excel
      - formula
      - spreadsheet
      - office
      - chinese
scope:
  - "自然语言转Excel公式"
  - "公式解释（中文说明每个参数）"
  - "常用公式库（200+模板）"
  - "错误排查（常见公式错误诊断）"
  - "公式优化建议"
install: |
  pip install openpyxl
env:
  OPENAI_API_KEY: "可选，用于AI增强公式生成。不配置则使用模板匹配。"
entry:
  script: scripts/excel_formula.py
  args: []
---

# Excel公式助手

## 功能
- 自然语言描述 → 自动生成Excel公式
- 公式中文解释（每个参数都有说明）
- 200+常用公式模板库
- 常见错误排查
- 公式优化建议

## 使用方法

### 生成公式
```bash
# 自然语言描述
python scripts/excel_formula.py generate "查找A列中与D2匹配的B列值"
# 输出：=VLOOKUP(D2, A:B, 2, FALSE)

# 带条件的求和
python scripts/excel_formula.py generate "求A列大于100且B列为'完成'的C列之和"
# 输出：=SUMIFS(C:C, A:A, ">100", B:B, "完成")
```

### 解释公式
```bash
python scripts/excel_formula.py explain "=VLOOKUP(D2,A:B,2,FALSE)"
# 输出中文解释
```

### 常用公式库
```bash
# 列出某类别公式
python scripts/excel_formula.py list --category lookup
python scripts/excel_formula.py list --category date
python scripts/excel_formula.py list --category text
```

### 错误排查
```bash
python scripts/excel_formula.py diagnose "=VLOOKUP(D2,A:B,2,FALSE)" --error "#N/A"
# 输出可能原因和修复方法
```

## 支持的公式类别

| 类别 | 常用公式 |
|------|---------|
| 查找引用 | VLOOKUP, HLOOKUP, INDEX+MATCH, XLOOKUP, INDIRECT |
| 条件统计 | SUMIFS, COUNTIFS, AVERAGEIFS, MAXIFS, MINIFS |
| 日期时间 | DATE, DATEDIF, EDATE, EOMONTH, NETWORKDAYS |
| 文本处理 | LEFT, RIGHT, MID, FIND, SUBSTITUTE, CONCATENATE |
| 逻辑判断 | IF, IFS, SWITCH, AND, OR, IFERROR |
| 数学计算 | ROUND, ROUNDUP, ROUNDDOWN, MOD, INT, ABS |
| 数据清洗 | TRIM, CLEAN, UPPER, LOWER, PROPER, TEXT |
| 数组公式 | UNIQUE, FILTER, SORT, SEQUENCE, TRANSPOSE |

## 典型场景
1. **数据查找**：根据姓名查工资、根据编号查详情
2. **条件汇总**：按部门/月份/状态分类统计
3. **日期计算**：工龄、合同到期、项目倒计时
4. **文本提取**：从身份证提取生日、提取邮箱域名
5. **错误处理**：#N/A、#VALUE!、#REF! 排查修复

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
