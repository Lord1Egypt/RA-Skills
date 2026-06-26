# 基础示例：读取简单 Excel 文件

## 场景
有一个简单的 Excel 文件 `data.xlsx`，需要读取数据。

## 执行步骤
1. 安装依赖库
2. 读取 Excel 文件
3. 处理数据
4. 验证结果

## 安装依赖
```bash
pip install pandas openpyxl
```

## 代码示例
```python
import pandas as pd

# 读取 Excel 文件
df = pd.read_excel('data.xlsx')

# 查看数据
print(df.head())
print(f"行数: {len(df)}")
print(f"列数: {len(df.columns)}")
print(f"列名: {df.columns.tolist()}")

# 基本统计
print(df.describe())
```

## 处理特定工作表
```python
# 读取特定工作表
df = pd.read_excel('data.xlsx', sheet_name='Sheet2')

# 读取多个工作表
all_sheets = pd.read_excel('data.xlsx', sheet_name=None)
for sheet_name, df in all_sheets.items():
    print(f"{sheet_name}: {len(df)} 行")
```

## 预期结果
- 成功读取 Excel 数据
- 数据加载到 DataFrame
- 可以进行数据分析

## 常用参数
```python
pd.read_excel(
    'data.xlsx',
    sheet_name='Sheet1',    # 工作表名称
    header=0,               # 标题行
    index_col=0,            # 索引列
    usecols='A:C',          # 读取的列
    skiprows=1,             # 跳过行数
    nrows=100               # 读取行数
)
```
