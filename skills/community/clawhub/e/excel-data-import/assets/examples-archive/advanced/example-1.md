# 高级示例：大数据 Excel 文件处理

## 场景
Excel 文件很大（>100MB），一次性读取会内存溢出。

## 前置条件
- Excel 文件 >50MB
- 需要分批处理

## 执行步骤
1. 分块读取
2. 流式处理
3. 增量写入
4. 内存优化

## 代码示例

### 方案 1：分块读取
```python
import pandas as pd

# 分块读取（每 10000 行一块）
chunk_size = 10000
chunks = pd.read_excel('large_file.xlsx', chunksize=chunk_size)

# 处理每个块
results = []
for i, chunk in enumerate(chunks):
    print(f"处理块 {i}: {len(chunk)} 行")

    # 数据清洗
    chunk = chunk.dropna()

    # 数据转换
    chunk['date'] = pd.to_datetime(chunk['date'])

    # 累积结果
    results.append(chunk)

    # 手动释放内存
    del chunk

# 合并所有块
df = pd.concat(results, ignore_index=True)
print(f"总计: {len(df)} 行")
```

### 方案 2：使用 openpyxl 优化
```python
from openpyxl import load_workbook
import pandas as pd

# 只读模式，内存优化
wb = load_workbook('large_file.xlsx', read_only=True)
sheet = wb.active

# 获取总行数
max_row = sheet.max_row
print(f"总行数: {max_row}")

# 分批读取
batch_size = 50000
all_data = []

for start_row in range(2, max_row + 1, batch_size):
    end_row = min(start_row + batch_size, max_row + 1)

    # 读取一个批次
    batch_data = []
    for row in sheet.iter_rows(min_row=start_row, max_row=end_row, values_only=True):
        batch_data.append(row)

    # 转为 DataFrame
    df_batch = pd.DataFrame(batch_data, columns=[
        'col1', 'col2', 'col3', 'col4'
    ])

    # 处理批次数据
    df_batch = df_batch.dropna()
    all_data.append(df_batch)

    print(f"处理行 {start_row}-{end_row}")

wb.close()

# 合并
df = pd.concat(all_data, ignore_index=True)
```

### 方案 3：转换为 CSV（推荐）
```python
import pandas as pd

# Excel 转 CSV（更快，内存占用更小）
df = pd.read_excel('large_file.xlsx')
df.to_csv('large_file.csv', index=False, encoding='utf-8')

# 后续使用 CSV
df = pd.read_csv('large_file.csv', chunksize=50000)
```

### 方案 4：使用 Dask（超大数据）
```python
import dask.dataframe as dd

# Dask 延迟加载，类似 pandas
# 但支持并行和内存优化

# 读取 Excel（先转 CSV）
df = dd.read_csv('large_file.csv')

# 惰性计算（不会立即执行）
df_clean = df.dropna()
df_grouped = df_clean.groupby('category').agg({'amount': 'sum'})

# 执行计算（此时才真正处理）
result = df_grouped.compute()
print(result)
```

## 性能对比

| 方法 | 100MB | 500MB | 1GB | 内存占用 |
|------|-------|-------|-----|----------|
| 直接读取 | 10s | ❌ OOM | ❌ OOM | 3GB |
| 分块读取 | 15s | 60s | ❌ OOM | 1GB |
| openpyxl 只读 | 20s | 90s | 180s | 500MB |
| CSV + 分块 | 5s | 20s | 40s | 200MB |
| Dask | 8s | 30s | 60s | 300MB |

## 关键要点
- 大文件优先转换为 CSV
- 使用分块处理
- 考虑使用数据库
- 监控内存使用
