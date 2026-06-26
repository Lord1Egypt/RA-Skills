# AShareSkill 📈

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![BaoStock](https://img.shields.io/badge/DataSource-BaoStock-orange)](http://baostock.com/)

> 专业A股数据获取工具，支持K线数据及完整技术指标分析

[English](#english) | [中文](#中文)

---

## 中文

### 🔥 功能特点

- **多维度数据获取**：支持单只股票、股票池、指数成分股批量查询
- **多级别K线**：日线(d)、周线(w)、月线(m)灵活切换
- **完整技术指标**：
  - 均线系统：MA5, MA10, MA20, MA30, MA60, MA120, MA250
  - MACD指标：DIF, DEA, MACD柱状图
  - KDJ指标：K值, D值, J值
  - RSI指标：6日/12日/24日相对强弱指标
  - 布林带(BOLL)：上轨、中轨、下轨
  - CCI指标：商品通道指数
- **智能股票识别**：支持股票名称或代码自动匹配
- **单一文件输出**：所有数据输出为CSV格式，便于分析

### 📦 安装

```bash
# 克隆仓库
git clone https://github.com/caoyachao/ashareskill.git
cd ashareskill

# 安装依赖
pip install -r requirements.txt
```

**依赖要求：**
- Python >= 3.8
- baostock >= 0.8.8
- pandas >= 1.3.0
- numpy >= 1.21.0

### 🚀 快速开始

#### 1. 命令行使用

```bash
# 获取单只股票日线数据
python scripts/ashareskill.py -s 贵州茅台 --start 2024-01-01 --end 2024-12-31

# 获取股票池周线数据
python scripts/ashareskill.py -s "贵州茅台,中国平安,宁德时代" --start 2024-01-01 -f w

# 获取指数成分股月线数据（中证500）
python scripts/ashareskill.py -i 000905 --start 2024-01-01 -f m -o zz500_monthly.csv

# 获取沪深300指数日线数据
python scripts/ashareskill.py -s 000300 --start 2025-01-01 -f d
```

#### 2. Python模块使用

```python
from scripts.ashareskill import AShareSkill

# 创建实例
skill = AShareSkill()

# 获取单只股票数据
df = skill.get_kline_data(
    stock_code="贵州茅台",
    start_date="2024-01-01",
    end_date="2024-12-31",
    frequency="d"
)

# 获取多只股票数据
df_pool = skill.get_stock_pool_data(
    stock_list=["贵州茅台", "中国平安", "宁德时代"],
    start_date="2024-01-01",
    frequency="w"
)

# 保存数据
skill.save_to_csv(df_pool, "output.csv")
```

### 📊 输出字段说明

| 字段名 | 说明 | 示例 |
|--------|------|------|
| `code` | 股票代码 | sh.600519 |
| `name` | 股票名称 | 贵州茅台 |
| `date` | 交易日期 | 2024-03-15 |
| `open` | 开盘价 | 1700.50 |
| `high` | 最高价 | 1720.00 |
| `low` | 最低价 | 1690.00 |
| `close` | 收盘价 | 1710.30 |
| `volume` | 成交量（股） | 2500000 |
| `amount` | 成交额（元） | 4275750000 |
| `turn` | 换手率 | 0.1992 |
| `pctChg` | 涨跌幅(%) | 0.57 |
| `peTTM` | 滚动市盈率 | 28.5 |
| `pbMRQ` | 市净率 | 8.2 |
| **均线指标** | | |
| `ma5` ~ `ma250` | 移动平均线 | 详见技术指标 |
| **MACD** | | |
| `macd_dif` | DIF线 | 1.25 |
| `macd_dea` | DEA线 | 0.85 |
| `macd` | MACD柱状 | 0.80 |
| **KDJ** | | |
| `kdj_k` | K值 | 65.32 |
| `kdj_d` | D值 | 58.45 |
| `kdj_j` | J值 | 79.06 |
| **RSI** | | |
| `rsi_6` | 6日RSI | 55.6 |
| `rsi_12` | 12日RSI | 52.3 |
| `rsi_24` | 24日RSI | 48.9 |
| **布林带** | | |
| `boll_upper` | 上轨 | 1750.00 |
| `boll_middle` | 中轨 | 1700.00 |
| `boll_lower` | 下轨 | 1650.00 |
| **CCI** | | |
| `cci` | CCI指标 | 45.2 |

### 📝 参数说明

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--stock` | `-s` | 股票名称或代码（多只用逗号分隔） | - |
| `--index` | `-i` | 指数代码（000905中证500等） | - |
| `--start` | - | 开始日期 (YYYY-MM-DD) | 一年前 |
| `--end` | - | 结束日期 (YYYY-MM-DD) | 今天 |
| `--freq` | `-f` | K线级别: d/w/m | d |
| `--adjust` | `-a` | 复权: 1前复权/2后复权/3不复权 | 3 |
| `--output` | `-o` | 输出文件名 | 自动生成 |

### 💡 使用示例

#### 示例1：获取个股技术指标
```bash
python scripts/ashareskill.py -s 600519 --start 2024-01-01 -f d -o maotai.csv
```

#### 示例2：批量获取股票池
```bash
python scripts/ashareskill.py -s "000001,000002,000333" --start 2024-06-01 -f w
```

#### 示例3：获取中证500成分股
```bash
python scripts/ashareskill.py -i 000905 --start 2024-01-01 -f m
```

### ⚠️ 注意事项

1. **首次使用**：会自动登录BaoStock并加载股票列表
2. **K线级别**：
   - `d` - 日线：每个交易日一条数据
   - `w` - 周线：每周一条数据
   - `m` - 月线：每月一条数据
3. **技术指标**：
   - 均线需要足够历史数据（MA120需120个交易日）
   - 周线/月线部分字段可能缺失（preclose, isST）
4. **指数支持**：
   - `000905` - 中证500
   - `000300` - 沪深300
   - `000016` - 上证50
5. **批量获取**：500只股票建议分批处理，避免超时

### 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

### 🤝 贡献

欢迎提交Issue和Pull Request！

---

## English

### 🔥 Features

- **Multi-dimensional Data**: Support single stock, stock pool, and index component queries
- **Multi-level K-lines**: Daily(d), Weekly(w), Monthly(m) flexibility
- **Complete Technical Indicators**: MA, MACD, KDJ, RSI, Bollinger Bands, CCI
- **Smart Stock Recognition**: Auto-match by stock name or code
- **Single File Output**: CSV format for easy analysis

### 📦 Installation

```bash
git clone https://github.com/caoyachao/ashareskill.git
cd ashareskill
pip install -r requirements.txt
```

### 🚀 Quick Start

```bash
# Single stock daily data
python scripts/ashareskill.py -s 600519 --start 2024-01-01

# Stock pool weekly data
python scripts/ashareskill.py -s "600519,000001,000002" -f w

# Index components monthly data
python scripts/ashareskill.py -i 000905 -f m
```

### 📄 License

[MIT License](LICENSE)

---

**免责声明**：本工具仅供学习研究使用，不构成投资建议。股市有风险，投资需谨慎。

**Disclaimer**: This tool is for educational purposes only and does not constitute investment advice.
