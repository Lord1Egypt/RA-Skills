---
name: chat2duckdb
description: 基于 DuckDB 引擎的高效数据分析工具；当用户需要对 CSV/JSON/Parquet/Excel 等数据文件进行 SQL 查询、数据分析、数据抽样或需要自动纠错的查询执行时使用
dependency:
  python:
    - duckdb>=1.5.0
    - pandas>=2.0.0
    - numpy>=1.24.0
    - openpyxl>=3.1.0
---

# Chat2DuckDB 数据分析

## 任务目标
- 本技能用于对数据文件进行快速、高效的 SQL 查询和分析
- 能力包含：数据文件注册为表、自然语言转 SQL、查询执行、数据抽样、错误校正、分析结论生成
- 触发条件：用户需要分析数据文件、执行 SQL 查询、探索数据结构、生成数据分析报告

## 前置准备
- 依赖说明：安装 DuckDB 和 pandas
  ```
  duckdb>=1.5.0
  pandas>=2.0.0
  ```

## 核心功能

### 1. 数据探索（Describe 模式）
- **基本信息**：总行数、列数、表结构
- **数值列统计**：平均值、中位数、标准差、最大/最小值
- **分类列统计**：唯一值数量、最常见值、Top 值分布
- **日期列统计**：最早/最晚日期、唯一日期数
- **数据质量**：缺失值统计、完整性分析

### 2. SQL 查询执行
- **智能 SQL 生成**：根据自然语言描述自动生成 SQL
- **自动重试机制**：最多 3 次智能重试
- **SQL 校正引擎**：
  - 语法错误自动修复（移除多余分号、逗号等）
  - 列名错误智能纠正（基于编辑距离匹配）
  - 引号规范化（双引号转单引号）
  - SQL 关键字大小写规范化
- **数据抽样**：支持按比例抽样查询，快速验证逻辑

### 3. 结果分析
- 查询结果格式化输出
- 执行时间和性能统计
- 数据洞察和业务建议生成

## 操作步骤

### 步骤 1：数据准备
确认数据文件路径（CSV/JSON/Parquet/Excel 等格式）

### 步骤 2：数据探索
```bash
# 完整统计模式（推荐）
python scripts/duckdb_analyzer.py --file_path ./data.csv --mode describe

# 简单模式（仅基本信息）
python scripts/duckdb_analyzer.py --file_path ./data.csv --mode describe --simple

# 导出分析报告
python scripts/duckdb_analyzer.py --file_path ./data.csv --mode describe --output report.json

# Excel 文件（默认读取第一个工作表）
python scripts/duckdb_analyzer.py --file_path ./data.xlsx --mode describe

# Excel 文件（指定工作表）
python scripts/duckdb_analyzer.py --file_path ./data.xlsx --excel_sheet "sheetTitle" --mode describe
```

### 步骤 3：SQL 查询
```bash
# 基础查询
python scripts/duckdb_analyzer.py --file_path ./data.csv --mode query \
  --sql "SELECT * FROM data LIMIT 10"

# 聚合查询
python scripts/duckdb_analyzer.py --file_path ./data.csv --mode query \
  --sql "SELECT category, SUM(price * quantity) as total_sales FROM data GROUP BY category"

# 抽样验证（先在小样本上测试）
python scripts/duckdb_analyzer.py --file_path ./data.csv --mode query \
  --sql "SELECT * FROM data WHERE price > 100" --sample_fraction 0.1

# 导出查询结果（支持 CSV/Excel/JSON/Parquet）
python scripts/duckdb_analyzer.py --file_path ./data.csv --mode query \
  --sql "SELECT * FROM data" --output result.csv

python scripts/duckdb_analyzer.py --file_path ./data.csv --mode query \
  --sql "SELECT * FROM data" --output result.xlsx

# 持久化到 DuckDB 文件（后续可直接关联查询）
python scripts/duckdb_analyzer.py --file_path ./data.csv --mode query \
  --persist_db_path ./analysis.duckdb --persist_table \
  --sql "SELECT category, SUM(price * quantity) as total_sales FROM data GROUP BY category"
```

### 步骤 4：结果分析
- 查看查询结果和数据预览
- 分析执行时间和重试次数
- 根据结果生成业务洞察

### 步骤 5：数据持久化（可选）
- `--persist_db_path`：指定 DuckDB 数据库文件路径
- `--persist_table`：将注册表持久化为普通表（默认是临时表）
- 典型用途：跨批次积累结果、后续多表关联查询、沉淀分析基表

