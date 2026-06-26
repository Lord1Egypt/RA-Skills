# -*- coding: utf-8 -*-
"""
跨境电商价格监控
E-commerce Price Monitor
作者: Kimi Claw
版本: 1.0.0
"""

import json
import re
import time
import hashlib
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
import requests

try:
    import schedule
    SCHEDULE_AVAILABLE = True
except ImportError:
    SCHEDULE_AVAILABLE = False


@dataclass
class Product:
    """产品数据类"""
    id: str
    name: str
    platform: str
    url: str
    current_price: float
    original_price: Optional[float] = None
    currency: str = "CNY"
    seller: str = ""
    rating: float = 0.0
    reviews: int = 0
    stock_status: str = "unknown"
    last_updated: str = ""
    price_history: List[Dict] = None
    
    def __post_init__(self):
        if self.price_history is None:
            self.price_history = []
        if not self.last_updated:
            self.last_updated = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class PriceAlert:
    """价格提醒"""
    product_id: str
    condition: str  # 'below', 'above', 'drop_percent', 'rise_percent'
    threshold: float
    notification_method: str = "console"  # console, email, webhook
    created_at: str = ""
    triggered: bool = False
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


class PriceMonitor:
    """价格监控器主类"""
    
    # 平台配置
    PLATFORMS = {
        "amazon": {
            "name": "Amazon",
            "base_url": "https://www.amazon.com",
            "currency": "USD"
        },
        "taobao": {
            "name": "淘宝",
            "base_url": "https://s.taobao.com",
            "currency": "CNY"
        },
        "jd": {
            "name": "京东",
            "base_url": "https://search.jd.com",
            "currency": "CNY"
        },
        "pdd": {
            "name": "拼多多",
            "base_url": "https://mobile.yangkeduo.com",
            "currency": "CNY"
        },
        "1688": {
            "name": "1688",
            "base_url": "https://s.1688.com",
            "currency": "CNY"
        }
    }
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        """初始化监控器"""
        self.config = self._load_config(config_path)
        self.products: Dict[str, Product] = {}
        self.alerts: List[PriceAlert] = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def _load_config(self, path: str) -> Dict:
        """加载配置"""
        default_config = {
            "check_interval": 3600,  # 默认1小时检查一次
            "price_drop_threshold": 0.1,  # 降价10%触发提醒
            "arbitrage_min_margin": 0.2,  # 套利最小利润率20%
            "proxy": None,
            "timeout": 30,
            "retry_count": 3,
            "notifications": {
                "console": True,
                "email": False,
                "webhook": False
            }
        }
        try:
            import yaml
            with open(path, 'r', encoding='utf-8') as f:
                return {**default_config, **yaml.safe_load(f)}
        except:
            return default_config
    
    def add_product(self, name: str, platform: str, url: str, 
                   target_price: Optional[float] = None) -> Product:
        """添加监控产品"""
        product_id = hashlib.md5(f"{platform}:{url}".encode()).hexdigest()[:12]
        
        product = Product(
            id=product_id,
            name=name,
            platform=platform,
            url=url,
            current_price=0.0,
            last_updated=datetime.now().isoformat()
        )
        
        self.products[product_id] = product
        
        # 如果设置了目标价格，添加价格提醒
        if target_price:
            self.add_alert(product_id, "below", target_price)
        
        return product
    
    def add_alert(self, product_id: str, condition: str, 
                  threshold: float, method: str = "console"):
        """添加价格提醒"""
        alert = PriceAlert(
            product_id=product_id,
            condition=condition,
            threshold=threshold,
            notification_method=method
        )
        self.alerts.append(alert)
    
    def scrape_amazon(self, asin: str) -> Optional[Product]:
        """抓取Amazon产品信息"""
        # 模拟数据（实际需要Selenium/API）
        mock_products = {
            "B08N5WRWNW": {
                "name": "Wireless Earbuds Pro",
                "price": 49.99,
                "original_price": 79.99,
                "rating": 4.5,
                "reviews": 12580,
                "seller": "Amazon"
            },
            "B08N5M7S6K": {
                "name": "Smart Watch Series 7",
                "price": 299.99,
                "original_price": 399.99,
                "rating": 4.7,
                "reviews": 8560,
                "seller": "Apple Official"
            }
        }
        
        data = mock_products.get(asin)
        if not data:
            return None
        
        return Product(
            id=asin,
            name=data["name"],
            platform="amazon",
            url=f"https://amazon.com/dp/{asin}",
            current_price=data["price"],
            original_price=data["original_price"],
            currency="USD",
            seller=data["seller"],
            rating=data["rating"],
            reviews=data["reviews"],
            last_updated=datetime.now().isoformat()
        )
    
    def scrape_taobao(self, item_id: str) -> Optional[Product]:
        """抓取淘宝产品信息"""
        mock_products = {
            "123456789": {
                "name": "无线蓝牙耳机",
                "price": 89.0,
                "original_price": 199.0,
                "rating": 4.8,
                "reviews": 25000,
                "seller": "数码旗舰店"
            }
        }
        
        data = mock_products.get(item_id)
        if not data:
            return None
        
        return Product(
            id=item_id,
            name=data["name"],
            platform="taobao",
            url=f"https://item.taobao.com/item.htm?id={item_id}",
            current_price=data["price"],
            original_price=data["original_price"],
            currency="CNY",
            seller=data["seller"],
            rating=data["rating"],
            reviews=data["reviews"],
            last_updated=datetime.now().isoformat()
        )
    
    def update_price(self, product_id: str) -> Optional[Product]:
        """更新产品价格"""
        product = self.products.get(product_id)
        if not product:
            return None
        
        # 根据平台调用对应的抓取方法
        if product.platform == "amazon":
            new_data = self.scrape_amazon(product_id)
        elif product.platform == "taobao":
            new_data = self.scrape_taobao(product_id)
        else:
            return None
        
        if not new_data:
            return None
        
        # 记录价格历史
        if product.current_price > 0:
            product.price_history.append({
                "price": product.current_price,
                "timestamp": product.last_updated
            })
        
        # 更新价格
        product.current_price = new_data.current_price
        product.original_price = new_data.original_price
        product.last_updated = datetime.now().isoformat()
        
        return product
    
    def check_all_prices(self) -> List[Dict]:
        """检查所有产品价格"""
        changes = []
        
        for product_id in self.products:
            old_price = self.products[product_id].current_price
            product = self.update_price(product_id)
            
            if product and old_price > 0:
                price_diff = product.current_price - old_price
                if abs(price_diff) > 0.01:
                    changes.append({
                        "product": product,
                        "old_price": old_price,
                        "new_price": product.current_price,
                        "change": price_diff,
                        "change_percent": (price_diff / old_price) * 100
                    })
        
        return changes
    
    def check_alerts(self) -> List[Dict]:
        """检查价格提醒"""
        triggered = []
        
        for alert in self.alerts:
            if alert.triggered:
                continue
            
            product = self.products.get(alert.product_id)
            if not product:
                continue
            
            should_trigger = False
            
            if alert.condition == "below" and product.current_price <= alert.threshold:
                should_trigger = True
            elif alert.condition == "above" and product.current_price >= alert.threshold:
                should_trigger = True
            elif alert.condition == "drop_percent":
                if product.price_history:
                    last_price = product.price_history[-1]["price"]
                    drop_percent = (last_price - product.current_price) / last_price
                    if drop_percent >= alert.threshold:
                        should_trigger = True
            
            if should_trigger:
                alert.triggered = True
                triggered.append({
                    "alert": alert,
                    "product": product
                })
                
                # 发送通知
                self._send_notification(alert, product)
        
        return triggered
    
    def _send_notification(self, alert: PriceAlert, product: Product):
        """发送通知"""
        message = f"""
🚨 价格提醒触发!

商品: {product.name}
平台: {product.platform}
当前价格: {product.current_price} {product.currency}
条件: {alert.condition} {alert.threshold}
链接: {product.url}
        """
        
        if alert.notification_method == "console":
            print(message)
        # TODO: 实现邮件和webhook通知
    
    def find_arbitrage(self, product_name: str) -> List[Dict]:
        """
        寻找套利机会
        
        对比多个平台的价格，找出利润率超过阈值的套利机会
        """
        opportunities = []
        min_margin = self.config.get('arbitrage_min_margin', 0.2)
        
        # 模拟套利机会
        mock_opportunities = [
            {
                "product_name": "Wireless Earbuds Pro",
                "buy_platform": "1688",
                "buy_price": 45,  # CNY
                "buy_url": "https://detail.1688.com/xxx",
                "sell_platform": "Amazon",
                "sell_price": 49.99,  # USD
                "sell_url": "https://amazon.com/dp/xxx",
                "profit_margin": 0.65,  # 65%利润率
                "estimated_profit": 18.5,  # USD
                "notes": "热销产品，月销量5000+"
            },
            {
                "product_name": "Phone Case Premium",
                "buy_platform": "PDD",
                "buy_price": 12,  # CNY
                "buy_url": "https://mobile.yangkeduo.com/xxx",
                "sell_platform": "eBay",
                "sell_price": 15.99,  # USD
                "sell_url": "https://ebay.com/xxx",
                "profit_margin": 0.85,
                "estimated_profit": 13.5,
                "notes": "轻小件，物流成本低"
            }
        ]
        
        for opp in mock_opportunities:
            if opp["profit_margin"] >= min_margin:
                opportunities.append(opp)
        
        return opportunities
    
    def get_price_trend(self, product_id: str, days: int = 30) -> Dict:
        """获取价格趋势"""
        product = self.products.get(product_id)
        if not product:
            return {}
        
        history = product.price_history[-days:] if len(product.price_history) > days else product.price_history
        
        if not history:
            return {
                "product_id": product_id,
                "current_price": product.current_price,
                "trend": "insufficient_data"
            }
        
        prices = [h["price"] for h in history]
        avg_price = sum(prices) / len(prices)
        min_price = min(prices)
        max_price = max(prices)
        
        # 判断趋势
        if len(prices) >= 3:
            recent_avg = sum(prices[-3:]) / 3
            older_avg = sum(prices[:3]) / 3 if len(prices) >= 6 else avg_price
            
            if recent_avg < older_avg * 0.95:
                trend = "dropping"
            elif recent_avg > older_avg * 1.05:
                trend = "rising"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"
        
        return {
            "product_id": product_id,
            "product_name": product.name,
            "current_price": product.current_price,
            "average_price": round(avg_price, 2),
            "min_price": min_price,
            "max_price": max_price,
            "trend": trend,
            "data_points": len(history)
        }
    
    def run_scheduler(self):
        """运行定时任务"""
        if not SCHEDULE_AVAILABLE:
            print("⚠️  schedule模块未安装，跳过定时任务")
            print("    安装命令: pip install schedule")
            return
        
        interval = self.config.get('check_interval', 3600)
        
        # 设置定时任务
        schedule.every(interval).seconds.do(self._scheduled_check)
        
        print(f"⏰ 价格监控已启动，每 {interval} 秒检查一次")
        
        while True:
            schedule.run_pending()
            time.sleep(1)
    
    def _scheduled_check(self):
        """定时检查任务"""
        print(f"\n🔍 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始价格检查...")
        
        changes = self.check_all_prices()
        if changes:
            print(f"📊 发现 {len(changes)} 个价格变动")
            for change in changes:
                product = change["product"]
                emoji = "📉" if change["change"] < 0 else "📈"
                print(f"  {emoji} {product.name}: {change['old_price']} -> {change['new_price']} "
                      f"({change['change_percent']:+.1f}%)")
        
        alerts = self.check_alerts()
        if alerts:
            print(f"🚨 {len(alerts)} 个价格提醒被触发")
        
        print("✅ 检查完成\n")
    
    def export_data(self, format: str = "json", filename: str = None) -> str:
        """导出数据"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"price_monitor_{timestamp}"
        
        data = {
            "products": {pid: p.to_dict() for pid, p in self.products.items()},
            "alerts": [asdict(a) for a in self.alerts],
            "export_time": datetime.now().isoformat()
        }
        
        if format == "json":
            filepath = f"{filename}.json"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return filepath
        
        return ""


def main():
    """示例用法"""
    print("💰 跨境电商价格监控")
    print("=" * 50)
    
    monitor = PriceMonitor()
    
    # 示例1: 添加监控产品
    print("\n📝 添加监控产品...")
    
    product1 = monitor.add_product(
        name="Wireless Earbuds Pro",
        platform="amazon",
        url="https://amazon.com/dp/B08N5WRWNW",
        target_price=45.0  # 目标价格提醒
    )
    print(f"  ✓ {product1.name} (ID: {product1.id})")
    
    product2 = monitor.add_product(
        name="Smart Watch Series 7",
        platform="amazon",
        url="https://amazon.com/dp/B08N5M7S6K"
    )
    print(f"  ✓ {product2.name} (ID: {product2.id})")
    
    # 示例2: 更新价格
    print("\n🔍 获取最新价格...")
    for pid in monitor.products:
        product = monitor.update_price(pid)
        if product:
            discount = ""
            if product.original_price and product.original_price > product.current_price:
                off = (1 - product.current_price / product.original_price) * 100
                discount = f" (省{off:.0f}%)"
            print(f"  {product.name}: {product.currency} {product.current_price}{discount}")
    
    # 示例3: 检查价格提醒
    print("\n🚨 检查价格提醒...")
    alerts = monitor.check_alerts()
    if alerts:
        for item in alerts:
            print(f"  ✓ {item['product'].name} 触发提醒!")
    else:
        print("  暂无提醒触发")
    
    # 示例4: 寻找套利机会
    print("\n💎 寻找套利机会...")
    opportunities = monitor.find_arbitrage("electronics")
    for i, opp in enumerate(opportunities[:3], 1):
        print(f"\n  {i}. {opp['product_name']}")
        print(f"     买入: {opp['buy_platform']} ¥{opp['buy_price']}")
        print(f"     卖出: {opp['sell_platform']} ${opp['sell_price']}")
        print(f"     利润率: {opp['profit_margin']*100:.0f}%")
        print(f"     预计利润: ${opp['estimated_profit']}")
    
    # 示例5: 价格趋势
    print("\n📈 价格趋势分析...")
    for pid in list(monitor.products.keys())[:1]:
        trend = monitor.get_price_trend(pid)
        print(f"  {trend.get('product_name', 'Unknown')}: {trend.get('trend', 'unknown')}")
    
    # 导出数据
    print("\n💾 导出数据...")
    filepath = monitor.export_data("json", "demo_export")
    print(f"  已导出: {filepath}")
    
    print("\n" + "=" * 50)
    print("✅ 演示完成!")
    print("\n提示: 实际使用时需要配置各平台的API或登录凭证")


if __name__ == "__main__":
    main()