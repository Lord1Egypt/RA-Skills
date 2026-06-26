"""
Seedance Video API 调用模块
可直接导入使用: from seedance_api import generate_video
"""
import requests
import os
import sys
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VOLCENGINE_API_KEY")
API_URL = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"
QUERY_URL = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"

MODELS = {
    "1.5-pro": "doubao-seedance-1-5-pro-251215",
    "1.0-pro": "doubao-seedance-1-0-pro-250121",
    "1.0-pro-fast": "doubao-seedance-1-0-pro-fast-250121",
    "1.0-lite-t2v": "doubao-seedance-1-0-lite-t2v-241118",
    "1.0-lite-i2v": "doubao-seedance-1-0-lite-i2v-241118",
}

DEFAULT_MODEL = MODELS["1.5-pro"]


def generate_video(prompt, model=None, duration=5, ratio="16:9", resolution="720p",
                  image=None, first_frame=None, last_frame=None, reference_images=None,
                  generate_audio=True, seed=None, camera_fixed=False, watermark=False,
                  download=True, output_dir="output", poll_interval=5, timeout=600):
    """
    调用火山引擎 Seedream 生成视频
    
    参数:
        prompt (str): 文本提示词
        model (str): 模型 ID，可选 "1.5-pro", "1.0-pro", "1.0-pro-fast", "1.0-lite-t2v", "1.0-lite-i2v" 或具体 ID，默认 1.5-pro
        duration (int): 视频时长(秒)，支持 2-12，默认 5
        ratio (str): 宽高比 "16:9", "4:3", "1:1", "3:4", "9:16", "21:9", "adaptive"，默认 16:9
        resolution (str): 分辨率 "480p", "720p", "1080p"，默认 720p
        image (str/list): 图生视频的参考图片 URL 或 Base64
        first_frame (str): 首帧图片 URL 或 Base64 (首尾帧模式)
        last_frame (str): 尾帧图片 URL 或 Base64 (首尾帧模式)
        reference_images (list): 参考图列表 1-4张 (参考图模式，仅 1.0-lite-i2v)
        generate_audio (bool): 是否生成音频，默认 True
        seed (int): 随机种子
        camera_fixed (bool): 是否固定摄像头，默认 False
        watermark (bool): 是否添加水印，默认 False
        download (bool): 是否下载到本地，默认 True
        output_dir (str): 输出目录，默认 "output"
        poll_interval (int): 轮询间隔(秒)，默认 5
        timeout (int): 超时时间(秒)，默认 600
    
    返回:
        dict: 包含生成的视频 URL 和本地路径
    
    可用模型:
        - "1.5-pro" / "doubao-seedance-1-5-pro-251215" (默认最新，支持有声视频)
        - "1.0-pro" / "doubao-seedance-1-0-pro-250121"
        - "1.0-pro-fast" / "doubao-seedance-1-0-pro-fast-250121"
        - "1.0-lite-t2v" / "doubao-seedance-1-0-lite-t2v-241118" (文生视频)
        - "1.0-lite-i2v" / "doubao-seedance-1-0-lite-i2v-241118" (图生视频)
    """
    if not API_KEY:
        raise ValueError("未设置 VOLCENGINE_API_KEY 环境变量")
    
    if model is None:
        model = DEFAULT_MODEL
    elif model in MODELS:
        model = MODELS[model]
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    content = [{"type": "text", "text": prompt}]
    
    if first_frame and last_frame:
        content.append({"type": "image_url", "image_url": {"url": first_frame}, "role": "first_frame"})
        content.append({"type": "image_url", "image_url": {"url": last_frame}, "role": "last_frame"})
    elif reference_images and isinstance(reference_images, list):
        for i, img in enumerate(reference_images[:4]):
            content.append({"type": "image_url", "image_url": {"url": img}, "role": "reference_image"})
    elif image:
        if isinstance(image, list):
            for img in image[:4]:
                content.append({"type": "image_url", "image_url": {"url": img}})
        else:
            content.append({"type": "image_url", "image_url": {"url": image}})
    
    data = {
        "model": model,
        "content": content,
        "duration": duration,
        "ratio": ratio,
        "resolution": resolution,
        "generate_audio": generate_audio,
        "camera_fixed": camera_fixed,
        "watermark": watermark
    }
    
    if seed is not None:
        data["seed"] = seed
    
    print(f"正在创建视频生成任务...")
    response = requests.post(API_URL, headers=headers, json=data)
    result = response.json()
    
    if "id" not in result:
        error_msg = result.get("error", {}).get("message", "未知错误")
        raise Exception(f"创建任务失败: {error_msg}")
    
    task_id = result["id"]
    print(f"任务 ID: {task_id}")
    print(f"正在生成视频 (超时: {timeout}秒)...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        query_response = requests.get(f"{QUERY_URL}/{task_id}", headers=headers)
        query_result = query_response.json()
        
        status = query_result.get("status", "unknown")
        print(f"状态: {status}")
        
        if status == "succeeded":
            video_url = query_result.get("content", {}).get("video_url")
            local_paths = []
            
            if download and video_url:
                os.makedirs(output_dir, exist_ok=True)
                filename = f"{prompt[:20]}_{int(time.time())}.mp4"
                filename = "".join(c for c in filename if c not in r'<>:"/\|?*')
                filepath = os.path.join(output_dir, filename)
                
                print(f"正在下载视频...")
                video_response = requests.get(video_url)
                with open(filepath, "wb") as f:
                    f.write(video_response.content)
                local_paths.append(filepath)
                print(f"已保存: {filepath}")
            
            return {
                "success": True,
                "task_id": task_id,
                "model": model,
                "video_url": video_url,
                "local_paths": local_paths if download else [],
                "duration": query_result.get("duration"),
                "ratio": query_result.get("ratio")
            }
        elif status in ["failed", "expired"]:
            error_msg = query_result.get("status", "任务失败")
            raise Exception(f"视频生成失败: {error_msg}")
        
        time.sleep(poll_interval)
    
    raise Exception(f"视频生成超时 ({timeout}秒)")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Seedance 视频生成")
    parser.add_argument("prompt", nargs="?", default="一只小猫对着镜头打哈欠", help="视频描述")
    parser.add_argument("-m", "--model", help=f"模型版本: {', '.join(MODELS.keys())} (默认: 1.5-pro)")
    parser.add_argument("-d", "--duration", type=int, default=5, help="视频时长 秒 (默认: 5)")
    parser.add_argument("-r", "--ratio", default="16:9", help="宽高比 (默认: 16:9)")
    parser.add_argument("-s", "--resolution", default="720p", help="分辨率 (默认: 720p)")
    parser.add_argument("-o", "--output-dir", default="output", help="输出目录 (默认: output)")
    parser.add_argument("-i", "--image", help="图生视频：参考图片 URL")
    parser.add_argument("--first-frame", help="首尾帧视频：首帧图片 URL")
    parser.add_argument("--last-frame", help="首尾帧视频：尾帧图片 URL")
    parser.add_argument("--no-audio", action="store_true", help="不生成音频")
    parser.add_argument("--seed", type=int, help="随机种子")
    parser.add_argument("--fixed", action="store_true", help="固定摄像头")
    parser.add_argument("--watermark", action="store_true", help="添加水印")
    
    args = parser.parse_args()
    
    print(f"正在生成视频: {args.prompt}")
    if args.model:
        print(f"使用模型: {args.model}")
    
    result = generate_video(
        prompt=args.prompt,
        model=args.model,
        duration=args.duration,
        ratio=args.ratio,
        resolution=args.resolution,
        image=args.image,
        first_frame=args.first_frame,
        last_frame=args.last_frame,
        generate_audio=not args.no_audio,
        seed=args.seed,
        camera_fixed=args.fixed,
        watermark=args.watermark,
        output_dir=args.output_dir
    )
    
    print(f"\n生成成功! (模型: {result['model']})")
    print(f"视频 URL: {result['video_url']}")
    
    if result["local_paths"]:
        print("\n本地文件:")
        for path in result["local_paths"]:
            print(f"  {path}")


if __name__ == "__main__":
    main()