## 资源索引
- 核心脚本：[scripts/duckdb_analyzer.py](scripts/duckdb_analyzer.py)（DuckDB 操作核心，支持数据注册、查询执行、抽样、错误处理）
- 数据格式参考：[references/data-formats.md](references/data-formats.md)（支持的文件格式和最佳实践）

## 注意事项

### 最佳实践
1. **先探索后查询**：先用 describe 模式了解数据结构，再生成 SQL
2. **复杂查询先抽样**：对于复杂查询，先用 `--sample_fraction` 参数在小样本上验证
3. **合理使用 LIMIT**：查询结果超过 1000 行时，建议使用 LIMIT 或聚合查询
4. **利用自动校正**：SQL 错误时会自动重试和校正，无需手动干预

### 性能建议
- 大数据集使用抽样验证后再执行完整查询
- 聚合查询比全表查询更高效
- 可以设置 `--max_retries` 参数调整重试次数

### 错误处理
- 语法错误会自动修复（多余分号、逗号等）
- 列名错误会尝试匹配最相似的列名（编辑距离≤2）
- 表名错误会提示检查表名
- 所有校正操作都会在输出中显示

## 使用示例

### 示例 1：完整数据探索
**场景**：拿到新数据集，需要了解数据结构和质量

**命令**：
```bash
python scripts/duckdb_analyzer.py --file_path ./sales_data.csv --mode describe
```

**输出包含**：
- 基本信息：20 行，7 列
- 表结构：各字段名称和数据类型
- 数值列统计：price 的平均值 356.99，中位数 264.99 等
- 分类列统计：category 有 2 个唯一值，Electronics 出现 12 次
- 日期列统计：sale_date 从 2024-01-15 到 2024-02-02
- 数据质量：所有列数据完整，无缺失值

### 示例 2：销售分析查询
**场景**：分析各类别产品的销售表现

**命令**：
```bash
python scripts/duckdb_analyzer.py --file_path ./sales_data.csv --mode query \
  --sql "SELECT category, COUNT(*) as num_products, SUM(price * quantity) as total_revenue, AVG(price) as avg_price FROM data GROUP BY category ORDER BY total_revenue DESC"
```

**输出**：
```
执行 SQL: SELECT category, COUNT(*) as num_products, SUM(price * quantity) as total_revenue, AVG(price) as avg_price FROM data GROUP BY category ORDER BY total_revenue DESC

【查询结果】
执行时间：0.05 秒
重试次数：0
结果行数：2

数据预览:
   category  num_products  total_revenue  avg_price
Electronics            12       42938.24     356.99
  Furniture             8       19949.23     356.99
```

**业务洞察**：
- Electronics 类别贡献了 68% 的总收入
- 两个类别的平均价格相同，但 Electronics 销量更高

### 示例 3：区域销售对比
**场景**：分析不同区域的销售情况

**命令**：
```bash
python scripts/duckdb_analyzer.py --file_path ./sales_data.csv --mode query \
  --sql "SELECT region, COUNT(*) as num_orders, SUM(price * quantity) as total_sales, AVG(price) as avg_order_value FROM data GROUP BY region ORDER BY total_sales DESC"
```

### 示例 4：高价产品筛选（带抽样验证）
**场景**：找出高价产品（price > 200），先在 10% 样本上验证

**命令**：
```bash
# 先在样本上验证
python scripts/duckdb_analyzer.py --file_path ./sales_data.csv --mode query \
  --sql "SELECT product_name, category, price FROM data WHERE price > 200" --sample_fraction 0.1

# 验证无误后执行完整查询
python scripts/duckdb_analyzer.py --file_path ./sales_data.csv --mode query \
  --sql "SELECT product_name, category, price FROM data WHERE price > 200 ORDER BY price DESC"
```

### 示例 5：自动 SQL 校正
**场景**：SQL 有语法错误（多余分号），系统自动校正

**命令**：
```bash
python scripts/duckdb_analyzer.py --file_path ./sales_data.csv --mode query \
  --sql "SELECT * FROM data WHERE price > 100;"
```

**输出**：
```
【SQL 校正记录】
  ✓ 语法校正：;\s*$ -> 

【查询结果】
执行时间：0.03 秒
重试次数：1
结果行数：15
```

### 示例 6：导出查询结果
**场景**：将查询结果保存为 CSV、Excel、JSON 或 Parquet 文件

**CSV 导出**：
```bash
python scripts/duckdb_analyzer.py --file_path ./sales_data.csv --mode query \
  --sql "SELECT category, region, SUM(price * quantity) as sales FROM data GROUP BY category, region" \
  --output sales_summary.csv
```

**Excel 导出**：
```bash
python scripts/duckdb_analyzer.py --file_path ./sales_data.csv --mode query \
  --sql "SELECT category, region, SUM(price * quantity) as sales FROM data GROUP BY category, region" \
  --output sales_summary.xlsx
```

