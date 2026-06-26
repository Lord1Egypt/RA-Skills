"""
任务进度检查工具模块
查询 ComfyCloud API 任务状态
"""

from utils import setup_logger, task_status

logger = setup_logger(__name__)

# 任务状态枚举
STATUS_PENDING = "pending"  # 任务已排队，等待开始
STATUS_IN_PROGRESS = "in_progress"  # 任务正在执行
STATUS_COMPLETED = "completed"  # 任务成功完成
STATUS_FAILED = "failed"  # 任务遇到错误
STATUS_CANCELLED = "cancelled"  # 任务被用户取消

STATUS_DESCRIPTION = {
    STATUS_PENDING: "任务已排队，等待开始",
    STATUS_IN_PROGRESS: "任务正在执行",
    STATUS_COMPLETED: "任务成功完成",
    STATUS_FAILED: "任务遇到错误",
    STATUS_CANCELLED: "任务被用户取消",
}


def register_tools(mcp):
    """注册工具到 MCP 服务器"""

    @mcp.tool()
    def check_progress(prompt_id: str) -> dict:
        """
        检查任务进度

        Args:
            prompt_id: 任务 ID

        Returns:
            dict: 任务状态信息，包含 status、status_desc、progress 等字段
        """
        logger.info(f"检查任务进度：prompt_id={prompt_id}")

        try:
            result = task_status(prompt_id)
            status = result.get("status", "unknown")

            # 添加状态描述
            result["status_desc"] = STATUS_DESCRIPTION.get(status, "未知状态")

            if status == STATUS_COMPLETED:
                logger.info(f"任务已完成：prompt_id={prompt_id}")
            elif status == STATUS_IN_PROGRESS:
                progress = result.get("progress", 0)
                logger.info(f"任务进行中：prompt_id={prompt_id}, progress={progress}%")
            elif status == STATUS_PENDING:
                logger.info(f"任务排队中：prompt_id={prompt_id}")
            elif status == STATUS_FAILED:
                logger.error(f"任务失败：prompt_id={prompt_id}, error={result.get('error', 'Unknown error')}")
            elif status == STATUS_CANCELLED:
                logger.warning(f"任务已取消：prompt_id={prompt_id}")
            else:
                logger.info(f"任务状态：prompt_id={prompt_id}, status={status}")

            return result
        except Exception as e:
            logger.error(f"检查进度失败：{e}")
            raise