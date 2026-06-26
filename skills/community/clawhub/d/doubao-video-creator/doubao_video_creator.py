#!/usr/bin/env python3
"""
豆包视频创作助手 - 核心功能模块 v3.0
火山引擎 Doubao Seedance 视频生成
支持文生视频和图生视频两种模式

v3.0 更新 (2026-04-28):
- 默认时长从 5 秒改为 10 秒
- 支持用户选择时长（10 秒或 15 秒）
- 支持用户选择模型版本（1.0/1.5/2.0）
- API 格式使用 content[]（已验证通过）
"""

import requests
import json
import time
import os
from datetime import datetime

# 配置
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"

# 临时目录
TEMP_DIR = "/root/.openclaw/workspace/doubao-video-temp"
os.makedirs(TEMP_DIR, exist_ok=True)

# 默认 API Key
DEFAULT_API_KEY = "65ae8f92-134c-4194-a3af-6e6cb74284e0"

# 可用模型列表
AVAILABLE_MODELS = {
    "2.0": "doubao-seedance-2-0-260128",
    "2.0-fast": "doubao-seedance-2-0-fast-260128",
    "1.5": "doubao-seedance-1-5-pro-251215",
    "1.0": "doubao-seedance-1-0-pro-250528",
    "1.0-fast": "doubao-seedance-1-0-pro-fast-251015",
}

# 默认模型
DEFAULT_MODEL = "doubao-seedance-2-0-260128"


