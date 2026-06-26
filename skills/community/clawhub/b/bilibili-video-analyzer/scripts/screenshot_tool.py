"""
FFmpeg 视频截图工具

功能:
- 使用 FFmpeg 在指定时间戳截取视频画面
- 支持单个截图和批量截图
- 自动处理截图失败重试
"""

import subprocess
import shutil
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm


def check_ffmpeg() -> bool:
    """检查 FFmpeg 是否安装且可用
    
    Returns:
        bool: True 表示 FFmpeg 可用
    
    Raises:
        RuntimeError: FFmpeg 不可用
    """
    if not shutil.which('ffmpeg'):
        raise RuntimeError(
            "❌ 未找到 FFmpeg!\n\n"
            "请先安装 FFmpeg:\n"
            "  macOS:    brew install ffmpeg\n"
            "  Ubuntu:   sudo apt install ffmpeg\n"
            "  Windows:  从 https://ffmpeg.org/download.html 下载\n"
        )
    
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ {version_line}")
            return True
        else:
            raise RuntimeError("FFmpeg 执行失败")
            
    except subprocess.TimeoutExpired:
        raise RuntimeError("FFmpeg 响应超时")
    except Exception as e:
        raise RuntimeError(f"FFmpeg 检查失败: {e}")


def capture_screenshot(
    video_path: Path,
    timestamp: float,
    output_path: Path,
    quality: int = 2,
    timeout: int = 10,
    retry: int = 3
) -> bool:
    """在指定时间戳截取视频画面
    
    Args:
        video_path: 视频文件路径
        timestamp: 时间戳(秒)
        output_path: 输出图片路径
        quality: 图片质量(1-31, 数字越小质量越高), 默认2
        timeout: 命令执行超时时间(秒), 默认10
        retry: 失败重试次数, 默认3
    
    Returns:
        bool: 成功返回 True, 失败返回 False
    
    FFmpeg 参数说明:
        -ss: 指定时间戳(秒数或 HH:MM:SS 格式)
        -i: 输入视频文件
        -frames:v 1: 只截取1帧
        -q:v: JPEG 质量(1-31)
        -y: 覆盖已存在的文件
    """
    video_path = Path(video_path)
    output_path = Path(output_path)
    
    if not video_path.exists():
        print(f"❌ 视频文件不存在: {video_path}")
        return False
    
    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 构造 FFmpeg 命令
    cmd = [
        'ffmpeg',
        '-ss', str(timestamp),        # 时间戳
        '-i', str(video_path),        # 输入视频
        '-frames:v', '1',             # 截取1帧
        '-q:v', str(quality),         # 质量
        '-y',                         # 覆盖已存在文件
        str(output_path)              # 输出路径
    ]
    
    # 重试机制
    for attempt in range(retry):
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode == 0 and output_path.exists():
                return True
            else:
                error_msg = result.stderr.strip()
                if attempt < retry - 1:
                    # 还有重试机会,不输出错误
                    continue
                else:
                    print(f"❌ 截图失败 (时间戳: {timestamp}s): {error_msg[:100]}")
                    return False
                    
        except subprocess.TimeoutExpired:
            if attempt < retry - 1:
                continue
            else:
                print(f"❌ 截图超时 (时间戳: {timestamp}s)")
                return False
                
        except Exception as e:
            if attempt < retry - 1:
                continue
            else:
                print(f"❌ 截图异常 (时间戳: {timestamp}s): {e}")
                return False
    
    return False


