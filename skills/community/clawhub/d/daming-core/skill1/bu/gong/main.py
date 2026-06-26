"""
工部 - 主入口文件
提供工部功能的统一接口
"""

from .scheduler import GongBuScheduler, create_gong_scheduler


def dispatch_task(task_id: str, action: str, params: dict = None) -> dict:
    """
    调度任务执行
    返回调度结果
    """
    scheduler = create_gong_scheduler()
    
    execution_params = {
        "action": action,
        "params": params or {},
        "estimated_tokens": params.get("estimated_tokens", 100) if params else 100
    }
    
    return scheduler.dispatch_with_budget_check(task_id, execution_params)


def check_budget(task_id: str, required_tokens: int = 100) -> dict:
    """检查Token预算"""
    scheduler = create_gong_scheduler()
    return scheduler.check_token_budget(task_id, required_tokens)


def get_execution_status(task_id: str, execution_id: str) -> dict:
    """获取执行状态"""
    scheduler = create_gong_scheduler()
    return scheduler.get_execution_status(task_id, execution_id)


class GongBu:
    """工部类（兼容接口）"""
    
    def __init__(self):
        self.scheduler = create_gong_scheduler()
    
    def dispatch(self, task_id: str, action: str, params: dict = None) -> dict:
        """调度执行（兼容方法）"""
        return dispatch_task(task_id, action, params)
    
    def check_budget(self, task_id: str, required_tokens: int = 100) -> dict:
        """检查预算（兼容方法）"""
        return check_budget(task_id, required_tokens)


if __name__ == "__main__":
    print("🏛️ 工部主模块测试")
    print("✅ 工部模块已加载")
    
    # 测试创建调度器
    scheduler = create_gong_scheduler()
    print(f"调度器类型: {type(scheduler).__name__}")
    
    # 测试工部类
    gongbu = GongBu()
    print(f"工部类已创建: {gongbu}")