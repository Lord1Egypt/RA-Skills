# BaoStock 金融数据技能

调用免费开源的A股金融数据平台BaoStock，无需注册即可获取历史K线、财务数据、宏观数据。

## 功能

- 历史K线数据（日/周/月/分钟线）
- 季频财务数据（盈利、营运、成长、偿债、现金流、杜邦）
- 季频公司报告（业绩快报、业绩预告）
- 证券基本资料
- 交易日/证券代码查询
- 宏观经济数据（存贷款利率、准备金率、货币供应量）
- 板块数据（行业分类、指数成分股）

## 安装

```bash
pip install baostock
```

## 使用示例

### 获取股票K线

```python
import baostock as bs
import pandas as pd

lg = bs.login()
rs = bs.query_history_k_data_plus("sh.600000", "date,code,open,high,low,close", 
                                   start_date='2024-01-01', end_date='2024-12-31')
data_list = []
while (rs.error_code == '0') & rs.next():
    data_list.append(rs.get_row_data())
df = pd.DataFrame(data_list, columns=rs.fields)
print(df)
bs.logout()
```

### 获取财务数据

```python
import baostock as bs

lg = bs.login()
rs = bs.query_profit_data(code="sh.600000", year=2024, quarter=2)
while rs.next():
    print(rs.get_row_data())
bs.logout()
```

## 股票代码

- `sh.600000` - 上海股票
- `sz.000001` - 深圳股票
- `sh.000001` - 上证指数
