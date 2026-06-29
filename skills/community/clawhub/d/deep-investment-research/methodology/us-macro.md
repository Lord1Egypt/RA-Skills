# 美国宏观研究 - 执行参考手册

## 前置协议

本文件与 `content-reading-protocol.md` 协同使用。内容读取的流程、标准、示例见该协议。

---

## 定位

美国宏观情报——Fed政策路径、经济数据趋势、政治风向、地缘军事，提炼对投资决策（尤其美股+黄金+美元）有用的信号。

---

## 输出模板（必须严格遵循）

```
# 🇺🇸 美国宏观日报 [日期]

## 🔴 今日核心变化（≤3条，没有就写"无重大变化"）
- [变化1]: 发生了什么 → 意味着什么 → 对市场的影响路径

## 🏦 Fed & 货币政策
### 最新动态
- Fed官员讲话/会议纪要/数据发布
- 利率预期变化（CME FedWatch）
- 关键判断：下次会议（日期）的市场定价

### Fed操作 & 流动性
- 逆回购(RRP)/TGA/准备金变化
- QT进度
- 贴现窗口/紧急贷款使用情况

### SEC & 交易所
- SEC最新裁决/规则变更
- NYSE/Nasdaq市场结构变化
- ETF审批/上市规则
- 加密货币监管动态

### 财政部/Treasury
- 国债发行计划与拍卖结果
- TGA账户变动
- 关键期限bid-to-cover比率

### 流动性观察
- 逆回购(RRP)/TGA/准备金变化
- QT进度

## 📈 经济数据
| 指标 | 最新值 | 预期 | 前值 | 解读 |
|------|--------|------|------|------|
| (今日发布的数据) |

### 趋势判断
- 就业：强/弱/转折？
- 通胀：粘性/回落/反弹？
- 增长：软着陆/衰退/过热？
- 消费：韧性/疲软？

## 🏛️ 政治/财政
- 白宫/国会动态
- 财政政策（支出法案/债务上限/税改）
- 选举/政治风险
- 监管变化（SEC/FTC/DOJ）

## ⚔️ 军事/地缘
- 美军部署/行动
- 中东/乌克兰/台海/朝鲜
- 国防预算/军工合同

## 🌍 国际
- 贸易政策（关税/制裁）
- 美元体系（去美元化进展/SWIFT/储备货币）
- 盟友关系（NATO/AUKUS/QUAD）

## 📊 市场含义
- 利率路径判断更新：
- 美元方向：
- 利好/利空的资产类别：
- 与持仓的关联：

## ⚠️ 信息盲区
- 今日未能覆盖的内容：
```

---

## 数据源清单（按优先级）

### 第一梯队：官方一手数据（API优先）

| 来源 | 获取方式 | 覆盖内容 |
|------|----------|----------|
| FRED (St. Louis Fed) | API | 利率/通胀/就业/GDP/流动性 |
| BLS (劳工统计局) | API/搜索 | NFP/CPI/PPI/失业率 |
| BEA (经济分析局) | 搜索 | GDP/PCE/个人收入支出 |
| Treasury | 搜索 | 国债发行/TGA/财政收支 |
| Fed官网 | 搜索 | FOMC声明/纪要/讲话/Beige Book |
| CME FedWatch | 搜索 | 利率期货隐含概率 |
| SEC EDGAR | 预处理数据 | 13F/内部人交易 |

### 第二梯队：高质量媒体/分析

| 来源 | 获取方式 | 特点 |
|------|----------|------|
| Reuters | 搜索 | 快速+权威 |
| Bloomberg | 搜索 | 市场+政策交叉 |
| WSJ | 搜索 | 深度+独家 |
| Financial Times | 搜索 | 全球视角 |
| Politico | 搜索 | 华盛顿政治内幕 |
| Defense One / War on the Rocks | 搜索 | 军事/安全 |

### 第三梯队：实时市场数据

| 来源 | 获取方式 | 用途 |
|------|----------|------|
| yfinance | Python API | 国债收益率/美元/VIX/商品 |
| Finnhub | API | 经济日历/新闻 |
| FRED | API | 宏观时间序列 |

---

## 执行方法论

### 0. 内容深度读取原则（硬性要求）

**搜索只是发现环节，不是研究本身。**

