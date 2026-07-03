#!/usr/bin/env python3
"""
Post-tool-use Hook示例

在工具执行后运行，可用于：
- 结果审计
- 数据收集
- 副作用处理
- 通知发送
"""

def post_tool_use(tool_name: str, tool_input: dict, tool_output: str) -> str:
    """
    工具执行后Hook
    
    Args:
        tool_name: 工具名称
        tool_input: 工具输入参数
        tool_output: 工具输出结果
        
    Returns:
        修改后的工具输出结果
    """
    print(f"[Hook] Post-tool-use: {tool_name}")
    print(f"[Hook] Output length: {len(tool_output)}")
    
    # 示例：记录审计日志
    import json
    from datetime import datetime
    
    audit_log = {
        "timestamp": datetime.now().isoformat(),
        "tool": tool_name,
        "input": tool_input,
        "output_length": len(tool_output)
    }
    
    with open("logs/audit.log", "a") as f:
        f.write(json.dumps(audit_log) + "\n")
    
    return tool_output
