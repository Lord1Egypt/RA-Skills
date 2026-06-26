"""
本地批量生成客户端请求封装
向本机 Electron 客户端的 HTTP 服务（127.0.0.1:17321）发送请求。
无需任何 API Key，只需保持本地客户端运行。
"""

from __future__ import annotations

import time
import threading
from typing import Any, Optional, Dict, List
from datetime import datetime, date

import requests


# ── 本地服务地址（固定，无需配置）──
LOCAL_BASE_URL = "http://127.0.0.1:17321"
DEFAULT_TIMEOUT = 30          # 普通请求超时（秒）
POLL_INTERVAL = 5             # 轮询间隔（秒）
DEFAULT_WAIT_TIMEOUT = 600    # 等待任务完成的最长时间（秒，10 分钟）


class ClientOfflineError(Exception):
    """本地客户端未运行或端口不可达。"""
    pass


class GenerateError(Exception):
    """任务提交失败。"""
    def __init__(self, message: str, task: dict | None = None) -> None:
        self.task = task
        super().__init__(message)


class DYULocalClient:
    """
    本地批量生成客户端封装。
    所有请求发往 http://127.0.0.1:17321，无需凭证。
    """

    def __init__(self, base_url: str = LOCAL_BASE_URL, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    # ── 工具方法 ──────────────────────────────────────────────────────────────

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def _get(self, path: str, params: dict | None = None) -> dict:
        try:
            resp = self.session.get(self._url(path), params=params, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.ConnectionError:
            raise ClientOfflineError(
                "无法连接到本地客户端（127.0.0.1:17321），请确认客户端已启动。"
            )

    def _post(self, path: str, body: Any) -> dict:
        try:
            resp = self.session.post(self._url(path), json=body, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.ConnectionError:
            raise ClientOfflineError(
                "无法连接到本地客户端（127.0.0.1:17321），请确认客户端已启动。"
            )

    # ── 状态检查 ──────────────────────────────────────────────────────────────

    def status(self) -> dict:
        """
        检查本地客户端状态。
        返回示例：{"success": True, "running": True, "version": "1.0.0", "ready": True}
        """
        return self._get("/api/status")

    def check_client(self) -> None:
        """
        确认本地客户端在线且已配置网关，否则抛出 ClientOfflineError。
        每次执行生成任务前调用此方法。
        """
        info = self.status()
        if not info.get("running"):
            raise ClientOfflineError("本地客户端未运行，请启动客户端后重试。")
        if not info.get("ready"):
            raise ClientOfflineError("本地客户端未配置网关（SK），请先在客户端完成 SK 配置。")

    # ── 单个任务 ──────────────────────────────────────────────────────────────

    def generate(self, task: dict) -> dict:
        """
        提交单个生成任务（视频或图片）。

        参数说明：
            task (dict): 任务参数，必填 model 和 prompt，其余按需填写：
                - model       (str, 必填): 模型名称
                - prompt      (str, 必填): 提示词
                - size        (str, 可选): 视频尺寸，如 "1920x1080"（Veo 必填）
                - image_url   (str, 可选): 参考图片 URL（Sora 图生视频）
                - style       (str, 可选): 视频风格（Sora）
                - metadata    (dict, 可选): 图片生成额外参数
                    - aspectRatio (str): "1:1" / "9:16" / "16:9" / "auto"
                    - urls        (list): 参考图片 URL 列表（图生图模式）
                - input_reference (str, 可选): Veo 参考图 JSON 字符串

        返回示例：
            {"success": True, "task_id": "task_xxx", "status": "queued", "model": "...", "prompt": "..."}
        """
        self.check_client()
        result = self._post("/api/generate", task)
        if not result.get("success"):
            raise GenerateError(result.get("error", "提交失败"), task)
        return result

    # ── 批量任务 ──────────────────────────────────────────────────────────────

    def generate_batch(self, tasks: list[dict]) -> dict:
        """
        批量提交生成任务。

        参数说明：
            tasks (list[dict]): 任务列表，每个元素与 generate() 的 task 参数相同。

        返回示例：
            {
                "success": True,
                "results": [
                    {"success": True, "task_id": "task_001", "status": "queued", ...},
                    {"success": True, "task_id": "task_002", "status": "queued", ...},
                    {"success": False, "error": "缺少 prompt", "task": {...}},
                ]
            }
        """
        if not tasks:
            return {"success": True, "results": []}
        self.check_client()
        result = self._post("/api/generate", tasks)
        return result

    # ── 任务查询 ──────────────────────────────────────────────────────────────

    def query_task(self, task_id: str) -> dict:
        """
        查询单个任务的状态和结果。

        返回示例（完成）：
            {"success": True, "id": "task_xxx", "status": "completed",
             "progress": 100, "url": "https://...", "model": "..."}

        返回示例（进行中）：
            {"success": True, "id": "task_xxx", "status": "processing", "progress": 45}

        返回示例（失败）：
            {"success": True, "id": "task_xxx", "status": "failed", "error": "内容违规"}
        """
        return self._get(f"/api/task/{task_id}")

    def query_tasks(self, task_ids: list[str]) -> dict:
        """
        批量查询多个任务状态。

        参数：
            task_ids (list[str]): 任务 ID 列表

        返回示例：
            {
                "success": True,
                "results": [
                    {"task_id": "task_001", "status": "completed", "url": "https://..."},
                    {"task_id": "task_002", "status": "processing", "progress": 60},
                ]
            }
        """
        return self._post("/api/tasks/query", {"task_ids": task_ids})

    def list_tasks(self, status: str | None = None) -> dict:
        """
        查询本地数据库中的任务列表（最近 50 条）。

        参数：
            status (str, 可选): 过滤状态，可选值：queued / processing / completed / failed

        返回示例：
            {"success": True, "tasks": [...]}
        """
        params = {"status": status} if status else None
        return self._get("/api/tasks", params=params)

    # ── 任务统计与筛选 ─────────────────────────────────────────────────────

    def _filter_tasks_by_date(self, tasks: List[dict], target_date: date | None) -> List[dict]:
        """
        按日期过滤任务（本地 DB 的 created_at 为毫秒时间戳）。
        target_date 为 None 时不过滤。
        """
        if not target_date:
            return tasks

        start_ts = datetime(target_date.year, target_date.month, target_date.day).timestamp()
        end_ts = start_ts + 86400  # 下一天
        start_ms, end_ms = int(start_ts * 1000), int(end_ts * 1000)

        result = []
        for t in tasks:
            created_at = t.get("created_at") or t.get("createdAt")
            if not isinstance(created_at, (int, float)):
                continue
            if start_ms <= int(created_at) < end_ms:
                result.append(t)
        return result

    def summarize_tasks(
        self,
        target_date: date | None = None,
        status: str | None = None,
    ) -> Dict[str, Any]:
        """
        统计任务信息（按日期和状态筛选），用于对话里的“今天生成了多少条任务、各类型多少、成功多少，把成功的 ID 发我一下”等需求。

        返回字段示例：
            {
              "total": 12,
              "by_type": {
                "veo": {"total": 5, "success": 4, "failed": 1, "ids": ["task_xxx", ...]},
                "sora": {"total": 3, "success": 3, "failed": 0, "ids": [...]},
                "image": {"total": 4, "success": 2, "failed": 2, "ids": [...]}
              }
            }
        """
        # 1. 先从本地接口拿所有任务（最多 50 条，足够覆盖“今天”的场景）
        resp = self.list_tasks(status=status)
        all_tasks = resp.get("tasks", [])
        if not isinstance(all_tasks, list):
            all_tasks = []

        # 2. 可选：按日期过滤（仅保留指定日期）
        tasks = self._filter_tasks_by_date(all_tasks, target_date)

        summary: Dict[str, Any] = {
            "total": len(tasks),
            "by_type": {
                "veo": {"total": 0, "success": 0, "failed": 0, "ids": []},
                "sora": {"total": 0, "success": 0, "failed": 0, "ids": []},
                "image": {"total": 0, "success": 0, "failed": 0, "ids": []},
            }
        }

        def classify(task: dict) -> str:
            model = str(task.get("model") or "").lower()
            category = str(task.get("category") or "").lower()
            # 图片：数据库 category 为 image-generation，或模型是 nano_banana 系
            if category == "image-generation" or model.startswith("nano_banana") or model.startswith("nano-banana"):
                return "image"
            # Veo：模型名里包含 veo
            if "veo" in model:
                return "veo"
            # Sora：模型名里包含 sora
            if "sora" in model:
                return "sora"
            # 未知：按视频归类到 sora 分组（也可以根据需要调整）
            return "sora"

        for t in tasks:
            group = classify(t)
            g = summary["by_type"][group]
            g["total"] += 1

            # 状态：本地 DB 使用 pending/processing/completed/failed
            status_val = str(t.get("status") or "").lower()
            is_success = status_val == "completed" or status_val == "success"
            is_failed = status_val == "failed"

            # 任务 ID：严格使用 upstream 的 task_id（video_id），要求是 task_xxx 这种
            video_id = t.get("video_id") or t.get("videoId")
            if isinstance(video_id, str) and video_id.startswith("task_"):
                if is_success:
                    g["success"] += 1
                    g["ids"].append(video_id)
                elif is_failed:
                    g["failed"] += 1

        return summary

    # ── 等待完成（单个）──────────────────────────────────────────────────────

    def wait_for_result(
        self,
        task_id: str,
        timeout: int = DEFAULT_WAIT_TIMEOUT,
        poll_interval: int = POLL_INTERVAL,
        on_progress: Any = None,
    ) -> dict:
        """
        轮询等待单个任务完成，返回最终任务状态。

        参数：
            task_id       (str): 任务 ID
            timeout       (int): 最长等待秒数，默认 600 秒（10 分钟）
            poll_interval (int): 轮询间隔秒数，默认 5 秒
            on_progress   (callable, 可选): 进度回调，签名 fn(task_id, status, progress)

        返回：
            最终任务状态字典，status 为 "completed" 或 "failed"。
            超时时返回 {"task_id": task_id, "status": "timeout", "error": "等待超时"}
        """
        deadline = time.time() + timeout
        while time.time() < deadline:
            result = self.query_task(task_id)
            task_status = result.get("status", "unknown")
            progress = result.get("progress", 0)

            if on_progress:
                try:
                    on_progress(task_id, task_status, progress)
                except Exception:
                    pass

            if task_status in ("completed", "failed"):
                return result

            time.sleep(poll_interval)

        return {"task_id": task_id, "status": "timeout", "error": f"等待超时（{timeout} 秒）"}

    # ── 结果链接规范化（用于对话输出）──────────────────────────────────────

    @staticmethod
    def extract_result_url(task: dict) -> str | None:
        """
        从任务查询结果中提取“最终下载链接”（完整保留 ? 与 & 参数）。
        优先级：
          1) video_url
          2) url
          3) links.mp4
          4) data[0].url（旧格式）
        """
        if not task or not isinstance(task, dict):
            return None
        if task.get("video_url"):
            return str(task.get("video_url"))
        if task.get("url"):
            return str(task.get("url"))
        links = task.get("links") or {}
        if isinstance(links, dict) and links.get("mp4"):
            return str(links.get("mp4"))
        nested = task.get("data")
        if isinstance(nested, dict):
            if nested.get("video_url"):
                return str(nested.get("video_url"))
            if nested.get("url"):
                return str(nested.get("url"))
            nlinks = nested.get("links") or {}
            if isinstance(nlinks, dict) and nlinks.get("mp4"):
                return str(nlinks.get("mp4"))
        data = task.get("data")
        if isinstance(data, list) and data and isinstance(data[0], dict) and data[0].get("url"):
            return str(data[0].get("url"))
        return None

    # ── 等待完成（批量，并发轮询）────────────────────────────────────────────

    def wait_for_results(
        self,
        task_ids: list[str],
        timeout: int = DEFAULT_WAIT_TIMEOUT,
        poll_interval: int = POLL_INTERVAL,
        on_progress: Any = None,
    ) -> list[dict]:
        """
        并发轮询等待多个任务全部完成。

        参数：
            task_ids      (list[str]): 任务 ID 列表
            timeout       (int): 每个任务的最长等待秒数
            poll_interval (int): 轮询间隔秒数
            on_progress   (callable, 可选): 进度回调，签名 fn(task_id, status, progress)

        返回：
            list[dict]，顺序与 task_ids 一致，每个元素为最终任务状态。
        """
        if not task_ids:
            return []

        results = [None] * len(task_ids)
        lock = threading.Lock()

        def poll_one(index: int, tid: str) -> None:
            final = self.wait_for_result(tid, timeout, poll_interval, on_progress)
            with lock:
                results[index] = final

        threads = [
            threading.Thread(target=poll_one, args=(i, tid), daemon=True)
            for i, tid in enumerate(task_ids)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        return results


# ── 全局单例 ─────────────────────────────────────────────────────────────────

_client: Optional[DYULocalClient] = None


def get_client(
    base_url: str = LOCAL_BASE_URL,
    timeout: int = DEFAULT_TIMEOUT,
) -> DYULocalClient:
    """
    获取全局 DYULocalClient 单例。
    无需任何凭证，直接使用即可。

    示例：
        from local_client import get_client
        client = get_client()
        status = client.status()
    """
    global _client
    if _client is None:
        _client = DYULocalClient(base_url, timeout)
    return _client