工作流：
1. 搜索 → 获取标题+摘要+URL列表
2. **对每个有价值的结果，必须 web_fetch 读取全文**
3. 基于全文内容进行分析和解读
4. 输出时引用具体内容（数据/引言/分析），而非转述标题

```bash
# 读取文章全文的标准方式（对搜索结果中的重要URL逐个执行）
python3 -c "
import urllib.request, re
url = 'TARGET_URL'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=15)
html = resp.read().decode('utf-8', errors='ignore')
html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
html = re.sub(r'<[^>]+>', ' ', html)
html = re.sub(r'\\s+', ' ', html).strip()
print(html[:3000])
"
```

**判断标准：哪些结果需要深读？**
- Fed声明/纪要/官员讲话 → 必读
- SEC/Treasury 官方公告 → 必读
- 权威媒体深度分析（Reuters/WSJ/FT） → 必读
- 与当前持仓/watchlist相关 → 必读
- 纯转载/标题党/旧闻 → 跳过

每次研究至少深读 5-8 篇文章全文。

### 1. Fed政策解读框架

对每次Fed沟通，分析：
1. **措辞变化**（vs上次声明/讲话逐字对比）
2. **点阵图/SEP变化**（如果有）
3. **市场定价vs Fed指引的gap**（预期差来源）
4. **下一个决策节点**（日期+条件）
5. **对资产的传导**（利率→美元→股票→黄金→新兴市场）

### 2. 经济数据解读

对每个重要数据：
1. **vs预期**（beat/miss多少，市场反应）
2. **趋势方向**（3个月趋势比单月更重要）
3. **领先/滞后**（这个数据是领先还是滞后指标？）
4. **对Fed决策的影响**（是否改变利率路径？）
5. **交叉验证**（其他数据是否印证？）

### 3. 政治风险评估

- 两党博弈：什么法案在推进/受阻？
- 行政命令：总统可单方面做什么？
- 司法：最高法院重大判决
- 选举周期：什么政策受选举影响？

### 4. 地缘/军事信号

- 航母群部署位置 → 热点区域
- 军援规模/种类 → 冲突升级/降级
- 制裁行动 → 供应链/能源影响
- 演习规模/位置 → 威慑信号

---

## 搜索命令参考

```bash
# FRED 数据
python3 -c "
from fredapi import Fred
fred = Fred(api_key=os.environ.get('FRED_API_KEY', ''))   # 未设置则跳过 FRED 数据源
# 10Y yield, CPI, unemployment, etc.
"

# yfinance 市场数据
python3 -c "
import yfinance as yf
for t in ['^TNX','^VIX','DX-Y.NYB','GC=F']:
    d = yf.Ticker(t).history(period='5d')
    print(f'{t}: {d[\"Close\"].iloc[-1]:.2f}')
"

# Fed/经济新闻
python3 "${SEARCH_SKILL_PATH:-~/.openclaw/skills/web-search-plus/scripts/search.py}" --query "Fed [topic] [date]" --provider serper --type news --max-results 5
python3 "${SEARCH_SKILL_PATH:-~/.openclaw/skills/web-search-plus/scripts/search.py}" --query "US economy [indicator]" --provider serper --type news --max-results 5

# 政治/地缘
python3 "${SEARCH_SKILL_PATH:-~/.openclaw/skills/web-search-plus/scripts/search.py}" --query "US politics Congress White House" --provider serper --type news --max-results 5
python3 "${SEARCH_SKILL_PATH:-~/.openclaw/skills/web-search-plus/scripts/search.py}" --query "US military deployment geopolitics" --provider serper --type news --max-results 5

# 深度研究
node ~/.openclaw/skills/tavily-search/scripts/search.mjs "US macro [topic]" --deep   # 未安装则用 web_search 工具兜底

# X/Twitter 实时舆情
python3 "${SEARCH_SKILL_PATH:-~/.openclaw/skills/web-search-plus/scripts/search.py}" --query "[topic] site:x.com" --provider serper --max-results 5
```

---

## 质量标准

1. **数据必须有来源标注**——"据XX数据/报道"
2. **解读必须有传导逻辑**——A发生→B因此变化→C资产受影响
3. **区分事实和判断**——事实直述，判断标注"我的判断："
4. **时间轴明确**——这个信号的影响是今天/本周/本月/本季？
5. **与持仓关联**——每个重大信号都要回答"和我的持仓有什么关系？"
6. **经济日历前瞻**——明天/本周有什么重要数据/事件要关注？
