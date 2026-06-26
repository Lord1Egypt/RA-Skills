"""
任务查询工具 - 提供便捷的任务状态查询接口
"""

from typing import Dict, Any, Optional
from toolkit.api_client import VolcengineAPIClient
from toolkit.error_handler import VolcengineError


class TaskQuery:
    """任务查询工具类"""
    
    def __init__(self, client: VolcengineAPIClient):
        self.client = client
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        查询任务状态
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务状态信息
        """
        try:
            # 视频任务查询
            result = self.client.get(f"/contents/generations/tasks/{task_id}")
            return {
                "id": result.get("id"),
                "status": result.get("status"),
                "created_at": result.get("created_at"),
                "updated_at": result.get("updated_at"),
                "content": result.get("content"),
                "error": result.get("error")
            }
        except VolcengineError as e:
            raise e
    
    def list_tasks(
        self,
        page_num: int = 1,
        page_size: int = 20,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        列出任务列表
        
        Args:
            page_num: 页码
            page_size: 每页数量
            status: 过滤状态 (queued, running, succeeded, failed, cancelled)
            
        Returns:
            任务列表
        """
        params = {
            "page_num": page_num,
            "page_size": page_size
        }
        if status:
            params["filter.status"] = status
        
        try:
            result = self.client.get("/contents/generations/tasks", params=params)
            return {
                "items": result.get("items", []),
                "total": result.get("total", 0)
            }
        except VolcengineError as e:
            raise e
    
    def download_result(self, task_id: str, output_path: str) -> str:
        """
        下载任务结果
        
        Args:
            task_id: 任务ID
            output_path: 输出路径
            
        Returns:
            保存的文件路径
        """
        status = self.get_task_status(task_id)
        
        if status["status"] != "succeeded":
            raise ValueError(f"Task status is {status['status']}, cannot download")
        
        content = status.get("content", {})
        video_url = content.get("video_url")
        
        if not video_url:
            raise ValueError("No video URL found in task result")
        
        # 下载视频
        import httpx
        response = httpx.get(video_url, follow_redirects=True)
        
        with open(output_path, "wb") as f:
            f.write(response.content)
        
        return output_path
