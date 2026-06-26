"""
路由模块 - 基于配置文件智能分发任务
"""

import os
import yaml
from typing import Optional, Dict, Any

DEFAULT_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 
    "config", 
    "team.yaml"
)


class TeamRouter:
    """团队路由基类"""
    
    def __init__(self, config_path: str = DEFAULT_CONFIG_PATH):
        self.config_path = config_path
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """加载团队配置"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def reload(self):
        """重新加载配置"""
        self.config = self._load_config()
    
    def route_task(self, task: str) -> Optional[str]:
        """
        根据任务内容路由到对应专家
        
        Args:
            task: 任务文本
            
        Returns:
            专家名称，未匹配返回 None
        """
        task_lower = task.lower()
        
        for specialist in self.config.get('specialists', []):
            keywords = specialist.get('keywords', [])
            for kw in keywords:
                if kw.lower() in task_lower:
                    return specialist['name']
        
        return None
    
    def get_specialist_info(self, name: str) -> Optional[Dict[str, Any]]:
        """获取专家信息"""
        for specialist in self.config.get('specialists', []):
            if specialist['name'] == name:
                return specialist
        return None
    
    def get_all_specialists(self) -> list:
        """获取所有专家列表"""
        return self.config.get('specialists', [])
    
    def get_coordinator_info(self) -> Dict[str, Any]:
        """获取调度中心信息"""
        return self.config.get('coordinator', {})


def route_task(task: str, config_path: str = DEFAULT_CONFIG_PATH) -> Optional[str]:
    """快捷路由函数"""
    router = TeamRouter(config_path)
    return router.route_task(task)


if __name__ == "__main__":
    # 测试路由
    router = TeamRouter()
    
    test_tasks = [
        "分析一下AI市场趋势",
        "写一个用户登录功能",
        "推广新产品",
        "研究竞品情况"
    ]
    
    print("路由测试:")
    for task in test_tasks:
        specialist = router.route_task(task)
        print(f"  '{task}' → {specialist}")
