"""
沙箱执行环境
规模: Professional
预期行数: ~100行

## ⚠ AI构建提示
根据用户需求生成以下内容:
1. SandboxConfig dataclass - allowed_dirs, max_file_size, timeout, network_enabled
2. Sandbox 类:
   - execute(tool_call: ToolCall) -> ToolResult - 在受限环境中执行工具调用
   - 文件系统隔离 (只允许在 allowed_dirs 内操作)
   - 超时控制 (asyncio.wait_for)
   - 文件大小限制
   - 命令执行限制 (可选)
3. ToolResult dataclass - success, output, error, duration

⚠ 使用 tempfile 创建临时工作目录
⚠ 所有文件操作必须验证路径在允许范围内
⚠ 设置超时防止无限循环
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SandboxConfig:
    """沙箱配置"""
    # TODO: allowed_dirs, max_file_size, timeout, network_enabled


@dataclass
class ToolResult:
    """工具执行结果"""
    # TODO: success, output, error, duration


class Sandbox:
    """沙箱执行环境"""

    # TODO: 实现 execute(), _validate_path(), _set_timeout()
    pass