--------------------------qAwQUvVPFzhhqp9rj4OUuw
Content-Disposition: form-data; name="file"; filename="SKILL.md"
Content-Type: application/octet-stream

# Price Monitor Skill

实时监控价格变动，自动提醒。

## 功能

- 监控商品/服务价格
- 价格变动提醒
- 历史价格分析
- 最佳购买时机建议
- 多平台对比

## 使用方式

```
监控 iPhone 15 的价格
```

```
设置 BTC 价格预警：低于 $50,000 提醒我
```

```
对比京东和淘宝的商品价格
```

## 配置

### 监控规则
```json
{
  "monitors": [
    {
      "name": "iPhone 15",
      "platforms": ["jd", "taobao", "pdd"],
      "target_price": 5999,
      "alert": "below"
    },
    {
      "name": "BTC",
      "target_price": 50000,
      "alert": "below"
    }
  ]
}
```

## 输出格式

```
📊 价格监控报告

## iPhone 15 Pro Max（256GB）

### 当前价格
- 京东：¥9,999
- 淘宝：¥9,888
- 拼多多：¥9,599 ⭐ 最低价

### 价格趋势
- 7 天前：¥10,299
- 30 天前：¥10,599
- 最低价：¥9,599（拼多多）
- 最高价：¥10,999（官网）

### 建议
✅ 拼多多价格最低，建议购买

### 预警设置
⚠️ 当价格低于 ¥9,500 时提醒我

---

## BTC 价格

### 当前价格
$52,345.67 (+2.3%)

### 价格趋势
- 24h 高：$53,200
- 24h 低：$51,000
- 7d 涨跌：+8.5%
- 30d 涨跌：+15.2%

### 预警状态
✅ 已设置：低于 $50,000 提醒
```

---

创建时间：2026-03-11
作者：ClawMart
--------------------------qAwQUvVPFzhhqp9rj4OUuw--
