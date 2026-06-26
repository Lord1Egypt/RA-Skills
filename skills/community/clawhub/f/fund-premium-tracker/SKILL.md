# 场内基金溢价率查询

A股场内基金（ETF/LOF/QDII）溢价率实时查询与历史分析工具。

## 触发词

"溢价率"、"场内基金溢价"、"ETF溢价"、"LOF溢价"、"基金折价"、"premium rate"、"套利"

## 功能

### 1. 实时溢价率查询

查询指定基金当前场内价格与净值的偏离程度。

```bash
python3 {baseDir}/scripts/premium_realtime.py <基金代码> [基金代码2 ...]
```

**示例：**
```bash
# 查单只
python3 {baseDir}/scripts/premium_realtime.py 513050

# 批量查询
python3 {baseDir}/scripts/premium_realtime.py 513050 159915 164824
```

**输出包含：**
- 场内实时价格
- 基金净值（盘中估值优先，无估值时用最新公布净值）
- 溢价率百分比及风险等级
- 涨跌幅

### 2. 历史溢价率查询

查看某只基金近N个交易日的溢价率变动趋势。

```bash
python3 {baseDir}/scripts/premium_history.py <基金代码> [--days N]
```

**示例：**
```bash
# 默认20个交易日
python3 {baseDir}/scripts/premium_history.py 513050

# 指定天数
python3 {baseDir}/scripts/premium_history.py 159941 --days 30
```

**输出包含：**
- 每日收盘价、净值、溢价率表格
- 简易柱状图
- 统计摘要（均值/最高/最低）
- 趋势判断与风险提示

## 支持的基金类型

| 类型 | 代码前缀 | 示例 |
|------|----------|------|
| 上海ETF | 51xxxx | 513050 中概互联网ETF |
| 深圳ETF | 15xxxx | 159915 创业板ETF |
| 上海LOF | 50xxxx | 501009 汇添富中证生物科技 |
| 深圳LOF | 16xxxx | 164824 印度基金LOF |
| QDII场内 | 各前缀 | 159941 纳指ETF |

## 数据源

东方财富公开API（免费、无需注册、无需Token）：
- 实时行情：push2.eastmoney.com
- 基金净值：api.fund.eastmoney.com
- 盘中估值：fundgz.1234567.com.cn
- 历史K线：push2his.eastmoney.com

## 溢价率计算逻辑

```
盘中溢价率 = (实时场内价 - 盘中估值) / 盘中估值 × 100%
收盘溢价率 = (收盘价 - 当日净值) / 当日净值 × 100%
```

**QDII/跨境基金特殊说明：**
由于时差，QDII基金净值通常滞后1-2个交易日公布。实时溢价率计算使用最新可用净值，可能存在偏差。

## 风险等级

| 溢价率范围 | 等级 |
|:---:|:---:|
| -1% ~ +1% | 正常 |
| ±1% ~ ±3% | 轻微溢价/折价 |
| ±3% ~ ±5% | ⚠️ 较高 |
| > ±5% | 🚨 极端 |

## 依赖

- Python 3（标准库，无需 pip install）
- 网络访问（东方财富API）
