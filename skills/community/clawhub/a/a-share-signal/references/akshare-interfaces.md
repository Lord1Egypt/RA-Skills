# AkShare 接口参考

当问题需要更具体的数据接口、字段方向或备用抓取方案时，读取这份参考。

## 使用原则

- 优先单只股票、单个问题的定向拉取，不要默认全市场扫描。
- 优先用 `AkShare`，只有在安装失败或目标接口失效时再考虑 `baostock` 之类的备选方案。
- 数据只用于分析与研究，不要表达成投资承诺。
- 接口偶尔会因为上游网页变动失效，必要时切换同类接口，不要因为单点失败直接终止。

## 安装

```bash
pip install akshare
```

## 常用接口

### 1. 实时行情

```python
import akshare as ak

# A股实时行情
ak.stock_zh_a_spot_em()

# 指定市场
ak.stock_zh_a_spot_em(symbol="北证A股")
```

适合用于：
- 搜索股票
- 看最新价格、涨跌幅、成交额、换手率
- 做候选股票快速筛选

### 2. 历史K线

```python
import akshare as ak

ak.stock_zh_a_hist(
    symbol="000001",
    period="daily",
    start_date="20240101",
    end_date="20241231",
    adjust="qfq",
)

ak.stock_zh_a_hist(
    symbol="000001",
    period="weekly",
    start_date="20240101",
    end_date="20241231",
    adjust="qfq",
)

ak.stock_zh_a_hist(
    symbol="000001",
    period="monthly",
    start_date="20240101",
    end_date="20241231",
    adjust="qfq",
)
```

适合用于：
- 均线系统
- 三周期共振
- KDJ、MACD 等指标
- 威科夫和缠论的基础结构判断

### 3. 财务数据

```python
import akshare as ak

ak.stock_financial_abstract_ths(symbol="000001", indicator="按报告期")
ak.stock_financial_analysis_indicator(symbol="000001")
```

适合用于：
- 排除基本面恶化
- 看营收、利润、现金流等关键指标

### 4. 板块与概念

```python
import akshare as ak

ak.stock_board_industry_name_em()
ak.stock_board_concept_name_em()
ak.stock_board_industry_cons_em(symbol="半导体")
```

适合用于：
- 识别行业强弱
- 判断板块共振
- 查看某行业或概念内成分股

### 5. 资金流向

```python
import akshare as ak

ak.stock_individual_fund_flow(stock="000001", market="sh")
ak.stock_individual_fund_flow(stock="000001", market="sh", symbol="大单净流入")
```

适合用于：
- 验证突破是否得到资金配合
- 看主力、大单资金是否持续流入

### 6. 龙虎榜与游资行为

```python
import akshare as ak

ak.stock_lhb_detail_em(date="20240930")
ak.stock_zlzj_em()
```

适合用于：
- 看活跃资金参与痕迹
- 观察短线题材情绪

### 7. 新股与 IPO

```python
import akshare as ak

ak.stock_new_ipo_em()
ak.stock_new_ipo_start_em()
```

适合用于：
- 新股申购信息
- 待上市新股跟踪

### 8. 融资融券

```python
import akshare as ak

ak.stock_margin_sse(symbol="600000")
ak.stock_rzrq_detail_em(symbol="600000", date="20240930")
```

适合用于：
- 看杠杆资金参与度
- 辅助判断风险偏好


## 备用方案：Baostock

如果 `AkShare` 安装失败，或特定环境下网络问题导致接口不可用，可用更轻量的 `baostock` 作为历史数据备选：

```python
import baostock as bs

lg = bs.login()
print(lg.error_msg)

rs = bs.query_history_k_data_plus(
    "sh.600519",
    "date,code,open,high,low,close,volume",
    start_date="20250101",
    end_date="20251231",
)

data_list = []
while rs.next():
    data_list.append(rs.get_row_data())

bs.logout()
```

## 实务建议

- 先查实时行情与历史K线，再决定是否补财务、板块、资金流。
- 如果用户问的是“这只票能不能做”，不要把回答做成接口清单，要把数据转成结论。
- 如果用户给了自己的规则，优先让接口为规则服务，而不是反过来堆数据。
