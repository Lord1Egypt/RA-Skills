"""
视频生成 Provider 统一管理器

提供对多个视频生成后端的统一抽象，包括：
- LumaAI Dream Machine
- Runway Gen-3/Gen-4
- Replicate (多模型)
- DALL-E + FFmpeg 管线
- ComfyUI (本地)
- Kling (可灵)

支持最小代价优先选择和自动降级回退。
"""

import json
import os
import subprocess
import sys
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# 将 scripts 目录加入路径
sys.path.insert(0, str(Path(__file__).parent))
from credential_manager import get_credential, list_available_providers


@dataclass
class VideoResult:
    """视频生成结果。"""
    success: bool
    video_path: Optional[str] = None
    job_id: Optional[str] = None
    provider: str = ""
    duration_seconds: float = 0
    resolution: str = ""
    error_message: Optional[str] = None
    metadata: dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class JobStatus:
    """异步任务状态。"""
    state: str  # pending/processing/completed/failed
    progress: float = 0.0  # 0-100
    message: str = ""
    result_url: Optional[str] = None


class VideoProvider(ABC):
    """视频生成 Provider 抽象基类。"""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def max_duration(self) -> int:
        """最大支持时长（秒）。"""
        pass

    @abstractmethod
    def generate(self, prompt: str, params: dict = None) -> VideoResult:
        """启动视频生成。"""
        pass

    @abstractmethod
    def check_status(self, job_id: str) -> JobStatus:
        """检查异步任务状态。"""
        pass

    @abstractmethod
    def download(self, result_url: str, output_path: str) -> str:
        """下载生成的视频。"""
        pass

    def _download_file(self, url: str, output_path: str) -> str:
        """通用文件下载。"""
        import urllib.request
        urllib.request.urlretrieve(url, output_path)
        return output_path


