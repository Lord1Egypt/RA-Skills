# AKShare 期货数据技能包

## 简介

本技能基于 AKShare 封装了期货市场的主要数据接口，提供实时行情、历史数据、合约信息、手续费、交易日历等数据的快速获取。所有功能通过一个命令行脚本 `futures_data.py` 实现，返回 JSON 格式数据，便于集成到其他应用或进行数据分析。

---

## 安装

确保已安装 Python 3.10+，然后安装依赖：

```bash
pip install akshare pandas
```

验证安装：

```bash
python -c "import akshare; print(akshare.__version__)"
```

## 快速开始

进入 `scripts/` 目录，运行以下命令获取螺纹钢主力连续合约的实时行情：

```bash
python3 futures_data.py spot RB2605
```

返回示例（JSON 格式）：

```json
[
  {
    "symbol": "RB2605",
    "open": 3200,
    "high": 3220,
    "low": 3190,
    "price": 3215,
    "..." : "..."
  }
]
```

## 命令参考

所有命令均通过 `python futures_data.py <命令> [参数...]` 调用。下表列出了当前支持的命令及其功能。

| 命令 | 功能说明 | 参数 | 示例 |
| :--- | :--- | :--- | :--- |
| `spot` | 获取期货实时行情 | `symbol`（合约代码，如 RB2605）<br>`market`（市场，默认 CF）<br>`adjust`（复权类型，默认 0） | `python3 futures_data.py spot RB2605` |
| `daily` | 获取期货历史日线数据（新浪） | `symbol`（合约代码或主力连续，如 RB0） | `python3 futures_data.py daily RB0` |
| `minute` | 获取期货分钟线数据 | `symbol`（合约代码）<br>`period`（周期：1=1分钟，5=5分钟，15=15分钟，30=30分钟，60=60分钟） | `python3 futures_data.py minute RB0 5` |
| `daily_ex` | 获取指定交易所的历史日线数据<br>*(注：此接口可能依赖特定 AKShare 版本，如不可用请使用 daily)* | `start_date`（开始日期，YYYYMMDD）<br>`end_date`（结束日期）<br>`market`（交易所代码，如 DCE） | `python3 futures_data.py daily_ex 20200701 20200716 DCE` |
| `fees` | 获取期货交易费用参照表 | 无 | `python3 futures_data.py fees` |
| `calendar` | 获取期货交易日历 | `date`（查询日期，YYYYMMDD） | `python3 futures_data.py calendar 20231205` |
| `contract_shfe` | 获取上期所期货合约信息 | `date`（日期，可选，默认 20240513） | `python3 futures_data.py contract_shfe 20240513` |
| `contract_ine` | 获取国际能源中心期货合约信息 | `date`（日期，可选） | `python3 futures_data.py contract_ine 20241129` |
| `contract_dce` | 获取大商所期货合约信息 | 无 | `python3 futures_data.py contract_dce` |
| `contract_czce` | 获取郑商所期货合约信息 | `date`（日期，可选） | `python3 futures_data.py contract_czce 20240228` |
| `contract_gfex` | 获取广期所期货合约信息 | 无 | `python3 futures_data.py contract_gfex` |
| `contract_cffex` | 获取中金所期货合约信息 | `date`（日期，可选） | `python3 futures_data.py contract_cffex 20240228` |
| `main_contracts` | 获取连续合约品种一览表 | 无 | `python3 futures_data.py main_contracts` |
| `spot_stock` | 获取现货与股票关联数据 | `symbol`（板块：能源、化工、塑料、纺织、有色、钢铁、建材、农副） | `python3 futures_data.py spot_stock 能源` |

## 数据格式

所有成功执行的命令均返回一个 JSON 数组，数组中的每个元素对应一条数据记录（字典）。字段名称与 AKShare 返回的 DataFrame 列名一致。

错误时返回 JSON 对象，包含 `error` 字段描述错误信息。

## 注意事项

- **数据来源**：所有数据均来自公开财经网站，仅用于学术研究和学习，不构成投资建议。
- **数据延迟**：实时行情可能存在数秒延迟，请勿用于高频交易。
- **接口稳定性**：AKShare 接口可能会随源网站变化而调整，如遇命令失效，请查阅 AKShare 官方文档 更新函数调用。
- **参数格式**：日期参数统一使用 `YYYYMMDD` 格式，如 `20240430`。

## 许可证

本项目仅供学习和研究使用，遵循 MIT License。

## 如有问题或建议

请提交 Issue 或联系维护者：
- 📧 Email: 12141234@qq.com
- 📚 文档：[AKShare 官方文档](https://akshare.akfamily.xyz/)
```