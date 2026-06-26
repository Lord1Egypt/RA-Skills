# EastMoney（东方财富）限流备忘

## 当前状况

服务器 IP `106.54.241.187` 已被 EastMoney 限制访问。症状：
- AKShare 的 `stock_board_industry_name_em()` 等东财接口 → `RemoteDisconnected`
- 直接 curl 东财 API → 空响应或 403
- 巨潮资讯网 cninfo → 500 Internal Server Error（IP 被临时封禁）

## 影响范围

| 功能 | 受影响的 AKShare 接口 | 替代方案 |
|:----|:--------------------|:--------|
| 研报查询 | `stock_jsyjs_anal_em()` | 暂停使用 |
| 公告 | `stock_zh_a_notice_report()` | 用 Tushare Pro `anns_d()` |
| 板块排行 | `stock_board_industry_name_em()` | ✅ **同花顺官网抓取** `q.10jqka.com.cn/thshy/` |
| 资金流向 | `stock_individual_fund_flow()` | 暂停使用 |
| 个股行情 | `stock_zh_a_spot_em()` | ✅ TDX + 腾讯财经（不受限） |

## 已验证的替代方案

### 板块排行 → 同花顺 BeautifulSoup 抓取

```python
import requests
from bs4 import BeautifulSoup

url = 'https://q.10jqka.com.cn/thshy/'  # 行业板块
resp = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(resp.text, 'html.parser')
table = soup.find('table')
rows = table.find_all('tr')
headers = [th.get_text(strip=True) for th in rows[0].find_all(['th','td'])]
data = []
for tr in rows[1:21]:
    cells = [td.get_text(strip=True) for td in tr.find_all('td')]
    data.append(dict(zip(headers, cells)))
```

### 公告 → Tushare Pro（仍有积分限制）

```python
import tushare as ts
import tushare.pro.client as client
client.DataApi._DataApi__http_url = "http://tushare.xyz"
pro = ts.pro_api('token')
df = pro.anns_d(ts_code='600519.SH', limit=20)
```

## 限流规避策略

如果被封后重启尝试：
1. 请求间隔 **1-2秒/次**
2. 轮换 User-Agent
3. 使用代理池多 IP 轮换
4. 本地缓存已下载数据，减少重复请求

## 被封恢复时长

- 东方财富: 通常几小时到 1 天自动恢复
- 巨潮资讯网: 通常 1-2 天恢复
