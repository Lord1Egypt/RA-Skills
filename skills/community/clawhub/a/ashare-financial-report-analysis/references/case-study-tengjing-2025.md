# 腾景科技(688195.SH) 2025年报拆解——实战记录

> 首次使用ashare-financial-report-analysis skill的完整实战案例
> 日期：2026-08-12
> 分析师：Hermes (未央)

## 调用链路（完整API调用顺序）

### 第一批（并行）：基本信息+报告期确认
- `stock_basic(ts_code=688195.SH)` → 公司名称、行业、上市日期
- `disclosure_date(ts_code=688195.SH, end_date=20251231)` → 年报披露日2026-04-25
- `disclosure_date(ts_code=688195.SH, end_date=20260630)` → 半年报预计2026-08-29
- `disclosure_date(ts_code=688195.SH, end_date=20260331)` → 一季报已2026-04-25披露

### 第二批（并行）：财务三表+配套数据
- `income(period=20251231, report_type=1)` → 2025年利润表
- `income(period=20241231, report_type=1)` → 2024年利润表（上年同期）
- `balancesheet(period=20251231)` → 2025资产负债表
- `cashflow(period=20251231)` → 2025现金流量表
- `cashflow(period=20241231)` → 2024现金流量表（上年同期）
- `fina_indicator(period=20251231)` → 2025财务指标
- `fina_mainbz(period=20251231, type=P)` → 主营产品构成

### 第三批（并行）：资产负债表上年同期+估值+股东
- `balancesheet(period=20241231)` → 2024资产负债表
- `daily_basic(trade_date=20260812)` → ⚠️返回空！
- `daily_basic(trade_date=20260811)` → ✅成功
- `daily(start_date=20260714, end_date=20260812)` → 近20日行情
- `top10_floatholders(period=20251231)` → 前十大流通股东
- `stk_holdernumber()` → 股东人数全历史
- `pledge_stat()` → 返回空（无质押）
- `share_float(start_date=20260812, end_date=20270212)` → 返回空（无解禁）
- `dividend()` → 历年分红
- `repurchase()` → 回购记录
- `forecast(period=20251231)` → 返回空（无业绩预告）

### 第四批：补充数据
- `fina_indicator(period=20241231)` → 上年财务指标
- `report_rc(start_date=20260701, end_date=20260812)` → 机构研报
- `news(src=财联社, ...)` → ⚠️40203无权限
- `anns_d(...)` → ⚠️40203无权限

### 第五批：单季度数据（Q4计算用）
- `income(period=20250930)` → 2025前三季度（用于Q4=年报-Q3）
- `income(period=20240930)` → 2024前三季度
- `income(period=20250331)` → 2025Q1（用于Q1 2026 YoY对比）
- `income(period=20260331)` → 2026Q1

### 第六批：execute_code批量计算
- 将所有原始数值写入Python字典
- 统一计算所有指标，输出格式化结果
- EPS反推核验自动完成

## 关键发现

### 1. Tushare free_cashflow字段错误
- cashflow接口返回`free_cashflow: 132178021.50`（+1.32亿）
- 自算：n_cashflow_act(69803736.85) - c_pay_acq_const_fiolta(90250138.85) = -20446402.00（-0.20亿）
- 方向相反！已在skill中标注"禁止使用"

### 2. Q4单季度利润塌方
- Q4 2025归母0.068亿 vs Q4 2024归母0.139亿 = -50.9%
- Q4毛利率32.16% vs Q4 2024毛利率35.46% = -3.30pp
- Q4研发费用0.233亿 vs Q4 2024研发0.139亿 = +68.0%
- 这是全年最重要的发现——全年归母仅+1.8%是因为Q1-Q3撑住了

### 3. 筹码分散信号
- 股东人数：2024-12-31: 10,540 → 2025-12-31: 22,805 (+116.3%)
- 最新2026-06-10: 27,132（继续分散）
- 无质押、无解禁 → 两项无风险

### 4. 估值极端
- PE-TTM 368.2x, PB 26.05x, PS-TTM 41.21x
- ROE仅7.40%
- 股息率TTM 0.08%
- 7月股价暴跌35%后反弹49% → 典型高弹性主题股

## 模板填充完整度

| 节 | 完整度 | 缺口原因 |
|----|--------|---------|
| 一、营收结构 | ✅ 完整 | fina_mainbz提供了分部数据 |
| 二、盈利与扣非 | ✅ 完整 | income+fina_indicator数据齐全 |
| 三、资产负债表 | ⚠️ 部分 | 2024年部分科目为推算值 |
| 四、现金流 | ✅ 完整 | cashflow数据齐全（但free_cashflow字段不可信） |
| 五、股东回报 | ✅ 完整 | dividend+repurchase数据齐全 |
| 六、股东结构 | ⚠️ 部分 | 前十大股东明细未展开 |
| 七、业务里程碑 | ❌ 推断 | API不提供业务进展，基于财务数据推断 |
| 八、战略动作 | ❌ 推断 | 无业绩说明会纪要 |
| 九、估值快照 | ✅ 完整 | daily_basic数据齐全 |
| 十、同业对比 | ❌ 空框架 | 未拉取可比公司数据 |
| 十一、风险扫描 | ✅ 完整 | 基于资产负债表+股东数据 |
| 十二、核心判断 | ✅ 完整 | 6点判断+框架对照 |
| 十三、持仓启示 | ✅ 完整 | |
| 十四、下次关键时点 | ✅ 完整 | |
| 十五、资料链接 | ✅ 完整 | |

## 教训总结

1. **news/anns_d API无权限** → 需用cn-web-search替代
2. **daily_basic当日返回空** → 回退前一交易日
3. **free_cashflow不可信** → 必须自算
4. **Q4需手动计算** → 年报-三季报逐项相减
5. **execute_code批量计算** → 有效避免手工误差，推荐作为标准步骤
6. **第七/八/十节通常需手动补充** → 纯API无法填充