**JSON 导出**：
```bash
python scripts/duckdb_analyzer.py --file_path ./sales_data.csv --mode query \
  --sql "SELECT category, region, SUM(price * quantity) as sales FROM data GROUP BY category, region" \
  --output sales_summary.json
```

**Parquet 导出**：
```bash
python scripts/duckdb_analyzer.py --file_path ./sales_data.csv --mode query \
  --sql "SELECT category, region, SUM(price * quantity) as sales FROM data GROUP BY category, region" \
  --output sales_summary.parquet
```

**结果**：根据文件扩展名自动选择导出格式，保存为相应文件

### 示例 7：时间序列分析
**场景**：分析销售趋势

**命令**：
```bash
python scripts/duckdb_analyzer.py --file_path ./sales_data.csv --mode query \
  --sql "SELECT DATE_TRUNC('month', sale_date) as month, SUM(price * quantity) as monthly_sales FROM data GROUP BY month ORDER BY month"
```

## 故障排查

### 常见问题

**Q1: 文件找不到？**
```
错误：数据文件不存在：./data.csv
```
解决：检查文件路径是否正确，使用绝对路径试试

**Q2: Excel 读取失败？**
```
错误：无法注册数据表：...
```
解决：
- 确认文件为 `.xlsx` 或 `.xls`
- 如工作表不在第一个，添加参数 `--excel_sheet "工作表名"`
- 检查是否安装 `openpyxl`

**Q3: SQL 执行失败？**
系统会自动重试和校正 SQL，如果仍然失败，检查：
- 列名是否正确（区分大小写）
- SQL 语法是否正确
- 表名是否使用了默认的 'data'

**Q4: 内存不足？**
解决：
- 使用抽样查询：`--sample_fraction 0.1`
- 添加 LIMIT 限制结果数量
- 使用聚合查询而非全表查询

## 输出格式说明

### Describe 模式输出
- **基本信息**：数据规模概览
- **表结构**：字段名和数据类型
- **数值列统计**：描述性统计指标
- **分类列统计**：分布和频率信息
- **日期列统计**：时间范围信息
- **数据质量**：缺失值统计
- **数据样本**：前 5 行数据预览

### Query 模式输出
- **SQL 校正记录**：如果有自动校正，会显示校正内容
- **查询结果**：执行时间、重试次数、结果行数
- **数据预览**：完整的查询结果表格

## 高级技巧

### 1. 链式分析
先用 describe 了解数据，再执行多个查询：
```bash
# 步骤 1：探索数据
python scripts/duckdb_analyzer.py --file_path ./data.csv --mode describe

# 步骤 2：基于了解执行针对性查询
python scripts/duckdb_analyzer.py --file_path ./data.csv --mode query \
  --sql "SELECT category, AVG(price) as avg_price FROM data GROUP BY category"
```

### 2. 性能优化
对于大数据集：
```bash
# 先用 1% 样本快速验证
python scripts/duckdb_analyzer.py --file_path ./large_data.csv --mode query \
  --sql "SELECT ..." --sample_fraction 0.01

# 验证通过后再执行完整查询
python scripts/duckdb_analyzer.py --file_path ./large_data.csv --mode query \
  --sql "SELECT ..."
```

### 3. 数据质量检查
```bash
python scripts/duckdb_analyzer.py --file_path ./data.csv --mode describe | grep "缺失"
```

## SQL 语法约束

- 仅使用 DuckDB SQL 方言，不使用其他数据库的专有语法
- 字段名支持英文和中文查询
- 包含中文、空格、连字符、冒号等特殊字符的字段名，必须使用双引号
- 当中文字段未加双引号时，查询引擎会自动校正并重试
- 支持中文标点自动转换（如 `，；（）` 转 `,;()`）
- 默认表名为 `data`
- 生成 SQL 时优先保证可执行性，再进行性能优化

## Pandas 使用边界

- Pandas 仅用于读取文件与将 DataFrame 注册到 DuckDB
- Pandas 可用于注册前的数据安全预处理（如 `inf/-inf -> NULL`）
- 不使用 Pandas 做业务聚合分析、统计计算或口径产出
- 最终分析结果必须通过 DuckDB SQL 查询 `data` 表生成

### 字段名示例

```sql
SELECT "销售渠道", SUM("售后退款-仅退货金额") AS total_return
FROM data
GROUP BY "销售渠道"
ORDER BY total_return DESC
LIMIT 10
```

```sql
SELECT 销售渠道, SUM(售后退款-仅退货金额) AS total_return
FROM data
GROUP BY 销售渠道
```
