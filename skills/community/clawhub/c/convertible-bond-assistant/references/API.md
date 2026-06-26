# 数据源 API 文档

## 📡 数据来源说明

本技能使用以下公开数据源：

---

## 一、可转债发行数据

### 东方财富网
**URL**: http://data.eastmoney.com/kzz/

**数据内容**:
- 可转债发行列表
- 申购日历
- 发行公告

**API 示例** (需逆向工程):
```
http://datacenter-web.eastmoney.com/api/data/v1/get
?reportName=RPT_BOND_CB_ISSUE
&columns=ALL
&filter=(SECURITY_TYPE_CODE="041001001")
&pageNum=1&pageSize=50
```

**字段说明**:
- SECURITY_CODE: 转债代码
- SECURITY_NAME: 转债名称
- ISSUE_AMOUNT: 发行金额（亿元）
- RATING: 信用评级
- SUBSCRIBE_DATE: 申购日期
- STOCK_CODE: 正股代码
- STOCK_NAME: 正股名称

---

## 二、可转债行情数据

### 新浪财经
**URL**: http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php

**API 示例**:
```
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php
?market=hs_kzz
&symbol=sh123205
```

**返回字段**:
- code: 转债代码
- name: 转债名称
- price: 当前价格
- change: 涨跌额
- changepercent: 涨跌幅
- volume: 成交量
- amount: 成交额

---

## 三、正股数据

### 腾讯财经
**URL**: http://qt.gtimg.cn/

**API 示例**:
```
http://qt.gtimg.cn/q=sh600000
```

**返回字段**:
- 正股价格
- 涨跌幅
- PE/PB
- 总市值

---

## 四、转股价值计算

**公式**:
```
转股价值 = 正股价格 / 转股价格 × 100
转股溢价率 = (转债价格 - 转股价值) / 转股价值 × 100%
```

**数据需求**:
- 正股价格（实时）
- 转股价格（发行公告）
- 转债价格（实时）

---

## 五、强赎/下修数据

### 巨潮资讯网
**URL**: http://www.cninfo.com.cn/

**数据内容**:
- 强赎公告
- 下修公告
- 回售公告

**爬取方式**:
```python
# 搜索关键词
keywords = ["可转债强赎", "可转债下修", "可转债回售"]

# 解析公告
for keyword in keywords:
    search_url = f"http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search&keyWord={keyword}"
```

---

## 六、历史数据

### 集思录
**URL**: https://www.jisilu.cn/data/cbnew/

**数据内容**:
- 可转债列表
- 转股溢价率
- 到期收益率
- 双低值

**注意**: 集思录需要登录，建议使用其 API（如有）或手动导出。

---

## 📦 数据缓存策略

### 缓存层级
1. **实时数据**（价格、涨跌幅）：5 分钟缓存
2. **日频数据**（申购日历、公告）：每日更新
3. **历史数据**（历史溢价率）：每周更新

### 缓存实现
```python
import sqlite3
from datetime import datetime, timedelta

class DataCache:
    def __init__(self, db_path="data/cache.db"):
        self.conn = sqlite3.connect(db_path)
    
    def get(self, key, expire_minutes=30):
        # 检查缓存是否过期
        cursor = self.conn.execute(
            "SELECT data, updated_at FROM cache WHERE key=?",(key,)
        )
        row = cursor.fetchone()
        
        if row:
            data, updated_at = row
            if datetime.now() - updated_at < timedelta(minutes=expire_minutes):
                return json.loads(data)
        
        return None
    
    def set(self, key, data):
        self.conn.execute(
            "INSERT OR REPLACE INTO cache (key, data, updated_at) VALUES (?, ?, ?)",
            (key, json.dumps(data), datetime.now())
        )
        self.conn.commit()
```

---

## ⚠️ 注意事项

1. **反爬虫**: 部分网站有反爬措施，需要设置 User-Agent、Referer
2. **频率限制**: 建议单个 IP 每分钟请求 < 60 次
3. **数据准确性**: 实时数据可能有延迟，以交易所为准
4. **合规性**: 仅用于个人学习研究，勿用于商业用途

---

## 🔧 开发建议

### 1. 使用 akshare（推荐）
```python
import akshare as ak

# 获取可转债列表
cb_list = ak.bond_cb_jsl()

# 获取可转债行情
cb行情 = ak.bond_zh_hs_spot()
```

**优点**:
- 免费开源
- 数据全面
- 更新及时

**安装**:
```bash
pip install akshare
```

### 2. 使用 Tushare Pro
```python
import tushare as ts

# 初始化
ts.set_token('your_token')
pro = ts.pro_api()

# 获取可转债信息
cb_info = pro.cb_basic()
```

**优点**:
- 数据规范
- 接口稳定

**缺点**:
- 需要积分
- 部分数据收费

---

## 📞 数据更新

如遇数据源变更或 API 失效，请更新对应模块：

1. `cb_calendar.py` - 申购日历数据
2. `cb_analysis.py` - 正股基本面数据
3. `cb_premium_predict.py` - 历史溢价数据
4. `cb_monitor.py` - 公告数据

---

**最后更新**: 2026-03-07