class LumaAIProvider(VideoProvider):
    """LumaAI Dream Machine Provider。"""

    name = "lumaai"
    max_duration = 5

    def __init__(self):
        self.api_key = get_credential("lumaai")
        self.base_url = "https://api.lumalabs.ai/dream-machine/v1"

    def generate(self, prompt: str, params: dict = None) -> VideoResult:
        import urllib.request

        params = params or {}
        payload = {
            "prompt": prompt,
            "aspect_ratio": params.get("aspect_ratio", "16:9"),
            "loop": params.get("loop", False),
        }

        req = urllib.request.Request(
            f"{self.base_url}/generations",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
                return VideoResult(
                    success=True,
                    job_id=data.get("id"),
                    provider=self.name,
                    metadata=data,
                )
        except Exception as e:
            return VideoResult(
                success=False,
                provider=self.name,
                error_message=str(e),
            )

    def check_status(self, job_id: str) -> JobStatus:
        import urllib.request

        req = urllib.request.Request(
            f"{self.base_url}/generations/{job_id}",
            headers={"Authorization": f"Bearer {self.api_key}"},
        )

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
                state = data.get("state", "unknown")
                return JobStatus(
                    state="completed" if state == "completed" else
                          "failed" if state == "failed" else "processing",
                    progress=100 if state == "completed" else 50,
                    message=data.get("failure_reason", ""),
                    result_url=data.get("assets", {}).get("video"),
                )
        except Exception as e:
            return JobStatus(state="failed", message=str(e))

    def download(self, result_url: str, output_path: str) -> str:
        return self._download_file(result_url, output_path)


class RunwayProvider(VideoProvider):
    """Runway Gen-3/Gen-4 Provider。"""

    name = "runway"
    max_duration = 10

    def __init__(self):
        self.api_key = get_credential("runway")
        self.base_url = "https://api.dev.runwayml.com/v1"

    def generate(self, prompt: str, params: dict = None) -> VideoResult:
        import urllib.request

        params = params or {}
        payload = {
            "promptText": prompt,
            "model": params.get("model", "gen3a_turbo"),
            "duration": min(params.get("duration", 5), self.max_duration),
            "ratio": params.get("aspect_ratio", "16:9"),
        }

        req = urllib.request.Request(
            f"{self.base_url}/image_to_video",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "X-Runway-Version": "2024-11-06",
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
                return VideoResult(
                    success=True,
                    job_id=data.get("id"),
                    provider=self.name,
                    metadata=data,
                )
        except Exception as e:
            return VideoResult(
                success=False, provider=self.name, error_message=str(e)
            )

    def check_status(self, job_id: str) -> JobStatus:
        import urllib.request

        req = urllib.request.Request(
            f"{self.base_url}/tasks/{job_id}",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "X-Runway-Version": "2024-11-06",
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
                status = data.get("status", "unknown")
                return JobStatus(
                    state="completed" if status == "SUCCEEDED" else
                          "failed" if status == "FAILED" else "processing",
                    progress=data.get("progress", 0) * 100,
                    result_url=data.get("output", [None])[0] if status == "SUCCEEDED" else None,
                )
        except Exception as e:
            return JobStatus(state="failed", message=str(e))

    def download(self, result_url: str, output_path: str) -> str:
        return self._download_file(result_url, output_path)


class ReplicateProvider(VideoProvider):
    """Replicate Provider（支持多模型）。"""

    name = "replicate"
    max_duration = 4  # 取决于模型

    def __init__(self):
        self.api_token = get_credential("replicate")
        self.base_url = "https://api.replicate.com/v1"

    def generate(self, prompt: str, params: dict = None) -> VideoResult:
        import urllib.request

        params = params or {}
        model = params.get("model", "stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438")

        payload = {
            "version": model.split(":")[-1] if ":" in model else model,
            "input": {"prompt": prompt},
        }

        req = urllib.request.Request(
            f"{self.base_url}/predictions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json",
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
                return VideoResult(
                    success=True,
                    job_id=data.get("id"),
                    provider=self.name,
                    metadata=data,
                )
        except Exception as e:
            return VideoResult(
                success=False, provider=self.name, error_message=str(e)
            )

    def check_status(self, job_id: str) -> JobStatus:
        import urllib.request

        req = urllib.request.Request(
            f"{self.base_url}/predictions/{job_id}",
            headers={"Authorization": f"Bearer {self.api_token}"},
        )

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
                status = data.get("status", "unknown")
                output = data.get("output")
                result_url = output if isinstance(output, str) else (
                    output[0] if isinstance(output, list) and output else None
                )
                return JobStatus(
                    state="completed" if status == "succeeded" else
                          "failed" if status in ("failed", "canceled") else "processing",
                    result_url=result_url,
                    message=data.get("error", ""),
                )
        except Exception as e:
            return JobStatus(state="failed", message=str(e))

    def download(self, result_url: str, output_path: str) -> str:
        return self._download_file(result_url, output_path)


class DalleFFmpegProvider(VideoProvider):
    """DALL-E 关键帧 + FFmpeg 拼接 Provider。"""

    name = "dalle_ffmpeg"
    max_duration = 30  # 通过帧数控制

    def __init__(self):
        self.api_key = get_credential("openai")
        self.base_url = "https://api.openai.com/v1"

    def generate(self, prompt: str, params: dict = None) -> VideoResult:
        import urllib.request
        import tempfile

        params = params or {}
        num_frames = params.get("num_frames", 8)
        fps = params.get("fps", 2)

        # 生成关键帧
        frames_dir = Path(tempfile.mkdtemp(prefix="ai_video_pro_"))
        frame_paths = []

        for i in range(num_frames):
            frame_prompt = f"Frame {i + 1}/{num_frames} of a sequence: {prompt}. Consistent style across all frames."

            payload = {
                "model": "dall-e-3",
                "prompt": frame_prompt,
                "n": 1,
                "size": params.get("size", "1024x1024"),
                "quality": "standard",
            }

            req = urllib.request.Request(
                f"{self.base_url}/images/generations",
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            )

            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    data = json.loads(resp.read())
                    image_url = data["data"][0]["url"]

                    frame_path = str(frames_dir / f"frame_{i:04d}.png")
                    urllib.request.urlretrieve(image_url, frame_path)
                    frame_paths.append(frame_path)
            except Exception as e:
                return VideoResult(
                    success=False, provider=self.name,
                    error_message=f"帧 {i + 1} 生成失败: {e}",
                )

        # FFmpeg 拼接
        output_path = str(frames_dir / "output.mp4")
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-framerate", str(fps),
            "-i", str(frames_dir / "frame_%04d.png"),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            output_path,
        ]

        try:
            subprocess.run(ffmpeg_cmd, capture_output=True, check=True, timeout=60)
            return VideoResult(
                success=True,
                video_path=output_path,
                provider=self.name,
                duration_seconds=num_frames / fps,
                metadata={"frames": len(frame_paths), "fps": fps},
            )
        except Exception as e:
            return VideoResult(
                success=False, provider=self.name,
                error_message=f"FFmpeg 拼接失败: {e}",
            )

    def check_status(self, job_id: str) -> JobStatus:
        return JobStatus(state="completed", progress=100)

    def download(self, result_url: str, output_path: str) -> str:
        # DALL-E 方案直接生成本地文件
        import shutil
        shutil.copy2(result_url, output_path)
        return output_path


# Provider 注册表
_PROVIDER_REGISTRY = {
    "lumaai": LumaAIProvider,
    "runway": RunwayProvider,
    "replicate": ReplicateProvider,
    "dalle_ffmpeg": DalleFFmpegProvider,
}

# 后端优先级排序（最小代价优先）
_BACKEND_PRIORITY = [
    "comfyui",       # 1: 免费本地
    "replicate",     # 2: 免费额度
    "lumaai",        # 3: 免费额度
    "runway",        # 4: 免费试用
    "kling",         # 5: 付费
    "dalle_ffmpeg",  # 7: 兜底
]


def get_provider(backend: str) -> VideoProvider:
    """获取指定后端的 Provider 实例。"""
    provider_class = _PROVIDER_REGISTRY.get(backend)
    if not provider_class:
        raise ValueError(
            f"不支持的后端: '{backend}'\n"
            f"可用后端: {', '.join(_PROVIDER_REGISTRY.keys())}"
        )
    return provider_class()


def select_best_provider(env_report: dict = None) -> str:
    """
    根据环境报告选择最优后端。

    Args:
        env_report: env_detect.py 的检测报告（可选）

    Returns:
        推荐的后端名称
    """
    available = list_available_providers()
    available_video = set(available.get("video", []))

    for backend in _BACKEND_PRIORITY:
        if backend in available_video and backend in _PROVIDER_REGISTRY:
            return backend

    return None


def generate_with_fallback(prompt: str, params: dict = None,
                           preferred_backend: str = None) -> VideoResult:
    """
    使用自动降级回退策略生成视频。

    尝试首选后端，失败则自动降级到下一个可用后端。
    """
    available = list_available_providers()
    available_video = available.get("video", [])

    # 构建尝试顺序
    backends_to_try = []
    if preferred_backend and preferred_backend in available_video:
        backends_to_try.append(preferred_backend)

    for backend in _BACKEND_PRIORITY:
        if backend in available_video and backend not in backends_to_try:
            backends_to_try.append(backend)

    if not backends_to_try:
        return VideoResult(
            success=False,
            error_message="没有可用的视频生成后端。请配置至少一个 API 密钥。",
        )

    # 依次尝试
    last_error = None
    for backend in backends_to_try:
        if backend not in _PROVIDER_REGISTRY:
            continue

        try:
            provider = get_provider(backend)
            result = provider.generate(prompt, params)
            if result.success:
                return result
            last_error = result.error_message
        except Exception as e:
            last_error = str(e)

    return VideoResult(
        success=False,
        error_message=f"所有后端均失败。最后错误: {last_error}",
    )


def wait_for_completion(provider: VideoProvider, job_id: str,
                        output_path: str, timeout: int = 300,
                        poll_interval: int = 5) -> VideoResult:
    """
    等待异步视频生成完成。

    Args:
        provider: Provider 实例
        job_id: 任务 ID
        output_path: 输出文件路径
        timeout: 超时秒数
        poll_interval: 轮询间隔秒数
    """
    start_time = time.time()

    while time.time() - start_time < timeout:
        status = provider.check_status(job_id)

        if status.state == "completed" and status.result_url:
            downloaded_path = provider.download(status.result_url, output_path)
            return VideoResult(
                success=True,
                video_path=downloaded_path,
                provider=provider.name,
            )
        elif status.state == "failed":
            return VideoResult(
                success=False,
                provider=provider.name,
                error_message=status.message or "生成失败",
            )

        time.sleep(poll_interval)

    return VideoResult(
        success=False,
        provider=provider.name,
        error_message=f"生成超时 ({timeout}秒)",
    )


if __name__ == "__main__":
    print("=== 视频生成 Provider 管理器 ===\n")

    available = list_available_providers()
    print(f"可用视频 Provider: {available.get('video', []) or '无'}")

    best = select_best_provider()
    if best:
        print(f"推荐后端: {best}")
    else:
        print("无可用后端，请配置 API 密钥")
