#!/usr/bin/env python3
"""
Pre-tool-use Hook示例

在工具执行前运行，可用于：
- 权限检查
- 参数验证
- 审计日志
- 动态审批
"""

def pre_tool_use(tool_name: str, tool_input: dict) -> dict:
    """
    工具执行前Hook
    
    Args:
        tool_name: 工具名称
        tool_input: 工具输入参数
        
    Returns:
        修改后的工具输入参数，或抛出异常阻止执行
    """
    print(f"[Hook] Pre-tool-use: {tool_name}")
    print(f"[Hook] Input: {tool_input}")
    
    # 示例：阻止危险命令
    if tool_name == "bash":
        command = tool_input.get("command", "")
        dangerous_patterns = ["rm -rf", "sudo", "dd if="]
        for pattern in dangerous_patterns:
            if pattern in command:
                raise PermissionError(f"Dangerous command detected: {command}")
    
    return tool_input
