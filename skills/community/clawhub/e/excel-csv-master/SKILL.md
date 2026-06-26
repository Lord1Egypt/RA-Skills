---
name: excel-csv-master
version: 1.0.0
description: Master Excel/CSV data processing - cleaning, transforming, merging, and analyzing spreadsheets with AI. Perfect for office workers, accountants, and business professionals.
author: 秘书
price: 19
currency: USD
keywords: [excel, csv, spreadsheet, data-processing, cleaning, transformation]
category: productivity
---

# 📊 Excel/CSV Master - 数据处理大师

**让 Excel/CSV 处理变得简单，AI 帮你搞定一切**

---

## 🎯 这个技能能帮你做什么？

✅ **数据清洗** - 自动修复格式、填充缺失值
✅ **数据转换** - 格式转换、列操作、透视表
✅ **数据合并** - 多表合并、去重、匹配
✅ **数据分析** - 统计、汇总、对比
✅ **格式化** - 批量格式化、条件格式
✅ **公式生成** - 自动生成 Excel 公式

---

## 📚 包含内容

### 第一部分：数据清洗（15+ 场景）

#### 1. 缺失值处理
```python
# 填充缺失值
df.fillna(0)  # 用0填充
df.fillna(method='ffill')  # 前向填充
df.dropna()  # 删除缺失行

# 智能填充
df['column'].fillna(df['column'].mean())  # 用均值填充
```

#### 2. 重复值处理
```python
# 删除完全重复的行
df.drop_duplicates()

# 基于特定列去重
df.drop_duplicates(subset=['email'], keep='first')

# 标记重复值
df['is_duplicate'] = df.duplicated()
```

#### 3. 数据类型转换
```python
# 转换为日期
df['date'] = pd.to_datetime(df['date'])

# 转换为数值
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

# 字符串处理
df['name'] = df['name'].str.strip()  # 去空格
df['name'] = df['name'].str.title()  # 首字母大写
```

#### 4. 异常值处理
```python
# IQR 方法
Q1 = df['amount'].quantile(0.25)
Q3 = df['amount'].quantile(0.75)
IQR = Q3 - Q1
df = df[(df['amount'] >= Q1 - 1.5*IQR) & (df['amount'] <= Q3 + 1.5*IQR)]

# Z-score 方法
from scipy import stats
df = df[(np.abs(stats.zscore(df['amount'])) < 3)]
```

---

### 第二部分：数据转换（20+ 操作）

#### 1. 列操作
```python
# 重命名列
df.rename(columns={'old_name': 'new_name'})

# 添加计算列
df['total'] = df['quantity'] * df['price']

# 删除列
df.drop(columns=['unnecessary_col'])

# 选择特定列
df[['col1', 'col2', 'col3']]
```

#### 2. 行操作
```python
# 过滤行
df[df['status'] == 'active']

# 排序
df.sort_values('date', ascending=False)

# 分组
df.groupby('category').sum()
```

#### 3. 透视表
```python
# 创建透视表
pivot = df.pivot_table(
    values='amount',
    index='category',
    columns='month',
    aggfunc='sum'
)

# 多级透视表
pivot = df.pivot_table(
    values='amount',
    index=['category', 'product'],
    columns='month',
    aggfunc=['sum', 'count']
)
```

#### 4. 数据重塑
```python
# 宽转长
df_long = df.melt(id_vars=['id'], var_name='month', value_name='amount')

# 长转宽
df_wide = df.pivot(index='id', columns='month', values='amount')
```

---

### 第三部分：数据合并（10+ 场景）

#### 1. 表格合并
```python
# 横向合并（列合并）
pd.concat([df1, df2], axis=1)

# 纵向合并（行合并）
pd.concat([df1, df2], axis=0)

# 按键合并
pd.merge(df1, df2, on='id', how='left')
pd.merge(df1, df2, on='id', how='inner')
pd.merge(df1, df2, on='id', how='outer')
```

#### 2. VLOOKUP 替代
```python
# Python 版 VLOOKUP
result = pd.merge(
    df1,
    df2[['id', 'name', 'price']],
    on='id',
    how='left'
)
```

