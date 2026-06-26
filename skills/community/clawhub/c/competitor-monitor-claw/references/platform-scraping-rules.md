# 平台采集规则

## 支持平台与数据字段

### 京东（JD）
- **当前价格**：`#J_DetailMeta .price-box .price` 或 API `jd.item.price`
- **促销价/到手价**：`.prom-price` 或优惠券叠加后价格
- **评价数量**：`.count-num` 内文本数字
- **评分**：`.percent-con .percent` 百分比转5分制（×5）
- **库存状态**：`#btn-reservation` 是否存在判断预售；`#btn-addToCart` disabled 判断无货

### 淘宝/天猫（Taobao/Tmall）
- **当前价格**：`.tb-rmb-num` 或 `.price`
- **促销价**：`.J_PromoPriceWrap .price`
- **评价数量**：`.tb-review-count`
- **评分**：`.tb-rate-percent` 好评率
- **库存**：`#J_BtnBuy` disabled 状态

### 拼多多（PDD）
- **当前价格**：`.price-section .price-current`
- **促销价**：`.coupon-price` 或 `.activity-price`
- **评价数量**：`.comment-count`
- **评分**：`.score-num`

## 反爬处理策略

| 策略 | 说明 |
|------|------|
| 请求间隔 | 同一平台请求间隔 ≥3 秒，高峰期 ≥10 秒 |
| UA 轮换 | 维护 10+ 个真实浏览器 UA 字符串，随机选取 |
| Cookie 管理 | 定期刷新 Cookie，避免长期使用同一 Session |
| 失败重试 | 遇到 429/503 时指数退避重试（1s→2s→4s→放弃） |
| 代理池 | 可选：配置代理 IP 池降低封禁风险 |

## 数据存储结构（SQLite）

```sql
-- 竞品基础信息
CREATE TABLE competitors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    platform TEXT NOT NULL,  -- jd/taobao/tmall/pdd
    product_url TEXT NOT NULL,
    sku_id TEXT,
    alert_threshold REAL DEFAULT 0.05,  -- 5% 价格变动预警
    monitor_freq TEXT DEFAULT 'daily',  -- hourly/daily/weekly
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 价格历史
CREATE TABLE price_history (
    id INTEGER PRIMARY KEY,
    competitor_id INTEGER REFERENCES competitors(id),
    price REAL NOT NULL,
    promo_price REAL,
    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 评价快照
CREATE TABLE review_snapshots (
    id INTEGER PRIMARY KEY,
    competitor_id INTEGER REFERENCES competitors(id),
    review_count INTEGER,
    rating REAL,
    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 变化事件
CREATE TABLE change_events (
    id INTEGER PRIMARY KEY,
    competitor_id INTEGER REFERENCES competitors(id),
    event_type TEXT,  -- price_drop/price_rise/new_product/promo_start/promo_end
    old_value TEXT,
    new_value TEXT,
    change_pct REAL,
    detected_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    notified INTEGER DEFAULT 0
);
```

## 竞品列表 CSV 格式（config/competitors.csv）

```csv
name,platform,product_url,sku_id,alert_threshold,monitor_freq,owner
竞品A-旗舰款,jd,https://item.jd.com/xxx.html,100012345,0.05,daily,张三
竞品B-主力款,taobao,https://item.taobao.com/item.htm?id=xxx,987654321,0.03,hourly,李四
```
