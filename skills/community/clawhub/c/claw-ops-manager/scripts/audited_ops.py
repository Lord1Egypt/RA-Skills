#!/usr/bin/env python3
"""
完整的自动记录器 - 集成友好描述和自动快照
"""
import sys
import os
import json
import subprocess
import time
from pathlib import Path
from datetime import datetime

# 添加技能路径
SKILL_PATH = Path.home() / ".openclaw" / "workspace" / "skills" / "claw-ops-manager"
sys.path.insert(0, str(SKILL_PATH))

from scripts.logger import OperationLogger
from scripts.describer import OperationDescriber
from scripts.snapshot import SnapshotManager

class AutoAuditedOperation:
    """自动审计的操作"""

    def __init__(self):
        self.logger = OperationLogger()
        self.describer = OperationDescriber()
        self.snapshot_manager = SnapshotManager()
        self.current_user = os.environ.get("USER", "unknown")
        self.enable_auto_snapshot = True

        # 自动快照的路径列表
        self.auto_snapshot_paths = [
            str(Path.home() / "Desktop"),
            str(Path.home() / "Documents"),
            str(Path.home() / "Downloads"),
            str(Path.home() / ".ssh"),
            "/etc/ssh",
            "/etc/sudoers.d",
        ]

    def execute_and_log(
        self,
        tool_name: str,
        action: str,
        parameters: dict,
        execute_func,
        create_snapshot: bool = True
    ):
        """
        执行并记录操作，自动创建快照

        Args:
            tool_name: 工具名称
            action: 操作类型
            parameters: 参数字典
            execute_func: 执行函数
            create_snapshot: 是否创建快照

        Returns:
            执行结果
        """
        # 生成友好描述
        friendly_desc = self.describer.describe(tool_name, action, parameters)

        print(f"📝 {friendly_desc}")

        # 检查权限
        target_path = None
        if tool_name == "exec" and action == "run_command":
            # 从命令中提取路径
            command = parameters.get("command", "")
            for path in self.auto_snapshot_paths:
                if path in command:
                    target_path = path
                    break
        elif "path" in parameters:
            target_path = parameters["path"]
        elif "file_path" in parameters:
            target_path = parameters["file_path"]

        allowed, rule = self.logger.check_permission(
            tool_name=tool_name,
            action=action,
            path=target_path
        )

        if not allowed:
            print(f"❌ 权限被拒绝: {rule}")
            # 记录被阻止的操作
            op_id = self._log_operation(
                tool_name, action, parameters,
                friendly_desc=friendly_desc,
                success=False
            )

            self.logger.create_alert(
                operation_id=op_id,
                alert_type="permission_denied",
                severity="high",
                message=f"权限规则 '{rule}' 阻止了操作: {friendly_desc}"
            )

            raise PermissionError(f"被规则 '{rule}' 阻止")

        # 创建操作前快照
        snapshot_id = None
        if create_snapshot and self.enable_auto_snapshot and target_path:
            try:
                if Path(target_path).exists():
                    snapshot = self.snapshot_manager.create_snapshot(
                        paths_to_snapshot=[target_path],
                        operation_desc=f"操作前: {friendly_desc}",
                        auto=True
                    )
                    snapshot_id = snapshot["id"]
                    print(f"📸 创建快照: {snapshot_id[:12]}")
            except Exception as e:
                print(f"⚠️  快照创建失败: {e}")

        # 执行操作
        start_time = time.time()
        try:
            result = execute_func()
            duration_ms = int((time.time() - start_time) * 1000)

            # 记录成功的操作
            op_id = self._log_operation(
                tool_name, action, parameters,
                friendly_desc=friendly_desc,
                result=result,
                success=True,
                duration_ms=duration_ms,
                snapshot_id=snapshot_id
            )

            print(f"✅ 操作成功 (ID: {op_id}, 耗时: {duration_ms}ms)")

            if snapshot_id:
                print(f"💾 可回滚到: {snapshot_id[:12]}")

            return result

        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)

            # 记录失败的操作
            op_id = self._log_operation(
                tool_name, action, parameters,
                friendly_desc=friendly_desc,
                result=str(e),
                success=False,
                duration_ms=duration_ms,
                snapshot_id=snapshot_id
            )

            print(f"❌ 操作失败: {e}")

            # 重要操作失败时创建告警
            if tool_name in ["exec", "write", "edit"]:
                self.logger.create_alert(
                    operation_id=op_id,
                    alert_type="operation_failed",
                    severity="medium",
                    message=f"{friendly_desc} 失败: {str(e)}"
                )

            raise

    def _log_operation(
        self,
        tool_name: str,
        action: str,
        parameters: dict,
        friendly_desc: str,
        result=None,
        success: bool = True,
        duration_ms: int = 0,
        snapshot_id: str = None
    ) -> int:
        """记录操作到数据库"""
        self.logger.connect()
        cursor = self.logger.conn.cursor()

        cursor.execute("""
            INSERT INTO operations (
                tool_name, action, parameters, result, success,
                duration_ms, user, timestamp, friendly_name, snapshot_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tool_name,
            action,
            json.dumps(parameters, default=str),
            json.dumps(result, default=str)[:1000] if result else None,
            success,
            duration_ms,
            self.current_user,
            datetime.now().isoformat(),
            friendly_desc,
            snapshot_id
        ))

        op_id = cursor.lastrowid
        self.logger.conn.commit()
        self.logger.close()

        return op_id

    def rollback(self, snapshot_id: str, paths: list = None):
        """回滚到指定快照"""
        print(f"🔄 回滚到快照: {snapshot_id[:12]}")

        result = self.snapshot_manager.restore_snapshot(snapshot_id, paths)

        if result["success"]:
            print(f"✅ 回滚成功!")
            print(f"   恢复的文件: {len(result['restored_files'])}")

            # 记录回滚操作
            self._log_operation(
                tool_name="snapshot",
                action="restore",
                parameters={"snapshot_id": snapshot_id, "paths": paths},
                friendly_desc=f"回滚到: {result['description']}",
                success=True,
                duration_ms=0
            )

            return True
        else:
            print(f"❌ 回滚失败: {result['error']}")
            return False


# 便捷函数
def audited_exec(command: str):
    """执行并记录命令"""
    auditor = AutoAuditedOperation()

    def execute():
        return subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

    return auditor.execute_and_log(
        tool_name="exec",
        action="run_command",
        parameters={"command": command},
        execute_func=execute
    )


def audited_write(file_path: str, content: str):
    """写入并记录文件"""
    auditor = AutoAuditedOperation()

    def execute():
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
        return True

    return auditor.execute_and_log(
        tool_name="write",
        action="create_file",
        parameters={"file_path": file_path, "content_length": len(content)},
        execute_func=execute
    )


def rollback_to(snapshot_id: str, paths: list = None):
    """回滚到快照"""
    auditor = AutoAuditedOperation()
    return auditor.rollback(snapshot_id, paths)


# 测试
if __name__ == "__main__":
    print("🧪 测试自动审计系统\n")

    # 测试 1: 删除操作
    print("测试 1: 删除文件")
    test_file = Path.home() / "Desktop" / "test_audit.txt"
    test_file.write_text("test content")

    try:
        result = audited_exec(f"rm {test_file}")
        print(f"返回码: {result.returncode}\n")
    except Exception as e:
        print(f"错误: {e}\n")

    # 测试 2: 创建文件
    print("测试 2: 创建文件")
    try:
        result = audited_write(f"{Path.home()}/Desktop/test_audit_2.txt", "hello")
        print(f"结果: {result}\n")
    except Exception as e:
        print(f"错误: {e}\n")

    print("✅ 测试完成!")
    print("🌐 查看: http://localhost:8080")