class DoubaoVideoCreator:
    """豆包视频生成器 v3.0"""
    
    def __init__(self, api_key: str = None, model_id: str = None):
        self.api_key = api_key or DEFAULT_API_KEY
        self.model_id = model_id or DEFAULT_MODEL
        self.temp_dir = TEMP_DIR
        
    def create_video_task(self, prompt, duration=10, resolution="720p", ratio="16:9",
                         image_url=None, model=None):
        """
        创建视频生成任务
        
        Args:
            prompt: 视频描述提示词
            duration: 时长（秒），10 或 15 秒，默认 10 秒
            resolution: 分辨率 480p/720p/1080p
            ratio: 比例 16:9/9:16/1:1
            image_url: 参考图片 URL（图生视频模式，可选）
            model: 模型 ID（可选，覆盖默认）
            
        Returns:
            task_id: 任务 ID，失败返回 None
        """
        url = f"{self.base_url}/contents/generations/tasks"
        model_id = model or self.model_id
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 构建内容（支持文生视频和图生视频）
        content = []
        if image_url:
            content.append({"type": "image_url", "image_url": {"url": image_url}})
        content.append({"type": "text", "text": prompt})
        
        payload = {
            "model": model_id,
            "content": content,
            "parameters": {
                "ratio": ratio,
                "duration": duration,
                "watermark": False
            }
        }
        
        mode = "图生视频" if image_url else "文生视频"
        print(f"🎬 创建{mode}视频任务...")
        print(f"   模型：{model_id}")
        print(f"   比例：{ratio} | 时长：{duration}秒")
        print(f"   提示词：{prompt[:50]}...")
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                task_id = result.get("id")
                print(f"✅ 任务创建成功！Task ID: {task_id}")
                return task_id
            else:
                print(f"❌ 任务创建失败：{response.status_code}")
                print(f"   错误：{response.text}")
                return None
                
        except Exception as e:
            print(f"❌ 请求异常：{e}")
            return None
    
    def get_task_status(self, task_id):
        """
        查询任务状态
        
        Args:
            task_id: 任务 ID
            
        Returns:
            (status, result): 状态和完整结果
        """
        url = f"{self.base_url}/contents/generations/tasks/{task_id}"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                status = result.get("status", "unknown")
                return status, result
            else:
                return "error", {"error": response.text}
                
        except Exception as e:
            return "error", {"error": str(e)}
    
    def wait_for_completion(self, task_id, timeout=600, interval=5):
        """
        等待任务完成
        
        Args:
            task_id: 任务 ID
            timeout: 超时时间（秒）
            interval: 轮询间隔（秒）
            
        Returns:
            result: 完成结果，失败返回 None
        """
        print(f"⏳ 等待视频生成完成...")
        print(f"   🕐 预计等待 1-3 分钟，最长等待 {timeout} 秒")
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status, result = self.get_task_status(task_id)
            
            elapsed = time.time() - start_time
            print(f"   [{int(elapsed)}s] 状态：{status}")
            
            if status == "succeeded":
                print(f"✅ 视频生成完成！")
                return result
            elif status in ["failed", "canceled"]:
                print(f"❌ 视频生成失败：{result}")
                return None
            elif status == "pending":
                print(f"   任务排队中...")
            elif status == "running":
                print(f"   视频生成中...")
            
            time.sleep(interval)
        
        print(f"⏰ 等待超时（{timeout}s）")
        return None
    
    def extract_video_url(self, result):
        """从结果中提取视频 URL"""
        if "content" in result:
            content = result["content"]
            if isinstance(content, list) and len(content) > 0:
                for item in content:
                    if isinstance(item, dict):
                        if item.get("type") == "video":
                            return item.get("url")
                        elif "video_url" in item:
                            return item["video_url"]
                        elif "url" in item:
                            return item["url"]
        return None
    
    def download_video(self, video_url, output_path=None):
        """
        下载生成的视频
        
        Args:
            video_url: 视频 URL
            output_path: 保存路径（默认自动生成）
            
        Returns:
            file_path: 下载的文件路径
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"{self.temp_dir}/video_{timestamp}.mp4"
        
        print(f"📥 下载视频到：{output_path}")
        
        try:
            response = requests.get(video_url, stream=True, timeout=120)
            
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"✅ 视频下载成功！")
                
                # 显示文件大小
                size_mb = os.path.getsize(output_path) / 1024 / 1024
                print(f"   文件大小：{size_mb:.2f} MB")
                
                return output_path
            else:
                print(f"❌ 视频下载失败：{response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ 下载异常：{e}")
            return None
    
    def generate_scene(self, prompt, duration=10, scene_id=1,
                      image_url=None, model=None):
        """
        生成单个场景视频
        
        Args:
            prompt: 场景提示词
            duration: 时长（秒），10 或 15 秒
            scene_id: 场景编号
            image_url: 参考图片 URL（图生视频模式，可选）
            model: 模型 ID（可选）
            
        Returns:
            (success, video_path): 是否成功和视频路径
        """
        if image_url:
            mode = "图生视频"
        else:
            mode = "文生视频"
            
        print(f"\n🎬 生成场景 {scene_id} ({mode}): {prompt[:50]}...")
        
        # 创建任务
        task_id = self.create_video_task(
            prompt, duration,
            image_url=image_url,
            model=model
        )
        if not task_id:
            return False, None
        
        # 等待完成
        result = self.wait_for_completion(task_id)
        if not result:
            return False, None
        
        # 提取 URL
        video_url = self.extract_video_url(result)
        if not video_url:
            print("❌ 未找到视频 URL")
            print(f"   响应内容：{json.dumps(result, indent=2, ensure_ascii=False)}")
            return False, None
        
        print(f"   视频 URL：{video_url}")
        
        # 下载视频
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_path = f"{self.temp_dir}/scene_{scene_id}_{timestamp}.mp4"
        
        downloaded_path = self.download_video(video_url, video_path)
        if downloaded_path:
            return True, downloaded_path
        else:
            return False, None


def main():
    """测试函数"""
    creator = DoubaoVideoCreator()
    
    # 测试文生视频
    prompt = "一只可爱的小猫在草地上玩耍，阳光明媚，微风吹拂，高清写实风格"
    success, video_path = creator.generate_scene(prompt, duration=10, scene_id=1)
    
    if success:
        print(f"\n🎉 视频生成成功！")
        print(f"   路径：{video_path}")
    else:
        print(f"\n❌ 视频生成失败")


if __name__ == "__main__":
    main()
