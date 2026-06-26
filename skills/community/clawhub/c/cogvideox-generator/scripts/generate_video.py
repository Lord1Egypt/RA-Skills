import os
import time
from zai import ZhipuAiClient

def generate_cogvideo(prompt: str, quality: str = "quality", size: str = "1920x1080", fps: int = 30, with_audio: bool = True) -> dict:
    """
    调用 CogVideoX (智谱AI) 接口生成视频
    
    Args:
        prompt (str): 视频生成的提示词
        quality (str): 输出模式，"quality" 为质量优先，"speed" 为速度优先
        size (str): 视频分辨率，例如 "1920x1080" 或 "3840x2160"
        fps (int): 帧率，支持 30 或 60
        with_audio (bool): 是否包含音频
        
    Returns:
        dict: 包含视频生成结果信息的字典
    """
    # 初始化客户端，请确保环境变量 ZHIPUAI_API_KEY 已设置
    api_key = os.getenv("ZHIPUAI_API_KEY")
    if not api_key:
        return {"error": "未找到 ZHIPUAI_API_KEY 环境变量，请设置后再试"}

    client = ZhipuAiClient(api_key=api_key)

    try:
        # 1. 提交生成任务
        print(f"正在提交生成任务: {prompt}...")
        response = client.videos.generations(
            model="cogvideox-3",
            prompt=prompt,
            quality=quality,
            with_audio=with_audio,
            size=size,
            fps=fps,
        )
        
        task_id = response.id
        print(f"任务已提交，ID: {task_id}")

        # 2. 轮询查询任务状态
        # 视频生成通常耗时较长，需要等待
        while True:
            result = client.videos.retrieve_videos_result(id=task_id)
            # 假设结果中有 task_status 字段，具体字段名需参考 SDK 文档
            # 这里根据常见的异步任务状态进行判断
            status = getattr(result, 'task_status', 'UNKNOWN')
            
            if status == 'SUCCESS':
                video_url = result.video_url # 假设返回对象中有 video_url 字段
                return {
                    "status": "success",
                    "message": "视频生成成功",
                    "video_url": video_url,
                    "result_raw": str(result)
                }
            elif status == 'FAILED':
                return {
                    "status": "failed",
                    "message": "视频生成失败",
                    "result_raw": str(result)
                }
            else:
                print(f"任务进行中 ({status})，等待 5 秒后重试...")
                time.sleep(5)
                
    except Exception as e:
        return {"error": str(e)}

# 技能定义元数据
__skill__ = {
    "name": "generate_cogvideo",
    "description": "使用 CogVideoX 模型根据文本提示词生成视频。",
    "parameters": {
        "prompt": {"type": "string", "description": "描述视频内容的提示词"},
        "quality": {"type": "string", "description": "输出模式：'quality' 或 'speed'", "default": "quality"},
        "size": {"type": "string", "description": "视频分辨率，如 '1920x1080'", "default": "1920x1080"},
        "fps": {"type": "integer", "description": "帧率，30 或 60", "default": 30},
        "with_audio": {"type": "boolean", "description": "是否生成音频", "default": True}
    }
}


