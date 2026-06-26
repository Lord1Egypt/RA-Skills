"""
UI自动化测试服务

管理UI测试脚本的配置、Playwright执行和结果收集
"""

import json
import os
import subprocess
import asyncio
import tempfile
from typing import Optional, List, Dict
from datetime import datetime
import logging

from sqlalchemy.orm import Session
from app.models.script import AutoScript
from app.models.task import TaskProgress
from app.schemas.ui_test import (
    UiScriptCreate, UiScriptUpdate,
    BrowserConfig, UiExecuteRequest, UiExecuteBatchRequest, UiExecuteResult
)

logger = logging.getLogger(__name__)


class UiTestService:
    """UI自动化测试服务类"""

    def __init__(self, db: Session):
        self.db = db
        self.browser_configs = {}  # 浏览器配置缓存

    def create_script(self, script_data: UiScriptCreate, created_by: str = None) -> dict:
        """
        创建UI测试脚本

        Args:
            script_data: 脚本数据
            created_by: 创建者（授权码）

        Returns:
            创建的脚本
        """
        script = AutoScript(
            name=script_data.name,
            content=script_data.content,
            type="ui",
            created_by=created_by
        )
        self.db.add(script)
        self.db.commit()
        self.db.refresh(script)

        # 保存到文件
        self._save_script_to_file(script)

        logger.info(f"创建UI测试脚本: {script.name}, ID: {script.id}")
        return script.to_dict()

    def get_script(self, script_id: int) -> Optional[AutoScript]:
        """获取UI脚本"""
        return self.db.query(AutoScript).filter(
            AutoScript.id == script_id,
            AutoScript.type == "ui"
        ).first()

    def list_scripts(self, created_by: str = None) -> List[AutoScript]:
        """列出UI脚本"""
        query = self.db.query(AutoScript).filter(AutoScript.type == "ui")

        if created_by:
            query = query.filter(AutoScript.created_by == created_by)

        return query.filter(AutoScript.status == "active").all()

    def update_script(self, script_id: int, script_data: UiScriptUpdate) -> Optional[dict]:
        """更新UI脚本"""
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

        logger.info(f"更新UI测试脚本: {script.name}, ID: {script_id}")
        return script.to_dict()

    def delete_script(self, script_id: int) -> bool:
        """删除UI脚本"""
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

        logger.info(f"删除UI测试脚本: ID: {script_id}")
        return True

    def configure_browser(self, script_id: int, config: BrowserConfig) -> bool:
        """
        配置浏览器

        Args:
            script_id: 脚本ID
            config: 浏览器配置

        Returns:
            是否配置成功
        """
        script = self.get_script(script_id)
        if not script:
            return False

        self.browser_configs[script_id] = {
            "browser_type": config.browser_type,
            "headless": config.headless,
            "viewport": config.viewport,
            "slow_mo": config.slow_mo
        }

        logger.info(f"配置浏览器: script_id={script_id}, browser={config.browser_type}")
        return True

    def get_browser_config(self, script_id: int) -> Optional[Dict]:
        """获取浏览器配置"""
        return self.browser_configs.get(script_id, {
            "browser_type": "chromium",
            "headless": True,
            "viewport": {"width": 1920, "height": 1080},
            "slow_mo": 0
        })

    def execute_script(self, request: UiExecuteRequest) -> Dict:
        """
        执行UI测试脚本

        Args:
            request: 执行请求

        Returns:
            执行结果
        """
        script = self.get_script(request.script_id)
        if not script:
            return {
                "error": "脚本不存在",
                "result": "fail"
            }

        try:
            # 获取浏览器配置
            browser_config = request.browser_config or BrowserConfig()
            config_dict = {
                "browser_type": browser_config.browser_type,
                "headless": browser_config.headless,
                "viewport": browser_config.viewport,
                "slow_mo": browser_config.slow_mo
            }

            # 执行脚本
            exec_result = asyncio.run(self._execute_playwright_script(
                script,
                config_dict,
                timeout=request.timeout
            ))

            return {
                "script_id": script.id,
                "script_name": script.name,
                "result": exec_result["result"],
                "duration": exec_result["duration"],
                "screenshot_count": exec_result.get("screenshot_count", 0),
                "trace_path": exec_result.get("trace_path"),
                "log": exec_result["log"]
            }
        except Exception as e:
            logger.error(f"执行UI脚本失败: {str(e)}")
            return {
                "script_id": script.id,
                "script_name": script.name,
                "result": "fail",
                "duration": 0,
                "screenshot_count": 0,
                "log": str(e)
            }

    def execute_batch(self, request: UiExecuteBatchRequest) -> List[Dict]:
        """
        批量执行UI脚本

        Args:
            request: 批量执行请求

        Returns:
            所有脚本的执行结果
        """
        results = []

        for script_id in request.script_ids:
            try:
                # 为每个脚本创建独立的执行请求
                exec_request = UiExecuteRequest(
                    script_id=script_id,
                    browser_config=request.browser_config,
                    timeout=request.timeout // len(request.script_ids)
                )
                result = self.execute_script(exec_request)
                results.append(result)
            except Exception as e:
                logger.error(f"批量执行失败 (script_id={script_id}): {str(e)}")
                results.append({
                    "script_id": script_id,
                    "result": "fail",
                    "log": str(e)
                })

        return results

    async def _execute_playwright_script(self, script: AutoScript, config: dict, timeout: int) -> Dict:
        """
        使用Playwright执行脚本

        Args:
            script: 脚本对象
            config: 浏览器配置
            timeout: 超时时间

        Returns:
            执行结果
        """
        import time

        start_time = time.time()

        try:
            # 准备截图和trace目录
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_dir = f"data/screenshots/{script.name}_{timestamp}"
            trace_dir = f"data/traces/{script.name}_{timestamp}"

            os.makedirs(screenshot_dir, exist_ok=True)
            os.makedirs(trace_dir, exist_ok=True)

            # 创建测试配置文件
            test_config = {
                "base_url": "http://localhost:3000",  # 默认前端地址
                "screenshot_dir": screenshot_dir,
                "trace_dir": trace_dir,
                **config
            }

            # 在脚本中注入配置
            script_content = f"""
# Playwright配置
from playwright.async_api import async_playwright

# 测试配置
TEST_CONFIG = {json.dumps(test_config, ensure_ascii=False)}

# 截图目录
SCREENSHOT_DIR = "{screenshot_dir}"
TRACE_DIR = "{trace_dir}"
"""
            script_content = script_content + script.content

            # 创建临时测试文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                f.write(script_content)
                temp_file = f.name

            try:
                # 构建pytest命令
                cmd = [
                    "pytest",
                    temp_file,
                    "-v",
                    "--tb=short",
                    "--asyncio-mode=auto"
                ]

                # 执行pytest
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

                try:
                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(),
                        timeout=timeout
                    )

                    duration = int(time.time() - start_time)

                    # 收集日志
                    log_lines = []
                    if stdout:
                        log_lines.extend(stdout.decode().split('\n'))
                    if stderr:
                        log_lines.extend(stderr.decode().split('\n'))

                    log = '\n'.join([line for line in log_lines if line.strip()])

                    # 统计截图数量
                    screenshot_count = len([f for f in os.listdir(screenshot_dir) if f.endswith('.png')])

                    # 查找trace文件
                    trace_path = None
                    if os.path.exists(trace_dir):
                        trace_files = [f for f in os.listdir(trace_dir) if f.endswith('.zip')]
                        if trace_files:
                            trace_path = os.path.join(trace_dir, trace_files[0])

                    # 解析结果
                    exec_result = {
                        "result": "success" if process.returncode == 0 else "fail",
                        "duration": duration,
                        "screenshot_count": screenshot_count,
                        "trace_path": trace_path,
                        "log": log
                    }

                    return exec_result

                except asyncio.TimeoutError:
                    logger.error(f"Playwright执行超时: {script.name}")
                    # 终止进程
                    process.kill()
                    await process.wait()

                    return {
                        "result": "fail",
                        "duration": int(time.time() - start_time),
                        "screenshot_count": 0,
                        "log": "执行超时"
                    }

            finally:
                # 清理临时文件
                try:
                    os.unlink(temp_file)
                except:
                    pass

        except Exception as e:
            logger.error(f"执行Playwright脚本异常: {str(e)}")
            return {
                "result": "fail",
                "duration": int(time.time() - start_time),
                "screenshot_count": 0,
                "log": str(e)
            }

    def _save_script_to_file(self, script: AutoScript):
        """保存UI脚本到文件"""
        try:
            file_path = self._get_script_file_path(script)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(script.content)

            logger.info(f"保存UI脚本到文件: {file_path}")
        except Exception as e:
            logger.error(f"保存UI脚本文件失败: {str(e)}")

    def _get_script_file_path(self, script: AutoScript) -> str:
        """获取UI脚本文件路径"""
        return f"data/scripts/{script.type}_script_{script.id}.py"

    def get_screenshot(self, script_id: int, screenshot_name: str) -> Optional[str]:
        """
        获取截图文件路径

        Args:
            script_id: 脚本ID
            screenshot_name: 截图文件名

        Returns:
            截图文件路径
        """
        script = self.get_script(script_id)
        if not script:
            return None

        # 查找最新的截图目录
        screenshot_dir = f"data/screenshots/{script.name}"
        if not os.path.exists(screenshot_dir):
            return None

        # 按时间戳排序，获取最新的目录
        import glob
        dirs = sorted(glob.glob(f"{screenshot_dir}_*"), reverse=True)

        if not dirs:
            return None

        latest_dir = dirs[0]
        screenshot_path = os.path.join(latest_dir, screenshot_name)

        if os.path.exists(screenshot_path):
            return screenshot_path

        return None

    def get_trace_file(self, script_id: int) -> Optional[str]:
        """
        获取Trace文件路径

        Args:
            script_id: 脚本ID

        Returns:
            Trace文件路径
        """
        script = self.get_script(script_id)
        if not script:
            return None

        # 查找最新的trace目录
        trace_dir = f"data/traces/{script.name}"
        if not os.path.exists(trace_dir):
            return None

        import glob
        dirs = sorted(glob.glob(f"{trace_dir}_*"), reverse=True)

        if not dirs:
            return None

        latest_dir = dirs[0]
        trace_files = glob.glob(f"{latest_dir}/*.zip")

        if trace_files:
            return trace_files[0]

        return None
