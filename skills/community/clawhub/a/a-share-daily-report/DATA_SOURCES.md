# A股日报 - 数据源配置表

> 本文档定义A股日报各模块的数据源优先级、具体接口和使用说明

---

## ✅ 环境检查结果

| 项目 | 状态 | 说明 |
|------|------|------|
| **Python venv** | ✅ 可用 | `/Users/yibiao/.openclaw/workspace-trader/venv/` |
| **akshare** | ✅ 已安装 | 版本 1.18.44（在 venv 中） |
| **tushare-skills** | ✅ 已全局配置 | Token 和接口地址已内置，无需手动配置 |
| **TUSHARE_TOKEN** | ✅ 已配置 | 环境变量已设置 |
| **MX_APIKEY** | ✅ 已配置 | 妙想金融数据 API key |
| **mx-data Skill** | ✅ 可用 | 已安装 |
| **mx-search Skill** | ✅ 可用 | 已安装 |

---

## 📊 完整数据源映射表

### 早报预测版 & 晚报复盘版 通用

| 模块 | 子模块 | 优先级1 | 优先级2 | 优先级3 | 优先级4 |
|------|--------|---------|---------|---------|---------|
| **【A股大盘】** | 四大指数（上证/深证/创业板/科创50） | 🎯 **akshare-cn-market Skill** `stock_zh_index_daily()` | 🎯 **tushare-skills Skill** `pro.index_daily()` | 🎯 **mx-data Skill** "查询指数行情" | 新浪财经API |
| **【市场情绪】** | 涨跌家数/涨跌停/连板高度/炸板率/昨日涨停表现 | 🎯 **akshare-cn-market Skill** `stock_zt_pool_em()` + `stock_zt_pool_previous_em()` | 🎯 **tushare-skills Skill** `pro.limit_list_d()` | 🎯 **mx-data Skill** "查询涨跌停数据" | 东方财富API |
| **【资金流向】** | 北向资金/主力资金 | 🎯 **akshare-cn-market Skill** `stock_hsgt_hist_em()` + `stock_market_fund_flow()` | 🎯 **tushare-skills Skill** `pro.moneyflow_hsgt()` + `pro.moneyflow_index()` | 🎯 **mx-data Skill** "查询资金流向" | 东方财富API |
| **【板块全景】** | 涨幅榜前5/跌幅榜前5/板块资金/热点概念 | 🎯 **akshare-cn-market Skill** `stock_sector_fund_flow_rank()` | 🎯 **tushare-skills Skill** `pro.sector()` | 🎯 **mx-data Skill** "查询板块涨跌" | 东方财富API |
| **【个股动态】** | 龙虎榜/异动股/新高新低 | 🎯 **akshare-cn-market Skill** `stock_lhb_detail_em()` | 🎯 **tushare-skills Skill** `pro.top_list()` | 🎯 **mx-data Skill** "查询龙虎榜" | 东方财富API |
| **【国际盘面-美股】** | 标普/纳斯达克/道指 | 新浪财经API `hq.sinajs.cn/list=gb_ixic,gb_inx,gb_dji` | 🎯 **tushare-skills Skill** `pro.us_daily()` | 🎯 **mx-data Skill** "查询美股指数" | Yahoo Finance |
| **【国际盘面-中概股】** | 腾讯/阿里/拼多多 | 新浪财经API `hq.sinajs.cn/list=gb_tceh,gb_baba,gb_pdd` | 🎯 **tushare-skills Skill** `pro.us_daily()` | 🎯 **mx-data Skill** "查询中概股" | - |
| **【国际盘面-港股】** | 恒生指数/恒生科技/腾讯/阿里/美团 | 🎯 **akshare-cn-market Skill** `hk_index_daily()` | 新浪财经API `rt_hkHSI,rt_hkHSCEI` | 🎯 **mx-data Skill** "查询港股" | 阿斯达克 |
| **【大宗商品】** | 原油/黄金/铜 | 新浪财经API `hf_OIL,hf_GC,hf_HG` | 🎯 **tushare-skills Skill** `pro.commodity()` | 🎯 **mx-data Skill** "查询商品期货" | Wind |
| **【外汇市场】** | 美元指数/人民币汇率 | 新浪财经API `fx_sUSDCNY,fx_dEURUSD` | 🎯 **tushare-skills Skill** `pro.fx_daily()` | 🎯 **mx-data Skill** "查询外汇" | 央行官网 |
| **【期指表现】** | A50期指/沪深300期指夜盘 | 新浪财经API `CFF_RE_IF,CFF_RE_IC` | 🎯 **mx-data Skill** "查询期指" | 东方财富API | - |
| **【国内要闻】** | 10篇新闻，分级显示 | 🎯 **mx-search Skill** "查询财经新闻" | 东方财富新闻API | 财联社API | 新浪财经新闻 |
| **【宏观事件】** | 重要政策/事件 | 🎯 **mx-search Skill** "查询宏观政策" | 🎯 **tushare-skills Skill** `pro.news()` | 东方财富新闻 | 财联社 |

