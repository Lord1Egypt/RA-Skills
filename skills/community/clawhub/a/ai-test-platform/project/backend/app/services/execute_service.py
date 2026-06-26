"""
测试执行服务

管理测试任务的调度、执行和结果收集
"""

import uuid
import asyncio
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
import logging

from app.models.script import AutoScript
from app.models.task import TaskProgress
from app.models.execute_record import ExecuteRecord
from app.services.api_test_service import ApiTestService
from app.schemas.api_test import ExecuteRequest, ExecuteBatchRequest

logger = logging.getLogger(__name__)


class ExecuteService:
    """测试执行服务类"""

    def __init__(self, db: Session):
        self.db = db
        self.api_test_service = ApiTestService(db)

    def execute_script_async(self, request: ExecuteRequest, auth_code: str) -> str:
        """
        异步执行单个脚本

        Args:
            request: 执行请求
            auth_code: 授权码

        Returns:
            任务ID
        """
        # 创建任务
        task_id = str(uuid.uuid4())
        task = TaskProgress(
            task_id=task_id,
            task_type="execute",
            status="pending",
            progress=0,
            message="任务已创建，等待执行"
        )
        self.db.add(task)

        # 查询脚本
        script = self.db.query(AutoScript).filter(AutoScript.id == request.script_id).first()
        if not script:
            task.status = "failed"
            task.message = "脚本不存在"
            return task_id

        self.db.commit()

        # 启动后台任务
        asyncio.create_task(self._execute_script_task(task_id, request, script, auth_code))

        return task_id

    def execute_batch_async(self, request: ExecuteBatchRequest, auth_code: str) -> str:
        """
        异步批量执行脚本

        Args:
            request: 批量执行请求
            auth_code: 授权码

        Returns:
            任务ID
        """
        # 创建任务
        task_id = str(uuid.uuid4())
        task = TaskProgress(
            task_id=task_id,
            task_type="execute",
            status="pending",
            progress=0,
            message="批量任务已创建，等待执行"
        )
        self.db.add(task)
        self.db.commit()

        # 启动后台任务
        asyncio.create_task(self._execute_batch_task(task_id, request, auth_code))

        return task_id

    async def _execute_script_task(self, task_id: str, request: ExecuteRequest,
                                   script: AutoScript, auth_code: str):
        """
        执行单个脚本的后台任务
        """
        task = self.db.query(TaskProgress).filter(TaskProgress.task_id == task_id).first()
        if not task:
            return

        try:
            # 更新任务状态
            task.status = "processing"
            task.progress = 10
            task.message = f"正在执行脚本: {script.name}"
            self.db.commit()

            # 执行脚本
            result = self.api_test_service.execute_script(
                request.script_id,
                environment=request.environment,
                timeout=request.timeout
            )

            # 保存执行记录
            record = ExecuteRecord(
                script_id=request.script_id,
                auth_code=auth_code,
                result=result.get("result", "fail"),
                log=result.get("log", ""),
                execute_time=datetime.now(),
                duration=result.get("duration", 0)
            )
            self.db.add(record)
            self.db.commit()

            # 更新任务状态
            task.status = "completed"
            task.progress = 100
            task.message = "执行完成"
            task.result_data = str({
                "success": result.get("result") == "success",
                "duration": result.get("duration", 0),
                "report_path": result.get("report_path")
            })
            self.db.commit()

            logger.info(f"脚本执行完成: {script.name}, 结果: {result.get('result')}")

        except Exception as e:
            logger.error(f"执行脚本失败: {str(e)}")
            task.status = "failed"
            task.message = f"执行失败: {str(e)}"
            task.progress = 0
            self.db.commit()

    async def _execute_batch_task(self, task_id: str, request: ExecuteBatchRequest, auth_code: str):
        """
        批量执行脚本的后台任务
        """
        task = self.db.query(TaskProgress).filter(TaskProgress.task_id == task_id).first()
        if not task:
            return

        try:
            total_scripts = len(request.script_ids)
            results = []

            for i, script_id in enumerate(request.script_ids):
                # 查询脚本
                script = self.db.query(AutoScript).filter(AutoScript.id == script_id).first()
                if not script:
                    results.append({
                        "script_id": script_id,
                        "result": "fail",
                        "message": "脚本不存在"
                    })
                    continue

                # 更新进度
                progress = int((i + 1) / total_scripts * 100)
                task.status = "processing"
                task.progress = progress
                task.message = f"正在执行 ({i + 1}/{total_scripts}): {script.name}"
                self.db.commit()

                # 执行脚本
                try:
                    result = self.api_test_service.execute_script(
                        script_id,
                        environment=request.environment,
                        timeout=request.timeout // total_scripts
                    )

                    # 保存执行记录
                    record = ExecuteRecord(
                        script_id=script_id,
                        auth_code=auth_code,
                        result=result.get("result", "fail"),
                        log=result.get("log", ""),
                        execute_time=datetime.now(),
                        duration=result.get("duration", 0)
                    )
                    self.db.add(record)

                    results.append({
                        "script_id": script_id,
                        "script_name": script.name,
                        "result": result.get("result", "fail"),
                        "duration": result.get("duration", 0),
                        "report_path": result.get("report_path")
                    })

                except Exception as e:
                    logger.error(f"执行脚本失败 (script_id={script_id}): {str(e)}")
                    results.append({
                        "script_id": script_id,
                        "result": "fail",
                        "message": str(e)
                    })

            self.db.commit()

            # 汇总结果
            success_count = sum(1 for r in results if r.get("result") == "success")
            fail_count = total_scripts - success_count

            # 更新任务状态
            task.status = "completed"
            task.progress = 100
            task.message = f"批量执行完成 - 成功: {success_count}, 失败: {fail_count}"
            task.result_data = str({
                "total": total_scripts,
                "success": success_count,
                "fail": fail_count,
                "results": results
            })
            self.db.commit()

            logger.info(f"批量执行完成: 总数={total_scripts}, 成功={success_count}, 失败={fail_count}")

        except Exception as e:
            logger.error(f"批量执行失败: {str(e)}")
            task.status = "failed"
            task.message = f"批量执行失败: {str(e)}"
            task.progress = 0
            self.db.commit()

    def get_execute_records(self, script_id: Optional[int] = None,
                          auth_code: Optional[str] = None,
                          limit: int = 100) -> List[dict]:
        """
        获取执行记录

        Args:
            script_id: 脚本ID（可选）
            auth_code: 授权码（可选）
            limit: 返回数量限制

        Returns:
            执行记录列表
        """
        query = self.db.query(ExecuteRecord)

        if script_id:
            query = query.filter(ExecuteRecord.script_id == script_id)

        if auth_code:
            query = query.filter(ExecuteRecord.auth_code == auth_code)

        records = query.order_by(ExecuteRecord.execute_time.desc()).limit(limit).all()

        return [
            {
                "id": record.id,
                "script_id": record.script_id,
                "result": record.result,
                "duration": record.duration,
                "execute_time": record.execute_time.strftime("%Y-%m-%d %H:%M:%S"),
                "log": record.log
            }
            for record in records
        ]

    def get_record_detail(self, record_id: int) -> Optional[dict]:
        """
        获取执行记录详情

        Args:
            record_id: 记录ID

        Returns:
            记录详情
        """
        record = self.db.query(ExecuteRecord).filter(ExecuteRecord.id == record_id).first()

        if not record:
            return None

        return {
            "id": record.id,
            "script_id": record.script_id,
            "auth_code": record.auth_code,
            "result": record.result,
            "log": record.log,
            "execute_time": record.execute_time.strftime("%Y-%m-%d %H:%M:%S"),
            "duration": record.duration
        }