#### 3. 多表合并
```python
# 合并多个 CSV
import glob
files = glob.glob('*.csv')
df = pd.concat([pd.read_csv(f) for f in files])
```

---

### 第四部分：Excel 公式生成器

#### 常用公式
```excel
# 条件求和
=SUMIF(range, criteria, sum_range)

# 多条件求和
=SUMIFS(sum_range, criteria_range1, criteria1, criteria_range2, criteria2)

# VLOOKUP
=VLOOKUP(lookup_value, table_array, col_index_num, FALSE)

# 条件计数
=COUNTIF(range, criteria)

# 文本处理
=LEFT(text, num_chars)
=RIGHT(text, num_chars)
=MID(text, start_num, num_chars)
=TRIM(text)

# 日期处理
=DATE(year, month, day)
=YEAR(date)
=MONTH(date)
=DAY(date)

# 条件判断
=IF(condition, value_if_true, value_if_false)
=IFS(condition1, value1, condition2, value2)
```

---

### 第五部分：批量处理模板

#### 批量导入 CSV
```python
import pandas as pd
import glob

# 导入文件夹中所有 CSV
files = glob.glob('data/*.csv')
dfs = [pd.read_csv(f) for f in files]
combined = pd.concat(dfs, ignore_index=True)

# 保存
combined.to_csv('combined.csv', index=False)
```

#### 批量格式化 Excel
```python
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill

wb = load_workbook('data.xlsx')
ws = wb.active

# 设置标题行样式
for cell in ws[1]:
    cell.font = Font(bold=True, color='FFFFFF')
    cell.fill = PatternFill(start_color='4F81BD', fill_type='solid')

# 保存
wb.save('formatted.xlsx')
```

---

## 🚀 快速开始

### 场景1：数据清洗
```
用户：这个 CSV 有很多缺失值和重复值，帮我清理

AI：
[加载数据]
[分析缺失值分布]
[检测重复值]
[自动清洗]
[生成清洗报告]

✅ 删除 230 个重复行
✅ 填充 45 个缺失值
✅ 修正 12 个格式错误
```

### 场景2：表格合并
```
用户：我有3个 Excel 文件，想按 ID 合并

AI：
[加载3个文件]
[识别共同列]
[合并数据]
[检查一致性]

✅ 合并完成：5000行 × 15列
⚠️ 发现 23 个不匹配的 ID
```

### 场景3：Excel 公式
```
用户：我需要一个公式，计算每个类别的总和

AI：使用这个公式：
=SUMIF(A:A, "category_name", B:B)

如果是多条件：
=SUMIFS(B:B, A:A, "category", C:C, "condition")
```

---

## 💡 特色功能

### 1. 智能数据类型识别
```
自动识别：
- 日期格式
- 货币格式
- 百分比
- 电话号码
- 邮箱

并转换为正确类型
```

### 2. 批量操作
```
一次处理：
- 100+ 个文件
- 数百万行数据
- 复杂转换
```

### 3. 错误检测
```
自动检测：
- 循环引用
- 公式错误
- 数据不一致
```

---

## 📊 适用场景

| 场景 | 推荐度 | 说明 |
|------|--------|------|
| **财务人员** | ⭐⭐⭐⭐⭐ | 日常表格处理 |
| **行政人员** | ⭐⭐⭐⭐⭐ | 数据整理 |
| **销售** | ⭐⭐⭐⭐ | 客户数据处理 |
| **HR** | ⭐⭐⭐⭐⭐ | 员工数据处理 |
| **学生** | ⭐⭐⭐⭐ | 作业数据处理 |

---

## 🎁 购买即得

1. **15+ 清洗场景代码**
2. **20+ 转换操作代码**
3. **10+ 合并场景代码**
4. **Excel 公式速查表**
5. **批量处理脚本**
6. **终身更新**
7. **技术支持**

---

## 🔧 版本历史

- v1.0.0 (2026-04-05): 首次发布

---

**立即购买，让 Excel/CSV 处理变得简单！** 🚀
