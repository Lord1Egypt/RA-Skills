"""
BigModel 图片与视频生成模块
使用智谱 AI CogView 和 CogVideoX API

安装依赖: pip install requests
环境变量: export BIGMODEL_API_KEY=your_key
"""

import os
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from typing import Optional


class BigModelClient:
    """BigModel API 客户端"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://open.bigmodel.cn/api",
        timeout: int = 60,
    ):
        self.api_key = api_key or os.environ.get("BIGMODEL_API_KEY")
        if not self.api_key:
            raise ValueError("需要设置 BIGMODEL_API_KEY 环境变量")
        self.base_url = base_url
        self.timeout = timeout
        self._headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def generate_image(
        self,
        prompt: str,
        model: str = "cogview-3-flash",
        quality: str = "standard",
        size: str = "1024x1024",
        watermark_enabled: bool = True,
    ) -> dict:
        """生成单张图片"""
        resp = requests.post(
            f"{self.base_url}/paas/v4/images/generations",
            headers=self._headers,
            json={
                "model": model,
                "prompt": prompt,
                "quality": quality,
                "size": size,
                "watermark_enabled": watermark_enabled,
            },
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return resp.json()

    def batch_generate_images(
        self,
        prompts: list[str],
        model: str = "cogview-3-flash",
        quality: str = "standard",
        size: str = "1024x1024",
        max_concurrent: int = 3,
    ) -> list[dict]:
        """批量生成图片"""
        def generate_one(prompt):
            return self.generate_image(prompt, model, quality, size)

        with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
            return list(executor.map(generate_one, prompts))

    def generate_video(
        self,
        prompt: str,
        model: str = "cogvideox-flash",
        quality: str = "quality",
        size: str = "1920x1080",
        fps: int = 30,
        duration: int = 5,
        with_audio: bool = True,
        watermark_enabled: bool = False,
        image_url: Optional[str] = None,
    ) -> dict:
        """生成视频（异步任务）"""
        payload = {
            "model": model,
            "prompt": prompt[:512],
            "quality": quality,
            "size": size,
            "fps": fps,
            "duration": duration,
            "with_audio": with_audio,
            "watermark_enabled": watermark_enabled,
        }
        if image_url:
            payload["image_url"] = image_url

        resp = requests.post(
            f"{self.base_url}/paas/v4/videos/generations",
            headers=self._headers,
            json=payload,
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return resp.json()

    def query_video_result(self, task_id: str) -> dict:
        """查询视频生成状态"""
        resp = requests.get(
            f"{self.base_url}/paas/v4/async-result/{task_id}",
            headers=self._headers,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def wait_for_video(
        self,
        task_id: str,
        max_wait_time: int = 300000,
        poll_interval: int = 5,
    ) -> dict:
        """等待视频生成完成"""
        start = time.time()
        while time.time() - start < max_wait_time / 1000:
            result = self.query_video_result(task_id)

            if result["task_status"] == "SUCCESS":
                return result

            if result["task_status"] == "FAIL":
                raise RuntimeError(f"视频生成失败: {result.get('error')}")

            print(f"等待中... ({int(time.time() - start)}s)")
            time.sleep(poll_interval)

        raise TimeoutError("视频生成超时")


# 全局客户端实例
_client: Optional[BigModelClient] = None


def get_client() -> BigModelClient:
    """获取或创建全局客户端实例"""
    global _client
    if _client is None:
        _client = BigModelClient()
    return _client


def generate_image(
    prompt: str,
    model: str = "cogview-3-flash",
    quality: str = "standard",
    size: str = "1024x1024",
    watermark_enabled: bool = True,
) -> dict:
    """生成单张图片"""
    return get_client().generate_image(prompt, model, quality, size, watermark_enabled)


def batch_generate_images(
    prompts: list[str],
    model: str = "cogview-3-flash",
    quality: str = "standard",
    size: str = "1024x1024",
    max_concurrent: int = 3,
) -> list[dict]:
    """批量生成图片"""
    return get_client().batch_generate_images(prompts, model, quality, size, max_concurrent)


def generate_video(
    prompt: str,
    model: str = "cogvideox-flash",
    quality: str = "quality",
    size: str = "1920x1080",
    fps: int = 30,
    duration: int = 5,
    with_audio: bool = True,
    watermark_enabled: bool = False,
    image_url: Optional[str] = None,
) -> dict:
    """生成视频"""
    return get_client().generate_video(
        prompt, model, quality, size, fps, duration, with_audio, watermark_enabled, image_url
    )


def query_video_result(task_id: str) -> dict:
    """查询视频状态"""
    return get_client().query_video_result(task_id)


def wait_for_video(
    task_id: str,
    max_wait_time: int = 300000,
    poll_interval: int = 5,
) -> dict:
    """等待视频生成完成"""
    return get_client().wait_for_video(task_id, max_wait_time, poll_interval)


if __name__ == "__main__":
    # 使用示例
    api_key = os.environ.get("BIGMODEL_API_KEY")
    if not api_key:
        print("请设置 BIGMODEL_API_KEY 环境变量")
        exit(1)

    client = BigModelClient(api_key=api_key)

    # 示例 1: 生成单张图片
    print("\n=== 生成单张图片 ===")
    result = client.generate_image(
        prompt="一只可爱的橘猫在草地上玩耍，阳光明媚",
        model="cogview-3-flash",
    )
    print(f"图片URL: {result['data'][0]['url']}")

    # 示例 2: 批量生成
    print("\n=== 批量生成图片 ===")
    prompts = ["日出", "日落", "星空"]
    results = client.batch_generate_images(prompts, max_concurrent=2)
    for i, r in enumerate(results):
        print(f"图片{i+1}: {r['data'][0]['url']}")

    # 示例 3: 生成视频
    print("\n=== 生成视频 ===")
    video = client.generate_video(
        prompt="一朵花在阳光下缓缓开放",
        duration=5,
    )
    print(f"任务ID: {video['id']}")
    print("等待视频生成...")
    final = client.wait_for_video(video["id"], max_wait_time=180000)
    print(f"视频URL: {final['video_result'][0]['url']}")
