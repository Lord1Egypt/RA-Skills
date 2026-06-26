"""
Fallback Manager - 备用工具自动匹配与切换能力
遵循PRD 4.3节要求
"""

import time
from typing import Callable, Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class FallbackPriority(Enum):
    """备用工具匹配优先级"""
    PERFECT_MATCH = 4      # 核心功能100%匹配，参数字段重合度≥90%
    HIGH_QUALITY = 3       # 平台官方认证、成功率≥95%
    USER_PREFERRED = 2     # 用户历史使用过的同类Skill
    STANDARD = 1           # 无投诉、无合规风险


@dataclass
class BackupTool:
    """备用工具信息"""
    name: str
    func: Callable
    param_mapping: Dict[str, str] = field(default_factory=dict)
    priority: FallbackPriority = FallbackPriority.STANDARD
    success_rate: float = 0.0
    is_official: bool = False
    requires_confirmation: bool = False


@dataclass
class FallbackResult:
    """备用工具切换结果"""
    success: bool
    result: Any = None
    exception: Optional[Exception] = None
    primary_tool: str = ""
    backup_tool: str = ""
    switch_count: int = 0
    param_mapping_applied: Dict[str, str] = field(default_factory=dict)
    duration: float = 0.0


class FallbackManager:
    """
    备用工具自动匹配与切换能力
    
    Features:
    - 自动匹配备用工具池
    - 智能参数映射适配
    - 支持人工确认开关
    - 最多2次切换保障
    """
    
    # 平台强制限制
    MAX_SWITCH_ATTEMPTS = 2
    
    def __init__(self):
        """初始化备用工具管理器"""
        self._backup_tools: Dict[str, List[BackupTool]] = {}
        self._tool_metadata: Dict[str, Dict] = {}
        self._user_preferences: Dict[str, str] = {}
        self._switch_history: List[Dict] = []
    
    def register_backup(
        self,
        primary: str,
        backup: str,
        backup_func: Callable,
        param_mapping: Optional[Dict[str, str]] = None,
        priority: FallbackPriority = FallbackPriority.STANDARD,
        success_rate: float = 0.0,
        is_official: bool = False,
        requires_confirmation: bool = False
    ):
        """
        注册备用工具
        
        Args:
            primary: 主工具名称
            backup: 备用工具名称
            backup_func: 备用工具函数
            param_mapping: 参数映射规则 {原参数: 备用参数}
            priority: 匹配优先级
            success_rate: 历史成功率
            is_official: 是否官方认证
            requires_confirmation: 是否需要人工确认
        """
        if primary not in self._backup_tools:
            self._backup_tools[primary] = []
        
        backup_tool = BackupTool(
            name=backup,
            func=backup_func,
            param_mapping=param_mapping or {},
            priority=priority,
            success_rate=success_rate,
            is_official=is_official,
            requires_confirmation=requires_confirmation
        )
        
        self._backup_tools[primary].append(backup_tool)
        
        # 按优先级排序
        self._backup_tools[primary].sort(
            key=lambda x: (x.priority.value, x.success_rate),
            reverse=True
        )
    
    def execute_with_fallback(
        self,
        primary_func: Callable,
        primary_name: str,
        args: Optional[tuple] = None,
        kwargs: Optional[dict] = None,
        on_switch: Optional[Callable] = None,
        confirmation_callback: Optional[Callable] = None
    ) -> FallbackResult:
        """
        执行主工具，失败时自动切换到备用工具
        
        Args:
            primary_func: 主工具函数
            primary_name: 主工具名称
            args: 位置参数
            kwargs: 关键字参数
            on_switch: 切换时的回调函数
            confirmation_callback: 人工确认回调函数
            
        Returns:
            FallbackResult: 切换执行结果
        """
        args = args or ()
        kwargs = kwargs or {}
        
        start_time = time.time()
        switch_count = 0
        primary_error = None
        
        # 1. 尝试执行主工具
        try:
            result = primary_func(*args, **kwargs)
            return FallbackResult(
                success=True,
                result=result,
                primary_tool=primary_name,
                switch_count=0,
                duration=time.time() - start_time
            )
        except Exception as e:
            primary_error = e  # 主工具失败，进入备用工具切换流程
        
        # 2. 获取备用工具列表
        backup_tools = self._backup_tools.get(primary_name, [])
        
        if not backup_tools:
            return FallbackResult(
                success=False,
                exception=primary_error,
                primary_tool=primary_name,
                switch_count=0,
                duration=time.time() - start_time
            )
        
        # 3. 尝试切换到备用工具
        last_exception = primary_error
        
        for backup_tool in backup_tools[:self.MAX_SWITCH_ATTEMPTS]:
            switch_count += 1
            
            # 检查是否需要人工确认
            if backup_tool.requires_confirmation and confirmation_callback:
                confirmed = confirmation_callback(
                    primary_tool=primary_name,
                    backup_tool=backup_tool.name,
                    reason=str(primary_error)
                )
                if not confirmed:
                    continue
            
            # 参数映射适配
            mapped_args, mapped_kwargs = self._apply_param_mapping(
                args, kwargs, backup_tool.param_mapping
            )
            
            try:
                # 执行备用工具
                result = backup_tool.func(*mapped_args, **mapped_kwargs)
                
                duration = time.time() - start_time
                
                # 记录切换历史
                self._record_switch(
                    primary=primary_name,
                    backup=backup_tool.name,
                    success=True,
                    duration=duration
                )
                
                # 执行回调
                if on_switch:
                    on_switch(primary_name, backup_tool.name, switch_count)
                
                return FallbackResult(
                    success=True,
                    result=result,
                    primary_tool=primary_name,
                    backup_tool=backup_tool.name,
                    switch_count=switch_count,
                    param_mapping_applied=backup_tool.param_mapping,
                    duration=duration
                )
                
            except Exception as e:
                last_exception = e
                
                # 记录失败的切换尝试
                self._record_switch(
                    primary=primary_name,
                    backup=backup_tool.name,
                    success=False,
                    error=str(e)
                )
        
        # 所有备用工具都失败
        duration = time.time() - start_time
        
        return FallbackResult(
            success=False,
            exception=last_exception,
            primary_tool=primary_name,
            switch_count=switch_count,
            duration=duration
        )
    
    def _apply_param_mapping(
        self,
        args: tuple,
        kwargs: dict,
        param_mapping: Dict[str, str]
    ) -> tuple:
        """
        应用参数映射
        
        Args:
            args: 原始位置参数
            kwargs: 原始关键字参数
            param_mapping: 参数映射规则
            
        Returns:
            tuple: (映射后的args, 映射后的kwargs)
        """
        if not param_mapping:
            return args, kwargs
        
        # 映射kwargs
        mapped_kwargs = {}
        for key, value in kwargs.items():
            mapped_key = param_mapping.get(key, key)
            mapped_kwargs[mapped_key] = value
        
        return args, mapped_kwargs
    
    def _record_switch(
        self,
        primary: str,
        backup: str,
        success: bool,
        duration: float = 0.0,
        error: str = ""
    ):
        """记录切换历史"""
        record = {
            'timestamp': time.time(),
            'primary_tool': primary,
            'backup_tool': backup,
            'success': success,
            'duration': duration
        }
        if error:
            record['error'] = error
        
        self._switch_history.append(record)
    
    def get_backup_tools(self, primary_name: str) -> List[BackupTool]:
        """获取指定主工具的备用工具列表"""
        return self._backup_tools.get(primary_name, [])
    
    def set_user_preference(self, task_type: str, preferred_tool: str):
        """设置用户对某类任务的偏好工具"""
        self._user_preferences[task_type] = preferred_tool
    
    def get_switch_history(self) -> List[Dict]:
        """获取切换历史记录"""
        return self._switch_history.copy()
    
    def clear_switch_history(self):
        """清空切换历史"""
        self._switch_history = []