---

## 🎯 数据源稳定性优先级（推荐使用顺序）

### Tier 1（最稳定，首选）
```
✅ akshare (新浪源) - 完全免费，无需token，极其稳定
   ├─ A股指数：stock_zh_index_daily()
   ├─ 涨跌停/情绪：stock_zt_pool_em()
   ├─ 资金流向：stock_market_fund_flow() + stock_hsgt_hist_em()
   ├─ 板块排行：stock_sector_fund_flow_rank()
   └─ 龙虎榜：stock_lhb_detail_em()
```

### Tier 2（稳定，需要token）
```
✅ mx-data (东方财富权威数据) - 需要 MX_APIKEY（已配置）
   ├─ 行情数据：自然语言查询
   ├─ 财务数据：基本面指标
   └─ 资金流向：实时数据
```

### Tier 3（稳定，已全局配置）
```
✅ tushare-skills - 已全局配置，无需手动设置token
   ├─ 使用方式：from skills.tushare-skills.tushare.scripts.tushare_init import pro
   ├─ 指数数据：pro.index_daily()
   ├─ 财务数据：pro.fina_indicator()
   ├─ 宏观数据：pro.cn_gdp(), pro.cn_cpi()
   └─ 接口地址：http://lianghua.nanyangqiankun.top（已内置）
```

### Tier 4（补充数据）
```
✅ 新浪财经API - 免费
   ├─ 美股：gb_ixic, gb_inx, gb_dji
   ├─ 中概股：gb_tceh, gb_baba, gb_pdd
   ├─ 商品：hf_OIL, hf_GC, hf_HG
   ├─ 外汇：fx_sUSDCNY
   └─ 期指：CFF_RE_IF
```

---

## 🔧 数据接口使用速查

### AKShare 常用接口（Tier 1，首选）
```python
import akshare as ak

# 指数K线
df = ak.stock_zh_index_daily(symbol="sh000001")  # 上证综指
df = ak.stock_zh_index_daily(symbol="sz399001")  # 深证成指
df = ak.stock_zh_index_daily(symbol="sz399006")  # 创业板指
df = ak.stock_zh_index_daily(symbol="sh000688")  # 科创50

# 涨跌停池
df = ak.stock_zt_pool_em(date="20260328")        # 涨停池
df = ak.stock_zt_pool_previous_em(date="20260328") # 昨日涨停
df = ak.stock_zt_pool_dtgc_em(date="20260328")   # 跌停池

# 资金流向
df = ak.stock_market_fund_flow()                    # 全市场主力资金
df = ak.stock_hsgt_hist_em(symbol="北向资金")      # 北向资金历史

# 板块排行
df = ak.stock_sector_fund_flow_rank(indicator="今日", sector_type="概念资金流向")

# 龙虎榜
df = ak.stock_lhb_detail_em(start_date="20260328", end_date="20260328")
```

