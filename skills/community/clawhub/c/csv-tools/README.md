# 📊 CSV Tools v1.1.0

**CSV 全方位处理工具集** — 预览、筛选、排序、合并、分割、去重、验证、统计、列操作、类型检测、数据画像、抽样。12个子命令覆盖CSV数据处理的完整工作流。

纯 Python 标准库（csv 模块），无任何外部依赖。

---

## 安装

无需安装。确保系统已安装 Python 3（≥3.8）。

```bash
# 验证
python3 --version
```

## 子命令一览

| 命令 | 功能 | 新增版本 |
|------|------|---------|
| `preview` | 预览CSV结构与前5行 | 1.0.0 |
| `filter` | 按条件筛选行 | 1.0.0 |
| `sort` | 按列排序 | 1.0.0 |
| `merge` | 纵向合并多个CSV | 1.0.0 |
| `split` | 按行数分割大文件 | 1.0.0 |
| `dedup` | 按指定列去重 | 1.0.0 |
| `validate` | 检查空值/异常值 | 1.0.0 |
| **`stats`** | **列统计（sum/avg/min/max/std）** | **1.1.0** |
| **`columns`** | **列操作（重命名/选择/计算列）** | **1.1.0** |
| **`detect`** | **数据类型自动检测** | **1.1.0** |
| **`profile`** | **数据画像（缺失率/唯一值/分布）** | **1.1.0** |
| **`sample`** | **随机抽样** | **1.1.0** |

## 快速上手指南

### 数据探索
```bash
# 先看结构
python3 scripts/csv_tools.py preview data.csv

# 检查数据类型
python3 scripts/csv_tools.py detect data.csv

# 数据完整性与画像
python3 scripts/csv_tools.py profile data.csv

# 列统计
python3 scripts/csv_tools.py stats data.csv
```

### 数据清洗
```bash
# 去重
python3 scripts/csv_tools.py dedup data.csv --on "email"

# 检查空值
python3 scripts/csv_tools.py validate data.csv --output issues.json

# 筛选有效数据
python3 scripts/csv_tools.py filter data.csv --where "status=active"
```

### 数据导出/分割
```bash
# 分割大文件
python3 scripts/csv_tools.py split data.csv --chunk-size 5000

# 合并多个文件
python3 scripts/csv_tools.py merge q1.csv q2.csv q3.csv --output yearly.csv

# 抽样
python3 scripts/csv_tools.py sample data.csv --n 50 --method random
```

### 列变换
```bash
# 重命名 + 选择
python3 scripts/csv_tools.py columns data.csv \
  --rename "amount=revenue" --select "id,name,revenue"

# 添加计算列
python3 scripts/csv_tools.py columns data.csv \
  --add "total=price * quantity" \
  --add "tax=total * 0.13" \
  --output with_calc.csv
```

## 输出说明

- 筛选/排序/合并/去重/列操作 → CSV 文件
- validate → JSON 文件（issuse数组）
- stats/detect/profile/preview → 终端输出
- sample → 终端输出，可选 CSV 导出

## 使用场景

| 场景 | 推荐命令 | 说明 |
|------|---------|------|
| 数据导入前检查 | `preview` + `validate` | 检查结构和缺失值 |
| 数据清洗 | `dedup` + `filter` | 去重和筛选 |
| 数据审计 | `profile` + `stats` + `detect` | 完整性、分布、类型 |
| 批量处理 | `split` → 并行处理 → `merge` | 分割后再合并 |
| 抽样分析 | `sample --method random` | 随机子集分析 |

## 法律声明

本工具提供的数据处理和统计功能仅供参考和辅助决策。使用者应：

- 自行验证计算结果的准确性
- 根据业务场景判断数据含义
- 不依赖工具输出做出重大财务或合规决策

## 安全说明

- ✅ 纯本地运行，无网络请求
- ✅ 仅读写用户指定的文件路径
- ❌ 无系统命令执行（subprocess/shell）
- ❌ 无数据上传或遥测

## 许可证

MIT License
