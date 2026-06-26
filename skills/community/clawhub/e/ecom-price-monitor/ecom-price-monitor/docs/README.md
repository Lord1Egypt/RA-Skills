# 💰 跨境电商价格监控

## 简介

专业的电商价格监控工具，支持Amazon、淘宝、京东、拼多多、1688等多平台价格追踪。自动发现价格异常、套利机会，支持低价提醒和定时监控。

## 核心功能

### ✅ 多平台价格监控
- **Amazon**: 支持ASIN监控，美元定价
- **淘宝/天猫**: 支持商品ID监控，人民币定价
- **京东**: 支持SKU监控
- **拼多多**: 支持批发价格监控
- **1688**: 支持工厂直销价格

### ✅ 智能价格提醒
- **目标价格提醒**: 低于设定价格时通知
- **降价百分比提醒**: 降价超过X%时通知
- **涨价提醒**: 防止错过最佳购买时机

### ✅ 套利机会发现
- 自动对比国内外平台价格
- 计算运费后的真实利润率
- 筛选高利润套利机会

### ✅ 价格趋势分析
- 历史价格曲线
- 最低价/最高价统计
- 价格趋势判断（上涨/下跌/稳定）

### ✅ 定时自动监控
- 自定义监控频率
- 后台持续运行
- 异常时自动重试

## 快速开始

### 1. 安装

```bash
# 安装依赖
pip install requests beautifulsoup4 schedule pandas pyyaml

# 复制技能到OpenClaw技能目录
cp -r ecom-price-monitor ~/.openclaw/skills/
```

### 2. 运行

```bash
cd ~/.openclaw/skills/ecom-price-monitor
python src/main.py
```

## 使用示例

### 基础用法

```python
from src.main import PriceMonitor

# 初始化监控器
monitor = PriceMonitor()

# 添加监控产品
product = monitor.add_product(
    name="无线蓝牙耳机",
    platform="amazon",
    url="https://amazon.com/dp/B08N5WRWNW",
    target_price=45.0  # 低于$45时提醒
)

# 立即获取价格
monitor.update_price(product.id)
print(f"当前价格: ${monitor.products[product.id].current_price}")

# 检查所有产品价格
changes = monitor.check_all_prices()
for change in changes:
    print(f"{change['product'].name}: ${change['old_price']} -> ${change['new_price']}")
```

### 设置价格提醒

```python
# 当价格下降超过20%时提醒
monitor.add_alert(
    product_id="product_123",
    condition="drop_percent",
    threshold=0.2,
    method="console"
)

# 检查提醒
alerts = monitor.check_alerts()
```

### 寻找套利机会

```python
# 自动寻找高利润套利机会
opportunities = monitor.find_arbitrage("electronics")

for opp in opportunities:
    print(f"""
    产品: {opp['product_name']}
    买入: {opp['buy_platform']} ¥{opp['buy_price']}
    卖出: {opp['sell_platform']} ${opp['sell_price']}
    利润率: {opp['profit_margin']*100:.0f}%
    """)
```

### 价格趋势分析

```python
# 获取30天价格趋势
trend = monitor.get_price_trend("product_123", days=30)

print(f"""
产品: {trend['product_name']}
当前价格: ${trend['current_price']}
平均价格: ${trend['average_price']}
历史最低: ${trend['min_price']}
历史最高: ${trend['max_price']}
趋势: {trend['trend']}  # rising/dropping/stable
""")
```

### 定时监控

```python
# 每小时检查一次价格
monitor.config['check_interval'] = 3600  # 秒

# 启动定时任务
monitor.run_scheduler()
```

## 配置说明

### 监控频率
```yaml
check_interval: 3600  # 每1小时检查一次
```

### 套利设置
```yaml
arbitrage:
  min_margin: 0.2  # 只显示利润率>20%的机会
  max_shipping_cost: 50  # 最大运费50元
```

### 通知方式
```yaml
notifications:
  console: true   # 控制台输出
  email: true     # 邮件通知
  webhook: true   # 钉钉/飞书机器人
```

## 平台配置

### Amazon
需要Amazon Product Advertising API Key

### 淘宝/京东/拼多多
需要申请开放平台API Key

### 1688
需要登录后获取Cookie

## 实战案例：跨境电商套利

### 场景：从美国Amazon进货，在淘宝销售

```python
monitor = PriceMonitor()

# 监控Amazon热销产品
products = [
    {"name": "蓝牙耳机", "asin": "B08N5WRWNW", "buy_price": 49.99},
    {"name": "充电宝", "asin": "B08N5M7S6K", "buy_price": 29.99}
]

for p in products:
    monitor.add_product(
        name=p["name"],
        platform="amazon",
        url=f"https://amazon.com/dp/{p['asin']}"
    )

# 检查套利机会
opportunities = monitor.find_arbitrage("electronics")

for opp in opportunities:
    # 计算最终利润
    cost = opp['buy_price'] * 7.2  # 换算成人民币
    shipping = 30  # 预估运费
    taobao_price = opp['buy_price'] * 1.5 * 7.2  # 淘宝售价(1.5倍)
    
    profit = taobao_price - cost - shipping
    
    print(f"""
    {opp['product_name']}
    成本: ¥{cost:.0f} (含运费)
    售价: ¥{taobao_price:.0f}
    利润: ¥{profit:.0f} ({profit/cost*100:.0f}%)
    """)
```

## 价格提醒类型

| 条件 | 说明 | 示例 |
|------|------|------|
| `below` | 低于目标价格 | `target_price=50`, 当前$45时触发 |
| `above` | 高于目标价格 | `target_price=100`, 当前$120时触发 |
| `drop_percent` | 降价百分比 | `threshold=0.2`, 降价20%时触发 |
| `rise_percent` | 涨价百分比 | `threshold=0.1`, 涨价10%时触发 |

## 数据结构

### Product（产品）
```python
{
    "id": "abc123",
    "name": "产品名称",
    "platform": "amazon",
    "url": "https://...",
    "current_price": 49.99,
    "original_price": 79.99,
    "currency": "USD",
    "seller": "卖家",
    "rating": 4.5,
    "reviews": 12580,
    "price_history": [...]
}
```

## 注意事项

### ⚠️ 合规提醒
1. **遵守平台规则**: 不要频繁请求，避免被封IP
2. **合理设置频率**: 建议每小时检查一次
3. **使用代理**: 大量监控时建议使用代理池

### ⚠️ 技术限制
1. 部分平台需要API Key或登录凭证
2. 价格数据可能有延迟
3. 库存状态可能不准确

## 价格

- **基础版**: $49 (一次性购买)
  - 5个平台监控
  - 价格提醒
  - 趋势分析
  - JSON导出
  
- **专业版**: $99
  - 无限产品监控
  - 自动套利发现
  - 邮件/Webhook通知
  - Excel导出
  - API接口

## 技术支持

- 📧 邮箱: support@ecom-monitor.bot
- 💬 微信: EcomMonitorBot

## 更新日志

### v1.0.0 (2026-03-24)
- 🎉 首次发布
- ✅ Amazon/淘宝/京东/拼多多/1688监控
- ✅ 价格提醒系统
- ✅ 套利机会发现
- ✅ 价格趋势分析
- ✅ 定时自动监控

---

**Made with ❤️ by Kimi Claw**