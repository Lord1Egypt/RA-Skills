"""
简单的AI团队协调器
演示如何协调多个AI员工工作
"""

from simple_ai_employee import SimpleAIEmployee
from simple_event_bus import SimpleEventBus, EventTypes
import time


class SimpleAITeamCoordinator:
    """简单的AI团队协调器"""

    def __init__(self):
        """初始化协调器"""
        self.employees = {}
        self.event_bus = SimpleEventBus()
        self.is_running = False

    def register_employee(self, employee: SimpleAIEmployee):
        """
        注册AI员工

        Args:
            employee: AI员工实例
        """
        self.employees[employee.name] = employee
        print(f"[Coordinator] 注册AI员工: {employee.name} ({employee.role})")

    def start(self):
        """启动AI团队"""
        print("[Coordinator] 启动AI团队")
        self.is_running = True
        self.run_cycle()

    def stop(self):
        """停止AI团队"""
        print("[Coordinator] 停止AI团队")
        self.is_running = False

    def run_cycle(self):
        """运行一个完整的工作循环"""
        print("\n=== 开始工作循环 ===\n")

        # 1. 机会发现阶段
        print("[阶段1] 机会发现")
        opportunity_task = {
            "id": "task_001",
            "description": "搜索市场机会",
            "type": "market_research"
        }

        if "market_researcher" in self.employees:
            result = self.employees["market_researcher"].work(opportunity_task)
            if result["status"] == "success":
                # 发布机会发现事件
                self.event_bus.publish(EventTypes.OPPORTUNITY_DISCOVERED, {
                    "title": "自动化测试工具需求",
                    "source": "GitHub Issues",
                    "market_size": "large",
                    "potential_revenue": 500
                })

        time.sleep(1)

        # 2. 产品设计阶段
        print("\n[阶段2] 产品设计")
        design_task = {
            "id": "task_002",
            "description": "设计自动化测试工具",
            "type": "product_design"
        }

        if "product_designer" in self.employees:
            result = self.employees["product_designer"].work(design_task)
            if result["status"] == "success":
                # 发布设计就绪事件
                self.event_bus.publish(EventTypes.DESIGN_READY, {
                    "product_name": "AutoTest Pro",
                    "features": ["自动生成测试", "集成CI/CD", "代码覆盖率分析"],
                    "pricing": {"starter": 29, "pro": 99}
                })

        time.sleep(1)

        # 3. 产品开发阶段
        print("\n[阶段3] 产品开发")
        dev_task = {
            "id": "task_003",
            "description": "开发AutoTest Pro v1.0",
            "type": "development"
        }

        if "developer" in self.employees:
            result = self.employees["developer"].work(dev_task)
            if result["status"] == "success":
                # 发布产品完成事件
                self.event_bus.publish(EventTypes.PRODUCT_COMPLETED, {
                    "product_id": "prod_001",
                    "name": "AutoTest Pro",
                    "version": "1.0.0",
                    "test_coverage": 0.85
                })

        time.sleep(1)

        # 4. 销售阶段
        print("\n[阶段4] 销售和营销")
        sales_task = {
            "id": "task_004",
            "description": "销售AutoTest Pro",
            "type": "sales"
        }

        if "sales_agent" in self.employees:
            result = self.employees["sales_agent"].work(sales_task)
            if result["status"] == "success":
                # 发布销售事件
                self.event_bus.publish(EventTypes.SALE_MADE, {
                    "customer": "John Doe",
                    "product_id": "prod_001",
                    "amount": 99,
                    "plan": "pro"
                })

        print("\n=== 工作循环完成 ===\n")

    def get_status(self):
        """获取团队状态"""
        return {
            "is_running": self.is_running,
            "employees": list(self.employees.keys()),
            "event_count": len(self.event_bus.get_history())
        }


# 使用示例
if __name__ == "__main__":
    print("=== AI CEO 自动化公司演示 ===\n")

    # 创建协调器
    coordinator = SimpleAITeamCoordinator()

    # 创建并注册AI员工
    market_researcher = SimpleAIEmployee("market_researcher", "市场研究专家")
    product_designer = SimpleAIEmployee("product_designer", "产品设计师")
    developer = SimpleAIEmployee("developer", "开发者")
    sales_agent = SimpleAIEmployee("sales_agent", "销售专家")

    coordinator.register_employee(market_researcher)
    coordinator.register_employee(product_designer)
    coordinator.register_employee(developer)
    coordinator.register_employee(sales_agent)

    # 设置事件监听器（用于演示）
    def on_opportunity(event_data):
        print(f"🎯 发现机会: {event_data['title']}")

    def on_design(event_data):
        print(f"📋 设计完成: {event_data['product_name']}")

    def on_product(event_data):
        print(f"🚀 产品发布: {event_data['name']} v{event_data['version']}")

    def on_sale(event_data):
        print(f"💰 销售成功: {event_data['customer']} 购买 ${event_data['amount']}")

    coordinator.event_bus.subscribe(EventTypes.OPPORTUNITY_DISCOVERED, on_opportunity)
    coordinator.event_bus.subscribe(EventTypes.DESIGN_READY, on_design)
    coordinator.event_bus.subscribe(EventTypes.PRODUCT_COMPLETED, on_product)
    coordinator.event_bus.subscribe(EventTypes.SALE_MADE, on_sale)

    # 启动AI团队
    coordinator.start()

    # 显示状态
    status = coordinator.get_status()
    print(f"\n团队状态: {status}")

    print("\n=== 演示完成 ===")
    print("这展示了AI公司如何自动运营:")
    print("1. 发现市场机会")
    print("2. 设计产品")
    print("3. 开发产品")
    print("4. 销售产品")
    print("5. 实现盈利")
