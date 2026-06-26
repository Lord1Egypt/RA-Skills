"""
大明朝廷体系 - 配置文件
定义常量、路径、配置参数
"""

import os
from pathlib import Path

# 基础路径
# 注意：在生产环境中，请根据实际部署位置修改这些路径
# PROJECT_ROOT 应该指向您的 daming_core 安装目录
PROJECT_ROOT = Path("{{PROJECT_ROOT}}")  # 生产环境需要配置
ACTIVE_TASKS_DIR = PROJECT_ROOT / "active_tasks"
LOCAL_LOGS_DIR = PROJECT_ROOT / "local_logs"

# 确保目录存在（在生产环境中运行时启用）
# ACTIVE_TASKS_DIR.mkdir(parents=True, exist_ok=True)
# LOCAL_LOGS_DIR.mkdir(parents=True, exist_ok=True)

# 部门配置
DEPARTMENTS = {
    "zhongshu": {
        "name": "中书省",
        "description": "政令草拟、任务创建",
        "priority": 1,
        "required": True
    },
    "menxia": {
        "name": "门下省", 
        "description": "政令审核、封驳权",
        "priority": 2,
        "required": True
    },
    "shangshu": {
        "name": "尚书省",
        "description": "任务分发、部门协调、进度追踪",
        "priority": 3,
        "required": True
    },
    "hu": {
        "name": "户部",
        "description": "资源管理、Token预算",
        "priority": 3,
        "required": True
    },
    "gong": {
        "name": "工部",
        "description": "资源调度、外部执行",
        "priority": 4,
        "required": True
    },
    "bing": {
        "name": "兵部",
        "description": "状态监控、执行追踪",
        "priority": 5,
        "required": False
    },
    "xing": {
        "name": "刑部",
        "description": "审计检查、合规验证",
        "priority": 6,
        "required": False
    },
    "li_bu": {
        "name": "吏部",
        "description": "结果格式化、报告生成",
        "priority": 7,
        "required": False
    },
    "jinyiwei": {
        "name": "锦衣卫",
        "description": "安全监控、异常检测",
        "priority": 8,
        "required": False
    },
    "li": {
        "name": "礼部",
        "description": "接口标准化、协议管理、礼仪规范",
        "priority": 9,
        "required": True
    }
}

# Token预算配置
DEFAULT_TOKEN_BUDGET = 1000
MIN_TOKEN_BUDGET = 100
MAX_TOKEN_BUDGET = 10000

# 执行配置
DEFAULT_EXECUTION_TIMEOUT = 300  # 5分钟
MAX_CONCURRENT_EXECUTIONS = 3

# 日志配置
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = LOCAL_LOGS_DIR / "daming_core.log"

# 状态定义
TASK_STATUSES = {
    "draft": "草拟中",
    "audited_pass": "审核通过",
    "audited_reject": "审核驳回",
    "executing": "执行中",
    "completed": "已完成",
    "failed": "已失败",
    "cancelled": "已取消"
}

# 审核状态
AUDIT_STATUSES = {
    "pending": "待审核",
    "pass": "通过",
    "reject": "驳回",
    "error": "错误"
}

# 执行状态
EXECUTION_STATUSES = {
    "pending": "待执行",
    "dispatched": "已调度",
    "executing": "执行中",
    "completed": "已完成",
    "failed": "已失败",
    "cancelled": "已取消"
}


def get_department_info(department_key: str) -> dict:
    """获取部门信息"""
    return DEPARTMENTS.get(department_key, {
        "name": "未知部门",
        "description": "未定义的部门",
        "priority": 99,
        "required": False
    })


def get_all_departments() -> list:
    """获取所有部门列表（按优先级排序）"""
    return sorted(
        [(key, info) for key, info in DEPARTMENTS.items()],
        key=lambda x: x[1]["priority"]
    )


def validate_token_budget(budget: int) -> bool:
    """验证Token预算是否有效"""
    return MIN_TOKEN_BUDGET <= budget <= MAX_TOKEN_BUDGET


def get_status_display(status_key: str, status_type: str = "task") -> str:
    """获取状态显示文本"""
    if status_type == "task":
        status_dict = TASK_STATUSES
    elif status_type == "audit":
        status_dict = AUDIT_STATUSES
    elif status_type == "execution":
        status_dict = EXECUTION_STATUSES
    else:
        return "未知状态"
    
    return status_dict.get(status_key, "未知状态")


if __name__ == "__main__":
    # 测试配置
    print("🏛️ 大明朝廷体系配置")
    print(f"项目根目录: {PROJECT_ROOT}")
    print(f"活跃任务目录: {ACTIVE_TASKS_DIR}")
    print(f"本地日志目录: {LOCAL_LOGS_DIR}")
    print(f"部门数量: {len(DEPARTMENTS)}")
    
    for dept_key, dept_info in get_all_departments():
        print(f"  {dept_info['priority']}. {dept_info['name']} ({dept_key}): {dept_info['description']}")