### tushare-skills 常用接口（Tier 2，已全局配置）
```python
# 注意：需要在正确的路径下导入
import sys
sys.path.append('/Users/yibiao/.openclaw/workspace-trader/skills/tushare-skills/tushare')

from scripts.tushare_init import pro, ts

# 指数日线数据
df = pro.index_daily(ts_code='000001.SH', start_date='20240101', end_date='20260328')

# 沪深300成分股
df = pro.index_weight(index_code='000300.SH', start_date='20260301', end_date='20260331')

# 北向资金历史
df = pro.moneyflow_hsgt(start_date='20240101', end_date='20260328')

# 财务指标
df = pro.fina_indicator(ts_code='600519.SH', start_date='20240101', end_date='20260328')

# 宏观数据
df = pro.cn_gdp(start_date='2024Q1', end_date='2026Q1')
df = pro.cn_cpi(start_date='202401', end_date='202603')

# 龙虎榜
df = pro.top_list(trade_date='20260328')
```

### 交易日历
```python
from skills.akshare-cn-market.scripts.trade_cal import (
    is_trade_day,
    next_trade_day,
    prev_trade_day
)

# 判断今天是否为交易日
if not is_trade_day("2026-03-28"):
    print("非交易日，使用最近一个收盘日数据")
    last_close = prev_trade_day("2026-03-28")
```

---

## 📰 新浪财经API速查

### 美股/中概股
```python
# 格式：http://hq.sinajs.cn/list=gb_<代码>
# 美股指数：ixic(纳指), inx(标普), dji(道指)
# 中概股：tceh(腾讯), baba(阿里), pdd(拼多多)

import urllib.request

url = "http://hq.sinajs.cn/list=gb_ixic,gb_inx,gb_dji,gb_tceh,gb_baba,gb_pdd"
content = urllib.request.urlopen(url).read().decode('gbk')

# 解析数据
import re
pattern = r'var hq_str_gb_(\w+)="([^"]+)";'
matches = re.findall(pattern, content)
for symbol, data_str in matches:
    parts = data_str.split(',')
    if len(parts) >= 6:
        name = parts[0]
        price = float(parts[1])
        change = float(parts[4])
        change_pct = float(parts[5])
```

### 大宗商品/外汇/期指
```python
# 原油：hf_OIL, 黄金：hf_GC, 铜：hf_HG
# 美元指数：fx_sUSDCNY, 人民币汇率：fx_dUSDCNY
# 沪深300期指：CFF_RE_IF, 中证500期指：CFF_RE_IC

url = "http://hq.sinajs.cn/list=hf_OIL,hf_GC,hf_HG,fx_sUSDCNY,CFF_RE_IF"
content = urllib.request.urlopen(url).read().decode('gbk')
```

---

## 🚨 数据获取失败处理规则

1. **非交易日处理**：自动使用 `prev_trade_day()` 获取最近一个收盘日数据
2. **单模块失败**：该模块显示「数据获取失败」，不影响其他模块
3. **主数据源降级**：优先级1失败 → 自动尝试优先级2 → 优先级3 → ...
4. **所有源失败**：对应模块显示「数据获取失败」，**不使用硬编码默认值**

---

## 📝 使用方式

### 在 venv 中运行（推荐）
```bash
cd /Users/yibiao/.openclaw/workspace-trader
source venv/bin/activate
python3 skills/a-share-daily-report/scripts/generate_report.py --mode morning
```

### 已配置的环境变量
```bash
# .env 文件中已配置：
TUSHARE_TOKEN
MX_APIKEY
```

### tushare-skills 使用注意事项
✅ 已全局配置完成，无需手动设置token和接口地址
- 接口地址：http://lianghua.nanyangqiankun.top
- Token：已内置
- 使用方式：`from skills.tushare-skills.tushare.scripts.tushare_init import pro, ts`
- 注意：需要添加正确的 sys.path 才能导入
```python
import sys
sys.path.append('/Users/yibiao/.openclaw/workspace-trader/skills/tushare-skills/tushare')
from scripts.tushare_init import pro, ts
```
