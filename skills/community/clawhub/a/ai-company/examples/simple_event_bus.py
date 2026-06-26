"""
简单的事件总线实现
用于AI员工之间的通信
"""

from typing import Dict, List, Callable, Any
from collections import defaultdict
import json


class SimpleEventBus:
    """简单的事件总线"""

    def __init__(self):
        """初始化事件总线"""
        self.subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self.event_history: List[Dict[str, Any]] = []

    def subscribe(self, event_type: str, callback: Callable[[Dict[str, Any]], None]):
        """
        订阅事件

        Args:
            event_type: 事件类型
            callback: 回调函数
        """
        self.subscribers[event_type].append(callback)
        print(f"[EventBus] 订阅事件: {event_type}")

    def unsubscribe(self, event_type: str, callback: Callable[[Dict[str, Any]], None]):
        """
        取消订阅

        Args:
            event_type: 事件类型
            callback: 回调函数
        """
        if callback in self.subscribers[event_type]:
            self.subscribers[event_type].remove(callback)
            print(f"[EventBus] 取消订阅: {event_type}")

    def publish(self, event_type: str, data: Dict[str, Any]):
        """
        发布事件

        Args:
            event_type: 事件类型
            data: 事件数据
        """
        print(f"[EventBus] 发布事件: {event_type}")

        # 记录事件历史
        event = {
            "type": event_type,
            "data": data,
            "timestamp": "2024-03-09T10:00:00"
        }
        self.event_history.append(event)

        # 通知所有订阅者
        for callback in self.subscribers[event_type]:
            try:
                callback(data)
            except Exception as e:
                print(f"[EventBus] 回调执行错误: {e}")

    def get_history(self, event_type: str = None) -> List[Dict[str, Any]]:
        """
        获取事件历史

        Args:
            event_type: 事件类型（可选）

        Returns:
            事件列表
        """
        if event_type:
            return [e for e in self.event_history if e["type"] == event_type]
        return self.event_history


# 定义事件类型常量
class EventTypes:
    """事件类型常量"""
    OPPORTUNITY_DISCOVERED = "opportunity.discovered"
    DESIGN_READY = "design.ready"
    PRODUCT_COMPLETED = "product.completed"
    SALE_MADE = "sale.made"
    ISSUE_DETECTED = "issue.detected"
    HUMAN_INTERVENTION_REQUIRED = "human.intervention.required"


# 使用示例
if __name__ == "__main__":
    # 创建事件总线
    event_bus = SimpleEventBus()

    # 定义事件处理器
    def on_opportunity_discovered(data):
        print(f"[Handler] 发现新机会: {data.get('title', '无标题')}")
        print(f"  - 市场规模: {data.get('market_size', '未知')}")
        print(f"  - 潜在收入: ${data.get('potential_revenue', 0)}")

    def on_design_ready(data):
        print(f"[Handler] 设计完成: {data.get('product_name', '无名称')}")
        print(f"  - 功能数: {len(data.get('features', []))}")

    def on_product_completed(data):
        print(f"[Handler] 产品完成: {data.get('product_id', '未知')}")
        print(f"  - 版本: {data.get('version', '0.0.0')}")

    def on_sale_made(data):
        print(f"[Handler] 成交！")
        print(f"  - 客户: {data.get('customer', '未知')}")
        print(f"  - 金额: ${data.get('amount', 0)}")

    # 订阅事件
    event_bus.subscribe(EventTypes.OPPORTUNITY_DISCOVERED, on_opportunity_discovered)
    event_bus.subscribe(EventTypes.DESIGN_READY, on_design_ready)
    event_bus.subscribe(EventTypes.PRODUCT_COMPLETED, on_product_completed)
    event_bus.subscribe(EventTypes.SALE_MADE, on_sale_made)

    print("\n=== 发布事件示例 ===\n")

    # 发布事件
    event_bus.publish(EventTypes.OPPORTUNITY_DISCOVERED, {
        "title": "自动化测试工具需求",
        "source": "GitHub Issues",
        "market_size": "large",
        "potential_revenue": 500
    })

    print()

    event_bus.publish(EventTypes.DESIGN_READY, {
        "product_name": "AutoTest Pro",
        "features": ["自动生成测试", "集成CI/CD", "代码覆盖率分析"]
    })

    print()

    event_bus.publish(EventTypes.PRODUCT_COMPLETED, {
        "product_id": "prod_001",
        "version": "1.0.0",
        "test_coverage": 0.85
    })

    print()

    event_bus.publish(EventTypes.SALE_MADE, {
        "customer": "John Doe",
        "product_id": "prod_001",
        "amount": 99
    })

    print("\n=== 事件历史 ===\n")
    history = event_bus.get_history()
    for event in history:
        print(f"{event['type']}: {event['timestamp']}")
