# 基础示例：数据清洗和验证

## 场景
Excel 数据有很多空值、重复值、格式问题，需要清洗。

## 执行步骤
1. 读取数据
2. 检测数据质量问题
3. 清洗数据
4. 验证清洗结果

## 代码示例
```python
import pandas as pd
import numpy as np

# 读取数据
df = pd.read_excel('data.xlsx')

# 1. 处理空值
print("空值统计:")
print(df.isnull().sum())

# 删除空值过多的行
df = df.dropna(thresh=len(df.columns) * 0.5)  # 至少50%非空

# 填充空值
df['name'].fillna('未知', inplace=True)
df['age'].fillna(df['age'].median(), inplace=True)

# 2. 删除重复行
print(f"重复行数: {df.duplicated().sum()}")
df = df.drop_duplicates()

# 3. 数据类型转换
df['date'] = pd.to_datetime(df['date'])
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

# 4. 删除异常值
df = df[(df['age'] > 0) & (df['age'] < 120)]
df = df[df['amount'] >= 0]

# 5. 标准化格式
df['name'] = df['name'].str.strip().str.title()
df['email'] = df['email'].str.lower()

# 验证结果
print("\n清洗后数据:")
print(df.info())
print(f"有效数据: {len(df)} 行")
```

## 数据质量检查清单
```python
def check_data_quality(df):
    """数据质量检查"""
    report = {
        '总行数': len(df),
        '总列数': len(df.columns),
        '空值占比': df.isnull().sum().to_dict(),
        '重复行数': df.duplicated().sum(),
        '数据类型': df.dtypes.to_dict(),
    }

    # 数值列统计
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        report['数值列统计'] = df[numeric_cols].describe().to_dict()

    return report

# 使用
quality_report = check_data_quality(df)
print("\n数据质量报告:")
for key, value in quality_report.items():
    print(f"{key}: {value}")
```

## 预期结果
- 数据质量提升
- 空值已处理
- 重复数据已删除
- 格式统一规范