def batch_capture(
    video_path: Path,
    timestamps: List[Dict],
    output_dir: Path,
    quality: int = 2,
    max_workers: int = 4,
    show_progress: bool = True
) -> Dict[float, Path]:
    """批量截取视频画面
    
    Args:
        video_path: 视频文件路径
        timestamps: 时间戳列表,每个元素为字典,包含:
                   - timestamp: 时间戳(秒)
                   - description: 截图说明(可选)
        output_dir: 截图输出目录
        quality: 图片质量(1-31), 默认2
        max_workers: 最大并发数, 默认4
        show_progress: 是否显示进度条, 默认True
    
    Returns:
        Dict[float, Path]: 时间戳到截图文件路径的映射
                          成功的截图会包含在字典中
    
    Example:
        timestamps = [
            {'timestamp': 83.5, 'description': '关键公式展示'},
            {'timestamp': 225.0, 'description': '实验演示'},
        ]
        
        results = batch_capture(
            video_path=Path('video.mp4'),
            timestamps=timestamps,
            output_dir=Path('./screenshots')
        )
    """
    video_path = Path(video_path)
    output_dir = Path(output_dir)
    
    if not video_path.exists():
        raise FileNotFoundError(f"视频文件不存在: {video_path}")
    
    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 准备截图任务
    tasks = []
    for item in timestamps:
        timestamp = float(item['timestamp'])
        description = item.get('description', '')
        
        # 生成输出文件名
        output_filename = f"screenshot_{int(timestamp)}.jpg"
        output_path = output_dir / output_filename
        
        tasks.append({
            'timestamp': timestamp,
            'output_path': output_path,
            'description': description
        })
    
    # 使用线程池并发执行截图
    screenshot_mapping = {}
    failed_count = 0
    
    if show_progress:
        pbar = tqdm(total=len(tasks), desc="截取关键画面", unit="张")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_task = {
            executor.submit(
                capture_screenshot,
                video_path,
                task['timestamp'],
                task['output_path'],
                quality
            ): task
            for task in tasks
        }
        
        # 收集结果
        for future in as_completed(future_to_task):
            task = future_to_task[future]
            timestamp = task['timestamp']
            output_path = task['output_path']
            description = task['description']
            
            try:
                success = future.result()
                
                if success:
                    screenshot_mapping[timestamp] = output_path
                    if show_progress:
                        pbar.set_postfix_str(f"成功: {len(screenshot_mapping)}")
                else:
                    failed_count += 1
                    
            except Exception as e:
                print(f"❌ 任务异常 (时间戳: {timestamp}s): {e}")
                failed_count += 1
            
            if show_progress:
                pbar.update(1)
    
    if show_progress:
        pbar.close()
    
    # 输出统计信息
    print(f"\n截图完成:")
    print(f"  ✅ 成功: {len(screenshot_mapping)} 张")
    if failed_count > 0:
        print(f"  ❌ 失败: {failed_count} 张")
    
    return screenshot_mapping


def capture_thumbnail(
    video_path: Path,
    output_path: Path,
    timestamp: float = 0.0,
    width: int = 640,
    quality: int = 2
) -> bool:
    """截取视频缩略图
    
    Args:
        video_path: 视频文件路径
        output_path: 输出图片路径
        timestamp: 时间戳(秒), 默认0(视频开头)
        width: 缩略图宽度(像素), 默认640, 高度自动按比例
        quality: 图片质量(1-31), 默认2
    
    Returns:
        bool: 成功返回 True
    """
    video_path = Path(video_path)
    output_path = Path(output_path)
    
    if not video_path.exists():
        print(f"❌ 视频文件不存在: {video_path}")
        return False
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        'ffmpeg',
        '-ss', str(timestamp),
        '-i', str(video_path),
        '-frames:v', '1',
        '-vf', f'scale={width}:-1',  # 设置宽度,高度自动
        '-q:v', str(quality),
        '-y',
        str(output_path)
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        return result.returncode == 0 and output_path.exists()
        
    except Exception as e:
        print(f"❌ 缩略图生成失败: {e}")
        return False


def get_video_info(video_path: Path) -> Optional[Dict]:
    """获取视频基本信息(时长、分辨率等)
    
    Args:
        video_path: 视频文件路径
    
    Returns:
        Optional[Dict]: 视频信息字典,包含:
                       - duration: 时长(秒)
                       - width: 宽度(像素)
                       - height: 高度(像素)
                       - fps: 帧率
    """
    video_path = Path(video_path)
    
    if not video_path.exists():
        return None
    
    cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format',
        '-show_streams',
        str(video_path)
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return None
        
        import json
        data = json.loads(result.stdout)
        
        # 查找视频流
        video_stream = None
        for stream in data.get('streams', []):
            if stream.get('codec_type') == 'video':
                video_stream = stream
                break
        
        if not video_stream:
            return None
        
        # 提取信息
        info = {
            'duration': float(data.get('format', {}).get('duration', 0)),
            'width': int(video_stream.get('width', 0)),
            'height': int(video_stream.get('height', 0)),
            'fps': eval(video_stream.get('r_frame_rate', '0/1'))
        }
        
        return info
        
    except Exception as e:
        print(f"⚠️  获取视频信息失败: {e}")
        return None


if __name__ == '__main__':
    # 测试代码
    import sys
    
    if len(sys.argv) < 3:
        print("用法: python screenshot_tool.py <视频文件> <时间戳(秒)> [输出文件]")
        sys.exit(1)
    
    video_file = Path(sys.argv[1])
    timestamp = float(sys.argv[2])
    output_file = Path(sys.argv[3]) if len(sys.argv) > 3 else Path(f"screenshot_{int(timestamp)}.jpg")
    
    try:
        # 检查 FFmpeg
        check_ffmpeg()
        
        # 获取视频信息
        info = get_video_info(video_file)
        if info:
            print(f"\n视频信息:")
            print(f"  时长: {info['duration']:.2f}秒")
            print(f"  分辨率: {info['width']}x{info['height']}")
            print(f"  帧率: {info['fps']:.2f} fps")
        
        # 截图
        print(f"\n正在截取画面 (时间戳: {timestamp}s)...")
        success = capture_screenshot(video_file, timestamp, output_file)
        
        if success:
            print(f"✅ 截图已保存: {output_file}")
        else:
            print("❌ 截图失败")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)
