"""
权限管理模块
规模: Professional
预期行数: ~120行

## ⚠ AI构建提示
根据用户需求生成以下内容:
1. PermissionRule dataclass - path_pattern, allowed_operations, deny_operations, reason
2. PermissionRequest dataclass - operation, path, tool_name
3. PermissionResult enum - ALLOWED, DENIED, ASK_USER
4. PermissionManager 类:
   - add_rule(rule: PermissionRule) - 添加规则
   - check(request: PermissionRequest) -> PermissionResult - 检查权限
   - 支持通配符路径匹配 (* 和 **)
   - 规则优先级: 具体路径 > 通配符路径, deny > allow

⚠ 路径匹配需要支持 glob 模式
⚠ 默认拒绝 (deny by default), 显式允许
⚠ 规则按优先级排序, 第一个匹配的规则生效
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum, auto
import fnmatch


class PermissionResult(Enum):
    """权限检查结果"""
    # TODO: ALLOWED, DENIED, ASK_USER


@dataclass
class PermissionRule:
    """权限规则"""
    # TODO: path_pattern, allowed_operations, deny_operations, reason


@dataclass
class PermissionRequest:
    """权限检查请求"""
    # TODO: operation, path, tool_name


class PermissionManager:
    """权限管理器"""

    # TODO: 实现 add_rule(), check(), _match_path()
    pass