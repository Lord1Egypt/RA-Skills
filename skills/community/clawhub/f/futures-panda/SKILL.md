---
name: futures-panda
description: 通过AKShare财经数据接口库封装，提供股期货、期权的实时数据、历史行情数据、仓单数据、席位数据、基差数据、期货合约基础数据和期货交易费用参照表数据。
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "requires": { "pip": ["akshare>=1.12", "pandas>=1.5"] },
        "install":
          [
            {
              "id": "pip-install",
              "kind": "pip",
              "packages": ["akshare>=1.12", "pandas>=1.5"],
              "label": "安装AKShare依赖"
            }
          ]
      }
  }
keywords:
  - 期货
  - 期权
  - 行情
  - 基本面
  - 期货基础数据
  - AKShare
---

# AKShare财经数据技能

## 快速开始

```bash
# 安装依赖
pip install akshare pandas

# 测试安装
python -c "import akshare; print(akshare.__version__)"
```

## 核心功能

### 1. 期货实时数据

```python
import akshare as ak

# 期货实时行情
futures_zh_spot(symbol='RB2605', market="CF", adjust='0')  # 单合约实时数据获取

```

### 2. 期货历史行情

```python
# 日线历史数据
futures_zh_daily_sina(symbol="RB0")  

# 交易所历史数据
get_futures_daily(start_date="20200701", end_date="20200716", market="DCE")()  

# 分时历史数据：1": "1分钟", "5": "5分钟", "15": "15分钟", "30": "30分钟", "60": "60分钟"
futures_zh_minute_sina(symbol="RB0", period="1")  

```

### 3. 手续费与保证金

```python
# 期货交易费用参照表
futures_fees_info()

```

### 4. 交易日历表

```python
# 期货交易日历 
futures_rule(date="20231205")

```

### 7. 合约信息

```python
# 上海期货交易所期货合约
futures_contract_info_shfe(date="20240513")
# 国际能源中心期货交易所期货合约
futures_contract_info_ine(date="20241129")
# 大连商品期货交易所期货合约
futures_contract_info_dce()
# 郑州期货交易所期货合约
futures_contract_info_czce(date="20240228")
# 广州期货交易所期货合约
futures_contract_info_gfex()
# 中金期货交易所期货合约
futures_contract_info_cffex(date="20240228")
#连续合约品种一览表接口
futures_display_main_sina()
```

### 8. 现货与股票

```python
# symbol="能源"; choice of {'能源', '化工', '塑料', '纺织', '有色', '钢铁', '建材', '农副'}
futures_spot_stock(symbol="能源")
```
## 实用脚本

除了直接调用 AKShare 函数，本技能还提供了封装好的命令行脚本，位于 `scripts/` 目录下：

- `futures_data.py`：**（新增）** 获取期货实时行情、历史数据、仓单、基差等

使用方法详见 `references/README.md` 中的示例。

## 注意事项

1. **数据来源**: 公开财经网站，仅用于学术研究
2. **商业风险**: 投资有风险，决策需谨慎
3. **更新频率**: 实时数据可能有延迟
4. **数据验证**: 建议多数据源交叉验证


## 参考文档

- AKShare文档: https://akshare.akfamily.xyz/
- GitHub: https://github.com/akfamily/akshare
