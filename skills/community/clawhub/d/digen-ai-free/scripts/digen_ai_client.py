"""
DigenAI Python Client - OpenClaw Skill 版本
支持两种模式:
  - 图片生成: 旧 API (api.digen.ai), 使用 DIGEN_TOKEN + DIGEN_SESSION_ID
  - 视频生成: 新 API, 使用 Authorization: Bearer <API_KEY>
"""

import os
import requests
import time
import json
import urllib3
from typing import Optional, Dict, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# ============ 旧 API (图片生成) ============
# Base URL for image generation
OLD_API_BASE = "https://api.digen.ai"

# ============ 新 API (视频生成) ============
# Base URL for video generation & key management
NEW_API_BASE = "https://api.cowork.digen.ai"

# ============ 错误提示信息 ============
NO_API_KEY_MESSAGE = """
❌ API Key Not Found!

To use DigenAI Video Generation, you need a free API key.

📌 How to get your API key:
   1. Visit: https://claw.digen.ai
   2. Or join our Discord: https://discord.gg/SRhbTt9hwp
   3. Or contact us on Telegram: @digen_skill_bot

Your API key starts with `ak_`

Then set: export DIGEN_API_KEY="your_key_here"
"""


class DigenAIClient:
    """DigenAI API 客户端 - 双模式支持"""

    # 图片生成 - 分辨率映射 (旧 API)
    RESOLUTION_MAP = {
        "1:1": "1024x1024",
        "16:9": "1024x576",
        "9:16": "576x1024",
        "4:3": "1024x768",
        "3:4": "768x1024",
        "3:2": "1024x683",
        "2:3": "683x1024",
        "5:4": "1024x819",
        "4:5": "819x1024",
        "21:9": "1280x512",
    }

    def __init__(
        self,
        token: str = None,
        session_id: str = None,
        api_key: str = None,
        old_api_token: str = None,
        old_api_session: str = None,
    ):
        """
        初始化客户端

        Args:
            token / session_id: 旧 API 凭证 (图片生成用)
            api_key: 新 API Key (视频生成用, 格式: ak_xxxx)
            old_api_token / old_api_session: 旧内部 API 凭证 (可选)
        """
        self.old_token = old_api_token or token or os.getenv("DIGEN_TOKEN")
        self.old_session = old_api_session or session_id or os.getenv("DIGEN_SESSION_ID")
        self.api_key = api_key or os.getenv("DIGEN_API_KEY")

        self.use_old_api = bool(self.old_token and self.old_session)
        self.use_new_api = bool(self.api_key)

        if not self.use_old_api and not self.use_new_api:
            raise NoAPIKeyError(NO_API_KEY_MESSAGE)

    # ==================== 新 API (视频生成) ====================

    def _new_headers(self) -> Dict[str, str]:
        """新 API 请求头"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _new_headers_upload(self) -> Dict[str, str]:
        """上传文件专用请求头"""
        return {
            "Authorization": f"Bearer {self.api_key}",
        }

    def _shorten_url(self, url: str) -> Optional[str]:
        """将长 URL 转换为短 URL (TinyURL)"""
        if not url:
            return None
        try:
            resp = requests.get(
                f"https://tinyurl.com/api-create.php?url={requests.utils.quote(url)}",
                timeout=10
            )
            if resp.status_code == 200 and resp.text.startswith("https://"):
                return resp.text
            return url
        except Exception:
            return url  # 失败时返回原始 URL

    def _new_request(self, method: str, endpoint: str,
                     data: Optional[Dict] = None,
                     files: Optional[Dict] = None) -> Dict:
        """新 API 请求"""
        url = f"{NEW_API_BASE}{endpoint}"

        try:
            if files:
                # 文件上传 (multipart/form-data)
                resp = requests.request(
                    method, url,
                    headers=self._new_headers_upload(),
                    files=files,
                    timeout=60
                )
            elif method.upper() == "GET":
                resp = requests.get(url, headers=self._new_headers(),
                                    params=data or {}, timeout=30)
            else:
                resp = requests.request(method, url,
                                        headers=self._new_headers(),
                                        json=data, timeout=60)
            return resp.json()
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def get_api_key_info(self) -> Dict[str, Any]:
        """
        查询当前 API Key 信息 (新 API)

        GET /b/v1/api-key

        Returns:
            {"api_key": "ak_xxx", "api_secret": "as_xxx...", "status": 1, ...}
        """
        if not self.use_new_api:
            return {"success": False, "error": "No API key configured"}

        result = self._new_request("GET", "/b/v1/api-key")
        if "error" in result:
            return {"success": False, "error": result["error"].get("message", "Invalid API key")}
        return {"success": True, "data": result}

    def upload_image(self, file_path: str = None, file_bytes: bytes = None,
                     filename: str = "image.jpg") -> Dict[str, Any]:
        """
        上传图片获取 URL (新 API)
        POST /b/v1/upload

        Args:
            file_path: 本地文件路径
            file_bytes: 或直接传字节数据
            filename: 文件名

        Returns:
            {"success": True, "url": "https://...", "width": 1920, "height": 1080}
        """
        if not self.use_new_api:
            return {"success": False, "error": "No API key configured"}

        if file_path:
            files = {"file": open(file_path, "rb")}
        elif file_bytes:
            files = {"file": (filename, file_bytes)}
        else:
            return {"success": False, "error": "No file provided"}

        try:
            result = self._new_request("POST", "/b/v1/upload", files=files)
            if "error" in result:
                return {"success": False, "error": result["error"].get("message", "Upload failed")}
            return {
                "success": True,
                "url": result.get("url"),
                "width": result.get("width"),
                "height": result.get("height"),
            }
        finally:
            if file_path:
                files["file"].close()

    def generate_video(
        self,
        prompt: str = None,
        image_url: str = None,
        model: str = "turbo",
        duration: int = 5,
        aspect_ratio: str = "16:9",
        resolution: str = "720p",
        image_end_url: str = None,
        webhook_url: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        生成视频 (新 API) - 图生视频或文生视频

        POST /b/v1/video/generate

        Args:
            prompt: 文本提示词 (可选)
            image_url: 输入图片 URL (可选, 图生视频)
            model: turbo (默认) | seedance-2.0
            duration: 5 或 10 秒
            aspect_ratio: 16:9 | 9:16 | 1:1
            resolution: 720p | 1080p (turbo model)
            image_end_url: 结束帧图片 URL (可选)
            webhook_url: 完成回调 URL (可选)

        Note: prompt 和 image_url 至少需要一个
        """
        if not self.use_new_api:
            return {"success": False, "error": "No API key configured"}

        if not prompt and not image_url:
            return {"success": False, "error": "Either prompt or image_url is required"}

        payload = {
            "model": model,
            "duration": duration,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
        }
        if prompt:
            payload["prompt"] = prompt
        if image_url:
            payload["image_url"] = image_url
        if image_end_url:
            payload["image_end_url"] = image_end_url
        if webhook_url:
            payload["webhook_url"] = webhook_url

        result = self._new_request("POST", "/b/v1/video/generate", payload)

        if "error" in result:
            return {"success": False, "error": result["error"].get("message", "Failed")}
        return {
            "success": True,
            "id": result.get("id"),
            "status": result.get("status"),
            "created_at": result.get("created_at"),
        }

    def get_video_status(self, video_id: str) -> Dict[str, Any]:
        """
        查询视频状态 (新 API)

        GET /b/v1/video/{id}

        Status: pending → processing → completed / failed
        """
        if not self.use_new_api:
            return {"success": False, "error": "No API key configured"}

        result = self._new_request("GET", f"/b/v1/video/{video_id}")

        if "error" in result:
            return {"success": False, "error": result["error"].get("message", "Failed")}

        return {
            "success": True,
            "id": result.get("id"),
            "status": result.get("status"),  # pending | processing | completed | failed
            "progress": result.get("progress", 0),
            "video_url": result.get("output", {}).get("video_url"),
            "video_url_short": self._shorten_url(result.get("output", {}).get("video_url")),
            "thumbnail_url": result.get("output", {}).get("thumbnail_url"),
            "error": result.get("error"),
            "created_at": result.get("created_at"),
            "completed_at": result.get("completed_at"),
        }

    def wait_for_video(self, video_id: str, timeout: int = 300,
                       interval: int = 5) -> Dict[str, Any]:
        """轮询等待视频生成完成"""
        start = time.time()
        while time.time() - start < timeout:
            result = self.get_video_status(video_id)
            if not result["success"]:
                return result
            status = result.get("status")
            if status == "completed":
                return result
            elif status == "failed":
                return {"success": False, "error": result.get("error") or "Generation failed"}
            time.sleep(interval)
        return {"success": False, "error": "Timeout waiting for video"}

    def generate_video_sync(self, image_url: str = None, prompt: str = None,
                            **kwargs) -> Dict[str, Any]:
        """同步生成视频"""
        result = self.generate_video(image_url=image_url, prompt=prompt, **kwargs)
        if not result["success"]:
            return result
        return self.wait_for_video(result["id"], **kwargs)

    # ==================== 旧 API (图片生成) ====================

    def _old_headers(self) -> Dict[str, str]:
        """旧 API 请求头"""
        return {
            "Content-Type": "application/json",
            "DIGEN-Token": self.old_token,
            "DIGEN-SessionID": self.old_session,
            "Referer": "https://digen.ai/",
            "Origin": "https://digen.ai",
        }

    def _old_request(self, method: str, endpoint: str,
                     data: Optional[Dict] = None) -> Dict:
        """旧 API 请求"""
        url = f"{OLD_API_BASE}{endpoint}"
        try:
            if method.upper() == "GET":
                resp = requests.get(url, headers=self._old_headers(),
                                   params=data or {}, timeout=30, verify=False)
            else:
                resp = requests.post(url, headers=self._old_headers(),
                                    json=data or {}, timeout=60, verify=False)
            return resp.json()
        except requests.exceptions.RequestException as e:
            return {"errCode": -1, "errMsg": str(e)}

    def generate_image(
        self,
        prompt: str,
        model: str = "default",
        resolution: str = "9:16",
        batch_size: int = 1,
        negative_prompt: str = "",
        **kwargs
    ) -> Dict[str, Any]:
        """
        生成图片 (旧 API)

        POST /v2/tools/text_to_image
        """
        if not self.use_old_api:
            return {"success": False, "error": "Old API credentials not configured for image generation"}

        payload = {
            "prompt": prompt,
            "mode": "text_to_image",
            "aspect_ratio": resolution,
            "image_size": self.RESOLUTION_MAP.get(resolution, "1024x576"),
            "model": model,
            "batch_size": batch_size,
        }
        if negative_prompt:
            payload["negative_prompt"] = negative_prompt

        result = self._old_request("POST", "/v2/tools/text_to_image", payload)

        if result.get("errCode") == 0:
            return {
                "success": True,
                "task_id": result["data"].get("id"),
                "item_id": result["data"].get("itemId"),
            }
        return {"success": False, "error": result.get("errMsg", "Unknown error")}

    def get_image_status(self, job_id: str) -> Dict[str, Any]:
        """查询图片任务状态 (旧 API)"""
        if not self.use_old_api:
            return {"success": False, "error": "Old API not configured"}

        result = self._old_request("POST", "/v6/video/get_task_v2", {"jobID": job_id})

        if result.get("errCode") == 0:
            data = result["data"]
            return {
                "success": True,
                "status": data.get("status"),
                "images": data.get("resource_urls", []),
            }
        return {"success": False, "error": result.get("errMsg")}

    def wait_for_image(self, job_id: str, timeout: int = 120,
                       interval: int = 3) -> Dict[str, Any]:
        """轮询等待图片生成完成 (旧 API)"""
        start = time.time()
        while time.time() - start < timeout:
            result = self.get_image_status(job_id)
            if not result["success"]:
                return result
            if result["status"] == 4:
                return result
            if result["status"] == 5:
                return {"success": False, "error": "Generation failed"}
            time.sleep(interval)
        return {"success": False, "error": "Timeout"}

    def generate_image_sync(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """同步生成图片 (旧 API)"""
        result = self.generate_image(prompt, **kwargs)
        if not result["success"]:
            return result
        return self.wait_for_image(result["task_id"])


class NoAPIKeyError(Exception):
    """API Key 未找到错误"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


# ============ 便捷函数 ============


def check_api_key_status(api_key: str) -> Dict[str, Any]:
    """
    检查新 API Key 状态

    GET /b/v1/api-key
    """
    try:
        resp = requests.get(
            f"{NEW_API_BASE}/b/v1/api-key",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10
        )
        data = resp.json()
        if "error" in data:
            return {"success": False, "valid": False, "error": data["error"].get("message")}
        return {"success": True, "valid": True, "data": data}
    except Exception as e:
        return {"success": False, "error": str(e)}


def check_old_api_status(token: str, session_id: str) -> Dict[str, Any]:
    """
    检查旧 API 凭证状态
    """
    try:
        resp = requests.post(
            f"{OLD_API_BASE}/v6/video/get_task_v2",
            headers={
                "DIGEN-Token": token,
                "DIGEN-SessionID": session_id,
                "Referer": "https://digen.ai/",
                "Origin": "https://digen.ai",
                "Content-Type": "application/json",
            },
            json={"jobID": "test"},
            timeout=10,
            verify=False
        )
        return resp.json()
    except Exception as e:
        return {"errCode": -1, "errMsg": str(e)}


# ============ 批量生成工具 ============


def batch_generate_images(
    prompts: List[str],
    token: str = None,
    session_id: str = None,
    resolution: str = "9:16",
    max_workers: int = 3
) -> List[Dict[str, Any]]:
    """并行批量生成图片 (旧 API)"""
    results = []

    def generate_one(prompt: str) -> Dict[str, Any]:
        client = DigenAIClient(old_api_token=token, old_api_session=session_id)
        return client.generate_image_sync(prompt, resolution=resolution)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(generate_one, p): p for p in prompts}
        for future in as_completed(futures):
            try:
                results.append(future.result())
            except NoAPIKeyError as e:
                results.append({"success": False, "error": e.message})
            except Exception as e:
                results.append({"success": False, "error": str(e)})

    return results


if __name__ == "__main__":
    import sys

    print("""
╔══════════════════════════════════════════════════════════════╗
║        DigenAI Skill Client - OpenClaw (v2)                   ║
╠══════════════════════════════════════════════════════════════╣
║  图片生成 (旧 API): DIGEN_TOKEN + DIGEN_SESSION_ID           ║
║  视频生成 (新 API): DIGEN_API_KEY (Bearer Token)             ║
╠══════════════════════════════════════════════════════════════╣
║  测试命令:                                                    ║
║    python digen_ai_client.py test image                      ║
║    python digen_ai_client.py test video                      ║
║    python digen_ai_client.py test key-info                   ║
╚══════════════════════════════════════════════════════════════╝
    """)

    if len(sys.argv) < 2 or sys.argv[1] != "test":
        sys.exit(0)

    mode = sys.argv[2] if len(sys.argv) > 2 else "image"
    api_key = os.getenv("DIGEN_API_KEY")
    old_token = os.getenv("DIGEN_TOKEN")
    old_session = os.getenv("DIGEN_SESSION_ID")

    if mode == "key-info" and api_key:
        print("🔍 Checking API key info (new API)...")
        client = DigenAIClient(api_key=api_key)
        result = client.get_api_key_info()
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif mode == "image":
        if old_token and old_session:
            print("🖼️  Testing image generation (old API)...")
            client = DigenAIClient(old_api_token=old_token, old_api_session=old_session)
            result = client.generate_image_sync(
                prompt="a cute cat, anime style, soft lighting, detailed fur",
                resolution="1:1"
            )
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("❌ Old API credentials (DIGEN_TOKEN, DIGEN_SESSION_ID) not found")
            print(NO_API_KEY_MESSAGE)

    elif mode == "video":
        if api_key:
            print("🎬 Testing video generation (new API)...")
            # 文生视频示例
            client = DigenAIClient(api_key=api_key)
            result = client.generate_video(
                prompt="A cute cat playing piano in a cozy room, soft lighting",
                model="turbo",
                duration=5,
                aspect_ratio="16:9",
            )
            print(json.dumps(result, indent=2, ensure_ascii=False))

            if result["success"]:
                video_id = result["id"]
                print(f"\n⏳ Waiting for video {video_id}...")
                final = client.wait_for_video(video_id, timeout=300)
                print(json.dumps(final, indent=2, ensure_ascii=False))
        else:
            print("❌ DIGEN_API_KEY not found")
            print(NO_API_KEY_MESSAGE)
