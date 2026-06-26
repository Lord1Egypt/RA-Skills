"""
接口自动化测试服务

管理API测试脚本的配置、调试和执行
"""

import json
import os
import subprocess
import tempfile
from typing import Optional, Dict, List
from datetime import datetime
import logging

from sqlalchemy.orm import Session
from app.models.script import AutoScript
from app.models.task import TaskProgress
from app.schemas.api_test import (
    ScriptCreate, ScriptUpdate, ScriptResponse,
    EnvironmentConfig, ExecuteResult
)

logger = logging.getLogger(__name__)


class ApiTestService:
    """接口自动化测试服务类"""

    def __init__(self, db: Session):
        self.db = db
        self.environments = {}  # 环境配置缓存

    def create_script(self, script_data: ScriptCreate, created_by: str = None) -> ScriptResponse:
        """
        创建API测试脚本

        Args:
            script_data: 脚本数据
            created_by: 创建者（授权码）

        Returns:
            创建的脚本
        """
        script = AutoScript(
            name=script_data.name,
            content=script_data.content,
            type=script_data.type,
            created_by=created_by
        )
        self.db.add(script)
        self.db.commit()
        self.db.refresh(script)

        # 保存到文件
        self._save_script_to_file(script)

        logger.info(f"创建API测试脚本: {script.name}, ID: {script.id}")
        return ScriptResponse(**script.to_dict())

    def get_script(self, script_id: int) -> Optional[AutoScript]:
        """获取脚本"""
        return self.db.query(AutoScript).filter(
            AutoScript.id == script_id,
            AutoScript.type == "api"
        ).first()

    def list_scripts(self, created_by: str = None) -> List[AutoScript]:
        """列出脚本"""
        query = self.db.query(AutoScript).filter(AutoScript.type == "api")

        if created_by:
            query = query.filter(AutoScript.created_by == created_by)

        return query.filter(AutoScript.status == "active").all()

    def update_script(self, script_id: int, script_data: ScriptUpdate) -> Optional[ScriptResponse]:
        """更新脚本"""
        script = self.get_script(script_id)
        if not script:
            return None

        if script_data.name:
            script.name = script_data.name
        if script_data.content:
            script.content = script_data.content
        if script_data.status:
            script.status = script_data.status

        self.db.commit()

        # 更新文件
        if script_data.content:
            self._save_script_to_file(script)

        logger.info(f"更新API测试脚本: {script.name}, ID: {script_id}")
        return ScriptResponse(**script.to_dict())

    def delete_script(self, script_id: int) -> bool:
        """删除脚本"""
        script = self.get_script(script_id)
        if not script:
            return False

        # 删除文件
        try:
            file_path = self._get_script_file_path(script)
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            logger.error(f"删除脚本文件失败: {str(e)}")

        self.db.delete(script)
        self.db.commit()

        logger.info(f"删除API测试脚本: ID: {script_id}")
        return True

    def debug_script(self, script_id: int, environment: str = None) -> Dict:
        """
        调试脚本（单次执行，不保存结果）

        Args:
            script_id: 脚本ID
            environment: 环境名称

        Returns:
            调试结果
        """
        script = self.get_script(script_id)
        if not script:
            return {"error": "脚本不存在"}

        try:
            # 准备执行环境
            exec_result = self._execute_script(script, environment, debug=True)

            return {
                "success": exec_result["result"] == "success",
                "log": exec_result["log"],
                "duration": exec_result["duration"],
                "request": exec_result.get("request"),
                "response": exec_result.get("response"),
                "status_code": exec_result.get("status_code")
            }
        except Exception as e:
            logger.error(f"调试脚本失败: {str(e)}")
            return {"error": str(e)}

    def execute_script(self, script_id: int, environment: str = None, timeout: int = 300) -> Dict:
        """
        执行API测试脚本

        Args:
            script_id: 脚本ID
            environment: 环境名称
            timeout: 超时时间（秒）

        Returns:
            执行结果
        """
        script = self.get_script(script_id)
        if not script:
            return {
                "error": "脚本不存在",
                "result": "fail"
            }

        try:
            # 执行脚本
            exec_result = self._execute_script(script, environment, timeout)

            # 返回完整结果
            return {
                "script_id": script.id,
                "script_name": script.name,
                "result": exec_result["result"],
                "duration": exec_result["duration"],
                "log": exec_result["log"],
                "report_path": exec_result.get("report_path")
            }
        except Exception as e:
            logger.error(f"执行脚本失败: {str(e)}")
            return {
                "script_id": script.id,
                "script_name": script.name,
                "result": "fail",
                "duration": 0,
                "log": str(e)
            }

    def execute_batch(self, script_ids: List[int], environment: str = None, timeout: int = 600) -> List[Dict]:
        """
        批量执行脚本

        Args:
            script_ids: 脚本ID列表
            environment: 环境名称
            timeout: 总超时时间（秒）

        Returns:
            所有脚本的执行结果
        """
        results = []

        for script_id in script_ids:
            try:
                result = self.execute_script(script_id, environment, timeout=timeout // len(script_ids))
                results.append(result)
            except Exception as e:
                logger.error(f"批量执行失败 (script_id={script_id}): {str(e)}")
                results.append({
                    "script_id": script_id,
                    "result": "fail",
                    "log": str(e)
                })

        return results

    def configure_environment(self, config: EnvironmentConfig):
        """
        配置测试环境

        Args:
            config: 环境配置
        """
        self.environments[config.name] = {
            "base_url": config.base_url,
            "headers": config.headers or {},
            "params": config.params or {}
        }

        logger.info(f"配置测试环境: {config.name}, base_url: {config.base_url}")

    def get_environment(self, name: str) -> Optional[Dict]:
        """获取环境配置"""
        return self.environments.get(name)

    def _save_script_to_file(self, script: AutoScript):
        """保存脚本到文件"""
        try:
            file_path = self._get_script_file_path(script)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(script.content)

            logger.info(f"保存脚本到文件: {file_path}")
        except Exception as e:
            logger.error(f"保存脚本文件失败: {str(e)}")

    def _get_script_file_path(self, script: AutoScript) -> str:
        """获取脚本文件路径"""
        return f"data/scripts/{script.type}_script_{script.id}.py"

    def _execute_script(self, script: AutoScript, environment: str = None,
                        timeout: int = 300, debug: bool = False) -> Dict:
        """
        执行脚本的核心方法

        Args:
            script: 脚本对象
            environment: 环境名称
            timeout: 超时时间
            debug: 是否调试模式

        Returns:
            执行结果
        """
        import time

        start_time = time.time()

        try:
            # 准备环境变量
            env_config = self.environments.get(environment) if environment else None

            # 创建临时文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                # 注入环境配置到脚本
                script_content = script.content

                if env_config:
                    # 在脚本开头添加环境配置
                    config_code = f'''
# 环境配置
TEST_BASE_URL = "{env_config["base_url"]}"
TEST_HEADERS = {json.dumps(env_config["headers"], ensure_ascii=False)}
TEST_PARAMS = {json.dumps(env_config["params"], ensure_ascii=False)}
'''
                    script_content = config_code + script_content

                # 添加pytest-json-report配置
                if not debug:
                    import_report = '''
import sys
import json
from io import StringIO

# 捕获pytest输出
old_stdout = sys.stdout
sys.stdout = mystdout = StringIO()
'''
                    script_content = import_report + script_content

                f.write(script_content)
                temp_file = f.name

            try:
                # 构建pytest命令
                cmd = [
                    "pytest",
                    temp_file,
                    "-v",
                    "--tb=short"
                ]

                if not debug:
                    # 添加JSON报告
                    cmd.extend([
                        "--json-report",
                        "--json-report-file=-"
                    ])

                # 执行pytest
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    cwd=os.path.dirname(temp_file)
                )

                duration = int(time.time() - start_time)

                # 收集日志
                log_lines = []
                if result.stdout:
                    log_lines.extend(result.stdout.split('\n'))
                if result.stderr:
                    log_lines.extend(result.stderr.split('\n'))

                log = '\n'.join([line for line in log_lines if line.strip()])

                # 解析结果
                exec_result = {
                    "result": "success" if result.returncode == 0 else "fail",
                    "duration": duration,
                    "log": log
                }

                # 保存报告
                if not debug and result.returncode == 0:
                    report_path = self._save_report(script, result.stdout)
                    if report_path:
                        exec_result["report_path"] = report_path

                return exec_result

            finally:
                # 清理临时文件
                try:
                    os.unlink(temp_file)
                except:
                    pass

        except subprocess.TimeoutExpired:
            logger.error(f"脚本执行超时: {script.name}")
            return {
                "result": "fail",
                "duration": int(time.time() - start_time),
                "log": "执行超时"
            }
        except Exception as e:
            logger.error(f"执行脚本异常: {str(e)}")
            return {
                "result": "fail",
                "duration": int(time.time() - start_time),
                "log": str(e)
            }

    def _save_report(self, script: AutoScript, report_output: str) -> Optional[str]:
        """
        保存测试报告

        Args:
            script: 脚本对象
            report_output: pytest输出

        Returns:
            报告文件路径
        """
        try:
            # 创建报告目录
            report_dir = f"data/reports/api"
            os.makedirs(report_dir, exist_ok=True)

            # 生成报告文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = f"{report_dir}/{script.name}_{timestamp}.html"

            # 这里可以生成HTML报告
            # 简单实现：保存日志
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(f"""
<!DOCTYPE html>
<html>
<head>
    <title>测试报告 - {script.name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #4CAF50; color: white; padding: 10px; }}
        .content {{ padding: 20px; }}
        pre {{ background: #f4f4f4; padding: 10px; overflow-x: auto; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>API测试报告 - {script.name}</h1>
        <p>执行时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>
    <div class="content">
        <h2>执行日志</h2>
        <pre>{report_output}</pre>
    </div>
</body>
</html>
""")

            logger.info(f"保存测试报告: {report_path}")
            return report_path

        except Exception as e:
            logger.error(f"保存测试报告失败: {str(e)}")
            return None
