#!/usr/bin/env python3
"""
OpenClaw 工具调用自动记录包装器

将此脚本集成到 OpenClaw 的工具调用链中，自动记录所有操作到审计系统
"""
import sys
import os
import json
import subprocess
import time
from pathlib import Path

# 添加技能路径
SKILL_PATH = Path.home() / ".openclaw" / "workspace" / "skills" / "claw-ops-manager"
sys.path.insert(0, str(SKILL_PATH))

from scripts.logger import OperationLogger

class AuditedToolCall:
    """工具调用包装器"""

    def __init__(self):
        self.logger = OperationLogger()
        self.current_user = os.environ.get("USER", "unknown")
        self.session_id = os.environ.get("OPENCLAW_SESSION", "main")

    def log_and_execute(self, tool_name, action, parameters, execute_func):
        """
        记录并执行工具调用

        Args:
            tool_name: 工具名称 (exec, read, write, browser, etc.)
            action: 操作名称
            parameters: 参数字典
            execute_func: 执行函数

        Returns:
            执行结果
        """
        # 检查权限
        allowed, rule = self.logger.check_permission(
            tool_name=tool_name,
            action=action,
            path=parameters.get("path") or parameters.get("file_path")
        )

        if not allowed:
            # 创建告警
            op_id = self.logger.log_operation(
                tool_name=tool_name,
                action=action,
                parameters=parameters,
                success=False,
                duration_ms=0,
                user=self.current_user
            )

            self.logger.create_alert(
                operation_id=op_id,
                alert_type="permission",
                severity="high",
                message=f"权限规则阻止操作: {rule}"
            )

            raise PermissionError(f"操作被规则 '{rule}' 阻止")

        # 记录开始时间
        start_time = time.time()

        # 执行操作
        try:
            result = execute_func()

            # 计算耗时
            duration_ms = int((time.time() - start_time) * 1000)

            # 记录成功的操作
            self.logger.log_operation(
                tool_name=tool_name,
                action=action,
                parameters=parameters,
                result=str(result)[:1000] if result else None,
                success=True,
                duration_ms=duration_ms,
                user=self.current_user
            )

            return result

        except Exception as e:
            # 计算耗时
            duration_ms = int((time.time() - start_time) * 1000)

            # 记录失败的操作
            op_id = self.logger.log_operation(
                tool_name=tool_name,
                action=action,
                parameters=parameters,
                result=str(e),
                success=False,
                duration_ms=duration_ms,
                user=self.current_user
            )

            # 如果是敏感操作失败，创建告警
            if tool_name in ["exec", "write", "edit"]:
                self.logger.create_alert(
                    operation_id=op_id,
                    alert_type="operation_failed",
                    severity="medium",
                    message=f"{tool_name}.{action} 失败: {str(e)}"
                )

            raise


# 全局实例
_audited_call = AuditedToolCall()

def audited_exec(command, **kwargs):
    """exec 工具的自动记录包装"""
    def execute():
        return subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            **kwargs
        )

    return _audited_call.log_and_execute(
        tool_name="exec",
        action="run_command",
        parameters={"command": command, "kwargs": kwargs},
        execute_func=execute
    )


def audited_write(file_path, content, **kwargs):
    """write 工具的自动记录包装"""
    def execute():
        with open(file_path, 'w') as f:
            f.write(content)
        return True

    return _audited_call.log_and_execute(
        tool_name="write",
        action="create_file",
        parameters={"file_path": file_path, **kwargs},
        execute_func=execute
    )


def audited_edit(file_path, old_text, new_text, **kwargs):
    """edit 工具的自动记录包装"""
    def execute():
        with open(file_path, 'r') as f:
            content = f.read()
        if old_text not in content:
            raise ValueError("old_text not found in file")
        content = content.replace(old_text, new_text)
        with open(file_path, 'w') as f:
            f.write(content)
        return True

    return _audited_call.log_and_execute(
        tool_name="edit",
        action="replace_text",
        parameters={"file_path": file_path, "old_length": len(old_text), "new_length": len(new_text)},
        execute_func=execute
    )


def audited_read(file_path, **kwargs):
    """read 工具的自动记录包装"""
    def execute():
        with open(file_path, 'r') as f:
            return f.read()

    return _audited_call.log_and_execute(
        tool_name="read",
        action="read_file",
        parameters={"file_path": file_path, **kwargs},
        execute_func=execute
    )


if __name__ == "__main__":
    # 测试
    print("🧪 测试自动记录...")

    try:
        result = audited_exec("ls -la ~")
        print(f"✅ 成功执行: ls -la ~")
        print(f"返回码: {result.returncode}")
    except Exception as e:
        print(f"❌ 执行失败: {e}")

    print("\n🌐 访问 http://localhost:8080 查看记录")
